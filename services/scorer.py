import config

class SustainabilityScorer:
    @staticmethod
    def calculate_score(product_data, weights=None):
        if weights is None:
            weights = {
                'gwp_weight': config.GWP_WEIGHT,
                'circularity_weight': config.CIRCULARITY_WEIGHT,
                'cost_weight': config.COST_WEIGHT
            }
        
        # GWP impact (lower is better)
        gwp_penalty = min(product_data['gwp'] * 2, 50)
        
        # Cost impact (normalized, higher cost = lower sustainability)
        cost_penalty = min(product_data['cost'], 30)
        
        # Circularity bonus (higher is better)
        circularity_bonus = product_data['circularity'] * 0.3
        
        # Material penalties
        material_penalty = sum(config.MATERIAL_PENALTIES.get(material.lower(), 0) 
                             for material in product_data['materials'])
        
        # Transport penalty
        transport_penalty = config.TRANSPORT_PENALTIES.get(product_data['transport'].lower(), 0)
        
        # Packaging penalty
        packaging_penalty = config.PACKAGING_PENALTIES.get(product_data['packaging'].lower(), 0)
        
        # Weight penalty
        weight_penalty = 0
        if product_data['weight_grams'] > config.WEIGHT_PENALTY_THRESHOLD:
            excess_weight = product_data['weight_grams'] - config.WEIGHT_PENALTY_THRESHOLD
            weight_penalty = excess_weight * config.WEIGHT_PENALTY_RATE
        
        # Weighted calculation
        gwp_component = (100 - gwp_penalty) * weights['gwp_weight']
        circularity_component = (product_data['circularity'] + circularity_bonus) * weights['circularity_weight'] / 100 * 100
        cost_component = (100 - cost_penalty) * weights['cost_weight']
        
        weighted_score = gwp_component + circularity_component + cost_component
        
        # Apply other penalties
        final_score = weighted_score - material_penalty - transport_penalty - packaging_penalty - weight_penalty
        
        return max(0, min(100, final_score))
    
    @staticmethod
    def get_rating(score):
        for rating, threshold in config.SCORE_THRESHOLDS.items():
            if score >= threshold:
                return rating
        return 'F'
    
    @staticmethod
    def generate_suggestions(product_data, score):
        suggestions = []
        
        if product_data['gwp'] > 10:
            suggestions.append("Consider materials with lower Global Warming Potential")
        
        if any(material.lower() in ['plastic', 'styrofoam'] for material in product_data['materials']):
            suggestions.append("Replace plastic/styrofoam with sustainable alternatives")
        
        if product_data['transport'].lower() == 'air':
            suggestions.append("Avoid air transport - use ground or sea shipping")
        
        if product_data['packaging'].lower() == 'non-recyclable':
            suggestions.append("Switch to recyclable or biodegradable packaging")
        
        if product_data['weight_grams'] > config.WEIGHT_PENALTY_THRESHOLD:
            suggestions.append("Optimize product design to reduce weight")
        
        if product_data['circularity'] < 50:
            suggestions.append("Improve product circularity and end-of-life considerations")
        
        if product_data['cost'] > 50:
            suggestions.append("Optimize cost efficiency while maintaining sustainability")
        
        if score < 60:
            suggestions.append("Consider comprehensive sustainability redesign")
        
        return suggestions[:4]