from app.aws.dynamodb_client import query_registry

def verify_institutional_source(domain: str, entity_name: str) -> dict:
    results = query_registry(entity_name, domain)
    
    if results and len(results) > 0:
        best_match = results[0]
        return {
            'is_verified': True,
            'match': best_match,
            'source_entity': best_match.get('entity_name'),
            'confidence': float(best_match.get('confidence', 0.9))
        }
        
    return {
        'is_verified': False,
        'match': None,
        'source_entity': None,
        'confidence': 0.0
    }
