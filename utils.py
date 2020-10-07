import numpy as np

def assertVectorEqual(vec1, vec2, rtol):
    result=np.sqrt(np.square(vec1-vec2))<rtol
    return np.all(result)