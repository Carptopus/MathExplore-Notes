"""S30完整376个标量层及Bernoulli适用门负控，不采样原矩阵参数。"""

from fractions import Fraction as F
from math import comb, factorial
import hashlib
import json

MIN_N = 16
MAX_N = 31


def occupancy_poly(occ):
    out = [F(1)]
    for v in occ:
        following = [F(0)] * (len(out)+1)
        for k,a in enumerate(out):
            following[k] += a
            following[k+1] += v*a
        out = following
    return out


def gamma(poly,n,j):
    if not MIN_N <= n <= MAX_N or not 0 <= j <= n:
        raise ValueError('固定完整标量域16<=n<=31，0<=j<=n')
    assert len(poly) == n+1
    return sum(F(comb(j,k)*factorial(n-k),comb(n,k)*n**(n-k))*poly[k]
               for k in range(j+1)) / 2**j


def cdf_one(parameters):
    out = [F(1)]
    for t in parameters:
        assert 0 <= t <= 1
        following = [F(0)] * (len(out)+1)
        for k,a in enumerate(out):
            following[k] += (1-t)*a
            following[k+1] += t*a
        out = following
    return sum(out[:2])


def main():
    assert sum(F(1,factorial(k)) for k in range(6)) == F(163,60) > F(27,10)
    assert F(27,10)**11 > 15**4
    assert F(22,7) < F(169,50)
    # mu=3/2时无条件Poisson尾门确实错误；用精确exp下界给严格负控。
    assert cdf_one([F(1),F(1,4),F(1,4)]) == F(9,16)
    exp_lower = sum(F(3,2)**k/factorial(k) for k in range(7))
    assert exp_lower > F(40,9)
    for params in ([F(1),F(1)], [F(3,4),F(3,4),F(1,2)]):
        original = cdf_one(params)
        for t in params:
            others = list(params); others.remove(t)
            assert sum(others) >= 1
            assert cdf_one([*others,t/2,t/2]) >= original
    records = []
    margins = []
    for n in range(MIN_N,MAX_N+1):
        b = occupancy_poly([1]*n)
        f1 = occupancy_poly([2]+[1]*(n-2)+[0])
        f2 = occupancy_poly([2,2]+[1]*(n-4)+[0,0])
        cn = F(factorial(n),n**n)
        zn = F(1,2**(n-1))
        env = [zn*x+F(1,4)*y+(F(3,4)-zn)*z for x,y,z in zip(b,f1,f2)]
        assert gamma(env,n,0) == cn
        assert gamma(b,n,n) < F(1,1024)
        for j in range(1,n+1):
            assert gamma(f1,n,j) >= gamma(f2,n,j)
            slope = F(j,2*n)-gamma(b,n,j)+gamma(f2,n,j)
            margin = (1-F(j,2*n))*cn+F(j,2*n)*zn-gamma(env,n,j)
            assert slope > 0 and margin > 0
            margins.append(f'{n}:{j}:{margin.numerator}/{margin.denominator}')
        records.append({'n':n,'all_half_interval_layers':n,'strict_margins':'EXACT_POSITIVE'})
    assert len(margins) == 376
    digest = hashlib.sha256('\n'.join(margins).encode('ascii')).hexdigest()
    print(json.dumps({'scope':'COMPLETE_SCALAR_WINDOW_NOT_MATRIX_ENUMERATION',
                      'records':records,'certified_layers':len(margins),'margin_sha256':digest,
                      'mu_below_two_shortcut':'REJECTED','general_parameter_bridge':'REQUIRES_PROOF_AUDIT',
                      'n_3_to_15':'UNPROVED'}))


if __name__ == '__main__': main()
