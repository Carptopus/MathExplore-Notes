"""S31无原参数的92层完整耦合证书；不是原矩阵离散采样。"""

from fractions import Fraction as F
from math import comb, factorial
import hashlib
import json

MIN_N = 8
MAX_N = 15


def occ_poly(occ):
    out = [F(1)]
    for v in occ:
        nxt = [F(0)] * (len(out)+1)
        for k,x in enumerate(out):
            nxt[k] += x
            nxt[k+1] += v*x
        out = nxt
    return out


def gamma(poly,n,j):
    if not MIN_N<=n<=MAX_N or not 0<=j<=n:
        raise ValueError('完整标量域8<=n<=15，0<=j<=n')
    assert len(poly)==n+1
    return sum(F(comb(j,k)*factorial(n-k),comb(n,k)*n**(n-k))*poly[k]
               for k in range(j+1))/2**j


def exp_lower(x):
    assert x>=0
    return sum(x**k/factorial(k) for k in range(13))


def main():
    assert F(65,24)+F(1,100)<F(11,4)
    mu=F(3,2)
    values={}
    for n,last in ((2,4),(3,3),(4,3),(5,2)):
        bracket=1/(1+mu)-F(n-1,2*n)
        if last>=3:bracket-=F(n-1,3*n*n)*mu
        if last>=4:bracket-=F(n-1,4*n**3)*mu**2
        assert bracket<=0
        values[n]=f'{bracket.numerator}/{bracket.denominator}'
    assert values[2]=='-29/640'
    assert values[3]=='-2/45'
    assert values[4]=='-11/160'
    # 不能删确定1分支，只留下Poisson项。
    exp_three_halves=sum(F(3,2)**k/factorial(k) for k in range(7))
    assert F(9,16)*exp_three_halves>F(5,2)
    records=[]
    for n in range(MIN_N,MAX_N+1):
        b=occ_poly([1]*n)
        f1=occ_poly([2]+[1]*(n-2)+[0])
        f2=occ_poly([2,2]+[1]*(n-4)+[0,0])
        cn=F(factorial(n),n**n);zn=F(1,2**(n-1))
        t=F(n-1,2);mu_star=t/2
        q=(1+mu_star)/exp_lower(mu_star)
        assert gamma(b,n,0)==cn
        for j in range(1,n+1):
            aa=(1-F(j,2*n))*cn-gamma(f2,n,j)
            bb=F(j,2*n)-gamma(b,n,j)+gamma(f2,n,j)
            cc=gamma(f1,n,j)-gamma(f2,n,j)
            gates=(bb,2*zn*bb-cc,aa+zn*bb*exp_lower(t-3)-cc,aa+zn*bb-cc*q)
            assert cc>=0 and gates[0]>0 and gates[1]>=0 and gates[2]>0 and gates[3]>0
            records.append(f'{n}:{j}:'+':'.join(f'{v.numerator}/{v.denominator}' for v in gates))
    assert len(records)==92
    print(json.dumps({'scope':'COMPLETE_SCALAR_COUPLING_WINDOW_NO_MATRIX_SAMPLING',
                      'layers':92,'four_gates_per_layer':'EXACT',
                      'certificate_sha256':hashlib.sha256('\n'.join(records).encode('ascii')).hexdigest(),
                      'small_N_log_brackets':values,'drop_deterministic_one_control':'REJECTED',
                      'continuous_mu_bridge':'REQUIRES_PROOF_AUDIT','n_3_to_7':'UNPROVED'}))


if __name__=='__main__':main()
