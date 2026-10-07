"""连续域端点间隙证书；不直接计算拟阵h*根。"""

from fractions import Fraction
from math import comb
import hashlib
import json
import sympy as sp


def coefficients(poly):
    return {key: Fraction(int(c.p), int(c.q)) for key, c in poly.terms()}


def bernstein_transform(arr, degrees, axes):
    for axis in axes:
        degree = degrees[axis]
        groups = {}
        for key, value in arr.items():
            rest = list(key)
            power = rest.pop(axis)
            groups.setdefault(tuple(rest), {})[power] = value
        arr = {}
        for rest, row in groups.items():
            for j in range(degree+1):
                value = sum(c*Fraction(comb(j,i), comb(degree,i))
                            for i,c in row.items() if i <= j)
                key = list(rest)
                key.insert(axis,j)
                arr[tuple(key)] = value
    return arr


def digest(arr):
    raw = '\n'.join(f'{key}:{value}' for key,value in sorted(arr.items()))
    return hashlib.sha256(raw.encode('ascii')).hexdigest()


def affine_coefficients(poly, d_scale, d_shift, u_shift):
    """在有理系数层完成仿射代换，避免巨大符号表达式重复展开。"""
    result = {}
    for (i,j,k), value in coefficients(poly).items():
        d_indices = [i] if d_shift == 0 else range(i+1)
        for h in d_indices:
            dc = comb(i,h)*d_scale**h*d_shift**(i-h)
            for t in range(k+1):
                uc = comb(k,t)*u_shift**(k-t)
                key = (h,j,t)
                result[key] = result.get(key,Fraction(0))+value*dc*uc
    return {key:value for key,value in result.items() if value}


def main():
    d,v,u,x = sp.symbols('d v u x')
    dp,vp,up = [sp.Poly(t,d,v,u) for t in (d,v,u)]
    z = (dp+vp)*(6+5*dp-vp)
    ell = 8*(1+dp)**2*(dp*dp+vp)
    tnum = (vp+dp**3)*(1+dp)
    anum = dp*dp*ell*ell+vp*vp*z*z+2*dp*ell*vp*z*up
    bnum = ell*ell+dp**4*z*z-2*dp*dp*z*ell*up
    cnum = (ell*ell-dp*vp*z*z)**2+4*dp*vp*z*z*ell*ell*up*up

    # 新零端点：正分母v*ell^4后的二次式判别式。
    p = sp.Poly((tnum*cnum-vp*bnum*bnum).as_expr(),u)
    a2,a1,a0 = p.nth(2),p.nth(1),p.nth(0)
    expected = 4*dp*vp*z*z*ell*ell*(dp**4+dp*vp+vp)
    assert sp.Poly(a2,d,v,u) == expected
    c2,c1,c0 = [sp.Poly(c,d,v) for c in (a2,a1,a0)]
    discriminant = 4*c2*c0-c1*c1
    divisor = sp.Poly((dp*dp*vp*(1+dp)**5*z*z*(dp*dp+vp)**2*(dp**3+vp)**2).as_expr(),d,v)
    h, rem = discriminant.div(divisor)
    assert rem.is_zero and h.degree_list() == (16,10)
    hb = bernstein_transform(coefficients(h),(16,10),[1])
    assert all(c >= 0 for c in hb.values())
    for j in range(11):
        assert any(c > 0 for (i,k),c in hb.items() if k == j)

    # 小d的加权算术平均充分条件，明确除掉已知正因子d。
    amraw = (vp+dp**3)*z*z*(2+3*dp+vp)*cnum-anum*cnum-2*vp*z*z*bnum*bnum
    am, rem = amraw.div(sp.Poly(d,d,v,u))
    assert rem.is_zero and am.degree_list() == (25,15,3)
    # 大d的1/3比较，正分母d²*ell^10*v²*(1+d)。
    large_raw = z*z*cnum*cnum*tnum**3*(dp+vp)-vp*vp*(1+dp)*anum*bnum**4
    assert large_raw.degree_list() == (49,28,5)
    large,rem = large_raw.div(dp*(1+dp))
    assert rem.is_zero
    assert large.degree_list() == (47,28,5)
    result = {'zero_endpoint': {'degree': [16,10], 'count': len(hb), 'digest': digest(hb)}}
    for start in (-1,0):
        sb = bernstein_transform(affine_coefficients(am,Fraction(1,4),Fraction(0),Fraction(start)),(25,15,3),[0,1,2])
        assert len(sb) == 1664 and all(c >= 0 for c in sb.values())
        # d>0、v>0时这四项确保含两个角端点的严格性。
        assert all(sb[(25,15,j)] > 0 for j in range(4))
        lb = bernstein_transform(affine_coefficients(large,Fraction(1),Fraction(1,4),Fraction(start)),(47,28,5),[1,2])
        assert len(lb) == 8352 and all(c > 0 for c in lb.values())
        result[str(start)] = {
            'small_count':len(sb), 'small_zero':sum(c == 0 for c in sb.values()), 'small_digest':digest(sb),
            'large_count':len(lb), 'large_zero':0, 'large_digest':digest(lb)
        }
    # 破坏控分别检验符号门和变换契约，不把零失配当根性。
    altered = dict(hb)
    altered[(16,10)] = Fraction(-1)
    assert not all(c >= 0 for c in altered.values())
    one = sp.Poly(x+2,x)
    transformed = bernstein_transform(coefficients(one),(1,),[0])
    assert transformed == {(0,):Fraction(2),(1,):Fraction(3)}
    assert {**transformed,(1,):Fraction(4)} != {(0,):Fraction(2),(1,):Fraction(3)}
    result.update({'status':'VERIFIED','negative_coefficient':'DETECTED','broken_transform':'DETECTED',
                   'scope':'continuous_zero_and_max_block_exponent_certificates_only','actual_roots':'NOT_CHECKED'})
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
