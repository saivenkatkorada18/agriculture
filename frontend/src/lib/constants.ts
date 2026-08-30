/**
 * Application Constants & Sample Agricultural Contexts
 */

export const SUPPORTED_CROPS = [
  { id: 'tomato', name: 'Tomato', icon: '🍅', diseases: ['Early Blight', 'Late Blight', 'Leaf Mold', 'Healthy'] },
  { id: 'potato', name: 'Potato', icon: '🥔', diseases: ['Early Blight', 'Late Blight', 'Healthy'] },
  { id: 'corn', name: 'Corn (Maize)', icon: '🌽', diseases: ['Common Rust', 'Northern Leaf Blight', 'Healthy'] },
  { id: 'apple', name: 'Apple', icon: '🍎', diseases: ['Apple Scab', 'Black Rot', 'Healthy'] },
  { id: 'grape', name: 'Grape', icon: '🍇', diseases: ['Black Rot', 'Leaf Blight'] },
  { id: 'pepper', name: 'Bell Pepper', icon: '🫑', diseases: ['Bacterial Spot', 'Healthy'] },
];

export const ASSISTANT_PROMPT_CHIPS = [
  "How do I prevent Early Blight in tomatoes?",
  "What does soil surface cracking indicate about watering?",
  "Organic treatment for powdery mildew and leaf mold",
  "How to distinguish nitrogen deficiency from disease?",
  "Best cover crops to boost soil organic matter",
];

export const SAMPLE_TEST_CASES = [
  {
    type: 'plant',
    label: 'Tomato Early Blight (Foliar)',
    description: 'Dark concentric brown rings on lower leaves',
    color: '#845327',
  },
  {
    type: 'plant',
    label: 'Corn Common Rust (Pustules)',
    description: 'Elongated reddish-cinnamon pustules',
    color: '#c2410c',
  },
  {
    type: 'plant',
    label: 'Healthy Bell Pepper Leaf',
    description: 'Vibrant green chlorophyll foliage',
    color: '#15803d',
  },
  {
    type: 'soil',
    label: 'Dry Soil with Surface Cracking',
    description: 'High fissure density, pale dry crusting',
    color: '#a18072',
  },
  {
    type: 'soil',
    label: 'Moist Humic Agricultural Loam',
    description: 'Dark brown crumb texture with organic residue',
    color: '#4a3227',
  },
];
