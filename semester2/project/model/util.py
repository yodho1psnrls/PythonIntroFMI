def sign(x):
    return int(x / abs(x) if bool(x) else 1)
    # return x / abs(x) * bool(x) + not bool(x)
