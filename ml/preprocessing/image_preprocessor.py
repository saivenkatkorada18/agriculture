"""
Image Preprocessing Pipeline for Agricultural Computer Vision
"""
import io
from typing import Tuple, Optional, Union
import numpy as np
import cv2
from PIL import Image

try:
    from ml.config.config import IMAGE_HEIGHT, IMAGE_WIDTH
except ImportError:
    IMAGE_HEIGHT, IMAGE_WIDTH = 224, 224

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}


class ImagePreprocessError(Exception):
    """Custom exception for image preprocessing failures."""
    pass


def validate_image_bytes(image_bytes: bytes) -> Tuple[bool, Optional[str], Optional[Image.Image]]:
    """
    Validates file size, integrity, and format using PIL.
    Returns (is_valid, error_message, pil_image).
    """
    if not image_bytes or len(image_bytes) == 0:
        return False, "Uploaded image file is empty.", None

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        return False, f"Image size exceeds 10MB limit ({len(image_bytes) / (1024*1024):.1f}MB).", None

    try:
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.verify()  # Verify file header and integrity
        # Re-open after verify() as verify alters file pointer
        pil_img = Image.open(io.BytesIO(image_bytes))
        format_name = (pil_img.format or "").upper()

        if format_name not in ALLOWED_FORMATS:
            return False, f"Unsupported image format: {format_name}. Allowed: JPG, JPEG, PNG, WEBP.", None

        return True, None, pil_img
    except Exception as e:
        return False, f"Corrupt or unreadable image file: {str(e)}", None


def load_image_as_rgb_array(image_input: Union[bytes, str, Image.Image, np.ndarray]) -> np.ndarray:
    """
    Converts various image inputs into a standard RGB NumPy uint8 array [H, W, 3].
    """
    if isinstance(image_input, bytes):
        is_valid, err, pil_img = validate_image_bytes(image_input)
        if not is_valid or pil_img is None:
            raise ImagePreprocessError(err or "Failed to validate image.")
        pil_img = pil_img.convert("RGB")
        return np.array(pil_img, dtype=np.uint8)

    elif isinstance(image_input, str):
        img_bgr = cv2.imread(image_input)
        if img_bgr is None:
            raise ImagePreprocessError(f"Could not read image from path: {image_input}")
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    elif isinstance(image_input, Image.Image):
        return np.array(image_input.convert("RGB"), dtype=np.uint8)

    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 2:
            return cv2.cvtColor(image_input, cv2.COLOR_GRAY2RGB)
        elif image_input.ndim == 3:
            if image_input.shape[2] == 4:
                return cv2.cvtColor(image_input, cv2.COLOR_RGBA2RGB)
            return image_input.astype(np.uint8)
        raise ImagePreprocessError("Unsupported array dimensions.")

    raise ImagePreprocessError("Unsupported image input type.")


def enhance_foliar_contrast(rgb_image: np.ndarray) -> np.ndarray:
    """
    Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) in LAB color space
    to enhance plant disease lesion boundaries without blowing out natural lighting.
    """
    lab = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)


def preprocess_for_inference(
    image_input: Union[bytes, str, Image.Image, np.ndarray],
    target_size: Tuple[int, int] = (IMAGE_HEIGHT, IMAGE_WIDTH),
    normalize_mode: str = "tf"  # "tf" scales to [-1, 1] for MobileNetV2; "torch" or "standard"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Standard preprocessing pipeline:
    1. Validate and convert to RGB array.
    2. Resize with high-quality cubic interpolation.
    3. Apply light noise filtering.
    4. Normalize for CNN model input.
    
    Returns:
        (preprocessed_batch_tensor [1, H, W, 3], clean_rgb_preview [H, W, 3])
    """
    rgb_img = load_image_as_rgb_array(image_input)
    
    # Resize
    resized_rgb = cv2.resize(rgb_img, target_size, interpolation=cv2.INTER_CUBIC)
    
    # Slight bilateral filter to preserve edges while smoothing sensor noise
    denoised_rgb = cv2.bilateralFilter(resized_rgb, d=5, sigmaColor=35, sigmaSpace=35)
    
    # Normalization
    img_float = denoised_rgb.astype(np.float32)
    if normalize_mode == "tf":
        normalized = (img_float / 127.5) - 1.0  # Range [-1.0, 1.0]
    elif normalize_mode == "scale":
        normalized = img_float / 255.0          # Range [0.0, 1.0]
    else:
        # Standard ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        normalized = ((img_float / 255.0) - mean) / std

    # Expand dims to batch shape [1, H, W, 3]
    batch_tensor = np.expand_dims(normalized, axis=0)
    return batch_tensor, denoised_rgb


def validate_domain_image(rgb_image: np.ndarray, domain: str = "plant") -> Tuple[bool, str, dict]:
    """
    Validates whether an uploaded image contains genuine agricultural specimens (plant foliage or soil surface).
    Rejects out-of-domain uploads such as human selfies/faces, indoor furniture, random objects, or solid background colors.

    Returns:
        (is_valid_specimen, warning_message, metrics_dict)
    """
    if rgb_image is None or rgb_image.size == 0:
        return False, "Empty or unreadable image data.", {"vegetation_ratio": 0.0, "skin_ratio": 0.0}

    # Resize to standard analysis canvas for fast feature extraction
    h, w, _ = rgb_image.shape
    if h > 300 or w > 300:
        analysis_img = cv2.resize(rgb_image, (250, 250), interpolation=cv2.INTER_AREA)
    else:
        analysis_img = rgb_image.copy()

    total_pixels = float(analysis_img.shape[0] * analysis_img.shape[1])

    # 1. Human Skin-Tone Detection (YCrCb color space: Cr in [133, 173], Cb in [77, 127])
    ycrcb = cv2.cvtColor(analysis_img, cv2.COLOR_RGB2YCrCb)
    cr = ycrcb[:, :, 1]
    cb = ycrcb[:, :, 2]
    skin_mask = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
    skin_ratio = float(np.count_nonzero(skin_mask) / total_pixels)

    # 2. Foliage & Plant Specimen Color Analysis (HSV space)
    hsv = cv2.cvtColor(analysis_img, cv2.COLOR_RGB2HSV)
    h_chan = hsv[:, :, 0]
    s_chan = hsv[:, :, 1]
    v_chan = hsv[:, :, 2]

    # Healthy Green foliage: H in [25, 85], S > 25, V > 25
    green_mask = (h_chan >= 25) & (h_chan <= 85) & (s_chan >= 25) & (v_chan >= 25)
    # Chlorotic / Yellow / Light Brown foliage: H in [10, 25], S > 20, V > 25
    yellow_brown_mask = (h_chan >= 10) & (h_chan < 25) & (s_chan >= 20) & (v_chan >= 25)
    # Necrotic dark brown / lesion foliage: H in [0, 10] or [160, 180], S > 15, V in [20, 180]
    necrotic_mask = ((h_chan < 10) | (h_chan >= 160)) & (s_chan >= 15) & (v_chan >= 20) & (v_chan <= 180)

    vegetation_ratio = float(np.count_nonzero(green_mask | yellow_brown_mask) / total_pixels)
    plant_feature_ratio = float(np.count_nonzero(green_mask | yellow_brown_mask | necrotic_mask) / total_pixels)

    # 3. Soil Surface Tones (HSV: H in [0, 30] or [150, 180], V in [20, 210])
    soil_mask = ((h_chan <= 30) | (h_chan >= 150)) & (v_chan >= 20) & (v_chan <= 210)
    soil_ratio = float(np.count_nonzero(soil_mask) / total_pixels)

    # Texture variance via Laplacian
    gray = cv2.cvtColor(analysis_img, cv2.COLOR_RGB2GRAY)
    texture_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    metrics = {
        "vegetation_ratio": round(vegetation_ratio, 3),
        "plant_feature_ratio": round(plant_feature_ratio, 3),
        "skin_ratio": round(skin_ratio, 3),
        "soil_ratio": round(soil_ratio, 3),
        "texture_var": round(texture_var, 1),
    }

    if domain == "plant":
        # Rule 1: Detect Human Face / Selfie
        if skin_ratio > 0.16 and vegetation_ratio < 0.20:
            return False, "This image appears to contain a person or human face rather than a plant leaf. Please upload a clear photograph of a crop leaf.", metrics

        # Rule 2: Out-of-Domain Non-Plant Image
        if plant_feature_ratio < 0.08 and vegetation_ratio < 0.05:
            return False, "Invalid image: No plant leaf foliage detected. Please upload a clear, focused photo of a crop leaf.", metrics

        # Rule 3: Extremely Blurry or Featureless Image
        if texture_var < 5.0 and plant_feature_ratio < 0.15:
            return False, "Image is too blurry or featureless. Please capture a clear, well-lit photograph of a plant leaf.", metrics

        return True, "Valid plant leaf specimen", metrics

    elif domain == "soil":
        # Rule 1: Detect Human Face / Selfie
        if skin_ratio > 0.18:
            return False, "This image appears to contain a person or human face rather than a soil surface. Please upload a photo of soil or ground field surface.", metrics

        # Rule 2: Out-of-Domain Non-Soil Image
        if soil_ratio < 0.10 and vegetation_ratio < 0.10:
            return False, "Invalid image: No soil or field surface detected. Please upload a clear photo of topsoil or agricultural ground.", metrics

        return True, "Valid soil surface specimen", metrics

    return True, "Valid specimen", metrics

