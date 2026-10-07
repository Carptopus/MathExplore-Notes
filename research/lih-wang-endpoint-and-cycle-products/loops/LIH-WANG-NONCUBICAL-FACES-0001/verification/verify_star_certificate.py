"""从原矩阵行选择重构连续证书；不导入发现公式或生成器。"""
import argparse
import json
from math import comb, factorial
from pathlib import Path
import sympy as sp


def direct_rook(n,k,a):
    matrix=sp.eye(n)
    for j in range(1,k+1):
        matrix[0,0]-=a
        matrix[j,j]-=a
        matrix[0,j]+=a
        matrix[j,0]+=a
    assert all(sp.expand(sum(matrix[i,j] for j in range(n)))==1 for i in range(n))
    dp={0:sp.Integer(1)}
    for i in range(n):
        nxt=dict(dp)
        for mask,v in dp.items():
            for j in range(n):
                if matrix[i,j]!=0 and not mask&(1<<j):
                    target=mask|(1<<j)
                    nxt[target]=nxt.get(target,0)+v*matrix[i,j]
        dp={mask:sp.expand(v) for mask,v in nxt.items()}
    h=[sp.Integer(0)]*(n+1)
    for mask,v in dp.items():
        h[mask.bit_count()]+=v
    return list(map(sp.expand,h))


def reconstruct(item,x,y):
    dx,dy=item["degrees"]
    return sp.expand(sum(sp.Rational(v)*comb(dx,i)*x**i*(1-x)**(dx-i)
                         *comb(dy,j)*y**j*(1-y)**(dy-j)
                         for i,row in enumerate(item["coefficients"])
                         for j,v in enumerate(row)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--certificate",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    data=json.loads(args.certificate.read_text(encoding="utf-8"))
    assert {(v["n"],v["k"]) for v in data["results"]}=={(n,k) for n in range(3,7) for k in range(2,n)}
    a,u,x,y=sp.symbols("a u x y")
    count=coeffcount=0
    for item in data["results"]:
        n,k=item["n"],item["k"]
        assert item["interval"]==["0",str(sp.Rational(1,k))]
        h=direct_rook(n,k,a)
        assert sp.expand(h[n]-(1-a)**(k-1)*(1-(k+1)*a+2*k*a*a))==0
        cn=sp.Rational(factorial(n),n**n)
        phi=sum(sp.Rational(factorial(n-j),n**(n-j))*h[j]*u**j*(1-u)**(n-j)
                for j in range(n+1))
        gap=sp.expand((1-u)*cn+u*h[n]-phi)
        assert gap.subs(u,0)==0
        actual=sp.expand(sp.cancel(gap/u).subs({a:x/k,u:y/2}))
        assert actual==reconstruct(item,x,y)
        coefficients=[sp.Rational(v) for row in item["coefficients"] for v in row]
        assert min(coefficients)>=0 and str(min(coefficients))==item["minimum"]
        # 破坏证书首项：原矩阵多项式的完全重构必须检出改变。
        bad=json.loads(json.dumps(item))
        bad["coefficients"][0][0]=str(sp.Rational(bad["coefficients"][0][0])+1)
        assert actual!=reconstruct(bad,x,y)
        count+=1
        coeffcount+=len(coefficients)
    thresholds=[]
    for n in (7,8):
        phihalf=sum(sp.Rational(factorial(n),factorial(n-d)*n**d) for d in range(n+1))/2**n
        threshold=2*phihalf-sp.Rational(factorial(n),n**n)
        q=sp.Rational((n-2)**(n-2),(n-1)**(n-1))
        assert q>threshold
        thresholds.append({"n":n,"threshold":str(threshold),"q":str(q)})
    result={"continuous_certificates":count,"exact_coefficients":coeffcount,
            "original_matrix_reconstruction":"PASS","corruption_controls":count,
            "thresholds":thresholds,"scope":"N_LE_6_CONTINUOUS_CERTIFICATES_AND_N7_N8_THRESHOLD_ONLY"}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":
    main()
