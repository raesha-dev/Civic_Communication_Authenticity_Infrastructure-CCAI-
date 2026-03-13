import re

# Lightweight rule-based detection for Hackathon MVP
SCAM_KEYWORDS = ['urgent', 'act now', 'immediate action required', 'account suspended', 'click here to verify']
PAYMENT_KEYWORDS = ['wire transfer', 'cryptocurrency', 'bitcoin', 'gift card', 'western union', 'venmo', 'cashapp']

def detect_fraud_signals(text: str) -> dict:
    text_lower = text.lower()
    
    flags = []
    
    # Check for urgency manipulation
    urgency_matches = [phrase for phrase in SCAM_KEYWORDS if phrase in text_lower]
    if urgency_matches:
        flags.append({
            'type': 'URGENCY_MANIPULATION',
            'description': 'Contains language typical of urgent scam manipulation.',
            'matches': urgency_matches
        })
        
    # Check for suspicious payment routing
    payment_matches = [phrase for phrase in PAYMENT_KEYWORDS if phrase in text_lower]
    if payment_matches:
        flags.append({
            'type': 'SUSPICIOUS_PAYMENT',
            'description': 'Requests unconventional payment methods.',
            'matches': payment_matches
        })
        
    score_reduction = min(len(flags) * 0.4, 1.0) # Up to 1.0 reduction depending on severity
    
    return {
        'has_fraud_signals': len(flags) > 0,
        'flags': flags,
        'fraud_score_penalty': score_reduction
    }
