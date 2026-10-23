# Uniform polynomial negative values for trigonometric sums with near-unit coefficients

Carptopus  
Preprint, version 0.1-beta, 23 October 2026

## Abstract

We prove a polynomial lower bound for the magnitude of the negative minimum of a trigonometric sum with distinct positive integer frequencies and continuously varying coefficients near 1. If \(|c_j-1|\leq 0.021\), then
\[
-\min_{x\in\mathbb T}\operatorname{Re}\sum_{j=1}^n c_j e^{2\pi i a_jx}\gg n^{1/12},
\]
with an absolute implied constant. A standard correlation argument gives an \(n^{1/24}\) bound when \(0.99\leq |c_j|\leq1.01\), with arbitrary independent phases. The proof combines the asymmetric-boundary count of Shankar with a continuous-coefficient version of Bedert's cubic Fourier gap. A four-factor directional multiplier suppresses the interior contribution without requiring coefficients from a fixed finite set. These bounds concern uniformity under continuous coefficient perturbations; they do not settle the square-root conjecture for unweighted cosine sums.

## 1. Results and relation to previous work

Write \(\mathbb T=\mathbb R/\mathbb Z\), endowed with probability Haar measure, and \(e(x)=\exp(2\pi i x)\).

**Theorem 1.** There is an absolute constant \(c>0\) such that, for every integer \(n\geq1\), every choice of distinct positive integers \(a_1,\ldots,a_n\), and every choice of complex numbers satisfying \(|c_j-1|\leq21/1000\),
\[
-\min_{x\in\mathbb T}\operatorname{Re}\sum_{j=1}^n c_j e(a_jx)\geq c n^{1/12}.
\]
The constant is independent of the coefficient set, its cardinality, and its separation.

**Corollary 2.** There is an absolute constant \(c'>0\) such that, under the same frequency hypotheses, if \(0.99\leq |c_j|\leq1.01\), then
\[
-\min_{x\in\mathbb T}\operatorname{Re}\sum_{j=1}^n c_j e(a_jx)\geq c'n^{1/24}.
\]
No restriction is imposed on the phases of the coefficients.

In particular, Theorem 1 applies to all real coefficients in \([0.98,1.02]\). Corollary 2 includes arbitrary signs with amplitudes in \([0.99,1.01]\). These are consequences of one result, not separate contributions.

For unweighted sums, Bedert [B, Theorem 1.1] proves the stronger exponent \(1/5-o(1)\), and Shankar [S] removes the subpolynomial loss. Bedert [B, Theorem 1.2] also treats coefficients from any fixed finite nonzero real set, with constants depending on that set. The interval-coefficient question attributed to Ruzsa is explicitly discussed on page 2 of [B, version 3]; a fixed finite coefficient set does not give the uniform interval assertion considered here. Ruzsa's earlier paper [R] supplies historical context for negative values of unweighted sums.

The boundary identity used below is due to Shankar. Its simultaneous boundary/interior selection consequence is a direct averaging argument. The positive multiplier, cubic convolution gap, and positivity method follow Bedert's framework. The additional connection here is a directional continuous-coefficient multiplier whose leakage is confined to the same interior controlled by that selection. The correlation operation in Corollary 2 is standard. For coefficients of *exactly* unit modulus, the same correlation argument and the known unweighted \(1/5\) bound already give exponent \(1/10\); we make no claim of first allowing arbitrary phases.

Recent related papers [BK] and [Y] give further unweighted results. In the portions checked for this manuscript, their indicator-spectrum or simple-graph hypotheses do not provide the continuous input-coefficient assertions above. An announced IAS talk by Julian Sahasrabudhe on 26 October 2026, describing recent joint work with Bedert on a graph analogue, is a further nearby source whose exact weighted scope was unavailable at the preparation date [BS]. This comparison is a statement about checked versions, not a certification of global priority. We claim neither an optimal exponent nor an optimal perturbation radius, and do not treat arbitrary bounded amplitude ratios.

## 2. A simultaneous boundary selection

Let \(A=-A\subset\mathbb Z\setminus\{0\}\) be nonempty and finite, and put \(N=|A|\). For \(t\in A\), define
\[
A_t=\{m\in A:m-t\in A\},\quad
B_t=\{m\in A:m-t\in A,\ m+t\notin A\},
\]
\[
I_t=\{m\in A:m-t,m+t\in A\},\qquad T=\sum_{t\in A}|A_t|.
\]
Thus \(A_t=B_t\sqcup I_t\).

**Lemma 3 (Shankar's count and its selection consequence).** One has
\[
\sum_{t\in A}|B_t|\geq T/3.
\tag{2.1}
\]
There is a \(t\in A\) such that
\[
|B_t|\geq T/(6N),\qquad |I_t|\leq4|B_t|.
\tag{2.2}
\]

*Proof.* For completeness we reproduce the count in [S, Lemma 3.1]. Put \(P=A\cap\mathbb N\),
\[
Q_0=\#\{(u,v)\in P^2:u+v\in P\},\quad
J_0=\#\{(u,v)\in P^2:u-v,u+v\in A\}.
\]
Let \(d_{uv}=1_A(u-v)\), \(p_{uv}=1_A(u+v)\). The four sign choices of an ordered pair of absolute values \((u,v)\) contribute \(2(d_{uv}-p_{uv})^2\) to the total boundary. This remains true for \(u=v\). The number of positive ordered pairs with \(u-v\in A\) is \(2Q_0\), by the bijection \((u,v)\mapsto(v,u-v)\) on \(u>v\) and symmetry. Therefore
\[
\sum_t|B_t|=6Q_0-4J_0.
\]
Zero-sum ordered triples in \(A\) have one of six sign patterns, each counted by \(Q_0\), so \(T=6Q_0\). As \(J_0\leq Q_0\), (2.1) follows.

Write \(S_B=\sum_t|B_t|\) and \(S_I=\sum_t|I_t|=T-S_B\leq2S_B\). On the bad columns \(|I_t|>4|B_t|\), the sum of \(|B_t|\) is at most \(S_I/4\leq S_B/2\). Hence the good columns carry at least \(S_B/2\geq T/6\) boundary points in total. Averaging over at most \(N\) columns proves (2.2). If \(T=0\), every column satisfies (2.2). \(\square\)

## 3. Positivity and a robust cubic gap

We prove a symmetric form of Theorem 1. Suppose that \(w_{-m}=\overline{w_m}\), that \(|w_m-1|\leq\delta=0.021\) for \(m\in A\), and that \(w_m=0\) outside \(A\). Set
\[
F(x)=\sum_m w_m e(mx),\qquad K=-\min_xF(x).
\]
The function \(F\) is real, has mean zero, and satisfies \(F+K\geq0\). Its nonzero Fourier coefficients are bounded in modulus by the mass \(K\) of \(F+K\). Consequently
\[
K\geq0.979,\qquad \|F\|_1\leq2K.
\tag{3.1}
\]

Put \(U(x)=\sum_{m\in A}e(mx)\). Since \(U\) is real and \(\sum_{m\in A}w_m\geq0.979N\), Cauchy--Schwarz with weight \(F+K\) gives
\[
0.979^2N^2\leq K\int |U|^2(F+K)
\leq K(KN+1.021T).
\tag{3.2}
\]
For the last inequality, expand the integral as \(KN+\sum_{a,b\in A}w_{a-b}\), take real parts, and use \(w_0=0\). If \(N<2K^2/0.979^2\), then \(N<3K^2\). Otherwise (3.2) implies \(T\geq N^2/(3K)\), since \(0.979^2/(2\cdot1.021)>1/3\). Lemma 3 then selects a nonzero \(t\in A\) with
\[
|B_t|\geq N/(18K),\qquad |I_t|\leq4|B_t|.
\tag{3.3}
\]
Until Section 5 assume this latter, large-support case.

Our convolution convention is \((f*g)(x)=\int f(y)g(x-y)\,dy\), so \(\widehat{f*g}(m)=\widehat f(m)\widehat g(m)\). Define
\[
F_\pm(x)=2(1\pm\sin(2\pi tx))F(x).
\]
These are real and bounded below by \(-4K\). Their means \(m_\pm\) satisfy \(|m_\pm|\leq2\delta=0.042\leq K\). Positivity of \((F_\pm+4K)^{*3}\) yields
\[
F_\pm^{*3}\geq-128K^3=:-L,
\tag{3.4}
\]
because the difference between this convolution and \(F_\pm^{*3}\) is the constant \((m_\pm+4K)^3-m_\pm^3\), of absolute value at most \(126K^3\).

Define finite coefficient sequences
\[
z_\pm(m)=2w_m\pm i(w_{m+t}-w_{m-t}),\quad
\rho_m=\tfrac12(z_+(m)^3+z_-(m)^3),\quad
\sigma_m=\frac{z_-(m)^3-z_+(m)^3}{2i}.
\]
Write \(P_2=\sum_m\rho_me(mx)\) and \(P_1=\sum_m\sigma_me(mx)\). Then \(F_+^{*3}=P_2-iP_1\), \(F_-^{*3}=P_2+iP_1\); in particular \(P_2\) is real and \(P_1\) is purely imaginary. Equation (3.4) implies
\[
|P_1|\leq P_2+L,\qquad P_2+L\geq0.
\tag{3.5}
\]

Compare with \(w_m^0=1_A(m)\), denoting the corresponding cubic coefficients by a superscript 0. One has \(|z_\pm^0|\leq\sqrt5\), \(|z_\pm-z_\pm^0|\leq4\delta=0.084\), and therefore
\[
|z_\pm^3-(z_\pm^0)^3|\leq3(0.084)(\sqrt5+0.084)^2<1.4.
\]
The indicator case has \(\rho_m^0\in\{0,2,8\}\), \(\sigma_m^0\in\{0,\pm1,\pm11\}\), with \(\sigma_m^0=11\) on \(B_t\). Thus
\[
|\rho_m|\leq9.4,\quad |\sigma_m|\leq14,\quad
\operatorname{Re}\sigma_m\geq9.6\quad(m\in B_t).
\tag{3.6}
\]
The coefficients need not be real; (3.5) and (3.6) are the precise properties used below.

## 4. The directional multiplier and correlation estimate

Set
\[
v_m=w_mw_{m-t}(w_{m-t}-w_{m+t})^2,\qquad h(x)=\sum_m v_me(mx).
\]
Let \(J=e(tx)F\) and \(D=e(tx)F-e(-tx)F\). Then \(h=F*J*D*D\), so Young's inequality and (3.1) give
\[
\|h\|_1\leq4\|F\|_1^4\leq64K^4.
\tag{4.1}
\]
The multiplier vanishes outside \(B_t\cup I_t\). On these two sets respectively,
\[
|v_m|\geq0.979^4>0.91\quad(m\in B_t),\qquad
|v_m|\leq1.021^2(0.042)^2<0.002\quad(m\in I_t).
\]
Put \(\alpha=0.91\), \(q=0.002\), and
\[
W=\sum_{m\in B_t}|v_m|^2,\qquad E=\sum_{m\notin B_t}|v_m|^2.
\]
By (3.3),
\[
W\geq\frac{N\alpha^2}{18K},\qquad E/W\leq4(q/\alpha)^2.
\tag{4.2}
\]
This uses the interior bound for the *same* chosen column; the cruder estimate \(E\leq Nq^2\) would lose the polynomial conclusion of this argument.

For any function \(g\), write \(\mathcal Cg(x)=\overline{g(-x)}\). Take \(Q=h*\mathcal Ch\) and \(u=|h|\). Then
\[
\widehat Q(m)=|v_m|^2,\quad |Q|\leq u*\mathcal Cu,\quad
\widehat{u*\mathcal Cu}(m)=|\widehat u(m)|^2,\quad
\int u*\mathcal Cu=\|h\|_1^2.
\tag{4.3}
\]
Here \(u*\mathcal Cu\) is pointwise nonnegative, since \(u\) is real and nonnegative. Parseval and (3.6) show
\[
9.6W-14E\leq\operatorname{Re}\int P_1\overline Q
\leq\left|\int P_1\overline Q\right|
\leq\int(P_2+L)(u*\mathcal Cu).
\]
In the last integral the \(P_2\) term is \(\sum_m\rho_{-m}|\widehat u(m)|^2\). Its absolute value is at most \(9.4\|u\|_2^2=9.4(W+E)\). Consequently
\[
0.2W-23.4E\leq128K^3\|h\|_1^2.
\tag{4.4}
\]
No positivity or reality of \(v_m\) or \(\rho_m\) has been assumed.

## 5. Completion of the proofs

By (4.2),
\[
23.4E/W\leq23.4\cdot4(0.002/0.91)^2
=36/79625<0.1.
\]
Equations (4.1)--(4.4) give
\[
0.1\frac{N\cdot0.91^2}{18K}\leq128K^3(64K^4)^2,
\]
and hence
\[
N\leq\frac{943718400000}{8281}K^{12}<120000000K^{12}.
\tag{5.1}
\]
The small-support case \(N<3K^2\) from Section 3 also satisfies (5.1), because \(K\geq0.979\) and \(3\cdot0.979^{-10}<4\).

For Theorem 1, take \(A=\{\pm a_1,\ldots,\pm a_n\}\), with \(w_{a_j}=c_j\) and \(w_{-a_j}=\overline{c_j}\). Then \(N=2n\) and \(F=2\operatorname{Re}\sum_jc_je(a_jx)\). Equation (5.1) proves Theorem 1, for example with \(c=\tfrac12(2/120000000)^{1/12}\).

For Corollary 2 use the same real, mean-zero \(F\) and \(K=-\min F\), now with coefficients of arbitrary phase. Both \(F+K\) and \(\mathcal CF+K\) are nonnegative. Thus
\[
H:=F*\mathcal CF\geq-K^2,
\]
and \(\widehat H(m)=|w_m|^2\) on \(A\). Put \(c_*=1.0001\) and \(G=H/c_*\). Its coefficients satisfy
\[
0.98\leq\frac{0.9801}{1.0001}\leq\widehat G(m)
\leq\frac{1.0201}{1.0001}\leq1.02.
\]
Apply (5.1) to \(G\), with \(K_G=-\min G\leq K^2/c_*\), to obtain
\[
2n\leq120000000\,c_*^{-12}K^{24}.
\]
Since \(K\) is twice the negative minimum in Corollary 2, this proves the assertion. \(\square\)

## 6. Verification, limitations, and assistance disclosure

The proof is analytic and combinatorial; no finite computation is used to establish a universal quantifier. The accompanying supplement contains `verification/check_correlation_controls.py` and the archived result `verification/results/correlation-controls.json`; execution instructions and full checksums are in `verification/README.md`. The script SHA256 is `B956499BEF727482FF9486A570E3B3F9E4F03B166F952DE667A846A14CF7C996`. It checks the finite Fourier identities, the multiplier support, constants, and destructive controls. Such checks supplement the proof and do not certify it by themselves.

The results concern only the two coefficient domains explicitly stated in Section 1. Neither the square-root order in the unweighted problem, the optimal exponent here, nor arbitrary fixed amplitude ratios are proved. The work is a preprint, not a peer-reviewed publication. A bounded prior-art review is not proof of global priority.

Carptopus is the human author and assumes authorial responsibility. Codex was used for AI-assisted research and writing, including proof exploration, source comparison, draft preparation, and checks. AI tools are not authors. Independent internal audits do not constitute external expert endorsement or journal peer review.

## References

[B] Benjamin Bedert, *Polynomial bounds for the Chowla cosine problem*, arXiv:2509.05260v3, 24 July 2026. https://arxiv.org/abs/2509.05260v3

[S] Abhishek Shankar, *A Log-Free n^(1/5) Bound for Chowla's Cosine Problem*, arXiv:2609.05338v1, 4 September 2026, especially Lemma 3.1. https://arxiv.org/abs/2609.05338v1

[R] Imre Z. Ruzsa, *Negative values of cosine sums*, Acta Arithmetica 111 (2004), no. 2, 179--186.

[BK] Bryan Bu, Fayzan Khan, Hyunjun Yi, Atharv Jha, Vihaan Vajpeyi, Ishaan Chandupatla, and Madhav Nagpal, *A Half-Constant Upper Bound for Chowla's Cosine Problem*, arXiv:2610.17160v1, 12 October 2026, especially Section 9. https://arxiv.org/abs/2610.17160v1

[Y] Fredy Yip, *Lower bounds for the magnitude of the minimum eigenvalue of graphs with applications to MaxCut and Chowla's cosine problem*, arXiv:2610.01657v2, 13 October 2026, especially Section 10. https://arxiv.org/abs/2610.01657v2

[BS] Julian Sahasrabudhe, *Sharp Bounds for the “Graph” Cholwa Cosine Problem*, IAS seminar announcement for 26 October 2026 (title spelling as listed). Abstract describing joint work with Benjamin Bedert; exact theorem and weighted scope not available in the checked announcement. https://www.ias.edu/math/events/computer-sciencediscrete-mathematics-seminar-i-634
