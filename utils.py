import numpy as np

#Assert ||vec-vec2||<rtol
def assertVectorEqual(vec1, vec2, rtol):
    result=np.sqrt(np.square(vec1-vec2))<rtol
    return np.all(result)