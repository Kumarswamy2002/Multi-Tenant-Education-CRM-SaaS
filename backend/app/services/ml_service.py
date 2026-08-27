import numpy as np
from typing import List, Dict, Any
from sklearn.linear_model import LogisticRegression
from app.context import TenantContext


class MLIntelligenceService:
    """
    Machine Learning Platform Service for Scikit-Learn based lead scoring models and skill vector matching.
    """

    def __init__(self):
        # Synthetic baseline model for demonstration & local inference
        self.model = LogisticRegression()
        X_train = np.array([
            [1, 10, 1],
            [0, 2, 0],
            [1, 15, 2],
            [0, 1, 0],
            [1, 20, 3]
        ])
        y_train = np.array([1, 0, 1, 0, 1])
        self.model.fit(X_train, y_train)

    def predict_conversion_probability(self, has_academic_interest: bool, engagement_score: float, custom_fields_count: int) -> float:
        feat = np.array([[1 if has_academic_interest else 0, engagement_score, custom_fields_count]])
        prob = self.model.predict_proba(feat)[0][1]
        return round(float(prob * 100), 2)

    @staticmethod
    def calculate_skill_similarity(candidate_skills: List[str], required_skills: List[str]) -> float:
        if not candidate_skills or not required_skills:
            return 0.0
        set_cand = set(s.lower().strip() for s in candidate_skills)
        set_req = set(s.lower().strip() for s in required_skills)
        intersection = set_cand.intersection(set_req)
        return round((len(intersection) / len(set_req)) * 100, 2)
