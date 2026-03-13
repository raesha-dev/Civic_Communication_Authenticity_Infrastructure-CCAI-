import numpy as np

def compute_cosine_similarity(vec_a: list, vec_b: list) -> float:
    a = np.array(vec_a)
    b = np.array(vec_b)
    
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
        
    cosine_similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(cosine_similarity)
