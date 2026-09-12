
\__cmd_normalize_type_g:w

Magenta: Closing the Loop Between Mathematical Reasoning and Lean Verification

Joshua Ong Jun Leang

Affiliation: Institute of Foundation Models

Affiliation: Imperial College London

Email: Joshua.Ong@mbzuai.ac.ae

  
Haonan Li

Affiliation: Institute of Foundation Models

Email: Haonan.Li@mbzuai.ac.ae

  
Zheng Zhao

Affiliation: University of Edinburgh

  
Xinyi Shang

Affiliation: University College London

  
Wenda Li

Affiliation: University of Edinburgh

  
Zhengzhong Liu

Affiliation: Institute of Foundation Models

  
Eric Xing

Affiliation: Institute of Foundation Models

  
Shay B. Cohen

Affiliation: University of Edinburgh

  
Eleonora Giunchiglia

Affiliation: Imperial College London

###### Abstract

 

Most of mathematical knowledge has been
communicated through so-called informal use of
mathematics and natural language. With large language models (LLMs) being highly adept in using natural language, they achieve strong performance, yet not perfect, in informal mathematical reasoning. Restraining LLMs to informal reasoning misses out on the opportunity to use the discrete verification abilities that machines offer through machine-checkable proofs. In this paper, we bridge the gap between informal and formal reasoning by integrating Lean signals into the informal reasoning process.
We introduce Magenta, a training-free agentic pipeline that, given only a natural-language problem, produces an answer, expresses it as a Lean 4 statement, and constructs a machine-checked proof.
A statement judge verifies whether the formalisation preserves the original problem, while an error-attribution judge routes failed attempts either to mathematical re-derivation or local Lean repair.
Magenta achieves $100\%$ accuracy across all evaluated olympiad benchmarks, including AIME 2025, AIME 2026, and HMMT February 2026. When paired with the open-weight K2-Horizon-7B reasoner, it solves all six IMO 2026 problems. Our analysis shows that statement adjudication is essential for preventing false certificates and that feedback-guided correction outperforms independent resampling on difficult problems.
 

[TABLE — see numbers in main context]

## 

$99.2\%$$70.0\%$

- 

- 

> [CAPTION] $\pi^{7}$$\pi^{6}$$\pi^{7}$$\pi^{6}$

## 

### 

$\mathcal{Q}$$\mathcal{C}$$\mathcal{A}$$\mathcal{S}$$\mathcal{P}$$\mathcal{E}_{p}$$\mathcal{E}_{s}$$\varnothing\in\mathcal{E}_{s}\cap\mathcal{E}_{p}$$\mathcal{F}_{\mathrm{math}}=(\mathcal{C}\times\mathcal{A}\times\mathcal{S}\times\mathcal{P}\times\mathcal{E}_{p})\cup\{\varnothing\}$$\varnothing$$\mathcal{B}$$\Delta(\mathcal{B})$$\mathcal{B}$$x\sim P$$x\in\mathcal{B}$$P\in\Delta(\mathcal{B})$

$R$$R:\mathcal{Q}\times\mathcal{F}_{\mathrm{math}}\rightarrow\Delta(\mathcal{C}\times\mathcal{A})$$q\in\mathcal{Q}$$\varphi\in\mathcal{F}_{\mathrm{math}}$$(c,a)$$c\in\mathcal{C}$$a\in\mathcal{A}$$(c,a)\sim R(q,\varphi)$$q$$\varphi$$c$$a$$\varphi=\varnothing$$\varphi$

$F$$F:\mathcal{Q}\times\mathcal{A}\rightarrow\Delta(\mathcal{S})$$q\in\mathcal{Q}$$a\in\mathcal{A}$$\mathcal{S}$$s\sim F(q,a)$$q$$a$$a$

$P$$P:\mathcal{Q}\times\mathcal{C}\times\mathcal{S}\times\mathcal{E}_{\mathrm{p}}\rightarrow\Delta(\mathcal{P})$$q\in\mathcal{Q}$$c\in\mathcal{C}$$s\in\mathcal{S}$$\epsilon\in\mathcal{E}_{p}$$\mathcal{P}$$\pi\sim P(q,c,s,\epsilon)$$q,c,s$$\epsilon$$\epsilon=\varnothing$$c$$a$$s$

$V$$V_{\mathrm{s}}:\mathcal{S}\rightarrow\{\top\}\cup\mathcal{E}_{\mathrm{s}}$$V_{\mathrm{p}}:\mathcal{S}\times\mathcal{P}\rightarrow\{\top\}\cup\mathcal{E}_{\mathrm{p}}$$\top$$V_{s}$$V_{p}$$\pi$$s$$\epsilon\in\mathcal{E}_{\mathrm{p}}$

$J$$J_{\mathrm{s}}:\mathcal{Q}\times\mathcal{A}\times\mathcal{S}\rightarrow\Delta(\{0,1\})$$q\in\mathcal{Q}$$a\in\mathcal{A}$$s\in\mathcal{S}$$J_{\mathrm{e}}:\mathcal{Q}\times\mathcal{C}\times\mathcal{A}\times\mathcal{S}\times\mathcal{P}\times\mathcal{E}_{{p}}\rightarrow\Delta(\{\textsc{math},\textsc{Syntax}\})$$\ell\sim J_{\mathrm{e}}(q,c,a,s,\pi,\epsilon)$$\ell=\textsc{math}$$\ell=\textsc{Syntax}$$J_{\mathrm{s}}$$J_{\mathrm{e}}$

### 

##### $R$

$T$$t=0,\ldots,T-1$$t$$(c_{t},a_{t})\sim R(q,\varphi_{t})$$\varphi_{0}=\varnothing$$t>0$$J_{\mathrm{e}}$$\varphi_{t}\in\mathcal{F}_{\mathrm{math}}$$(c_{t},a_{t})$$T$

##### $F$

$M$$m=0,\ldots,M-1$$m$$s_{t}^{m}\sim F(q,a_{t})$$q$$a_{t}$

##### $V_{\mathrm{s}}$

$s_{t}^{m}$$V_{\mathrm{s}}(s_{t}^{m})\neq\top$$F$$s_{t}^{m}$$(c_{t},a_{t})$$(c_{t},a_{t})$

##### $J_{\mathrm{s}}$

$s_{t}^{m}$$V_{\mathrm{s}}(s_{t}^{m})=\top$$b\sim J_{\mathrm{s}}(q,a_{t},s_{t}^{m}).$$s_{t}^{m}$$q$$a_{t}$$b=0$$F$$M$$b=1$$s_{t}$$(c_{t},a_{t})$$s_{t}$$q$

##### $P$

$K$$k=0,\ldots,K-1$$k=0$$\pi_{t}^{k}\sim P(q,c_{t},s_{t},\epsilon_{k})$$\epsilon_{0}=\varnothing$$c_{t}$

##### $V_{\mathrm{p}}$

$\pi_{t}^{k}$$V_{\mathrm{p}}$$V_{p}(s_{t},\pi_{t}^{k})=\top$$(s_{t},a_{t},c_{t},\pi_{t}^{k})$$c_{t}$$a_{t}$$V_{\mathrm{p}}(s_{t},\pi_{t}^{k})=\epsilon_{t}^{k}$

##### $J_{\mathrm{e}}$

$\pi_{t}^{k}$$\epsilon_{t}^{k}$$J_{\mathrm{e}}$$\ell\sim J_{\mathrm{e}}(q,c_{t},a_{t},s_{t},\pi_{t}^{k},\epsilon_{t}^{k})$$\ell=$$\pi_{t}^{k+1}$$c_{t},a_{t}$$s_{t}$$\ell=\textsc{math}$$\varphi_{t}\in\mathcal{F}_{\mathrm{math}}$

### 

##### 

$V_{\mathrm{p}}(s,\pi)=\top$$\pi\text{ is a valid proof of }s$$s$$q$$a$$s$$q$

##### 

$V_{\mathrm{p}}$$\ell\sim J_{\mathrm{e}}(q,c,a,s,\pi,e),$$\ell\in$

[TABLE — see numbers in main context]
$\ell=\textsc{Syntax}\ \Longrightarrow\ \pi^{\prime}\sim P(q,c,s,e),\qquad\ell=\textsc{math}\ \Longrightarrow\ (c^{\prime},a^{\prime})\sim R(q,\varphi).$

$(c,a,s)$$\varphi\in\mathcal{F}_{\mathrm{math}}$$J_{\mathrm{e}}$

##### 

$q\in\mathcal{Q}$$\mathcal{A}(q)$$M(q)$$\mathcal{Q}$

$\gamma\in(0,1)$$M(q)\leq\log_{1/(1-\gamma)}|\mathcal{A}(q)|$$M(q)\leq\log_{2}|\mathcal{A}(q)|$$\gamma$$M(q)$$\gamma$

## 

### 

##### 

$R$$F$$P$$F$$P$$T$$M$$K$

### 

> [CAPTION] 

[TABLE — see numbers in main context]
$+$$\uparrow 16.67$$\uparrow 20.00$$\uparrow 39.39$$\uparrow 25.81$$+$$\uparrow 6.67$$\uparrow 10.00$$\uparrow 27.27$$\uparrow 15.05$$+$$\uparrow 0.00$$\uparrow 13.33$$\uparrow 12.12$$\uparrow 8.60$$+$$\uparrow 10.00$$\uparrow 13.33$$\uparrow 21.21$$\uparrow 15.05$

##### 

$8.6$$25.8$

##### $+$

[FIGURE-FILE: 07_self_corrections_per_problem.svg]

> [CAPTION] $+$

##### 

$5$$2$$5.7$

## 

### 

#### 

$66\%$$42\%$$6$$120$$68\%$

[FIGURE-FILE: 01_goedel_vs_codex_formal_statement_calls_notitle_enhanced_v2.svg]

> [CAPTION] 

$M=6$$M$

#### 

$100\%$

[TABLE — see numbers in main context]
$\mathrm{Pass}_{u}(\beta)=\frac{1}{|\mathcal{D}|}\sum_{q\in\mathcal{D}}\mathbf{1}\!\left[\mathrm{Ver}(q)=1\wedge u(q)\leq\beta\right],\vskip-6.45831pt$

[FIGURE-FILE: 01_pass_rate_vs_internal_calls_enhanced_v2.svg]

> [CAPTION] 

$u(q)$$\operatorname{Ver}(q)$$q$$\beta$

> [CAPTION] $100\%$

[FIGURE-FILE: 07_codex_external_vs_leanstral_internal_plus_external_calls_log_enhanced_v2.svg]

> [CAPTION] 

[FIGURE-FILE: external_02_codex_vs_leanstral_code_failure_rounds_enhanced_v2.svg]

> [CAPTION] 

[FIGURE-FILE: 05_codex_vs_leanstral_reasoner_tokens_enhanced_v2.svg]

> [CAPTION] 

[FIGURE-FILE: 06_codex_vs_leanstral_final_lean_code_tokens_enhanced_v2.svg]

> [CAPTION] 

$42\%$$17\%$$6\times 10^{4}$$9\times 10^{5}$$1.1\times 10^{4}$$2\times 10^{4}$

$3\times 10^{2}$$3\times 10^{3}$$58\%$$83\%$

### 

> [CAPTION] $\Delta$

[TABLE — see numbers in main context]
$\bm{\Delta}$

$\Delta$$3.3$$10.0$$100\%$$\Delta=0$

### 

$J_{\mathrm{s}}$$J_{\mathrm{e}}$

##### 

> [CAPTION] 

[TABLE — see numbers in main context]
$\bm{\mathrm{Ver}}\uparrow$$\bm{\mathrm{VerCor}}\uparrow$$\bm{\mathrm{FCR}}\downarrow$$J_{\mathrm{s}}$$63.3\%$$63.3\%$$0.0\%$$J_{\mathrm{s}}$$36.7\%$$20.0\%$$45.5\%$

$\mathrm{Ver}$$\mathrm{VerCor}$$\mathrm{FCR}=1-\mathrm{VerCor}/\mathrm{Ver}$$V$$\mathrm{FCR}>0$$J_{\mathrm{s}}$

$\mathrm{Ver}$$63.3\%$$36.7\%$$\mathrm{VerCor}$$43.3$$20.0\%$$\mathrm{FCR}$$45.5\%$

##### 

$p>0$$n$$V$$1-(1-p)^{n}\geq 1-e^{-np}$$29/30$$96.7\%$$30/30$

$8$$16$$1/6$$16.7\%$$p$

## 

##### 

##### 

##### 

## 

## 

- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 

## 

### 

> [CAPTION] 

[TABLE — see numbers in main context]
$\mathcal{Q},q$$q\in\mathcal{Q}$$\mathcal{A},a_{t}$$a_{t}\in\mathcal{A}$$t$$a^{\star},\hat{a}$$\in\mathcal{A}$$\mathcal{C},c_{t}$$c_{t}\in\mathcal{C}$$t$$\mathcal{S},s$$s\in\mathcal{S}$$\mathcal{P},\pi$$\pi\in\mathcal{P}$$\mathcal{E}_{\mathrm{s}}$$V_{\mathrm{s}}$$\mathcal{E}_{\mathrm{p}},e$$e\in\mathcal{E}_{\mathrm{p}}$$V_{\mathrm{p}}$$\mathcal{F}_{\mathrm{math}},\varphi_{t}$$\varphi_{t}\in\mathcal{F}_{\mathrm{math}}$$(c_{t},a_{t},s,\pi,e)$$J_{\mathrm{e}}$$\varnothing$$\varphi=\varnothing$$\epsilon=\varnothing$$R$$\mathcal{Q}\times\mathcal{F}_{\mathrm{math}}\!\to\!\mathcal{C}\times\mathcal{A}$$F$$\mathcal{Q}\times\mathcal{A}\to\mathcal{S}$$P$$\mathcal{Q}\times\mathcal{C}\times\mathcal{S}\times\mathcal{E}_{\mathrm{p}}\!\to\!\mathcal{P}$$V_{\mathrm{s}}$$\mathcal{S}\to\{\top\}\cup\mathcal{E}_{\mathrm{s}}$$s$$V_{\mathrm{p}}$$\mathcal{S}\times\mathcal{P}\to\{\top\}\cup\mathcal{E}_{\mathrm{p}}$$J_{\mathrm{s}},b$$b\in\{0,1\}$$b=1$$J_{\mathrm{e}},\ell$$\ell\in\{\textsc{math},\textsc{Syntax}\}$$\top$$V_{\mathrm{s}}$$V_{\mathrm{p}}$$T,M,K$$\in\mathbb{N}$$\mathcal{D}$$\mathrm{Ver}(q)$$\in\{0,1\}$$q$$u,\beta$$u:\mathcal{D}\to\mathbb{R}_{\geq 0}$

### 

$T$$M$$K$$(c,a,s,\pi)$$T$$TM$$TK$$M\ll K$

> [CAPTION] 

$q$$R,F,P,V_{\mathrm{s}},V_{\mathrm{p}},J_{\mathrm{s}},J_{\mathrm{e}}$$T,M,K$

$(c,a,s,\pi)$

$\varphi\leftarrow\varnothing$$\triangleright$

$t=1,\dots,T$

$(c_{t},a_{t})\sim R(q,\varphi)$$\triangleright$

$z_{s}\leftarrow 0$$\triangleright$

$m=1,\dots,M$$\triangleright$

$s_{m}\sim F(q,a_{t})$

$u_{m}\leftarrow V_{\mathrm{s}}(s_{m})$

$u_{m}\neq\top$$\triangleright$

$b_{m}\sim J_{\mathrm{s}}(q,a_{t},s_{m})$

$b_{m}=1$$s\leftarrow s_{m}$$z_{s}\leftarrow 1$

$z_{s}=0$

$\epsilon\leftarrow\varnothing$

$z_{\mathrm{math}}\leftarrow 0$

$k=1,\dots,K$$\triangleright$

$\pi\sim P(q,c_{t},s,\epsilon)$

$e\leftarrow V_{\mathrm{p}}(s,\pi)$

$e=\top$$(c_{t},a_{t},s,\pi)$$\triangleright$

$\ell\sim J_{\mathrm{e}}(q,c_{t},a_{t},s,\pi,e)$$\triangleright$

$\ell=\textsc{math}$

$\varphi\leftarrow(c_{t},a_{t},s,\pi,e)$$z_{\mathrm{math}}\leftarrow 1$$\triangleright$$\mathcal{F}_{\mathrm{math}}$

$\epsilon\leftarrow e$$\triangleright$

$z_{\mathrm{math}}=0$

$\triangleright$

$F$$V_{\mathrm{s}}$$J_{\mathrm{s}}$$(c,a)$$R$$P$$\mathcal{F}_{\mathrm{math}}$$R$

> [CAPTION] 

$q$$R,F,P,V_{\mathrm{s}},V_{\mathrm{p}},J_{\mathrm{s}},J_{\mathrm{e}}$$T,M,K$

$(c,a,s,\pi)$

$\varphi\leftarrow\varnothing$

$t=1,\ldots,T$$\triangleright$

$(c_{t},a_{t})\sim R(q,\varphi)$

$(z_{s},s)\leftarrow\operatorname{StatementSearch}(q,a_{t};F,V_{\mathrm{s}},J_{\mathrm{s}},M)$

$z_{s}=\textsc{rejected}$

$(z_{p},\pi,e)\leftarrow\operatorname{ProofSearch}(q,c_{t},a_{t},s;P,V_{\mathrm{p}},J_{\mathrm{e}},K)$

$z_{p}=\textsc{certified}$$(c_{t},a_{t},s,\pi)$

$z_{p}=\textsc{math-error}$

$\varphi\leftarrow(c_{t},a_{t},s,\pi,e)$$\triangleright$$\mathcal{F}_{\mathrm{math}}$

$z_{p}=\textsc{repair-exhausted}$

$\triangleright$

> [CAPTION] 

$q$$a$$F$$V_{\mathrm{s}}$$J_{\mathrm{s}}$$M$

$(\textsc{accepted},s)$$(\textsc{rejected},\varnothing)$

$m=1,\ldots,M$

$s_{m}\sim F(q,a)$$\triangleright$

$u_{m}\leftarrow V_{\mathrm{s}}(s_{m})$$\triangleright$

$u_{m}\neq\top$$\triangleright$$F$

$b_{m}\sim J_{\mathrm{s}}(q,a,s_{m})$

$\triangleright$

$b_{m}=1$$(\textsc{accepted},s_{m})$

$(\textsc{rejected},\varnothing)$

> [CAPTION] 

$q$$c$$a$$s$$P$$V_{\mathrm{p}}$$J_{\mathrm{e}}$$K$

$\{\textsc{certified},\textsc{math-error},\textsc{repair-exhausted}\}$

$\epsilon\leftarrow\varnothing$$\pi_{\mathrm{last}}\leftarrow\varnothing$$e_{\mathrm{last}}\leftarrow\varnothing$

$k=1,\ldots,K$

$\pi_{k}\sim P(q,c,s,\epsilon)$$\triangleright$$q,c,s$

$\pi_{\mathrm{last}}\leftarrow\pi_{k}$

$e_{k}\leftarrow V_{\mathrm{p}}(s,\pi_{k})$$\triangleright$

$e_{k}=\top$$(\textsc{certified},\pi_{k},\varnothing)$

$e_{\mathrm{last}}\leftarrow e_{k}$

$\ell_{k}\sim J_{\mathrm{e}}(q,c,a,s,\pi_{k},e_{k})$

$\ell_{k}=\textsc{math}$

$(\textsc{math-error},\pi_{k},e_{k})$$\triangleright$

$\epsilon\leftarrow e_{k}$$\triangleright$

$(\textsc{repair-exhausted},\pi_{\mathrm{last}},e_{\mathrm{last}})$

$(q,c,a)$$(s,\pi)$

## 

### 

### 

- 

$T=32$$M=512$$K=4096$$32$
- 

$0.6$$=0.95$$64{,}000$$128{,}000$$42$$524{,}288$$T$
- 

$0.9$$=20$$=0.95$$16{,}384$$42$$40{,}960$
- 

$1.0$$=1.0$$32{,}000$$65{,}536$$8$$1$$0.90$$256$
- 

- 

$2.18.4$$1.0$$200{,}000$$168{,}000$$80{,}000$$32{,}000$$4{,}000{,}000$
- 

- 

## 

> [CAPTION] 

[TABLE — see numbers in main context]

## 

$\pi$$A=\{1,2,3,4,5,6\}$$A$$a\in A$$\pi(\pi(\pi(\pi(\pi(\pi(a))))))=a.$

$\Downarrow$$\pi(\pi(\pi(\pi(\pi(\pi(a))))))=a\qquad\text{for all }a\in A$$\pi$$\pi^{7}=\operatorname{id}_{A}.$$\pi$$7$$7$$1$$7$$6$$6$$6$$7$$\pi^{7}=\operatorname{id}_{A}$$\boxed{1}$

$\Downarrow$

$\Downarrow$

$\Downarrow$

$\Downarrow$

$\Downarrow$$\pi(\pi(\pi(\pi(\pi(\pi(a))))))=a$$a\in A$$\pi$$\pi^{6}=\operatorname{id}_{A}$$\pi$$A$$A$$A$$\pi$$A$$\pi$$S_{6}$$\{1,2,3,6\}$$(6-1)!=120$$\frac{6!}{3^{2}\cdot 2!}=\frac{720}{18}=40$$\frac{6!}{3\cdot 2\cdot 1}=\frac{720}{6}=120$$\frac{6!}{3\cdot 1^{3}\cdot 3!}=\frac{720}{18}=40$$\frac{6!}{2^{3}\cdot 3!}=\frac{720}{48}=15$$\frac{6!}{2^{2}\cdot 2!\cdot 1^{2}\cdot 2!}=\frac{720}{16}=45$$\frac{6!}{2\cdot 1^{4}\cdot 4!}=\frac{720}{48}=15$$1$$120+40+120+40+15+45+15+1=396$$\boxed{396}$

$\Downarrow$

$\Downarrow$

$\Downarrow$

## 

### 

> [CAPTION] 

[TABLE — see numbers in main context]

$30$

$67.08\%$$32.92\%$$44.64\%$$21.91\%$$J_{\mathrm{s}}$

### 

$54.73\%$

> [CAPTION] 

[TABLE — see numbers in main context]

### 

> [CAPTION] $14$

[TABLE — see numbers in main context]

$17017$$107017$$N=1000$$N=10000$$39$$3$$3^{9}$

## 

### 

### 

### 

[FIGURE-FILE: 01_final_k3_solution_tokens_iclr.svg]

> [CAPTION] 

### 

#### 
$1$$m>1$$n>1$$\gcd(m,n)\qquad\text{and}\qquad\frac{\operatorname{lcm}(m,n)}{\gcd(m,n)}.$$M>1$$M$$a_{1},a_{2},\dots,a_{2026}$$a_{i}>1$$i$$f:\{1,2,\dots,2026\}\to\mathbb{N}_{>1}$$i,j$$m=f(i)>1$$n=f(j)>1$$g=\gcd(m,n),\qquad h=\frac{\operatorname{lcm}(m,n)}{\gcd(m,n)}.$

#### 
$b$$\{1,\dots,2026\}$$N(b)=\#\{\,i\mid b(i)>1\,\},\qquad P(b)=\prod_{i=1}^{2026}b(i).$$b(i)$$P(b)$$b\to c$$N(c)\leq N(b)$$N(c)=N(b)$$P(c)<P(b)$$i,j$$m=b(i)>1,\;n=b(j)>1$$g=\gcd(m,n)$$h=\operatorname{lcm}(m,n)/g$$c(i)=g,\;c(j)=h$$c(k)=b(k)$$k\neq i,j$$k\notin\{i,j\}$$N$$P$$g=1$$h=\operatorname{lcm}(m,n)=mn$$\gcd(m,n)=1$$m,n>1$$h>1$$>1$$>1$$h$$1$$g$$N(c)=N(b)-1$$P(c)=P(b)\cdot\frac{g\,h}{m\,n}=P(b)\cdot\frac{1\cdot mn}{mn}=P(b).$$g>1$$m=g\,m^{\prime},\;n=g\,n^{\prime}$$\gcd(m^{\prime},n^{\prime})=1$$h=\frac{\operatorname{lcm}(m,n)}{g}=\frac{g\,m^{\prime}\,n^{\prime}}{g}=m^{\prime}\,n^{\prime}.$$h=1$$m^{\prime}=n^{\prime}=1$$m=n=g$$>1$$g>1$$1$$N(c)=N(b)-1$$P(c)=P(b)\cdot\frac{g\cdot 1}{g\cdot g}=\frac{P(b)}{g}<P(b)\quad(\text{since }g>1).$$h>1$$>1$$>1$$g>1,\;h>1$$N(c)=N(b)$$P(c)=P(b)\cdot\frac{g\,h}{m\,n}=P(b)\cdot\frac{g\,(m^{\prime}\,n^{\prime})}{g\,m^{\prime}\,g\,n^{\prime}}=\frac{P(b)}{g}<P(b)\quad(\text{since }g>1).$$N(c)\leq N(b)$$N(c)=N(b)$$P(c)<P(b)$$\square$$\mathbb{N}\times\mathbb{N}$$\mathbb{N}$$(N,P)$$b$$>1$$>1$$b(i)=1$$N(b)=0$$N=2026$$N$$N=0$$N=2026$$2026$$N$$N$$1$$0$$>1$$N=1$$N=0$$N=1$$i$$b(i)>1$$j\neq i$$b(j)=1$$M=b(i)$$M>1$

#### $M$
$p$$x$$v_{p}(x)$$p$$x$$v_{p}(1)=0$$b$$G_{p}(b)=\gcd\{\,v_{p}(b(i))\mid i=1,\dots,2026\,\}.$$0$$G_{p}(b)$$i,j$$m=b(i),\;n=b(j)$$a=v_{p}(m),\;b=v_{p}(n)$$v_{p}(\gcd(m,n))=\min(a,b),\qquad v_{p}(\operatorname{lcm}(m,n))=\max(a,b).$$h=\operatorname{lcm}(m,n)/\gcd(m,n)$$v_{p}(h)=v_{p}(\operatorname{lcm}(m,n))-v_{p}(\gcd(m,n))=\max(a,b)-\min(a,b)=|a-b|.$$p$$\{a,b\}$$\{\min(a,b),|a-b|\}$$R$$2024$$\gcd\bigl(\{a,b\}\cup R\bigr)=\gcd\bigl(\gcd(a,b),\gcd(R)\bigr),$$\gcd\bigl(\{\min(a,b),|a-b|\}\cup R\bigr)=\gcd\bigl(\gcd(\min(a,b),|a-b|),\gcd(R)\bigr).$$\gcd(\min(a,b),|a-b|)=\gcd(a,b).$$a\geq b$$\min(a,b)=b$$|a-b|=a-b$$d$$b$$a-b$$d$$b+(a-b)=a$$d$$b$$a$$d$$a-b$$\{b,a-b\}$$\{a,b\}$$(*)$$\square$$M>1$$2025$$1$$\{v_{p}(M)\}\cup\{0,0,\dots,0\}$$v_{p}(M)$$\gcd(v_{p}(M),0)=v_{p}(M)$$G_{p}(\text{final})=v_{p}(M).$$G_{p}(\text{final})=G_{p}(\text{initial})$$p$$v_{p}(M)=G_{p}(\text{initial})\qquad\text{for all primes }p.$$M=\prod_{p\text{ prime}}p^{\,G_{p}(\text{initial})}.$$M$$\square$$\boxed{\begin{minipage}[336.12549pt]\centering The process terminates with exactly one integer $M>1$ on the board, and
$$M=\prod_{p}p^{\,g_{p}},\qquad g_{p}=\gcd\!\bigl(v_{p}(a_{1}),\ldots,v_{p}(a_{2026})\bigr),$$which is independent of the choices.
\@add@centering\end{minipage}}$$M>1$

#### 
$ABC$$M$$N$$AB$$AC$$K$$L$$BMC$$BNC$$K$$\angle LBA$$L$$\angle ACK$$\angle KBA=\angle ACL,\qquad\angle LBK=\angle LNC,\qquad\angle LCK=\angle BMK.$$O$$AKL$$OM=ON$$ABC$$A$$B=(b_{1},b_{2})$$C=(c_{1},c_{2})$$\triangle ABC$$B$$C$$\displaystyle D$$\displaystyle=\det(B,C)=b_{1}c_{2}-b_{2}c_{1}\neq 0,$$\displaystyle\qquad r$$\displaystyle=|B|^{2}=b_{1}^{2}+b_{2}^{2},$$\displaystyle s$$\displaystyle=B\!\cdot\!C=b_{1}c_{1}+b_{2}c_{2},$$\displaystyle\qquad t$$\displaystyle=|C|^{2}=c_{1}^{2}+c_{2}^{2}.$$P,Q$$P-Q$$Q$$P$$u,v$$\det(u,v)$$u\!\cdot\!v$

#### $K$$L$
$K$$\triangle BMC$$\alpha,\beta,\gamma$$\alpha+\beta+\gamma=1$$K=\alpha B+\beta M+\gamma C.$$M$$AB$$M=\frac{1}{2}(A+B)=\frac{1}{2}B$$K=\Bigl(\alpha+\frac{\beta}{2}\Bigr)B+\gamma C.$$x=\alpha+\frac{\beta}{2},\qquad y=\gamma.$$K=xB+yC$$\alpha,\beta,\gamma>0$$\alpha+\beta+\gamma=1$$0<x<1,\qquad 0<y<1,\qquad x+y=\alpha+\frac{\beta}{2}+\gamma=1-\frac{\beta}{2}<1.$$L$$\triangle BNC$$N$$N=\frac{1}{2}C$$\alpha^{\prime},\beta^{\prime},\gamma^{\prime}$$\alpha^{\prime}+\beta^{\prime}+\gamma^{\prime}=1$$L=\alpha^{\prime}B+\beta^{\prime}N+\gamma^{\prime}C=\alpha^{\prime}B+\Bigl(\frac{\beta^{\prime}}{2}+\gamma^{\prime}\Bigr)C.$$p=\alpha^{\prime},\qquad q=\frac{\beta^{\prime}}{2}+\gamma^{\prime}.$$L=pB+qC$$0<p<1,\qquad 0<q<1,\qquad p+q=1-\frac{\beta^{\prime}}{2}<1.$

#### $K$$\angle LBA$$L$$\angle ACK$
$K$$\angle LBA$$BK$$BA$$BL$$A=0$$u,v$$K-B=u(L-B)+v(A-B)=u(L-B)-vB.$$K-B=(x-1)B+yC$$L-B=(p-1)B+qC$$(*)$$(x-1)B+yC=u\bigl[(p-1)B+qC\bigr]-vB=\bigl[u(p-1)-v\bigr]B+uqC.$$B$$C$$y=uq,\qquad x-1=u(p-1)-v.$$u=y/q>0$$v=u(p-1)-(x-1)=\frac{y}{q}(p-1)-(x-1)=\frac{y(p-1)-q(x-1)}{q}.$$d=q(1-x)-y(1-p).$$y(p-1)-q(x-1)=d$$v=d/q$$v>0$$q>0$$d>0.$$L$$\angle ACK$$u^{\prime},v^{\prime}$$L-C=u^{\prime}(A-C)+v^{\prime}(K-C)=-u^{\prime}C+v^{\prime}(K-C).$$L-C=pB+(q-1)C$$K-C=xB+(y-1)C$$(**)$$pB+(q-1)C=v^{\prime}\bigl[xB+(y-1)C\bigr]-u^{\prime}C=(v^{\prime}x)B+\bigl[v^{\prime}(y-1)-u^{\prime}\bigr]C.$$p=v^{\prime}x,\qquad q-1=v^{\prime}(y-1)-u^{\prime}.$$v^{\prime}=p/x>0$$u^{\prime}=v^{\prime}(y-1)-(q-1)=\frac{p}{x}(y-1)-(q-1)=\frac{p(y-1)-x(q-1)}{x}.$$e=x(1-q)-p(1-y).$$p(y-1)-x(q-1)=e$$u^{\prime}=e/x$$u^{\prime}>0$$x>0$$e>0.$

#### 
$u,v,u^{\prime},v^{\prime}$$u$$v$$u^{\prime}$$v^{\prime}$$\det(u,v)\det(u^{\prime},v^{\prime})>0$$\det(u,v)\,(u^{\prime}\!\cdot\!v^{\prime})=\det(u^{\prime},v^{\prime})\,(u\!\cdot\!v).$$\frac{u\!\cdot\!v}{|u||v|}=\frac{u^{\prime}\!\cdot\!v^{\prime}}{|u^{\prime}||v^{\prime}|}.$$\frac{|\det(u,v)|}{|u||v|}=\frac{|\det(u^{\prime},v^{\prime})|}{|u^{\prime}||v^{\prime}|}.$$\frac{\det(u,v)}{|u||v|}=\frac{\det(u^{\prime},v^{\prime})}{|u^{\prime}||v^{\prime}|}.$$\star$$\square$

#### 
$\angle KBA$$\angle ACL$$u=K-B,\;v=A-B=-B,\;u^{\prime}=A-C=-C,\;v^{\prime}=L-C$$\det(K-B,-B)=yD,\qquad\det(-C,L-C)=pD.$$y>0,\;p>0$$D\neq 0$$(K-B)\!\cdot\!(-B)=(1-x)r-ys,\qquad(-C)\!\cdot\!(L-C)=t(1-q)-ps.$$\star$$yD\bigl(t(1-q)-ps\bigr)=pD\bigl((1-x)r-ys\bigr).$$D$$rp(1-x)=ty(1-q).$$\angle LBK$$\angle LNC$$u=L-B,\;v=K-B,\;u^{\prime}=L-N,\;v^{\prime}=C-N$$\det(L-B,K-B)=dD,\qquad\det(L-N,C-N)=\frac{p}{2}D.$$d>0,\;p>0$$\displaystyle(L-B)\!\cdot\!(K-B)$$\displaystyle=r(1-p)(1-x)$$\displaystyle-s\bigl((1-p)y+q(1-x)\bigr)+tqy,$$\displaystyle(L-N)\!\cdot\!(C-N)$$\displaystyle=\frac{sp+t(q-\tfrac{1}{2})}{2}.$$\star$$\displaystyle dD\cdot\frac{sp+t(q-\tfrac{1}{2})}{2}={}$$\displaystyle\frac{p}{2}D\cdot\Bigl[r(1-p)(1-x)$$\displaystyle-s\bigl((1-p)y+q(1-x)\bigr)+tqy\Bigr].$$D$$2$$\displaystyle d\bigl(sp+t(q-\tfrac{1}{2})\bigr)={}$$\displaystyle p\Bigl[r(1-p)(1-x)$$\displaystyle-s\bigl((1-p)y+q(1-x)\bigr)+tqy\Bigr].$$\angle LCK$$\angle BMK$$u=L-C,\;v=K-C,\;u^{\prime}=B-M,\;v^{\prime}=K-M$$\det(L-C,K-C)=eD,\qquad\det(B-M,K-M)=\frac{y}{2}D.$$e>0,\;y>0$$\displaystyle(L-C)\!\cdot\!(K-C)$$\displaystyle=rpx-s\bigl(p(1-y)+x(1-q)\bigr)$$\displaystyle+t(1-q)(1-y),$$\displaystyle(B-M)\!\cdot\!(K-M)$$\displaystyle=\frac{r(x-\tfrac{1}{2})+sy}{2}.$$\star$$\displaystyle eD\cdot\frac{r(x-\tfrac{1}{2})+sy}{2}={}$$\displaystyle\frac{y}{2}D\cdot\Bigl[rpx-s\bigl(p(1-y)+x(1-q)\bigr)$$\displaystyle+t(1-q)(1-y)\Bigr].$$D$$2$$\displaystyle e\bigl(r(x-\tfrac{1}{2})+sy\bigr)={}$$\displaystyle y\Bigl[rpx-s\bigl(p(1-y)+x(1-q)\bigr)$$\displaystyle+t(1-q)(1-y)\Bigr].$

#### 
$\displaystyle E_{1}$$\displaystyle=rp(1-x)-ty(1-q)=0$$\displaystyle\text{(from (I))},$$\displaystyle E_{2}$$\displaystyle=p\bigl[r(1-p)(1-x)-s\bigl((1-p)y+q(1-x)\bigr)+tqy\bigr]$$\displaystyle-d\bigl(sp+t(q-\tfrac{1}{2})\bigr)=0$$\displaystyle\text{(from (II))},$$\displaystyle E_{3}$$\displaystyle=y\bigl[rpx-s\bigl(p(1-y)+x(1-q)\bigr)+t(1-q)(1-y)\bigr]$$\displaystyle-e\bigl(r(x-\tfrac{1}{2})+sy\bigr)=0$$\displaystyle\text{(from (III))}.$$c_{1}=(x+y)(p+2q-1)-(p+q)(1-x).$$F=c_{1}E_{1}+2(x+y)(1-q)E_{2}-2(p+q)(1-x)E_{3}.$$E_{1},E_{2},E_{3}$$F=0$$F$$d$$e$$d=q(1-x)-y(1-p),\qquad e=x(1-q)-p(1-y),$$\displaystyle F=(1-x)(1-q)\Bigl[{}$$\displaystyle r\bigl(2(p+q)x^{2}-2(x+y)p^{2}-(xq-yp)\bigr)$$\displaystyle+s\bigl(4(p+q)xy-4(x+y)pq\bigr)$$\displaystyle+t\bigl(2(p+q)y^{2}-2(x+y)q^{2}+(xq-yp)\bigr)\Bigr].$$0<x<1$$0<q<1$$(1-x)(1-q)\neq 0$$\displaystyle 2(p+q)(rx^{2}+2sxy+ty^{2})$$\displaystyle-2(x+y)(rp^{2}+2spq+tq^{2})=(xq-yp)(r-t).$

#### $O$$\triangle AKL$
$A$$OA=OK=OL$$|O|^{2}=|O-K|^{2}=|O-L|^{2}.$$2\,O\!\cdot\!K=|K|^{2},\qquad 2\,O\!\cdot\!L=|L|^{2}.$$K=xB+yC$$L=pB+qC$$\displaystyle x\,(O\!\cdot\!B)+y\,(O\!\cdot\!C)$$\displaystyle=\frac{rx^{2}+2sxy+ty^{2}}{2},$$\displaystyle p\,(O\!\cdot\!B)+q\,(O\!\cdot\!C)$$\displaystyle=\frac{rp^{2}+2spq+tq^{2}}{2}.$$u=O\!\cdot\!B$$v=O\!\cdot\!C$$u,v$$OM=ON$$M=\frac{1}{2}B$$N=\frac{1}{2}C$$\displaystyle OM^{2}$$\displaystyle=|O-\tfrac{1}{2}B|^{2}=|O|^{2}-u+\frac{r}{4},$$\displaystyle ON^{2}$$\displaystyle=|O-\tfrac{1}{2}C|^{2}=|O|^{2}-v+\frac{t}{4}.$$OM=ON$$OM^{2}=ON^{2}$$v-u=\frac{t-r}{4}.$$u$$v$$p+q$$x+y$$\displaystyle(p+q)(xu+yv)-(x+y)(pu+qv)$$\displaystyle=\frac{1}{2}\Bigl[(p+q)(rx^{2}+2sxy+ty^{2})$$\displaystyle-(x+y)(rp^{2}+2spq+tq^{2})\Bigr].$$(py-xq)(v-u).$$\displaystyle(py-xq)(v-u)={}$$\displaystyle\frac{1}{2}\Bigl[(p+q)(rx^{2}+2sxy+ty^{2})$$\displaystyle-(x+y)(rp^{2}+2spq+tq^{2})\Bigr].$$2$$\displaystyle(p+q)(rx^{2}+2sxy+ty^{2})$$\displaystyle-(x+y)(rp^{2}+2spq+tq^{2})=\frac{(xq-yp)(r-t)}{2}.$$(py-xq)(v-u)=\frac{(xq-yp)(r-t)}{4}.$$py-xq=-(xq-yp)$$-(xq-yp)(v-u)=\frac{(xq-yp)(r-t)}{4}.$$AKL$$O$$K$$L$$A$$\det(K,L)=(xq-yp)D\neq 0,$$D\neq 0$$xq-yp\neq 0$$-(v-u)=\frac{r-t}{4}\quad\Longrightarrow\quad v-u=\frac{t-r}{4},$$OM^{2}=ON^{2}$$OM=ON$$\square$

#### 
$n$$1$$n$$n$$c$$[0,1]$$n$$n$$y_{1}\geq y_{2}\geq\cdots\geq y_{m}>0$$\frac{1+D}{2}$$D=\sum_{i\text{ odd}}y_{i}-\sum_{i\text{ even}}y_{i}.$$D$$m$$m=1$$m-1$$m$$y_{j}$$j>1$$y_{j}$$G_{j}$$y_{j}$$j=1$$G_{1}=y_{2}+y_{4}+\cdots$$j>1$$y_{j}$$j$$y_{i}$$i<j$$i$$i>j$$i$$G_{j}=\sum_{\begin{subarray}{c}i<j\\
i\text{ odd}\end{subarray}}y_{i}\;+\;\sum_{\begin{subarray}{c}i>j\\
i\text{ even}\end{subarray}}y_{i}.$$G_{j}-G_{1}=\Bigl(\sum_{\begin{subarray}{c}i<j\\
i\text{ odd}\end{subarray}}y_{i}+\sum_{\begin{subarray}{c}i>j\\
i\text{ even}\end{subarray}}y_{i}\Bigr)-\sum_{i\text{ even}}y_{i}.$$\sum_{i\text{ even}}y_{i}=\sum_{\begin{subarray}{c}i<j\\
i\text{ even}\end{subarray}}y_{i}+(y_{j}\text{ if }j\text{ is even else }0)+\sum_{\begin{subarray}{c}i>j\\
i\text{ even}\end{subarray}}y_{i}$$G_{j}-G_{1}=\sum_{\begin{subarray}{c}i<j\\
i\text{ odd}\end{subarray}}y_{i}-\sum_{\begin{subarray}{c}i<j\\
i\text{ even}\end{subarray}}y_{i}-(y_{j}\text{ if }j\text{ is even else }0)=\sum_{\begin{subarray}{c}i<j\\
i\text{ odd}\end{subarray}}y_{i}-\sum_{\begin{subarray}{c}i\leq j\\
i\text{ even}\end{subarray}}y_{i}.$$j=2h$$\sum_{i<2h,i\text{ odd}}y_{i}=y_{1}+y_{3}+\cdots+y_{2h-1}=\sum_{r=1}^{h}y_{2r-1}$$\sum_{i\leq 2h,i\text{ even}}y_{i}=y_{2}+y_{4}+\cdots+y_{2h}=\sum_{r=1}^{h}y_{2r}$$G_{j}-G_{1}=\sum_{r=1}^{h}(y_{2r-1}-y_{2r})\geq 0$$j=2h+1$$\sum_{i<2h+1,i\text{ odd}}y_{i}=y_{1}+y_{3}+\cdots+y_{2h-1}=\sum_{r=1}^{h}y_{2r-1}$$\sum_{i\leq 2h+1,i\text{ even}}y_{i}=y_{2}+y_{4}+\cdots+y_{2h}=\sum_{r=1}^{h}y_{2r}$$G_{j}-G_{1}=\sum_{r=1}^{h}(y_{2r-1}-y_{2r})\geq 0$$G_{j}\geq G_{1}$$y_{1}$$\square$$S$$S$$r>0$$r=0$$S$$D=\sum_{\text{odd }i}s_{i}-\sum_{\text{even }i}s_{i}$$r$$S$$r$$r$$r$$0$$r$$+$$+$$r$$0$$D=r$$r=0$$D=0$$\square$

#### $D\geq\delta$
$\delta=\dfrac{1}{2^{\,n+1}-1}$$(2^{k}-1)\delta$$k=1,2,\dots,n$$n+1$$I_{k}=\bigl[(2^{k-1}-1)\delta,\;(2^{k}-1)\delta\bigr],\qquad k=1,\dots,n+1,$$l_{k}=2^{\,k-1}\delta$$\delta(2^{n+1}-1)=1$$n$$m$$2n$$m\leq 2n+1$$2n+2$$m<2n+1$$m=2n+1$$(a_{1},b_{1}),\dots,(a_{n+1},b_{n+1})$$a_{i}\geq b_{i}\geq 0$$I_{k}$$D$$G$$I_{1},\dots,I_{n+1}$$D$$(a_{i},b_{i})$$a_{i}$$b_{i}$$G$$V=n+2$$E=n+1$$I_{k}$$D$$2n+2-m\geq 1$$\geq 1$$G$$C$$E_{C}\geq V_{C}-1$$V_{C}-1$$E\geq V-c$$c$$E=V-1$$V-1\geq V-c$$c\geq 1$$E_{C}\geq V_{C}$$E\geq V$$E=V-1$$T$$E_{T}=V_{T}-1$$\geq 1$$T$$E_{T}=V_{T}-1$$V_{T}$$T$$T$$U\cup W$$U$$W$$P=\{k:I_{k}\in U\}$$Q=\{k:I_{k}\in W\}$$D$$P\cup Q$$e=(A,B)$$T$$A$$a_{i}$$B$$b_{i}$$\operatorname{sgn}(e)=+1$$A\in U,\,B\in W$$-1$$A\in W,\,B\in U$$d_{e}=a_{i}-b_{i}$$d_{e}\geq 0$$v$$L(v)$$v$$v$$T$$v$$T$$\sum_{e\in T}\operatorname{sgn}(e)\,d_{e}=\sum_{v\in U}L(v)-\sum_{v\in W}L(v).$$e=(A,B)$$\operatorname{sgn}(e)(a_{i}-b_{i})$$A\in U,\,B\in W$$a_{i}-b_{i}$$A\in W,\,B\in U$$b_{i}-a_{i}$$U$$+1$$W$$-1$$T$$v\in U$$+1$$v\in W$$-1$$L(I_{k})=l_{k}=2^{\,k-1}\delta$$k=1,\dots,n+1$$L(D)=0$$\sum_{U}L-\sum_{W}L$$l_{k}$$\pm 1$$l_{k}$$\delta$$\delta$$P$$Q$$P\cup Q$$\sum_{k\in P}2^{k-1}=\sum_{k\in Q}2^{k-1}$$P=Q$$P=Q=\varnothing$$P\cup Q$$\delta$$D=\sum_{i=1}^{n+1}(a_{i}-b_{i})=\sum_{e\in E}d_{e}$$d_{e}\geq 0$$D\geq\sum_{e\in T}d_{e}\geq\Bigl|\sum_{e\in T}\operatorname{sgn}(e)\,d_{e}\Bigr|=\Bigl|\sum_{U}L-\sum_{W}L\Bigr|\geq\delta.$$\frac{1+\delta}{2}$

#### $D\leq\delta$
$n$$n$$n$$D=0\leq\delta$$n$$n+1$$a_{0},a_{1},\dots,a_{n}>0$$\sum a_{i}=1$$\{0,1,\dots,n\}$$2^{\,n+1}$$[0,1]$$0$$1$$s_{1}\leq s_{2}\leq\cdots\leq s_{2^{\,n+1}}$$2^{\,n+1}-1$$1$$\frac{1}{2^{\,n+1}-1}=\delta$$X,Y\subseteq\{0,\dots,n\}$$|\sum X-\sum Y|\leq\delta$$|X|+|Y|$$A=X,\;B=Y$$\sum A\geq\sum B$$r=\sum A-\sum B$$0\leq r\leq\delta$$A\cap B=\varnothing$$Z=A\cap B\neq\varnothing$$A^{\prime}=A\setminus Z,\;B^{\prime}=B\setminus Z$$A^{\prime},B^{\prime}$$|\sum A^{\prime}-\sum B^{\prime}|=r\leq\delta$$|A^{\prime}|+|B^{\prime}|=|A|+|B|-2|Z|<|A|+|B|$$\square$$A,B$$p=|A|,\;q=|B|$$B=\varnothing$$A$$\sum A=r\leq\delta$$|A|=1$$|A|\geq 2$$\{i\}\subset A$$\sum\{i\}=a_{i}\leq r\leq\delta$$|\{i\}|\!+\!|\varnothing|=1<|A|$$A=\{k\}$$k$$r=a_{k}\leq\delta$$I_{k}$$n$$n$$r$$2n$$n$$D=r\leq\delta$$B\neq\varnothing$$q\geq 1$$A,B$$A$$\alpha_{1},\dots,\alpha_{p}$$A_{0}=0,A_{1}=\alpha_{1},\dots,A_{p}=\sum A$$B$$\beta_{1},\dots,\beta_{q}$$B_{0}=0,\dots,B_{q}=\sum B$$k$$1\leq k<p$$A_{k}\leq\sum B$$\sum B<A_{k}<\sum A$$k<p$$T$$A$$\{\alpha_{k+1},\dots,\alpha_{p}\}$$\sum T=\sum A-A_{k}<r\leq\delta$$|T|=p-k<p+q$$q\geq 1$$(T,\varnothing)$$|\sum T-\sum\varnothing|=\sum T\leq\delta$$|T|+0=p-k<p+q$$\square$$A_{p-1}\leq\sum B\leq A_{p}$$A_{j}$$B_{j}$$A$$[0,\sum A]$$\alpha_{j}$$[A_{j-1},A_{j}]$$B$$[0,\sum B]$$0=t_{0}<t_{1}<\dots<t_{s}=\sum B$$S=\{0\}\cup\{A_{1},\dots,A_{p-1}\}\cup\{B_{1},\dots,B_{q}\}.$$A_{p-1}\leq\sum B$$A_{j}$$j<p$$\leq\sum B$$B_{q}=\sum B$$B$$B_{j}$$1\leq j\leq q$$A$$[A_{k-1},A_{k}]$$A$$B_{j}-A_{k-1}$$A$$A_{j}$$1\leq j\leq p-1$$B$$[B_{k-1},B_{k}]$$B$$A_{j}-B_{k-1}$$\leq p+q-1$$A$$B$$A$$B$$\sum B$$t_{i}-t_{i-1}$$A_{p-1}\leq\sum B\leq A_{p}$$[\sum B,\sum A]$$A$$r$$r=0$$A$$B$$n+1-p-q$$n+1-p-q$$(p+q-1)+(n+1-p-q)=n$$n$$r$$r>0$$D$$r$$0$$r=0$$r\leq\delta$$D\leq\delta$

#### 
$\frac{1+\delta}{2}$$\frac{1+\delta}{2}$$c$$c=\frac{1+\delta}{2}=\frac{1+\frac{1}{2^{\,n+1}-1}}{2}=\frac{2^{\,n}}{2^{\,n+1}-1}.$$\boxed{\dfrac{2^{n}}{2^{n+1}-1}}$

#### 
$\theta$$0^{\circ}<\theta<180^{\circ},$$T$$T$$\theta$$P$$T$$P$$T$$T$$T$$\theta$$\theta$$0^{\circ}<\theta<180^{\circ}$$A,B,C$$A+B+C=180^{\circ}$$A$$A,B,C$$P$$BC$$B,C$$AP$$(x,\;B,\;180^{\circ}-x-B)\qquad\text{and}\qquad(A-x,\;C,\;180^{\circ}-(A-x)-C)$$x$$0<x<A$$B$$C$$A$$x$$A-x$$180^{\circ}$$\theta$

#### $\theta$$180^{\circ}$
$\theta\nmid 180^{\circ}$$k$$180^{\circ}=k\theta$$T$$A,B,C$$\theta$$T$$\theta$$A$$A$$x$$A-x$$0<x<A$$T_{1}=(x,\;B,\;180^{\circ}-x-B),\qquad T_{2}=(A-x,\;C,\;180^{\circ}-(A-x)-C).$$T_{1}$$T_{2}$$\theta$$T_{1}$$B$$T_{2}$$C$$T$$T_{1}$$x$$T_{2}$$A-x$$A=x+(A-x)$$\theta$$T_{1}$$x$$T_{2}$$180^{\circ}-(A-x)-C$$180^{\circ}-(A-x)-C=B+x\qquad(\text{since }A+B+C=180^{\circ}).$$B+x$$\theta$$x$$\theta$$B$$\theta$$T_{1}$$180^{\circ}-x-B$$T_{2}$$A-x$$180^{\circ}-x-B=(A-x)+C\qquad(\text{again using }A+B+C=180^{\circ}),$$C$$\theta$$(180^{\circ}-x-B)+(180^{\circ}-(A-x)-C)=360^{\circ}-(A+B+C)=180^{\circ},$$(p+q)\theta=180^{\circ}$$p,q$$\theta\nmid 180^{\circ}$$T_{1},T_{2}$$\theta$$\square$$\theta$$60^{\circ},60^{\circ},60^{\circ}$$60^{\circ}$$\theta$$180^{\circ}=3\cdot 60^{\circ}$$\theta$$\theta\nmid 180^{\circ}$$\theta$$\theta$$\theta$$\theta\nmid 180^{\circ}$

#### $\theta$$180^{\circ}$
$180^{\circ}=m\theta$$m\geq 2$$\theta<180^{\circ}$$m>1$$T$$A,B,C$$\theta$$T$$\theta$$A=q\theta$$q\geq 2$$A$$\theta$$(q-1)\theta$$T_{1}=(\theta,\;B,\;A+C-\theta),\qquad T_{2}=((q-1)\theta,\;C,\;B+\theta).$$A+C-\theta=180^{\circ}-B-\theta$$B+\theta=180^{\circ}-C-(q-1)\theta$$180^{\circ}$$T_{1}$$\theta$$T_{1}$$T_{2}$$q=2$$T_{2}$$\theta$$q>2$$T_{2}$$(q-1)\theta$$\theta$$q-1$$T$$\theta$$\theta$$i\in\{0,1,2\}$$p$$T(i+1)<p\theta<T(i)+T(i+1)\qquad(\text{indices modulo }3).$$i$$T(i)>\theta$$p$$p\theta>T(i+1)$$p$$T(i+1)<180^{\circ}=m\theta$$(p-1)\theta\leq T(i+1)<p\theta$$T(i)>\theta$$p\theta\leq T(i+1)+\theta<T(i+1)+T(i),$$p\theta<T(i)+T(i+1)$$T(i+1)<p\theta$$T(i)\leq\theta$$\theta$$T(i)<\theta$$i$$i=0$$T(1)<\theta$$T(0)+T(1)=180^{\circ}-T(2)>180^{\circ}-\theta=(m-1)\theta\geq\theta\quad(\text{since }m\geq 2).$$T(1)<\theta<T(0)+T(1)$$p=1$$\square$$i$$p$$x=p\theta-T(i+1)$$0<x<T(i)$$i$$T(i)$$x$$T(i)-x$$L=(x,\;T(i+1),\;(m-p)\theta),\qquad R=(T(i)-x,\;T(i+2),\;p\theta).$$A+B+C=180^{\circ}$$180^{\circ}=m\theta$$L$$R$$\theta$$\theta$$\theta$$q\theta$$q\geq 2$$q-1$$p\leq m-1$$p$$m-p$$q\leq m-1$$m-1$$m$

#### 
$\theta$$180^{\circ}$$\boxed{\theta=\frac{180^{\circ}}{k}\quad\text{for some integer }k\geq 2}.$

#### 
$f:\mathbb{R}_{>0}\to\mathbb{R}_{>0}$$\sqrt{(x^{2}+f(y)^{2})/2}\geq(f(x)+y)/2\geq\sqrt{xf(y)}$$x,y\in\mathbb{R}_{>0}$$f:(0,\infty)\to(0,\infty)$$\sqrt{\frac{x^{2}+f(y)^{2}}{2}}\;\geq\;\frac{f(x)+y}{2}\;\geq\;\sqrt{x\,f(y)}\qquad(\forall x,y>0).$$\frac{x^{2}+f(y)^{2}}{2}\geq\Bigl(\frac{f(x)+y}{2}\Bigr)^{2}\;\Longleftrightarrow\;2x^{2}+2f(y)^{2}\geq(f(x)+y)^{2},$$\Bigl(\frac{f(x)+y}{2}\Bigr)^{2}\geq x\,f(y)\;\Longleftrightarrow\;(f(x)+y)^{2}\geq 4x\,f(y).$$x,y>0$$2x^{2}+2f(y)^{2}\;\geq\;(f(x)+y)^{2}\;\geq\;4x\,f(y).$

#### 
$x=f(y)$$f(y)>0$$2f(y)^{2}+2f(y)^{2}\geq(f(f(y))+y)^{2}\geq 4f(y)^{2},$$(f(f(y))+y)^{2}=4f(y)^{2}$$f(f(y))+y>0$$f(f(y))+y=2f(y)\qquad(\forall y>0),$$f(f(y))=2f(y)-y.$

#### $g$
$g(y)=f(y)-y$$y>0$$f(y)=y+g(y)$$g(f(y))=f(f(y))-f(y)=(2f(y)-y)-f(y)=f(y)-y=g(y).$

#### $g$
$y>0$$n\in\mathbb{N}$$g(y+n\,g(y))=g(y)\qquad\text{and}\qquad y+n\,g(y)>0.$$n=0$$g(y)=g(y)$$y>0$$n$$f(y+n\,g(y))=(y+n\,g(y))+g(y+n\,g(y))=y+(n+1)g(y).$$y+n\,g(y)>0$$f(z)>0$$z>0$$f(y+n\,g(y))>0$$y+(n+1)g(y)>0$$g(y+(n+1)g(y))=g\bigl(f(y+n\,g(y))\bigr)=g(y+n\,g(y))=g(y),$$n+1$$g(y)<0$$y>0$$-g(y)>0$$n\in\mathbb{N}$$n>\dfrac{y}{-g(y)}$$y+n\,g(y)=y-n(-g(y))<0,$$g(y)\geq 0\qquad(\forall y>0).$$f(y)=y+g(y)\geq y$$y>0$

#### 
$x,y>0$$\Delta=g(x)-g(y)$$\displaystyle 2x^{2}+2f(y)^{2}-(f(x)+y)^{2}$$\displaystyle=(x-f(y))^{2}-2\Delta\,(x+f(y))-\Delta^{2},$$\displaystyle(f(x)+y)^{2}-4x\,f(y)$$\displaystyle=(x-f(y))^{2}+2\Delta\,(x+f(y))+\Delta^{2}.$$(x-f(y))^{2}-2\Delta\,(x+f(y))-\Delta^{2}\geq 0,$$(x-f(y))^{2}+2\Delta\,(x+f(y))+\Delta^{2}\geq 0.$$4f(y)\Delta+\bigl((x-f(y))+\Delta\bigr)^{2}=(x-f(y))^{2}+2\Delta\,(x+f(y))+\Delta^{2}.$$0\leq 4f(y)\bigl(g(x)-g(y)\bigr)+\bigl((x-f(y))+(g(x)-g(y))\bigr)^{2}\leq 2(x-f(y))^{2}.$$x,y>0$

#### $g$
$u,v>0$$4\min(u,v)\,|g(u)-g(v)|\leq(u-v)^{2}.$$g(v)\leq g(u)$$x=f(u),\;y=v$$\displaystyle 0\leq{}$$\displaystyle 4f(v)\bigl(g(f(u))-g(v)\bigr)$$\displaystyle+\bigl((f(u)-f(v))+(g(f(u))-g(v))\bigr)^{2}$$\displaystyle\leq 2(f(u)-f(v))^{2}.$$g(f(u))=g(u)$$f(v)=v+g(v)$$\displaystyle 4(v+g(v))(g(u)-g(v))$$\displaystyle+\bigl((f(u)-f(v))+(g(u)-g(v))\bigr)^{2}$$\displaystyle\leq 2(f(u)-f(v))^{2}.$$f(u)=u+g(u),\;f(v)=v+g(v)$$f(u)-f(v)=(u-v)+(g(u)-g(v)).$$\Delta=g(u)-g(v)\geq 0$$f(u)-f(v)=(u-v)+\Delta,\qquad(f(u)-f(v))+\Delta=(u-v)+2\Delta.$$4v\Delta+4g(v)\Delta+(u-v)^{2}+4\Delta(u-v)+4\Delta^{2}\leq 2(u-v)^{2}+4\Delta(u-v)+2\Delta^{2},$$4v\Delta+4g(v)\Delta+2\Delta^{2}\leq(u-v)^{2}.$$g(v)\geq 0$$\Delta\geq 0$$4v\Delta\leq 4(v+g(v))\Delta\leq(u-v)^{2}-2\Delta^{2}\leq(u-v)^{2}.$$4v\,(g(u)-g(v))\leq(u-v)^{2}.$$g(u)\leq g(v)$$u$$v$$x=f(v),\;y=u$$4u\,(g(v)-g(u))\leq(u-v)^{2}.$

#### $g$
$p,q>0$$g(p)\neq g(q)$$p<q$$E=|g(q)-g(p)|>0$$n$$n>\frac{(q-p)^{2}}{4pE}.$$d=\dfrac{q-p}{n}>0$$z_{k}=p+kd$$k=0,1,\dots,n$$z_{n}=q$$k$$z_{k}>0$$\min(z_{k+1},z_{k})=z_{k}\geq p$$(z_{k+1},z_{k})$$4z_{k}\,|g(z_{k+1})-g(z_{k})|\leq(z_{k+1}-z_{k})^{2}=d^{2}.$$z_{k}\geq p$$4p\,|g(z_{k+1})-g(z_{k})|\leq 4z_{k}\,|g(z_{k+1})-g(z_{k})|\leq d^{2}.$$k=0,1,\dots,n-1$$4p\sum_{k=0}^{n-1}|g(z_{k+1})-g(z_{k})|\leq nd^{2}=\frac{(q-p)^{2}}{n}.$$\sum_{k=0}^{n-1}|g(z_{k+1})-g(z_{k})|\geq|g(z_{n})-g(z_{0})|=|g(q)-g(p)|=E.$$4pE\leq\frac{(q-p)^{2}}{n}.$$\dfrac{(q-p)^{2}}{n}<4pE$$g(p)=g(q)$$p,q>0$$g$

#### $f$
$g(y)=c$$y>0$$f(y)=y+c$$f(y)>0$$y>0$$c\geq 0$$c<0$$y=-c/2>0$$f(y)=c/2<0$$c\geq 0$$f(x)=x+c$$x,y>0$$\sqrt{\frac{x^{2}+(y+c)^{2}}{2}}\;\geq\;\frac{x+y+c}{2}\;\geq\;\sqrt{x(y+c)}.$$(x+y+c)^{2}\geq 4x(y+c)$$(x-y-c)^{2}\geq 0$$2(x^{2}+(y+c)^{2})\geq(x+y+c)^{2}$$(x-(y+c))^{2}\geq 0$$\boxed{\,f(x)=x+c\quad\text{for an arbitrary constant }c\geq 0\,}$

#### 
$a_{1},a_{2},a_{3},\ldots$$1$$n$$a_{n+1}$$a_{n}$$\gcd(a_{n+1},a_{i})>1$$1\leq i\leq n$$T$$L$$a_{n+T}=a_{n}+L$$n$$(a_{n})_{n\geq 1}$$>1$$x>1$$\gcd(x,a_{i})>1$$i\geq 1$$m,n\geq 1$$\gcd(a_{m},a_{n})>1$$m=n$$a_{m}>1$$\gcd(a_{m},a_{m})=a_{m}>1$$m<n$$a_{n}$$>a_{n-1}$$\gcd(a_{n},a_{i})>1$$i\leq n-1$$m\leq n-1$$\gcd(a_{n},a_{m})>1$$m>n$$\gcd(a_{m},a_{n})>1$$\square$$a_{n}$$i$$i<n$$\gcd(a_{n},a_{i})>1$$i>n$$\gcd(a_{i},a_{n})>1$$i=n$$a_{n}>1$$a_{n}\geq a_{1}+n-1$$n\geq 1$$a_{n+1}>a_{n}$$a_{n}\geq a_{1}+n-1$$\square$$\geq a_{1}$$\{a_{n}:n\geq 1\}$$a_{n}$$a_{n}\geq a_{1}$$x$$x\geq a_{1}$$x=a_{1}$$x>a_{1}$$N\geq 2$$a_{N}\geq x$$a_{N-1}<x\leq a_{N}$$x=a_{N}$$x<a_{N}$$a_{N}$$i\leq N-1$$\gcd(x,a_{i})=1$$x$$x=a_{N}$$\square$$x,y$$z=y^{\,a_{1}+1}$$y>1$$a_{1}\geq 2$$z>a_{1}$$i$$y$$p\mid y$$p\mid a_{i}$$p\mid z$$\gcd(z,a_{i})\geq p>1$$i$$z$$z=a_{N}$$N$$x$$\gcd(x,a_{N})>1$$\gcd(x,z)>1$$\gcd(x,y)=1$$\gcd(x,y^{\,a_{1}+1})=1$$\gcd(x,y)>1$$\square$$B=a_{1}^{\,a_{1}+1}+a_{1}+2$$x$$i\geq 1$$p<B$$p\mid x$$p\mid a_{i}$$k>a_{1}$$j\geq 1$$a_{j}<k$$\gcd(k,a_{j})=1$$a_{n}\to\infty$$N$$a_{N}>k$$n$$a_{n}<k$$a_{n}<k<a_{n+1}$$k=a_{n+1}$$k$$k\neq a_{n+1}$$a_{n}<k<a_{n+1}$$a_{n+1}$$i\leq n$$\gcd(k,a_{i})=1$$j=i$$a_{j}\leq a_{n}<k$$\gcd(k,a_{j})=1$$\square$$d>1$$d$$f$$d$$d\leq f$$d$$x$$d$$x$$d$$d\mid x$$f$$d$$f$$x$$d\leq f$$d$$d$$d$$<B$$d$$d$$d$$\gcd(d,a_{1})>1$$d$$d\mid a_{1}$$d\leq a_{1}<B$$d$$<B$$d$$d^{\prime}<d$$p$$d$$d=p\,e$$e>1$$d$$e$$e$$d$$e<d$$e>a_{1}$$e$$e>a_{1}$$j$$a_{j}<e$$\gcd(e,a_{j})=1$$c$$a_{j}$$c$$c\mid a_{j}$$c\leq a_{j}<e<d$$c$$\gcd(e,c)=1$$c\mid a_{j}$$\gcd(e,a_{j})=1$$c$$d$$\gcd(c,d)>1$$q\mid\gcd(c,d)$$q\mid d=p\,e$$q\mid p$$q\mid e$$\gcd(e,c)=1$$q\nmid e$$q\mid p$$p$$q=p$$p\mid c$$c$$c<d$$c$$<B$$p<B$$e\leq a_{1}$$k=e^{\,a_{1}+1}$$e>1$$a_{1}\geq 2$$k>a_{1}$$k\leq a_{1}^{\,a_{1}+1}<B$$e\mid k$$k$$k$$i$$\gcd(k,a_{i})>1$$k$$e$$\gcd(e,a_{i})>1$$i$$e$$k$$k>a_{1}$$j$$a_{j}<k$$\gcd(k,a_{j})=1$$k$$c$$a_{j}$$c$$c\mid a_{j}$$c\leq a_{j}<k$$c$$\gcd(e,c)=1$$e\mid k$$\gcd(k,a_{j})=1$$c$$d$$\gcd(c,d)>1$$q$$\gcd(c,d)$$q\mid p\,e$$\gcd(e,c)=1$$q\mid p$$q=p$$p\mid c$$c<k\leq a_{1}^{\,a_{1}+1}<B$$p\leq c<B$$p<B$$\square$$x$$i\geq 1$$d$$x$$d$$d$$<B$$d$$\gcd(d,a_{i})>1$$p\mid\gcd(d,a_{i})$$p\mid d\mid x$$p\mid a_{i}$$p<B$$\square$$L=B!$$B$$x>1$$\text{good}(x)\iff\text{good}(x+L)$$\text{good}(x)$$i$$p<B$$p\mid x$$p\mid a_{i}$$p<B$$p\mid L$$p\mid x+L$$\gcd(x+L,a_{i})\geq p>1$$x+L>1$$\text{good}(x+L)$$\text{good}(x+L)$$i$$x+L$$p<B$$p\mid x+L$$p\mid a_{i}$$p\mid L$$p\mid(x+L)-L=x$$p\mid x$$p\mid a_{i}$$x>1$$x\leq 1$$x=1$$x$$p\mid 1$$\gcd(x,a_{i})>1$$i$$\text{good}(x)$$\square$$T$$L$$a_{1}$$\text{good}(a_{1}+L)$$a_{1}+L\geq a_{1}$$N$$a_{N}=a_{1}+L$$L>0$$N>1$$T=N-1,\qquad L=B!.$$T>0$$a_{1+T}=a_{1}+L$$n\geq 1$$a_{n+T}=a_{n}+L$$n$$n=1$$a_{1+T}=a_{1}+L$$a_{n+T}=a_{n}+L$$a_{n+1}$$a_{n+1}+L$$a_{n+T}=a_{n}+L<a_{n+1}+L.$$a_{n+T+1}$$a_{n+T}$$a_{n+T+1}\leq a_{n+1}+L.$$a_{n+T+1}<a_{n+1}+L$$x=a_{n+T+1}-L$$a_{n}<x<a_{n+1}.$$a_{n+1}$$i\leq n$$\gcd(x,a_{i})=1$$a_{n+T+1}$$\text{good}(x)$$\text{good}(x+L)$$\gcd(x,a_{i})>1$$i$$\gcd(x,a_{i})=1$$a_{n+T+1}=a_{n+1}+L$$a_{(n+1)+T}=a_{n+1}+L$$\square$$T$$L$$a_{1}$$a_{n+T}=a_{n}+L$$n\geq 1$$\boxed{\begin{gathered}\text{There exist positive integers }T\text{ and }L\text{ such that}\\
a_{n+T}=a_{n}+L\quad\text{for all }n\geq 1.\end{gathered}}$
---

# 부록 — 검증 수치표 (webReader 원문 추출, 집필 수치 계약용)

> 아래 수치는 원문 HTML(webReader 마크다운)에서 직접 추출한 값이다. 본문 인용 수치는 전부 이 표와 대조해야 한다.

## 저자 (HTML 원문 직접 확인 — webReader 요약에는 누락됨)

Joshua Ong Jun Leang, Haonan Li, Zheng Zhao, Xinyi Shang, Wenda Li, Zhengzhong Liu, Eric Xing, Shay B. Cohen, Eleonora Giunchiglia — MBZUAI Institute of Foundation Models · University of Edinburgh · University College London · Imperial College London

## Table 1 — 벤치마크 정확도(%) (총 93문제)

| Model | AIME 2025 | AIME 2026 | HMMT Feb. 2026 | Overall |
|---|---|---|---|---|
| Claude Opus 5 | 100.00 | 100.00 | 96.97 | 98.92 |
| Gemini 3.7 Flash | 100.00 | 100.00 | 90.91 | 96.77 |
| Kimi K3 | 93.33 | 90.00 | 78.79 | 87.10 |
| K2-Horizon-7B | 83.33 | 80.00 | 60.61 | 74.19 |
| K2-Horizon-7B + Magenta | 100.00 (+16.67) | 100.00 (+20.00) | 100.00 (+39.39) | 100.00 (+25.81) |
| K2-Horizon-375B | 93.33 | 90.00 | 72.73 | 84.95 |
| K2-Horizon-375B + Magenta | 100.00 (+6.67) | 100.00 (+10.00) | 100.00 (+27.27) | 100.00 (+15.05) |
| Qwen3.8-27B | 100.00 | 86.67 | 87.88 | 91.40 |
| Qwen3.8-27B + Magenta | 100.00 (+0.00) | 100.00 (+13.33) | 100.00 (+12.12) | 100.00 (+8.60) |
| GPT-5.6-Sol (Codex) | 90.00 | 86.67 | 78.79 | 84.95 |
| GPT-5.6-Sol (Codex) + Magenta | 100.00 (+10.00) | 100.00 (+13.33) | 100.00 (+21.21) | 100.00 (+15.05) |

## Table 2 — 패러프레이즈 강건성 (AIME 2026, %)

| Model | Original | Paraphrased | Δ |
|---|---|---|---|
| K2-Horizon-375B | 90.0 | 86.7 | -3.3 |
| K2-Horizon-375B + Magenta | 100.0 | 100.0 | 0.0 |
| K2-Horizon-7B | 80.0 | 70.0 | -10.0 |
| K2-Horizon-7B + Magenta | 100.0 | 100.0 | 0.0 |

## Table 3 — 명제 심사 절제 (Goedel formaliser, AIME 2026)

| Setting | Ver↑ | VerCor↑ | FCR↓ |
|---|---|---|---|
| With Js | 63.3% | 63.3% | 0.0% |
| Without Js | 36.7% | 20.0% | 45.5% |

## Table 5 — 모델·데이터셋별 정제 라운드 (초기 시도=1로 카운트)

| Dataset | K2-Horizon-7B avg/max | K2-Horizon-375B avg/max |
|---|---|---|
| AIME2025 | 1 / 3 | 1 / 1 |
| AIME2026 | 2 / 5 | 1 / 2 |
| HMMT2026 | 3 / 10 | 1 / 2 |

## Table 6 — 명제 생성·심사 오류 (%) (AIME 2026 전체 30문제)

| Outcome or first failure category | Generated | Conditional |
|---|---|---|
| Lean elaborated | 66.55 | – |
| Lean compiler error | 33.08 | – |
| Statement extraction failure | 0.22 | – |
| Input context overflow | 0.16 | – |
| Type, coercion, or projection mismatch | 17.47 | 52.23 |
| Typeclass or instance synthesis | 7.85 | 23.46 |
| Parser or notation syntax | 4.78 | 14.28 |
| Unknown name or API misuse | 2.73 | 8.17 |
| Statement extraction failure (rejected) | 0.22 | 0.66 |
| Input context overflow (rejected) | 0.16 | 0.47 |
| Metavariables or underspecified binders | 0.13 | 0.38 |
| Pattern, binder, or match elaboration | 0.10 | 0.31 |
| Tactic failure or open goal | 0.01 | 0.02 |
| Resource timeout | 0.01 | 0.02 |
| Rejected before judge: Lean error | 33.08 | – |
| Rejected before judge: extraction error | 0.22 | – |
| Rejected before judge: context overflow | 0.16 | – |
| DeepSeek semantic rejection | 44.64 | 67.08 |
| DeepSeek semantic acceptance | 21.91 | 32.92 |

## Table 7 — 증명 오류 분포 (%) (AIME 2026 전체 30문제)

| Primary error category | Leanstral int. | Leanstral ext. | Codex ext. |
|---|---|---|---|
| Tactic failure or open goals | 42.70 | 63.78 | 30.28 |
| Forbidden token or policy | – | 26.77 | – |
| Unknown name or API misuse | 15.19 | – | 15.31 |
| Tool, protocol, or runtime failure | 13.68 | – | 2.16 |
| Parser or syntax error | 8.18 | 0.79 | 0.67 |
| Type or coercion mismatch | 6.70 | – | 45.92 |
| Resource limit or timeout | 5.72 | 8.66 | 2.66 |
| Other Lean diagnostic | 5.23 | – | – |
| Typeclass or instance synthesis | 2.60 | – | 1.83 |
| Metavariables or invalid declaration | – | – | 0.83 |
| Noncomputable definition | – | – | 0.33 |

## Table 8 — 수학 오류 근원 (%) (K2-Horizon-7B, AIME 2026에서 오류 판사가 귀인한 14건)

| Cause | Percent |
|---|---|
| Input interpretation or transcription | 28.6 |
| Unsupported logical or proof step | 28.6 |
| Arithmetic, algebra, or cardinality | 21.4 |
| Escalation after repeated Lean repair could not preserve the contract | 14.3 |
| Invalid construction or counterexample | 7.1 |

## 본문 핵심 수치 (해설 인용용)

- 예산: T=32(리즈너), M=512(명제 샘플), K=4096(증명 시도). 절제실험은 배치 32.
- Figure 2(자기수정): IMO 2026 P1~P6 = 0, 3, 20, 2, 1, 8회(평균 5.7회). AIME 2026 평균 5회(7B) vs 2회(375B).
- Figure 3: Codex 첫 호출 통과 약 66% vs Goedel 42%. 전체 커버리지 Codex 6호출 vs Goedel 약 120호출. 6호출 시 Goedel 약 68%.
- Figure 5(b): 외부 실패 0회로 해결 — Leanstral 42% vs Codex 17%. 외부 실패가 라우터 도달 — Leanstral 58% vs Codex 83%.
- Figure 5(c): 전체 커버리지 리즈너 토큰 약 6×10^4 vs 9×10^5.
- Figure 5(d): 검증된 증명 길이 약 1.1×10^4 vs 2×10^4 토큰(약 절반).
- Figure 4: Leanstral 내부 호출 — 중앙 커버리지 약 3×10^2, 전체 커버리지 최대 3×10^3.
- 리샘플링 대비: AIME 2026 리샘플링 29/30(96.7%) vs 자기수정 30/30. IMO 2026 리샘플링(문제당 8~16회 독립 생성) 1/6(16.7%) vs 자기수정 6/6.
- 성공확률 p의 독립 n회 시도: 1-(1-p)^n ≥ 1-e^{-np}.
- 명제심사 없을 때 거짓 증명 5건 중 3건이 약화·답 내장 대리 목표, 1건 문제 조건 누락, 1건 기하 오역. 모순 문맥 통과 0건.
- Figure 1 예시: AIME 2026 문제, 초기 추론 π^7 오류 → math 귀인 → 재도출로 π^6 수정.
- 리즈너 설정: temperature 0.6, top_p 0.95, 최대 출력 64,000토큰(IMO는 128,000), seed 42, 컨텍스트 524,288.
- Leanstral: 최대 출력 80,000/요청(실험 래퍼 32,000), 누적 4,000,000토큰/궤적, 컴팩션 168,000.
- Lean v4.29.1 + Mathlib + SafeVerify(금지: sorry, admit, 신규 공리, native_decide).
- 형식화 갭 오류 유형: 17017↔107017 치환, N=1000↔10000, 3^9↔39, 6회↔7회 반복 해석 등.
