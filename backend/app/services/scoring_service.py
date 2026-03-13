from app.config import Config
import logging

logger = logging.getLogger(__name__)

def calculate_authenticity_score(domain_verified: bool, semantic_similarity: float, fraud_penalty: float) -> dict:
    """
    Weighted score:
    - Domain verification weight = 0.40
    - Semantic similarity weight = 0.35
    - Fraud detection weight = 0.25 (as a penalty)
    """
    
    # 0.0 to 1.0 for each factor
    domain_score = 1.0 if domain_verified else 0.0
    similarity_score = max(0.0, min(1.0, semantic_similarity))
    
    # The fraud score is inverted (1.0 = no fraud, 0.0 = high fraud)
    fraud_score = 1.0 - fraud_penalty
    
    raw_score = (
        (domain_score * Config.DOMAIN_VERIFICATION_WEIGHT) +
        (similarity_score * Config.SEMANTIC_SIMILARITY_WEIGHT) +
        (fraud_score * Config.FRAUD_DETECTION_WEIGHT)
    )
    
    # Map raw_score (0.0 - 1.0) to final score (1-5)
    if raw_score >= 0.80:
        final_score = 5
    elif raw_score >= 0.60:
        final_score = 4
    elif raw_score >= 0.40:
        final_score = 3
    elif raw_score >= 0.20:
        final_score = 2
    else:
        final_score = 1
        
    return {
        'raw_score': round(raw_score, 4),
        'authenticity_score': final_score,
        'breakdown': {
            'domain_contribution': round(domain_score * Config.DOMAIN_VERIFICATION_WEIGHT, 4),
            'similarity_contribution': round(similarity_score * Config.SEMANTIC_SIMILARITY_WEIGHT, 4),
            'fraud_contribution': round(fraud_score * Config.FRAUD_DETECTION_WEIGHT, 4)
        }
    }
