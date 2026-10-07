"""从原矩阵重构整个连续参数多项式；不导入发现端的路径公式或分盒实现。"""

import argparse
from fractions import Fraction as F
from itertools import product, permutations
from math import comb, factorial, prod
import hashlib
import json
from pathlib import Path
import time

DEADLINE = None


def check_time():
    if time.monotonic() > DEADLINE:
        raise TimeoutError('独立证书未完成，停止而不记通过')


def add_into(target, source, scale=F(1)):
    for power, value in source.items():
        target[power] = target.get(power, F(0)) + scale * value
        if not target[power]:
            del target[power]


def multiply(a, b):
    out = {}
    for pa, va in a.items():
        for pb, vb in b.items():
            power = tuple(x+y for x, y in zip(pa, pb))
            out[power] = out.get(power, F(0)) + va*vb
    return {p:v for p,v in out.items() if v}


def original_matrix(lengths, fixed, group_count):
    n = 1 + sum(l-1 for l in lengths) + fixed
    zero = (0,)*group_count
    one = {zero:F(1)}
    matrix = [[{} for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = dict(one)
    short = lengths.count(2)
    long_index = 0
    offset = 1
    for length in lengths:
        if short and length == 2:
            index = group_count-1
            scale = F(1, short)
        else:
            index = long_index
            long_index += 1
            scale = F(1)
        exponent = [0]*group_count
        exponent[index] = 1
        weight = {tuple(exponent):scale}
        vertices = [0, *range(offset, offset+length-1)]
        for i, vertex in enumerate(vertices):
            add_into(matrix[vertex][vertex], weight, F(-1))
            add_into(matrix[vertex][vertices[(i+1) % length]], weight)
        offset += length-1
    for row in matrix:
        total = {}
        for entry in row:
            add_into(total, entry)
        assert total == one
    for col in range(n):
        total = {}
        for row in matrix:
            add_into(total, row[col])
        assert total == one
    return matrix


def all_minors_from_rows(matrix, group_count):
    # 可跳行的原矩阵列掩码DP；变量是原连续组权重，不是路径状态。
    dp = {0:{(0,)*group_count:F(1)}}
    for row in matrix:
        nxt = {mask:dict(poly) for mask,poly in dp.items()}
        for mask, poly in dp.items():
            for col, entry in enumerate(row):
                if entry and not mask & (1 << col):
                    add_into(nxt.setdefault(mask | (1 << col), {}), multiply(poly,entry))
        dp = nxt
        check_time()
    h = [{} for _ in range(len(matrix)+1)]
    for mask, poly in dp.items():
        add_into(h[mask.bit_count()],poly)
    return h


def power_gap(h, groups):
    n = len(h)-1
    zero = (0,)*groups
    cn = F(factorial(n), n**n)
    assert h[0] == {zero:F(1)}
    assert h[1] == {zero:F(n)}
    out = {}
    for j in range(1,n+1):
        layer = {}
        if j == 1:
            add_into(layer,h[n])
            add_into(layer,{zero:cn},F(-1))
        for k in range(j+1):
            factor = -F(factorial(n-k), n**(n-k))*comb(n-k,j-k)*(-1)**(j-k)
            add_into(layer,h[k],factor)
        for power,value in layer.items():
            out[(*power,j-1)] = value
    return out


def cube_substitution(raw, groups):
    out = {}
    for power, value in raw.items():
        weight_power = power[:-1]
        expansions = []
        for i in range(groups):
            suffix = sum(weight_power[i+1:])
            expansions.append([(weight_power[i]+j,F(comb(suffix,j)*(-1)**j))
                               for j in range(suffix+1)])
        for choices in product(*expansions):
            index = tuple(v[0] for v in choices)+(power[-1],)
            coefficient = value*prod(v[1] for v in choices)/2**power[-1]
            out[index] = out.get(index,F(0))+coefficient
        check_time()
    return {p:v for p,v in out.items() if v}


def initial_tensor(poly, degrees):
    tensor = {}
    for index in product(*(range(d+1) for d in degrees)):
        value = F(0)
        for power,coef in poly.items():
            if all(p <= i for p,i in zip(power,index)):
                factor = F(1)
                for i,p,d in zip(index,power,degrees):
                    factor *= F(comb(i,p),comb(d,p))
                value += coef*factor
        tensor[index] = value
        check_time()
    return tensor


def restrict_half(tensor,degrees,axis):
    # 直接二项式限制公式，独立于发现端de Casteljau逐级平均实现。
    children = [{},{}]
    d = degrees[axis]
    for index in tensor:
        k = index[axis]
        def term(j):
            source = list(index)
            source[axis] = j
            return tensor[tuple(source)]
        children[0][index] = sum(F(comb(k,j),2**k)*term(j) for j in range(k+1))
        children[1][index] = sum(F(comb(d-k,j-k),2**(d-k))*term(j) for j in range(k,d+1))
    return children


def complete_box_certificate(tensor,degrees):
    stack = [(tensor,tuple((F(0),F(1)) for _ in degrees),0)]
    leaves = []
    full_coefficients = []
    nodes = 0
    while stack:
        coeffs,box,depth = stack.pop()
        nodes += 1
        if nodes > 128 or depth > 20:
            raise RuntimeError('独立分盒规模门；证书未完成')
        check_time()
        if min(coeffs.values()) >= 0:
            text = '\n'.join(f'{i}:{v}' for i,v in sorted(coeffs.items()))
            leaves.append({'box':[[str(a),str(b)] for a,b in box],
                           'minimum':str(min(coeffs.values())),
                           'coefficient_sha256':hashlib.sha256(text.encode('ascii')).hexdigest()})
            full_coefficients.append([str(v) for _,v in sorted(coeffs.items())])
            continue
        # 若负值出现在某顶点则不能作为非负证书；严格失败，不隐藏未闭合盒。
        if any(v < 0 and all(k in (0,d) for k,d in zip(i,degrees)) for i,v in coeffs.items()):
            raise ArithmeticError('盒顶点负值，当前证书失败')
        axis = max((i for i,d in enumerate(degrees) if d),
                   key=lambda i:degrees[i]*(box[i][1]-box[i][0]))
        left,right = restrict_half(coeffs,degrees,axis)
        low,high = box[axis]
        mid = (low+high)/2
        lb = list(box); rb = list(box)
        lb[axis]=(low,mid); rb[axis]=(mid,high)
        stack.append((right,tuple(rb),depth+1)); stack.append((left,tuple(lb),depth+1))
    assert sum(prod(b-a for a,b in [[F(a),F(b)] for a,b in leaf['box']]) for leaf in leaves)==1
    return leaves,full_coefficients,nodes


def evaluate(poly,values):
    return sum(v*prod(x**p for x,p in zip(values,power)) for power,v in poly.items())


def numeric_control(matrix,poly,groups):
    xs = [F(i+2,groups+5) for i in range(groups)]
    weights = []; rest=F(1)
    for x in xs:
        weights.append(rest*x); rest *= 1-x
    numeric = [[evaluate(entry,weights) for entry in row] for row in matrix]
    n=len(matrix); u=F(1,3)
    def permanent(a):
        return sum(prod(a[i][sigma[i]] for i in range(n)) for sigma in permutations(range(n)))
    p = permanent(numeric)
    mixed = [[u*v+(1-u)/n for v in row] for row in numeric]
    gap=(1-u)*F(factorial(n),n**n)+u*p-permanent(mixed)
    assert gap >= 0
    actual=evaluate(poly,[*xs,2*u])
    assert actual == gap/u
    assert actual != (gap+u)/u  # 破坏端点per一个单位必须失配。
    return {'u':str(u),'gap':str(gap),'raw_permanent':str(p),
            'method':'DIRECT_COLUMN_PERMUTATIONS','broken_endpoint':'REJECTED'}


def main():
    global DEADLINE
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--case-index',type=int,required=True)
    parser.add_argument('--mutate-root',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    DEADLINE=time.monotonic()+44
    packet=json.loads(args.packet.read_text(encoding='utf-8'))
    assert len(packet['cases'])==32
    assert 0 <= args.case_index < 32
    record=packet['cases'][args.case_index]
    case=record['case']; discovery=record['certificate']
    lengths=case['lengths']; fixed=case['fixed']
    assert 3 <= case['n'] <= 7 and len(lengths)>=2 and max(lengths)>=3
    assert case['n']==1+sum(l-1 for l in lengths)+fixed
    groups=len(lengths)-lengths.count(2)+int(2 in lengths)
    assert groups <= 3
    matrix=original_matrix(lengths,fixed,groups)
    poly=cube_substitution(power_gap(all_minors_from_rows(matrix,groups),groups),groups)
    degrees=tuple(max(power[i] for power in poly) for i in range(groups+1))
    assert list(degrees)==discovery['degrees']
    assert prod(d+1 for d in degrees)<=3000
    controls=numeric_control(matrix,poly,groups)
    tensor=initial_tensor(poly,degrees)
    if args.mutate_root:
        first=min(tensor)
        tensor[first]+=1
    leaves,coefficients,nodes=complete_box_certificate(tensor,degrees)
    digest=hashlib.sha256(json.dumps(leaves,sort_keys=True).encode('ascii')).hexdigest()
    if digest != discovery['leaf_packet_sha256']:
        raise AssertionError('独立原矩阵证书与冻结发现包摘要失配')
    assert nodes==discovery['visited_boxes']
    assert len(leaves)==discovery['certified_leaf_count']
    certificate={'case':case,'degrees':degrees,'status':'VERIFIED_FROM_ORIGINAL_MATRIX',
                      'power_sha256':hashlib.sha256('\n'.join(f'{i}:{v}' for i,v in sorted(poly.items())).encode('ascii')).hexdigest(),
                      'visited_boxes':nodes,'leaf_packet_sha256':digest,
                      'leaves':leaves,'leaf_coefficients':coefficients,'controls':controls,
                      'bridge':'SHORT_EQUALIZATION_PROOF_SEPARATELY_REQUIRED'}
    target=args.output.resolve()
    root=Path(__file__).resolve().parents[3]
    if not target.is_relative_to(root/'tmp') or target.exists():
        raise ValueError('独立单项中间证据仅写入项目tmp内的新文件')
    target.write_text(json.dumps(certificate,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':certificate['status'],'case':case,'output':str(target),
                      'leaf_packet_sha256':digest,'visited_boxes':nodes}))


if __name__=='__main__':
    main()
