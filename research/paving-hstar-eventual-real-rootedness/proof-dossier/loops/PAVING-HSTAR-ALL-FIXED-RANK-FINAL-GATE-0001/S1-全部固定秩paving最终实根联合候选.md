# 全部固定秩paving：最终实根联合候选

2026-10-06，冻结接合候选待新上下文独审，不是论文稿或发布材料。

## 1. 精确对象和主张

对每固定整数r>=3，存在共同非显式整数N_r，使所有n>=N_r的全部
n元素rank-r paving拟阵M，其基多面体Ehrhart h*_M的全部零点简单严格负实。
常数多项式零点为空，按通常含义解释；不要求连通。

paving指每个circuit大小至少r。连通对象维数n-1；不连通对象使用
其真实格点仿射维数，不人为乘1-x。有效H为大小至少r的rank-(r-1)
超平面，不同有效H交集至多r-2。无有效H时M为uniform，令s=r-1。
本结论不含rank2（该层已有非实根例）、全部小n、跨r共同阈值或一般matroid。

## 2. 明确数学输入，不以审计标签作证明

I0：HIGHER-RANK-CRITICAL-KERNEL的S91，以S90全核为输入的真实整类
定理。每固定r>=4、固定非负整数C，全部充分大n的连通paving，
s<=D_u+C，D_u=n-ceil(n/r)，实际h*全简单负根。
准确degree为n-max(ceil(n/r),ceil((s+1)/(r-1)))。
S90采用S88+R1及全部连续证书有效组合；S93保存当前结算，
S90A和S91A分别记录核与实际接合，不将旧大r或大g门冒充全部r。

I1：GENERAL-RANK-GIANT-ENDPOINT的S8，绑定S6+R1、S5+R1、S4+R1、
S3+R1和全部真实输入；每固定r>=5、0<p_max<1/r，共同N(r,p_max)，
全部连通对象最大有效H=n-q、2<=q<=p_max n实际全简单负根。
包含固定小q，不需要q趋无穷；允许全部合法附加H，不限单帽。

I2：GENERAL-RANK-GIANT-CRITICAL-MOVING的S4，绑定S2+R1、S1、S3
和有效实际倒端/全移动两域；每固定r>=5的任意真实连通对象序列，
q/n趋1/r且n-rq趋无穷时，实际h*最终全简单负根。无速度限制。
共同U网格、准确J/k端根和真实degree分别支付，不把核LP当实际结论。

I3：r=3的MOVING-CRITICAL S22+S22R1、S23、最终S24，以及r=4的
HIGHER-RANK-CRITICAL-KERNEL S57，已分别给完整自然整类共同阈值。
本页只联合r>=5，不重用r3/r4组件为一般r的证明。

I4：SPARSE-PAVING-HSTAR-MULTIMODE S3，lambda=0即准确uniform
H_(k,m)=h*_(U_(k,m))，每固定k>=3、充分大m全简单负根。
只用于不连通边界的uniform，不声称任意k秩拟阵实根。

## 3. 全部连通对象的坏序列穷尽

固定r>=5。若不存在共同N_conn，则每j取n_j>=j的失败连通对象M_j。
各子列仍保留原真实对象和全部附加H。
如果s<=D_u无限次，I0取C=0已矛盾。剩余可令delta=s-D_u>0。
若delta在某无限子列有界delta<=C，取这一个固定整数C由I0矛盾；
不对无限多个C取最大阈值。若没有有界子列，则抽delta趋无穷。

连通对象没有coloop，rank-(r-1)超平面的补不是单元素，故q=n-s>=2。
令b_u=r*ceil(n/r)-n∈{0,...,r-1}，准确恒等式

    n-rq=r*s-(r-1)n=r*delta-b_u ->infinity。

所以最终0<q/n<1/r；紧性给再子列p=q/n趋p0∈[0,1/r]。
若p0<1/r，选择一个固定p_max∈(p0,1/r)；该子列最终q<=p_max n，
由I1矛盾。这里p0=0也包含固定q，不强加q发散。
若p0=1/r，保留n-rq发散，完整I2矛盾。
所有坏序列均被有限类型的子列穷尽，因此存在共同非显式N_conn(r)。
没有从逐对象阈值取无穷最大，也没有要求整个区间的p_max共同阈值。

## 4. 不连通对象的准确分类和格点边界

固定r>=5，n>r。因paving无loop、无平行对，每个分量正秩。
任一含circuit分量C有某circuit大小<=rank(C)+1且>=r，
故rank(C)>=r-1。2(r-1)>r，所以至多一个含circuit分量。
若没有这种分量，M为自由拟阵，n=r，已被排除。
其余不含circuit的连通分量是单元素coloop。
不连通要求至少一个coloop；总秩r强迫唯一非自由分量秩r-1，
并恰有一个coloop。该分量所有(r-1)-子集独立，所以准确为

    M=U_(r-1,n-1) ⊕ U_(1,1)。

反向其circuits大小r，确为paving。删除固定为1的coloop坐标给基多面体
的整数格仿射同构；每l倍时该坐标固定为l，Ehrhart计数及真实h*不变。
由I4固定k=r-1>=4的uniform最终简单负根，得到共同N_disc(r)。
取N_r=max(N_conn(r),N_disc(r),r+1)，完成r>=5。
r=3/r=4各用I3共同阈值，故第1节全部固定r>=3成立。

## 5. 自然边界及禁止外推

该联合若通过，覆盖此前同线所有固定r>=3、充分大n的真实paving
子域；稳健扰动盒、辅助整函数及全部小n的sparse-paving定理仍保留
独立范围。各前导文件、修订、反例、证书与历史全部保留，不重复排稿。
此页不是r随n增长的统一定理，也不解决全部小n或rank2/一般matroid问题。
不从证明长度、计算投入或覆盖内部特例判断科研影响力。
最终精确自然整类的先行覆盖另核；目前新颖性UNKNOWN、全部内部HOLD。
