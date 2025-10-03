GWP_WEIGHT = 0.4
CIRCULARITY_WEIGHT = 0.3
COST_WEIGHT = 0.3

MATERIAL_PENALTIES = {
    'plastic': 15,
    'styrofoam': 25,
    'aluminum': 5,
    'steel': 8,
    'glass': 3,
    'wood': -5,
    'bamboo': -10,
    'cardboard': -3
}

TRANSPORT_PENALTIES = {
    'air': 30,
    'truck': 15,
    'ship': 5,
    'rail': 3,
    'local': -5
}

PACKAGING_PENALTIES = {
    'non-recyclable': 20,
    'recyclable': 0,
    'biodegradable': -10,
    'reusable': -15
}

WEIGHT_PENALTY_THRESHOLD = 500  # grams
WEIGHT_PENALTY_RATE = 0.02  # penalty per gram over threshold

SCORE_THRESHOLDS = {
    'A': 80,
    'B': 60,
    'C': 40,
    'D': 0
}