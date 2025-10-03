from datetime import datetime
from collections import defaultdict

class InMemoryStorage:
    def __init__(self):
        self.submissions = []
    
    def add_submission(self, product_data, score, rating, suggestions):
        submission = {
            'id': len(self.submissions) + 1,
            'timestamp': datetime.now().isoformat(),
            'product_name': product_data['product_name'],
            'materials': product_data['materials'],
            'weight_grams': product_data['weight_grams'],
            'transport': product_data['transport'],
            'packaging': product_data['packaging'],
            'gwp': product_data['gwp'],
            'cost': product_data['cost'],
            'circularity': product_data['circularity'],
            'sustainability_score': score,
            'rating': rating,
            'suggestions': suggestions
        }
        self.submissions.append(submission)
        return submission
    
    def get_recent_submissions(self, limit=10):
        return self.submissions[-limit:] if self.submissions else []
    
    def get_summary_stats(self):
        if not self.submissions:
            return {
                'total_products': 0,
                'average_score': 0,
                'ratings': {},
                'top_issues': []
            }
        
        total_products = len(self.submissions)
        average_score = sum(s['sustainability_score'] for s in self.submissions) / total_products
        
        rating_counts = defaultdict(int)
        for submission in self.submissions:
            rating_counts[submission['rating']] += 1
        
        # Count common issues
        issue_counts = defaultdict(int)
        for submission in self.submissions:
            if any(material.lower() in ['plastic', 'styrofoam'] for material in submission['materials']):
                issue_counts['Plastic/Styrofoam used'] += 1
            if submission['transport'].lower() == 'air':
                issue_counts['Air transport'] += 1
            if submission['packaging'].lower() == 'non-recyclable':
                issue_counts['Non-recyclable packaging'] += 1
            if submission['gwp'] > 10:
                issue_counts['High GWP materials'] += 1
            if submission['circularity'] < 50:
                issue_counts['Low circularity'] += 1
        
        top_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_products': total_products,
            'average_score': round(average_score, 1),
            'ratings': dict(rating_counts),
            'top_issues': [issue for issue, _ in top_issues]
        }

storage = InMemoryStorage()