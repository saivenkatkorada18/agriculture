import json
from pathlib import Path

disease_info = {
  "classes": {
    "Apple___Apple_scab": {
      "crop": "Apple",
      "disease_name": "Apple Scab",
      "scientific_name": "Venturia inaequalis",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Olive-green to velvety dark brown lesions on leaves and fruit. Leaves twist, pucker, and yellow before dropping prematurely.",
      "causes": "Fungal pathogen overwintering in fallen leaf litter. Ascospores released during moist spring weather during bud break.",
      "organic_treatment": [
        "Rake and destroy fallen leaves in autumn to reduce spore inoculum.",
        "Apply liquid lime sulfur or elemental sulfur sprays during primary scab infection periods."
      ],
      "chemical_treatment": [
        "Apply protectant and systemic fungicides such as captan, myclobutanil, or cyprodinil timed with spring rainfall."
      ],
      "prevention_tips": [
        "Plant scab-resistant cultivars (e.g., Liberty, Prima, Enterprise).",
        "Prune tree canopy in dormant season to promote rapid drying and good air circulation."
      ]
    },
    "Apple___Black_rot": {
      "crop": "Apple",
      "disease_name": "Black Rot (Frogeye Leaf Spot)",
      "scientific_name": "Botryosphaeria obtusa",
      "is_healthy": False,
      "severity": "Moderate to High",
      "symptoms": "Purple spots on leaves expanding into circular spots with brown centers ('frogeye'). Fruit develops firm brown rot with concentric rings.",
      "causes": "Fungus entering through mechanical wounds, fire blight cankers, or dead wood.",
      "organic_treatment": [
        "Prune out dead shoots, mummified fruit, and cankered branches 15 cm below infection zones.",
        "Apply copper octanoate sprays at bud break."
      ],
      "chemical_treatment": [
        "Fungicide sprays including thiophanate-methyl, captan, or mancozeb from petal fall onwards."
      ],
      "prevention_tips": [
        "Remove all mummified apples from trees and orchard floor before spring growth.",
        "Maintain orchard sanitation and control insect vectors."
      ]
    },
    "Apple___Cedar_apple_rust": {
      "crop": "Apple",
      "disease_name": "Cedar Apple Rust",
      "scientific_name": "Gymnosporangium juniperi-virginianae",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Bright yellow-orange leaf spots on upper leaf surfaces. Orange tube-like sporangia develop on lower leaf surfaces, causing early defoliation.",
      "causes": "Heteroecious fungus requiring both apple trees and Eastern red cedar (Juniperus virginiana) to complete its lifecycle.",
      "organic_treatment": [
        "Remove nearby Eastern red cedar trees or galls within a 1-2 mile radius.",
        "Apply sulfur or neem oil sprays at pink bud stage."
      ],
      "chemical_treatment": [
        "Apply sterol-inhibiting fungicides (myclobutanil, propiconazole) from blossom cluster stage through petal fall."
      ],
      "prevention_tips": [
        "Select rust-resistant apple varieties (e.g., Freedom, Redfree, Enterprise).",
        "Eradicate wild junipers near the orchard perimeter."
      ]
    },
    "Apple___healthy": {
      "crop": "Apple",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Malus domestica",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Crisp green leaves with clear serrated margins, firm texture, and undamaged fruit clusters.",
      "causes": "Balanced soil nutrition, optimal moisture, and healthy canopy microclimate.",
      "organic_treatment": [
        "Apply organic compost mulch around tree root drip line."
      ],
      "chemical_treatment": [
        "No chemical intervention required."
      ],
      "prevention_tips": [
        "Routine dormant oil spray for scale and mite suppression.",
        "Install pheromone traps for codling moth scouting."
      ]
    },
    "Blueberry___healthy": {
      "crop": "Blueberry",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Vaccinium corymbosum",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Vibrant, thick deep-green leaves without chlorosis, rust spots, or stem dieback.",
      "causes": "Optimal acidic soil pH (4.5–5.5), well-drained organic soil, and proper irrigation.",
      "organic_treatment": [
        "Mulch with pine bark or wood chips to maintain soil acidity and moisture."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Monitor soil pH annually and apply elemental sulfur if pH rises above 5.2.",
        "Provide consistent drip irrigation to prevent drought stress."
      ]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
      "crop": "Cherry",
      "disease_name": "Powdery Mildew",
      "scientific_name": "Podosphaera clandestina",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "White to grayish powdery fungal patches on terminal leaves and young shoots. Affected leaves curl upward and drop.",
      "causes": "Fungal spores spreading during warm, dry days with high relative humidity at night.",
      "organic_treatment": [
        "Prune dense canopy to increase sunlight penetration.",
        "Apply potassium bicarbonate, sulfur, or neem oil sprays."
      ],
      "chemical_treatment": [
        "Apply systemic fungicides (myclobutanil, quinoxyfen, or tebuconazole) starting at shuck fall."
      ],
      "prevention_tips": [
        "Avoid high-nitrogen fertilizer applications late in the season.",
        "Prune water sprouts and suckers to keep foliage dry."
      ]
    },
    "Cherry_(including_sour)___healthy": {
      "crop": "Cherry",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Prunus avium",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Lush, glossy green foliage free of spots, yellowing, or leaf curl.",
      "causes": "Appropriate winter chilling hours, balanced soil fertility, and proper pruning.",
      "organic_treatment": [
        "Maintain clean tree basins free of weeds and fallen debris."
      ],
      "chemical_treatment": [
        "No treatment needed."
      ],
      "prevention_tips": [
        "Annual dormant pruning to balance leaf-to-fruit ratio.",
        "Regular monitoring for cherry fruit fly and aphid vectors."
      ]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
      "crop": "Corn (Maize)",
      "disease_name": "Gray Leaf Spot",
      "scientific_name": "Cercospora zeae-maydis",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Rectangular, tan-to-gray necrotic lesions bounded by leaf veins on lower leaves, turning blighted and necrotic.",
      "causes": "Fungal spores overwintering in corn stubble, favored by warm temperatures (25-30°C) and high humidity.",
      "organic_treatment": [
        "Plow down crop residue after harvest to accelerate decomposition."
      ],
      "chemical_treatment": [
        "Apply foliar fungicides (azoxystrobin, pyraclostrobin, propiconazole) at tasseling stage (VT to R1)."
      ],
      "prevention_tips": [
        "Plant corn hybrids with high resistance ratings for Gray Leaf Spot.",
        "Implement a 2-year crop rotation with non-host crops like soybeans or alfalfa."
      ]
    },
    "Corn_(maize)___Common_rust_": {
      "crop": "Corn (Maize)",
      "disease_name": "Common Rust",
      "scientific_name": "Puccinia sorghi",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Oval to elongated reddish-brown pustules scattered across both leaf surfaces. Pustules turn black as plants mature.",
      "causes": "Airborne spores blown northward from southern regions, favored by moist, cool-to-moderate weather (16-25°C).",
      "organic_treatment": [
        "Scout early; minor infections rarely reduce yield significantly.",
        "Apply bio-fungicides or sulfur dusts if detected early."
      ],
      "chemical_treatment": [
        "Apply strobilurin or triazole fungicides if rust reaches upper leaves before dent stage."
      ],
      "prevention_tips": [
        "Plant rust-resistant corn hybrids.",
        "Plant early in the season to complete grain fill prior to heavy spore buildup."
      ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
      "crop": "Corn (Maize)",
      "disease_name": "Northern Corn Leaf Blight",
      "scientific_name": "Setosphaeria turcica",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Long, elliptical cigar-shaped grayish-green to tan lesions (2.5 to 15 cm long) starting on lower leaves.",
      "causes": "Fungus overwintering in infected crop debris; spread by rain splash and wind.",
      "organic_treatment": [
        "Shred and deep-till residue following harvest."
      ],
      "chemical_treatment": [
        "Apply foliar fungicides at VT-R1 growth stage when disease threshold is reached."
      ],
      "prevention_tips": [
        "Select hybrid varieties carrying dominant Ht resistance genes.",
        "Rotate fields out of corn for at least 1-2 seasons."
      ]
    },
    "Corn_(maize)___healthy": {
      "crop": "Corn (Maize)",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Zea mays",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Vigorous, deep green leaves with intact leaf blades and parallel venation.",
      "causes": "Adequate NPK nutrition, optimal soil drainage, and good solar radiation.",
      "organic_treatment": [
        "Side-dress with organic nitrogen during V6 stage."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Maintain soil pH between 6.0 and 6.8.",
        "Ensure uniform planting depth and optimal seed spacing."
      ]
    },
    "Grape___Black_rot": {
      "crop": "Grape",
      "disease_name": "Black Rot",
      "scientific_name": "Phyllosticta ampelicida",
      "is_healthy": False,
      "severity": "Critical",
      "symptoms": "Small reddish-brown spots on leaves with black fruiting specks. Grapes shrivel into hard, black, wrinkled mummies.",
      "causes": "Overwinters in grape mummies on vines or soil; spores dispersed by rain splash during warm spring days.",
      "organic_treatment": [
        "Hand-pick and remove all mummified grape clusters during dormant pruning.",
        "Preventative copper and sulfur sprays."
      ],
      "chemical_treatment": [
        "Apply tebuconazole, myclobutanil, or azoxystrobin from early bloom through 4 weeks post-bloom."
      ],
      "prevention_tips": [
        "Thin foliage and pull leaves around fruit zones to promote fast canopy drying.",
        "Orient vineyard rows parallel to prevailing wind direction."
      ]
    },
    "Grape___Esca_(Black_Measles)": {
      "crop": "Grape",
      "disease_name": "Esca (Black Measles)",
      "scientific_name": "Phaeomoniella chlamydospora",
      "is_healthy": False,
      "severity": "High to Severe",
      "symptoms": "'Tiger-stripe' chlorotic and necrotic patterns on leaves. Berries display small dark purple spots ('measles') and dry out.",
      "causes": "Complex vascular fungal disease invading through pruning wounds on older wood.",
      "organic_treatment": [
        "Prune out infected cordons/spurs down to healthy wood and seal pruning cuts.",
        "Apply Trichoderma-based bio-fungicides to fresh cuts."
      ],
      "chemical_treatment": [
        "Apply pruning paint protectants (thiophanate-methyl) immediately after winter pruning."
      ],
      "prevention_tips": [
        "Practice double-pruning or late winter pruning during dry weather.",
        "Sanitize shears with 70% alcohol between vines."
      ]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
      "crop": "Grape",
      "disease_name": "Grape Leaf Blight",
      "scientific_name": "Pseudocercospora vitis",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Irregular dark brown to black spots on leaf surfaces with velvet-like spore growth under leaves. Causes early defoliation.",
      "causes": "High humidity and wet weather during late summer and autumn.",
      "organic_treatment": [
        "Collect and burn fallen leaves post-harvest.",
        "Bordeaux mixture or copper sprays."
      ],
      "chemical_treatment": [
        "Apply mancozeb or copper-based fungicides during late summer."
      ],
      "prevention_tips": [
        "Maintain open trellis system for maximum leaf sunlight exposure.",
        "Avoid excessive canopy shade."
      ]
    },
    "Grape___healthy": {
      "crop": "Grape",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Vitis vinifera",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Broad green leaves with sharp lobes, intact venation, and healthy cluster sets.",
      "causes": "Proper vine training, balanced moisture, and good root stock selection.",
      "organic_treatment": [
        "Mulch rows with organic straw to suppress weeds."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Routine canopy hedging and shoot positioning.",
        "Soil test annually for potassium and magnesium sufficiency."
      ]
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
      "crop": "Orange",
      "disease_name": "Huanglongbing (Citrus Greening)",
      "scientific_name": "Candidatus Liberibacter asiaticus",
      "is_healthy": False,
      "severity": "Critical",
      "symptoms": "Asymmetrical yellow mottling on leaves, yellow shoots, small lopsided bitter fruit that remains green at the bottom.",
      "causes": "Bacterium transmitted by the Asian citrus psyllid (Diaphorina citri).",
      "organic_treatment": [
        "Control citrus psyllid populations using horticultural oils and beneficial insect predators (Tamarixia radiata).",
        "Remove heavily infected trees to stem orchard spread."
      ],
      "chemical_treatment": [
        "Systemic insecticide soil drenches (imidacloprid, thiamethoxam) to suppress psyllids.",
        "Nutritional foliar sprays to prolong tree productivity."
      ],
      "prevention_tips": [
        "Plant only certified disease-free nursery stock from screenhouses.",
        "Install yellow sticky traps for vector monitoring."
      ]
    },
    "Peach___Bacterial_spot": {
      "crop": "Peach",
      "disease_name": "Bacterial Spot",
      "scientific_name": "Xanthomonas arboricola pv. pruni",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Small angular purple to dark brown spots on leaves that drop out creating a 'shot-hole' appearance. Pitted, cracked spots on fruit.",
      "causes": "Bacterium entering stomata during warm, humid spring rainstorms.",
      "organic_treatment": [
        "Apply copper sprays at bud break.",
        "Apply bio-bactericides (Bacillus subtilis)."
      ],
      "chemical_treatment": [
        "Oxytetracycline or copper-mancozeb tank mixes applied during bloom and shuck split."
      ],
      "prevention_tips": [
        "Plant resistant peach varieties (e.g., Candor, Reliance, Sentinel).",
        "Avoid overhead irrigation."
      ]
    },
    "Peach___healthy": {
      "crop": "Peach",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Prunus persica",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Lance-shaped vibrant green leaves without leaf curl, shot-holes, or gumming.",
      "causes": "Proper dormant oil applications, adequate sun, and proper drainage.",
      "organic_treatment": [
        "Maintain clean orchard floor."
      ],
      "chemical_treatment": [
        "No treatment needed."
      ],
      "prevention_tips": [
        "Apply copper during dormant season to prevent peach leaf curl.",
        "Prune center of tree for open vase canopy."
      ]
    },
    "Pepper,_bell___Bacterial_spot": {
      "crop": "Pepper (Bell)",
      "disease_name": "Bacterial Spot",
      "scientific_name": "Xanthomonas campestris pv. vesicatoria",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Small blistering dark spots on leaves with yellow halos, leading to severe defoliation and scabby fruit spots.",
      "causes": "Seed-borne bacterium spread by rain splash, overhead irrigation, and handling wet foliage.",
      "organic_treatment": [
        "Copper hydroxide plus bio-bactericide sprays.",
        "Hot water seed treatment (50°C for 25 min)."
      ],
      "chemical_treatment": [
        "Copper bactericides mixed with mancozeb for copper-resistant strains."
      ],
      "prevention_tips": [
        "Use certified disease-free seeds and resistant varieties.",
        "Avoid working in pepper fields when foliage is wet."
      ]
    },
    "Pepper,_bell___healthy": {
      "crop": "Pepper (Bell)",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Capsicum annuum",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Glossy green leaves with intact epidermis and vigorous flowers.",
      "causes": "Warm soil, steady moisture, and balanced calcium nutrition.",
      "organic_treatment": [
        "Drip irrigation and organic mulch."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Stake plants to support heavy pepper yield.",
        "Maintain constant moisture to avoid blossom end rot."
      ]
    },
    "Potato___Early_blight": {
      "crop": "Potato",
      "disease_name": "Early Blight",
      "scientific_name": "Alternaria solani",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Brown concentric ring spots on older leaves turning necrotic, causing leaf drop.",
      "causes": "Fungal spores overwintering in soil debris, spread by wind and rain.",
      "organic_treatment": [
        "Copper octanoate sprays at first symptom.",
        "Prune infected lower foliage."
      ],
      "chemical_treatment": [
        "Chlorothalonil, mancozeb, or azoxystrobin sprays."
      ],
      "prevention_tips": [
        "3-year crop rotation out of Solanaceae.",
        "Kill vines 2-3 weeks prior to harvest."
      ]
    },
    "Potato___Late_blight": {
      "crop": "Potato",
      "disease_name": "Late Blight",
      "scientific_name": "Phytophthora infestans",
      "is_healthy": False,
      "severity": "Critical",
      "symptoms": "Water-soaked dark lesions on leaves turning black with white fuzzy growth underneath in humid conditions.",
      "causes": "Cool, wet weather. Infected seed tubers primary source of field inoculum.",
      "organic_treatment": [
        "Destroy and dispose of infected plants immediately.",
        "Fixed copper sprays."
      ],
      "chemical_treatment": [
        "Metalaxyl, cyazofamid, or dimethomorph systemic fungicides."
      ],
      "prevention_tips": [
        "Plant certified disease-free seed potatoes.",
        "Eliminate cull piles near potato fields."
      ]
    },
    "Potato___healthy": {
      "crop": "Potato",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Solanum tuberosum",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Deep green foliage with thick stems and no chlorosis or leaf spots.",
      "causes": "Clean seed stock and well-drained fertile soil.",
      "organic_treatment": [
        "Hill soil around stem bases to protect tubers."
      ],
      "chemical_treatment": [
        "No treatment needed."
      ],
      "prevention_tips": [
        "Scout for Colorado potato beetles.",
        "Maintain consistent drip watering."
      ]
    },
    "Raspberry___healthy": {
      "crop": "Raspberry",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Rubus idaeus",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Bright green compound leaves with serrated margins and healthy canes.",
      "causes": "Well-drained soil, raised beds, and proper cane trellising.",
      "organic_treatment": [
        "Apply organic compost to cane base."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Prune out old floricanes after fruiting.",
        "Maintain air gaps between canes."
      ]
    },
    "Soybean___healthy": {
      "crop": "Soybean",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Glycine max",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Trifoliate green leaves without rust pustules, yellowing, or leaf spots.",
      "causes": "Optimal Rhizobium inoculation and balanced soil nutrients.",
      "organic_treatment": [
        "Inoculate seed with Rhizobium japonicum before planting."
      ],
      "chemical_treatment": [
        "No treatment needed."
      ],
      "prevention_tips": [
        "Rotate with corn to break pest cycles.",
        "Maintain clean weed-free canopy boundaries."
      ]
    },
    "Squash___Powdery_mildew": {
      "crop": "Squash",
      "disease_name": "Powdery Mildew",
      "scientific_name": "Podosphaera xanthii",
      "is_healthy": False,
      "severity": "Moderate to High",
      "symptoms": "White powdery fungal growth covering upper and lower leaf surfaces, causing leaves to turn brown and dry up.",
      "causes": "Airborne fungal spores favored by dry weather and high humidity in dense canopies.",
      "organic_treatment": [
        "Potassium bicarbonate, neem oil, or sulfur sprays.",
        "Prune old heavily shaded leaves."
      ],
      "chemical_treatment": [
        "Myclobutanil, triflumizole, or azoxystrobin sprays."
      ],
      "prevention_tips": [
        "Plant resistant squash cultivars.",
        "Avoid overhead irrigation."
      ]
    },
    "Strawberry___Leaf_scorch": {
      "crop": "Strawberry",
      "disease_name": "Leaf Scorch",
      "scientific_name": "Diplocarpon earlianum",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Numerous small dark purple spots on leaves expanding into blotches. Leaves dry up and look scorched.",
      "causes": "Fungus overwintering on diseased leaves; spread by rain splash.",
      "organic_treatment": [
        "Mow and collect old leaves post-harvest.",
        "Copper sprays in early spring."
      ],
      "chemical_treatment": [
        "Captan or myclobutanil sprays from leaf emergence to bloom."
      ],
      "prevention_tips": [
        "Plant resistant strawberry varieties.",
        "Use straw mulch to prevent splash infection."
      ]
    },
    "Strawberry___healthy": {
      "crop": "Strawberry",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Fragaria × ananassa",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Deep green shiny leaves with clean petioles and healthy runner plants.",
      "causes": "Raised bed production, clean drip irrigation, and straw mulching.",
      "organic_treatment": [
        "Mulch beds with pine straw."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Renovate strawberry beds annually.",
        "Scout for spider mites."
      ]
    },
    "Tomato___Bacterial_spot": {
      "crop": "Tomato",
      "disease_name": "Bacterial Spot",
      "scientific_name": "Xanthomonas vesicatoria",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Small water-soaked dark spots on leaves surrounded by yellow halos, causing leaf drop and rough spots on fruit.",
      "causes": "Seed-borne bacterial pathogen spread by rain and wind.",
      "organic_treatment": [
        "Copper octanoate combined with bio-bactericide.",
        "Hot water seed treatment."
      ],
      "chemical_treatment": [
        "Copper plus mancozeb sprays."
      ],
      "prevention_tips": [
        "Plant resistant varieties.",
        "Use drip irrigation."
      ]
    },
    "Tomato___Early_blight": {
      "crop": "Tomato",
      "disease_name": "Early Blight",
      "scientific_name": "Alternaria solani",
      "is_healthy": False,
      "severity": "Moderate to High",
      "symptoms": "Dark brown spots with concentric target-board rings on lower leaves, causing leaf yellowing and drop.",
      "causes": "Fungi surviving in soil and plant residue.",
      "organic_treatment": [
        "Prune infected lower leaves.",
        "Apply copper sprays."
      ],
      "chemical_treatment": [
        "Chlorothalonil or mancozeb."
      ],
      "prevention_tips": [
        "2-3 year crop rotation.",
        "Mulch plant bases."
      ]
    },
    "Tomato___Late_blight": {
      "crop": "Tomato",
      "disease_name": "Late Blight",
      "scientific_name": "Phytophthora infestans",
      "is_healthy": False,
      "severity": "Critical",
      "symptoms": "Large water-soaked lesions turning dark brown with white fuzzy mold on leaf undersides.",
      "causes": "Cool wet conditions.",
      "organic_treatment": [
        "Remove and destroy infected plants.",
        "Copper sprays."
      ],
      "chemical_treatment": [
        "Cymoxanil, mandipropamid, fluopicolide."
      ],
      "prevention_tips": [
        "Plant resistant varieties.",
        "Ensure fast leaf drying."
      ]
    },
    "Tomato___Leaf_Mold": {
      "crop": "Tomato",
      "disease_name": "Leaf Mold",
      "scientific_name": "Passalora fulva",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Pale green yellow spots on upper leaf surfaces, olive velvet mold on undersides.",
      "causes": "High humidity (>85%) in greenhouses.",
      "organic_treatment": [
        "Increase greenhouse ventilation.",
        "Bio-fungicide sprays."
      ],
      "chemical_treatment": [
        "Copper hydroxide or difenoconazole."
      ],
      "prevention_tips": [
        "Keep relative humidity below 80%.",
        "Space plants well."
      ]
    },
    "Tomato___Septoria_leaf_spot": {
      "crop": "Tomato",
      "disease_name": "Septoria Leaf Spot",
      "scientific_name": "Septoria lycopersici",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Small circular spots with dark brown margins and gray centers containing tiny black specks.",
      "causes": "Fungus overwintering on tomato crop residue and Solanaceous weeds.",
      "organic_treatment": [
        "Prune diseased lower foliage.",
        "Apply copper fungicides."
      ],
      "chemical_treatment": [
        "Chlorothalonil or mancozeb applied preventatively."
      ],
      "prevention_tips": [
        "Mulch heavily under plants.",
        "Avoid overhead watering."
      ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
      "crop": "Tomato",
      "disease_name": "Two-Spotted Spider Mites",
      "scientific_name": "Tetranychus urticae",
      "is_healthy": False,
      "severity": "Moderate to High",
      "symptoms": "Yellow stippling/speckling on leaf surfaces with fine silken webbing on undersides. Leaves turn bronze and dry up.",
      "causes": "Hot, dry conditions accelerating mite reproduction.",
      "organic_treatment": [
        "Spray leaves with insecticidal soap or neem oil.",
        "Release predatory mites (Phytoseiulus persimilis)."
      ],
      "chemical_treatment": [
        "Apply selective miticides (abamectin, bifenazate)."
      ],
      "prevention_tips": [
        "Avoid excessive nitrogen fertilization.",
        "Keep field dust under control."
      ]
    },
    "Tomato___Target_Spot": {
      "crop": "Tomato",
      "disease_name": "Target Spot",
      "scientific_name": "Corynespora cassiicola",
      "is_healthy": False,
      "severity": "Moderate",
      "symptoms": "Small necrotic leaf spots expanding into circular lesions with light brown centers and dark borders.",
      "causes": "High humidity and warm weather.",
      "organic_treatment": [
        "Copper sprays.",
        "Prune low canopy."
      ],
      "chemical_treatment": [
        "Azoxystrobin or chlorothalonil."
      ],
      "prevention_tips": [
        "Maintain crop rotation.",
        "Space plants for ventilation."
      ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
      "crop": "Tomato",
      "disease_name": "Tomato Yellow Leaf Curl Virus",
      "scientific_name": "Beguomovirus (TYLCV)",
      "is_healthy": False,
      "severity": "Critical",
      "symptoms": "Severe leaf stunting, upward leaf curling, yellowing leaf margins, and bushy plant growth with zero fruit set.",
      "causes": "Virus vectored by silverleaf whiteflies (Bemisia tabaci).",
      "organic_treatment": [
        "Cover crops with fine insect netting.",
        "Apply neem oil or insecticidal soaps to kill whiteflies."
      ],
      "chemical_treatment": [
        "Apply systemic insecticides (imidacloprid, spirotetramat) to control whitefly vector."
      ],
      "prevention_tips": [
        "Plant TYLCV-resistant tomato cultivars (e.g., Tycoon, Inbar).",
        "Use reflective silver mulches to repel whiteflies."
      ]
    },
    "Tomato___Tomato_mosaic_virus": {
      "crop": "Tomato",
      "disease_name": "Tomato Mosaic Virus",
      "scientific_name": "Tobamovirus (ToMV)",
      "is_healthy": False,
      "severity": "High",
      "symptoms": "Light and dark green mosaic patterns on leaves, fern-like leaf distortion, and internal brown fruit necrosis.",
      "causes": "Highly contagious virus spread mechanically on hands, tools, and seeds.",
      "organic_treatment": [
        "Remove and destroy infected plants immediately.",
        "Wash hands and tools in skim milk or 10% trisodium phosphate (TSP)."
      ],
      "chemical_treatment": [
        "No chemical cure exists for viral plant infections."
      ],
      "prevention_tips": [
        "Use certified virus-free seeds.",
        "Prohibit tobacco use near tomato production areas."
      ]
    },
    "Tomato___healthy": {
      "crop": "Tomato",
      "disease_name": "Healthy Foliage",
      "scientific_name": "Solanum lycopersicum",
      "is_healthy": True,
      "severity": "None",
      "symptoms": "Vibrant green foliage with uniform leaf surface, robust stems, and healthy blossom clusters.",
      "causes": "Balanced nutrition, proper staking, and clean environment.",
      "organic_treatment": [
        "Mulch and compost tea applications."
      ],
      "chemical_treatment": [
        "No treatment required."
      ],
      "prevention_tips": [
        "Weekly scouting for hornworms and aphids.",
        "Maintain drip watering schedule."
      ]
    }
  }
}

target_file = Path(r"c:\Users\saive\OneDrive\Documents\angriculture\ml\models\disease_info.json")
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(disease_info, f, indent=2)

print("Successfully wrote disease_info.json with", len(disease_info["classes"]), "classes.")
