from sys import getsizeof
import pyarrow as pa
from functools import wraps
import numpy as np

@wraps
def log_reduction(func):
    def inner(func, *args, **kargs):
        # size_before = getsizeof(args)
        size_before = 0
        ret = func(*args, **kargs)
        # size_after = getsizeof(args)
        size_after = 0

        # Calculating the diff in system memory
        delta = size_before / size_after
        delta_sign = '+' if delta>=0 else '-'
        print(f'size change: {delta_sign:.2f}')
        return ret
    return inner(func)

@log_reduction
def serialize(obj):
    # obj = pa.serialize(obj.data.tobytes())
    return obj

@log_reduction
def deserialize(obj):
    # obj =  pa.deserialize(obj).to_numpy().reshape((1,3,224,224))
    return obj


if __name__ == '__main__':
    print('pyten started')
    x = np.random.random((1,3,224,224)).astype('float32')
    _x = serialize(x)
    x2 = deserialize(_x)
    np.testing.assert_allclose(x,x2, atol=1e-7)