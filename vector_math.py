def dot_prod(v1, v2):
    product = 0
    for n in range(3):
        product += v1[n] * v2[n]
    return product


def cross_prod(v1, v2):
    product = [0, 0, 0]
    product[0] = (v1[1]*v2[2]) - (v1[2]*v2[1])
    product[1] = (v1[2]*v2[0]) - (v1[0]*v2[2])
    product[2] = (v1[0]*v2[1]) - (v1[1]*v2[0])
    return product


def add_vect(v1, v2):
    resultant = [0, 0, 0]
    for n in range(3):
        resultant[n] = v1[n] + v2[n]
    return resultant


def subtract(v1, v2):
    resultant = [0, 0, 0]
    for n in range(3):
        resultant[n] = v1[n] - v2[n]
    return resultant


def scalar_mult(k, v):
    resultant = [0, 0, 0]
    for n in range(3):
        resultant[n] = k * v[n]
    return resultant


def magnitude(v):
    vector = list(map(lambda x: x**2, v))
    result = sum(vector) ** .5
    return result
