
import numpy as np


# Convenience zfill function
def zfill(a, width=None):
    if width is None:
        return a
    elif hasattr(a, '__getitem__'):
        return np.char.zfill(list(map(str, a)), width)
    else:
        return str(a).zfill(width)


# Convenience zfill range function
def zfillr(n, width=None):
    return zfill(range(n), width)


if __name__ == '__main__':
    print(zfill(range(5), 2))
