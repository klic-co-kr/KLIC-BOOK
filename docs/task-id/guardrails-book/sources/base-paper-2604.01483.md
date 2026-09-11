# Type-Checked Compliance: Deterministic Guardrails for Agentic Financial Systems Using Lean 4 Theorem Proving

- 원문: arXiv 2604.01483v1 (HTML판, 2026)
- 저자: Devakh Rashie, Veda Rashi — Thomas Jefferson High School for Science and Technology, Alexandria, VA, USA
- 코드/데모: https://github.com/arkanemystic/lean-agent-protocol · https://axiom.devrashie.space

> 본 파일은 원고 집필용 원문 사본이다. webReader로 https://arxiv.org/html/2604.01483v1 를 변환한 마크다운이며, 집필 에이전트는 이 파일을 기본 소스로 쓴다.

## Abstract

The rapid evolution of autonomous, agentic artificial intelligence within financial services has introduced an existential architectural crisis: large language models (LLMs) are probabilistic, non-deterministic systems operating in domains that demand absolute, mathematically verifiable compliance guarantees. Existing guardrail solutions—including NVIDIA NeMo Guardrails and Guardrails AI—rely on probabilistic classifiers and syntactic validators that are fundamentally inadequate for enforcing complex multi-variable regulatory constraints mandated by the SEC, FINRA, and OCC. This paper presents the *Lean-Agent Protocol*, a formal-verification-based AI guardrail platform that leverages the Aristotle neural-symbolic model developed by Harmonic AI to auto-formalize institutional policies into Lean 4 code. Every proposed agentic action is treated as a mathematical conjecture: execution is permitted if and only if the Lean 4 kernel proves that the action satisfies pre-compiled regulatory axioms. This architecture provides cryptographic-level compliance certainty at microsecond latency, directly satisfying SEC Rule 15c3-5, OCC Bulletin 2011-12, FINRA Rule 3110, and CFPB explainability mandates. A three-phase implementation roadmap from shadow verification through enterprise-scale deployment is provided.

Keywords: formal verification, AI guardrails, Lean 4, agentic AI, financial regulation, theorem proving, neural-symbolic AI, SEC compliance, formal methods

## 1. Introduction: Deterministic Governance in Agentic AI

The rapid evolution of artificial intelligence within the financial services sector has catalyzed a transition from isolated, predictive analytics and generative text models to fully autonomous, agentic systems. These frameworks possess the capability to interpret complex user intent, dynamically synthesize contextual data, formulate multi-step execution plans, and autonomously interact with external environments through application programming interfaces (APIs) and tool-calling mechanisms (IBM, 2026). While this paradigm shift offers massive operational efficiencies in algorithmic trading, dynamic risk assessment, and autonomous portfolio management, it simultaneously introduces an existential architectural crisis regarding systemic reliability and regulatory compliance (FINRA, 2026a).

Traditional enterprise automation relies on deterministic systems—such as robotic process automation (RPA) bots and hard-coded workflow engines—that execute predefined logical paths with mathematical precision (IBM, 2026). If a condition is not explicitly defined, execution halts, bounding operational risk. Conversely, LLMs and the agentic architectures built upon them operate probabilistically (PurpleSec, 2026). They navigate continuous, high-dimensional vector spaces to generate responses that are *statistically likely* rather than mathematically certain (Rainbird, 2025). This stochastic nature renders them highly adaptable to ambiguous inputs but inherently susceptible to hallucinations, context drift, and adversarial prompt injections (PurpleSec, 2026). In highly regulated domains such as global financial markets—where a single algorithmic deviation can precipitate catastrophic capital depletion or systemic market instability—probabilistic execution without rigid constraints is architecturally and legally untenable (FINRA, 2021).

The contemporary industry response has been the deployment of *AI Guardrails*—secondary software layers designed to filter, monitor, and control LLM inputs and outputs (Verma, 2026). However, the vast majority of existing guardrail solutions rely heavily on probabilistic classifiers, vector similarity searches, or syntactic schema validation (NVIDIA, 2026a). While these tools excel at content moderation, they are fundamentally inadequate for enforcing the complex, multi-variable regulatory constraints demanded by the SEC, FINRA, and OCC (FINRA, 2026a).

To reconcile the agility of agentic AI with the uncompromising mandates of financial regulation, a paradigm shift toward formal verification is required. This paper delineates the technical blueprint, regulatory feasibility, and implementation roadmap for the Lean-Agent Protocol. By leveraging the Aristotle model (Harmonic AI, 2025) developed by Harmonic AI, this platform translates natural language institutional policies into the dependently typed formal programming language Lean 4 (Lean FRO, 2026). Acting as a deterministic gateway, the Lean-Agent Protocol treats every proposed agentic action as a mathematical conjecture: execution is permitted if and only if the Lean 4 kernel can definitively prove that the action satisfies the pre-compiled regulatory axioms. V. Rashi led the formal mapping of SEC Rule 15c3-5 and FINRA Rule 3110 regulatory mandates into the Lean-Agent logical framework.

## 2. Technical Integration and Workflow Dynamics

### 2.1. The Aristotle Model: Neural-Symbolic Architecture

At the foundational core of the Lean-Agent Protocol is the Aristotle model, engineered by the Silicon Valley-based startup Harmonic AI (Harmonic AI, 2026). Aristotle represents a structural departure from purely autoregressive LLMs by pioneering a neural-symbolic methodology designed specifically for automated theorem proving and the generation of formally verified, hallucination-free reasoning (Harmonic AI, 2026). The system gained international prominence by achieving gold-medal-equivalent performance on the 2025 International Mathematical Olympiad (IMO), successfully generating machine-verifiable solutions in Lean 4 for five out of the six competition problems (Harmonic AI, 2025).

The architecture of Aristotle integrates three distinct but synergistic components: (1) a continuous Lean proof search system, (2) an informal reasoning engine dedicated to generating and formalizing intermediary lemmas, and (3) a specialized geometry solver (Harmonic AI, 2025). Unlike traditional models that predict the next token in isolation, Aristotle utilizes the Lean 4 compiler as an infallible, high-speed reward signal within a reinforcement learning loop (Harmonic AI, 2025). This mathematical grounding forces the model to continuously validate its internal reasoning against the strict rules of the Calculus of Inductive Constructions (CIC) (Carneiro, 2024).

The primary capability that enables the Lean-Agent Protocol is Aristotle's proficiency in *auto-formalization*—the automated translation of unstructured, natural language concepts into rigorous formal code (Lu et al., 2024). During its training and deployment, Aristotle has made novel contributions to Mathlib (Lean's comprehensive mathematical library), formalized proofs for long-standing open conjectures including Erdős Problems 1026 and 728, and identified subtle logical errors within established academic textbooks (Harmonic AI, 2026).

Crucially, Aristotle is engineered to handle "epistemic gaps" and incomplete proof skeletons. When translating a complex financial policy, the initial mapping may leave certain logical steps unproven—denoted in Lean by the sorry tactic (Harmonic AI, 2026). Aristotle possesses the capability to autonomously deduce and fill multiple sorry markers within a single theorem, effectively bridging the gap between high-level regulatory directives and the granular logic gates required for machine execution (Harmonic AI, 2026).

### 2.2. Translation Error Rates and Handling of Complex Logical Constraints

A critical concern when translating natural language policies into executable code is the fidelity of the translation. The Aristotle model mitigates this risk not by achieving perfect initial generation, but by leveraging the deterministic constraints of the Lean environment to execute autonomous self-repair (Harmonic AI, 2025).

In the formalization of complex theorems, Aristotle's informal reasoning engine occasionally generates text containing subtle semantic confusions—for example, conflating the mathematical definitions of "strictly decreasing sequences," "weakly decreasing sequences," and sequences that merely decrease at some point (Harmonic AI, 2025). In a standard generative AI pipeline, this semantic error would pass through unnoticed. However, within the Aristotle architecture, the informal proof is immediately submitted to the Lean 4 kernel for formalization (Harmonic AI, 2025). The Lean compiler deterministically rejects the flawed logic and generates a highly specific compiler error, often including explicit counterexamples (Harmonic AI, 2026). Aristotle ingests this error state and autonomously repairs the logical gaps, adjusting its approach until the Lean compiler returns a successful verification (Harmonic AI, 2025). The final output is therefore guaranteed to be correct relative to the formalized problem statement, effectively neutralizing the risk of "hallucinated compliance" (Harmonic AI Employee, 2026).

### 2.3. Architectural Design: The Deterministic Request-Response Loop

To operationalize the Aristotle engine as a secure guardrail, the Lean-Agent Protocol employs a state-machine-driven Request-Response loop. This architecture intercepts the probabilistic output of a primary trading agent and forces it through a deterministic verification bottleneck prior to API execution. The architectural flow is divided into two distinct temporal phases:

#### 2.3.1. Phase 1: Asynchronous Policy Configuration

1. Natural Language Ingestion. Compliance officers author institutional trading limits, risk parameters, and regulatory mandates in standard English (e.g., "Do not execute trades exceeding 10% of the firm's available daily capital.").
2. Aristotle Translation. The Aristotle API processes these documents, utilizing its informal reasoning engine to parse the text and its proof search system to auto-formalize the constraints into Lean 4 code.
3. Compilation and Storage. The generated code is compiled by the Lean kernel. Any logical inconsistencies are iteratively repaired by Aristotle. Once successfully compiled, the resulting axioms, theorems, and definitions are stored in an immutable repository known as the *Policy Environment*.

#### 2.3.2. Phase 2: Synchronous Runtime Authorization (The Agentic Loop)

1. Intent Generation. The primary Agentic AI (e.g., a portfolio rebalancing agent) analyzes real-time market data and generates an intent to execute a specific API tool (e.g., execute_trade(symbol="AAPL", volume=50000, type="market")).
2. Orchestrator Interception. The Orchestrator node intercepts this API call before it reaches the execution environment. It tokenizes the request, extracting parameters and current systemic state variables (available capital, recent volatility indices) (NVIDIA, 2026a).
3. Conjecture Formulation. The Orchestrator maps these parameters against the Lean-verified theorems in the Policy Environment, formatting the agent's proposed action as a formal mathematical conjecture (Breen et al., 2025).
4. Lean Kernel Verification. The conjecture is submitted to the Lean 4 type-checker, which attempts to prove that the proposed action satisfies all constraints within the Policy Environment.
5. Deterministic Actuation.
   - State A ("Proven" / Allowed): If the kernel successfully verifies the proof, it returns a binary True. The Gateway API unlocks and the original API call is routed to the execution layer.
   - State B ("Refuted" / Blocked): If the kernel cannot verify the proof (e.g., the trade volume exceeds the capital theorem), it returns a binary False. The action is definitively blocked, and the system generates a formal error trace for the audit log (Rulebricks, 2026).

### 2.4. Real-Time Computational Latency in the Agentic Loop

A persistent historical critique of formal verification methods is their high computational overhead, which traditionally rendered them unsuitable for low-latency, real-time applications such as high-frequency trading (HFT) (Chen et al., 2026). However, architectural advancements within Lean 4, specifically the decoupling of proof generation from proof checking, fundamentally resolve this latency bottleneck.

In the Lean-Agent Protocol, the computationally intensive process of generating proofs and formalizing policies occurs entirely asynchronously during the configuration phase (Harmonic AI, 2026). During synchronous runtime execution, the system only requires the Lean 4 kernel to perform type-checking and proof verification against pre-compiled binaries (Carneiro, 2024). The Lean trusted kernel is heavily optimized, relying on minimal primitive operations written in highly performant C++ (Carneiro, 2024).

Empirical benchmarking derived from Amazon Web Services' (AWS) deployment of the Cedar authorization policy language—which is formally verified using Lean 4—demonstrates the extreme efficiency of this approach (Amazon Web Services, 2026). In differential testing environments, evaluating a formalized access control input against the Lean model requires an average of only 5 microseconds (Amazon Web Services, 2026). This execution speed is notably faster than the equivalent evaluation in highly optimized Rust code, which averages 7 microseconds per test case (Amazon Web Services, 2026).

Furthermore, recent updates to the Lean 4 ecosystem have introduced advanced automated reasoning tactics, such as grind, which integrate SMT (Satisfiability Modulo Theories) solving capabilities directly into the prover (Lean FRO, 2025). Consequently, when the Orchestrator submits a simple arithmetic constraint (e.g., checking if Trade_Value ≤ Capital_Limit), the Lean kernel resolves the statement with sub-millisecond latency (Ospanov et al., 2025). This completely removes formal verification as a bottleneck in the execution critical path (Ospanov et al., 2025).

## 3. Financial Regulatory and Compliance Mapping

### 3.1. SEC Rule 15c3-5: The Market Access Rule and Hard Guardrails

The deployment of autonomous trading agents introduces severe risks to market integrity, prompting intense regulatory scrutiny. Following instances of devastating algorithmic failures—such as the 1987 market crash and the Knight Capital incident in 2012 (where an unchecked algorithm lost $440 million in 45 minutes)—the Securities and Exchange Commission (SEC) implemented Rule 15c3-5, known as the Market Access Rule (Nasdaq, 2025).

SEC Rule 15c3-5 mandates that broker-dealers providing market access must "establish, document, and maintain a system of risk management controls and supervisory procedures reasonably designed to manage the financial, regulatory, and other risks" (FINRA, 2025b). Specifically, the rule requires the implementation of pre-trade controls that: (1) prevent the entry of orders that exceed appropriate pre-set credit or capital thresholds; and (2) prevent the entry of erroneous orders by rejecting requests that exceed appropriate price or size parameters (U.S. Securities and Exchange Commission, 2011).

Crucially, the SEC dictates that these controls must be under the "direct and exclusive control" of the broker-dealer (WilmerHale, 2011). Deploying a secondary, probabilistic LLM as a safety filter constitutes a severe regulatory vulnerability (PurpleSec, 2026). LLMs are fundamentally non-deterministic; their behavior is governed by stochastic sampling across continuous vector representations (Christodorescu et al., 2026). A probabilistic filter might successfully block 99.9% of non-compliant trades, but the inherent mathematical possibility of an evasion means the firm cannot guarantee absolute compliance, thereby failing the standard of "exclusive control" (PurpleSec, 2026).

The Lean-Agent Protocol directly satisfies the rigid mandates of SEC Rule 15c3-5 by enforcing *hard* deterministic guardrails (Moveo.AI, 2026). Because the capital thresholds and price parameters are formalized as immutable Lean 4 axioms, the AI agent's execution layer is cryptographically bound by mathematical logic (Huber, 2026). The verification kernel does not interpret intent or estimate probability; it computes binary truth. If an agent proposes a trade where the size parameter mathematically exceeds the stated limit, the proof fails compilation and the order is deterministically rejected at the gateway level (Rulebricks, 2026). This framework provides regulators with verifiable, mathematical proof that erroneous orders cannot physically reach the market, fully aligning agentic automation with the strictest interpretations of the Market Access Rule.

### 3.2. OCC Bulletin 2011-12 and FINRA Rule 3110: Supervisory Obligations

Beyond direct market access, the Office of the Comptroller of the Currency (OCC) and the Financial Industry Regulatory Authority (FINRA) impose broad requirements for organizational risk management and the supervision of automated systems. OCC Bulletin 2011-12 (SR 11-7) established the foundational framework for Model Risk Management (MRM), requiring robust model development, implementation, continuous validation, and sound governance (Office of the Comptroller of the Currency, 2011).

Traditional MRM frameworks were designed under the assumption that computational models were deterministic entities with easily interpretable inputs and predictable outputs (Moody's, 2026). The introduction of generative AI and autonomous agents completely fractures these assumptions, introducing high opacity, stochastic reasoning, and autonomous decision-making loops that bypass static validation cycles (Moody's, 2026). Concurrently, FINRA Rule 3110 requires member firms to establish and maintain a system to supervise the activities of all associated persons and systems to achieve compliance with securities laws (FINRA, 2026b).

In Regulatory Notice 24-09 and the 2026 Annual Regulatory Oversight Report, FINRA explicitly clarified that its rules are technology-neutral; if a firm deploys Generative AI tools, those tools must be supervised with the same rigor as human communications and traditional decision-making systems (FINRA, 2025a).

The Lean-Agent Protocol serves as the vital structural bridge between the opacity of LLMs and the transparency required by FINRA and the OCC. By isolating the probabilistic "thinking" of the AI agent from the deterministic "doing" of the execution API, institutions can foster innovation without compromising governance. Because the execution of any agentic task is entirely dependent on clearing the Lean kernel, the firm can demonstrate to OCC and FINRA examiners that the overarching supervisory system remains firmly in human control, operating with 100% predictability regardless of the underlying LLM's stochastic output (Moveo.AI, 2026).

### 3.3. The Right to Explanation and Reverse Auto-Formalization for Audit Trails

One of the most complex regulatory challenges facing the deployment of AI in financial services is the legal mandate for algorithmic transparency, commonly referred to as the "Right to Explanation" (VerityAI, 2026). Under the Equal Credit Opportunity Act (ECOA) and the Fair Credit Reporting Act (FCRA), creditors are legally obligated to provide consumers with specific, accurate, and easily understandable reasons when taking an adverse action (Consumer Financial Protection Bureau, 2023). The Consumer Financial Protection Bureau (CFPB) has issued explicit guidance stating that the use of complex, "black-box" algorithms or AI models does not exempt institutions from these transparency requirements (Consumer Financial Protection Bureau, 2023). Similarly, in Europe, the GDPR and the newly enacted EU AI Act mandate that individuals subject to automated decision-making have the right to obtain meaningful explanations of the logic involved (AAAI Publications, 2025).

When the Lean-Agent Protocol blocks an AI agent's proposed action, the output of a failed Lean compilation is a highly technical, dependently typed mathematical error trace. While this perfectly enforces a deterministic block, presenting a formal logic compiler error to a consumer or non-technical auditor is legally insufficient and violates plain-language disclosure requirements (VerityAI, 2026). To solve this, the Lean-Agent Protocol executes a process of *reverse auto-formalization* or "back-translation," converting rigid mathematical failure states back into compliant, natural language adverse action notices (VerityAI, 2026).

This capability is modeled on advancements embodied in the Herald dataset and the NL2Lean reinforcement learning framework (Gao et al., 2025; Fang et al., 2025). The Herald framework demonstrates how static analysis tools can be used to extract structured metadata—including theorem declarations, dependency relationships, and precise proof states—from Lean 4 environments (Gao et al., 2025). When a proof fails in the Lean-Agent gateway, the system isolates the exact line of code and the specific logical tactic that triggered the rejection (e.g., identifying that the agent's proposed action failed the Debt_to_Income < 0.43 axiom) (Gao et al., 2025). Using an approach similar to NL2Lean, a specialized, fine-tuned translation model ingests this isolated proof state and, utilizing a Retrieval-Augmented Generation (RAG) pipeline, generates a precise, step-wise informal explanation of the failure (Gao et al., 2025). This ensures that the explanation provided to the auditor or consumer is not a hallucinated rationale, but a direct, one-to-one translation of the mathematical constraint that forced the denial (Gao et al., 2025).

## 4. Security, Vulnerability Analysis, and Formal Sandboxing

### 4.1. Formal Methods for LLM Safety

The prevailing methodology for securing Large Language Models relies on empirical techniques such as Reinforcement Learning from Human Feedback (RLHF), constitutional AI alignment, and automated red-teaming (Doshi et al., 2026). While these techniques shape core behavioral tendencies, they are fundamentally reactive and probabilistic. As LLMs are integrated into multi-agent systems with access to APIs, databases, and execution environments, the attack surface expands exponentially—often referred to as the "lethal trifecta" of tool access, natural language interfaces, and untrusted external data (Mozilla.ai, 2026).

The concept of Formal Methods for LLM Safety seeks to elevate AI security from empirical testing to mathematical certainty (Zhang et al., 2024). By applying techniques traditionally reserved for safety-critical hardware and aerospace engineering, formal methods guarantee that a system satisfies specific functional and security properties across all possible state spaces (Zhang et al., 2024). The Lean-Agent Protocol embodies this paradigm: rather than endlessly patching an LLM against every conceivable adversarial input, the protocol assumes the LLM is compromised and instead secures the execution perimeter using mathematically verified code generation and runtime evaluation (Miculicich et al., 2025).

### 4.2. Vulnerability Analysis: Jailbreaking the Aristotle Translation Layer

While the Lean 4 kernel provides absolute security at the execution level, the system's primary vulnerability resides in the translation layer. If an adversary can manipulate the Aristotle model into generating structurally valid but semantically malicious Lean code, they can effectively bypass the policy constraints. This threat vector is explored in recent security literature under the terms "logical jailbreaks" and "formalization drift."

#### 4.2.1. Logical Jailbreaks

Traditional alignment training conditions models to refuse clearly harmful natural language prompts. However, adversaries utilize techniques like LogiBreak and QueryAttack to systematically translate malicious intents into complex logical expressions, structured non-natural query languages, or ciphers (Peng et al., 2025). By shifting the prompt's distribution away from the standard safety-alignment training data while preserving the underlying semantic intent, these attacks successfully trick the model into processing the request (Zou et al., 2025).

#### 4.2.2. Formalization Drift and Perturbation

Attackers employ Sentence-Level Perturbations (SLPs)—such as rephrasing, adding irrelevant context, or using synonym substitutions—to confuse the model's semantic mapping (Li et al., 2026). In LLM-based logical translators, this linguistic variation often leads to "symbol drift" or "formalization drift" (Li et al., 2026). If an attacker utilizes an Indirect Prompt Injection that causes Aristotle to map a restricted action variable to a permitted Lean symbol, the Lean kernel will successfully verify the proof, unwittingly authorizing a policy violation (Li et al., 2025).

#### 4.2.3. Mitigation via Concept-Symbol Constraints

To secure the translation layer, the Lean-Agent Protocol must enforce rigid structure on the Aristotle formalization process. Drawing on frameworks like MenTaL (Mapping Equivalent Natural language To Assigned Logic), the architecture must compel the LLM to explicitly build a concept-symbol mapping table before initiating the translation into Lean (Li et al., 2025). By algorithmically linking varied linguistic expressions to a hard-coded registry of shared Lean 4 symbols, the system mitigates symbol drift and ensures that adversarial synonyms cannot hijack the logic solver (Li et al., 2025). Furthermore, the Orchestrator node must aggressively sanitize context hydration, utilizing static parsing to extract only necessary variables and completely stripping untrusted external text before the prompt reaches the formalization engine (FINOS, 2026).

### 4.3. Execution Sandboxing: The Strategic Imperative of WebAssembly (WASM)

Because Agentic AI systems are designed to autonomously plan, write, and execute code, any code generated by the agent must be inherently treated as a hostile payload (Cardoso, 2026). Executing untrusted code introduces severe security risks, including potential Remote Code Execution (RCE), arbitrary file system manipulation, and sensitive data exfiltration (NVIDIA, 2026b).

Traditional containerization platforms such as Docker possess critical architectural flaws that render them inadequate for securing highly untrusted AI execution (Diallo, 2026). Docker containers share the host operating system's kernel. If an AI agent generates a payload containing a kernel exploit, it can escape container boundaries, escalate privileges, and compromise the host machine and internal networks (Cardoso, 2026).

To achieve bulletproof isolation without sacrificing performance, the Lean-Agent Protocol mandates the use of WebAssembly (WASM) as its execution substrate (Diallo, 2026). WASM is a highly compact, portable binary instruction format designed to execute code at near-native speeds within a mathematically secure sandbox (Diallo, 2026). The security guarantees of WebAssembly are rooted in its architecture:

- Linear Memory Model. WASM modules operate within a single, contiguous block of linear memory. Executing code has zero visibility into addresses outside this designated block, providing strict fault isolation from the host and other modules (Isobe, 2026).
- Protected Call Stack. WASM utilizes a protected call stack logically separated from the module's heap memory. This renders control-flow hijacking mathematically impossible (WebAssembly Community Group, 2024).
- Capability-Based Security (WASI). By integrating the WebAssembly System Interface (WASI), the sandbox operates on a strict principle of least privilege. The WASM instance has zero default access to the host's filesystem, network sockets, or environment variables (Diallo, 2026).

By compiling both the Lean 4 verification environment and the agent's executable tools into WASM binaries, the Lean-Agent Protocol establishes a zero-trust execution perimeter. This guarantees that even if a sophisticated adversary successfully jailbreaks the Aristotle translation layer and engineers a malicious Lean proof, the resulting execution remains permanently trapped within the WASM sandbox, neutralizing the threat of systemic compromise (Diallo, 2026).

## 5. Competitive and Market Landscape

### 5.1. Evaluating Existing AI Guardrails: Probabilistic vs. Formal Approaches

As organizations race to operationalize generative AI, a vibrant ecosystem of guardrail solutions has emerged. However, a critical comparative analysis reveals that the dominant market players—NVIDIA NeMo Guardrails and Guardrails AI—rely on methodologies that are fundamentally misaligned with the deterministic requirements of financial regulation.

NVIDIA NeMo Guardrails is a comprehensive, open-source toolkit that utilizes a specialized modeling language called Colang to define dialog flows and topical boundaries (NVIDIA, 2026d). The system architecture is inherently probabilistic (NVIDIA, 2026e). When a user or agent submits a prompt, NeMo invokes an LLM to generate a "canonical form" of the intent, then utilizes vector similarity algorithms to match this intent against predefined rules (NVIDIA, 2026a). This approach introduces significant vulnerabilities: vector spaces are continuous, and adversarial perturbations can easily manipulate the semantic distance, causing the system to misclassify a restricted action as benign (Christodorescu et al., 2026). Furthermore, NeMo relies heavily on secondary "LLM-as-a-judge" calls for evaluation, which incurs severe computational latency—often adding hundreds of milliseconds to the critical path—and decreases overall system throughput (NVIDIA, 2026c).

Guardrails AI focuses on syntactic validation, utilizing the RAIL specification and Python-based libraries (like Pydantic) to enforce structural consistency on LLM outputs (Verma, 2026). While syntactic validation is fast and deterministic, it is logically shallow (AI Agent Store, 2026). Pydantic can guarantee that an agent's proposed trade volume is an integer, but it cannot dynamically prove that the specific integer, when combined with historical margin usage and real-time capital constraints, adheres to a multi-tiered regulatory policy.

The Lean-Agent Protocol transcends both paradigms. By shifting the verification burden to the Lean 4 kernel, the platform abandons probabilistic vector matching (NeMo) in favor of deep mathematical theorem proving, while simultaneously vastly exceeding the logical depth of simple schema validation (Guardrails AI) (AI Agent Store, 2026). The architecture provides absolute, binary certainty of compliance with ultra-low, microsecond latency, uniquely positioning it as the only viable solution for high-frequency, regulated financial execution (Amazon Web Services, 2026).

Table 1. Comparative Analysis of AI Guardrail Platforms (원문에 표 존재 — NeMo Guardrails / Guardrails AI / Lean-Agent Protocol 비교).

### 5.2. Applied Formal Methods in FinTech and Access Control

The theoretical proposition of utilizing Lean 4 as an enterprise-grade execution gateway is powerfully substantiated by existing large-scale deployments in cloud computing and decentralized finance.

The most prominent validation is found in Amazon Web Services' development of Cedar, an open-source authorization policy language (Amazon Web Services, 2026). AWS utilizes Lean 4 in a process known as "verification-guided development" to formally model and verify Cedar's core components—the evaluator, authorizer, and validator (Amazon Web Services, 2026). By proving overarching theorems such as guaranteeing that a "forbid" policy will always trump a "permit" policy regardless of evaluation order, AWS ensures that its access control mechanisms behave flawlessly across quadrillions of production authorizations (Amazon Web Services, 2023). The efficiency of the Lean model—capable of executing differential testing inputs in an average of 5 microseconds—proves unequivocally that formal verification can scale to support the highest-throughput enterprise infrastructures in the world (Amazon Web Services, 2026).

Furthermore, researchers have successfully leveraged Lean 4 to formalize the complex economic behaviors of Automated Market Makers (AMMs) like Uniswap (Pusceddu and Bartoletti, 2024). Historically, the economic security of decentralized exchanges relied on pen-and-paper proofs regarding constant-product formulas (x·y=k) and arbitrage opportunities (Dessalvi et al., 2026). Recent studies have mechanically formalized these properties, along with complex trading fee mechanisms, directly into the Lean 4 theorem prover (Pusceddu and Bartoletti, 2024).

The critical importance of moving from theoretical models to machine-checked code is underscored by landmark failures in algorithmic trading. The Knight Capital failure—where an unchecked algorithmic error caused a $440 million loss—and the 2007 "Hammer" case—where basic algorithms were manipulated to illegally move settlement prices in NYMEX futures—demonstrate that financial markets cannot tolerate software ambiguity (Nasdaq, 2025).

## 6. Strategic Implementation Roadmap

The deployment of the Lean-Agent Protocol within a financial institution requires a meticulous, phased integration to manage the complexities of neuro-symbolic formalization and execution sandboxing.

### 6.1. Phase 1: Minimum Viable Product — Stateless Policy Translation and Shadow Verification

The objective of the MVP phase is to validate the auto-formalization capabilities of the Aristotle model without exposing production systems to risk.

- Action: Compliance teams input a static, bounded subset of institutional policies—such as basic capital thresholds derived from SEC Rule 15c3-5 and fundamental data privacy rules—into the Aristotle API.
- Process: Aristotle translates these natural language directives into Lean 4 axioms. To prevent formalization drift, engineering teams implement MenTaL-style concept-to-symbol constraints, ensuring rigorous, one-to-one mapping of financial terminology to Lean logic.
- Execution: The system operates asynchronously in "shadow mode." Live agentic outputs are logged and subsequently passed to the Orchestrator for post-execution verification. The Lean kernel's judgments are compared against human compliance reviews to measure Aristotle's translation fidelity and baseline error rates.

### 6.2. Phase 2: Beta — WASM Integration and Synchronous Interception

Phase 2 transitions the protocol from an analytical tool into an active, synchronous security gateway.

- Action: The verified Lean 4 Policy Environment is compiled and deployed within a hardened WebAssembly (WASM) runtime. WASI capabilities are strictly configured, granting the sandbox zero access to the host network or filesystem.
- Process: The Orchestrator node is moved into the critical path of the agentic loop. It intercepts real-time API requests, formulates Lean conjectures, and leverages SMT-backed grind tactics to achieve sub-millisecond kernel verification.
- Execution: The "Right to Explanation" back-translation pipeline is introduced. Utilizing the Herald dataset methodology, any action refuted by the Lean kernel triggers a reverse auto-formalization process. A localized RAG model translates the specific Lean error trace back into a plain-language adverse action notice, satisfying ECOA and FCRA mandates.

### 6.3. Phase 3: Production-Ready — High-Frequency Deployment and Enterprise Scaling

The final phase expands the Lean-Agent Protocol to encompass fully autonomous, high-frequency enterprise operations.

- Action: The Policy Environment is scaled to ingest complex, multi-tiered compliance rules spanning global directives (e.g., GDPR, EU AI Act, Basel III).
- Process: Advanced orchestration primitives, including bounded MPSC (Multi-Producer, Single-Consumer) mailboxes and work-stealing schedulers, are deployed to support concurrent multi-agent meshes, maintaining ultra-low latency under massive load.
- Execution: Comprehensive, cryptographically secure audit logging is finalized. Every agentic action executed by the firm is inextricably linked to an immutable Lean 4 mathematical proof stored in the execution telemetry. The institution achieves a zero-trust, mathematically verified AI infrastructure, enabling the limitless scaling of Agentic AI while remaining absolutely impervious to regulatory violations.

## 7. Conclusion

This paper has presented the Lean-Agent Protocol, a novel formal-verification-based guardrail architecture designed to address the fundamental incompatibility between the probabilistic nature of agentic AI and the deterministic demands of financial regulation. By leveraging the Aristotle neural-symbolic model to auto-formalize regulatory mandates into Lean 4 axioms—and enforcing execution through a Lean 4 kernel operating at microsecond latency—the protocol provides cryptographic-level compliance certainty for the first time.

The protocol directly maps to and satisfies the requirements of SEC Rule 15c3-5 (Market Access Rule), OCC Bulletin 2011-12 (Model Risk Management), FINRA Rule 3110 (Supervision), ECOA/FCRA adverse action mandates, and EU AI Act explainability requirements. Comparatively, the protocol transcends the probabilistic limitations of NVIDIA NeMo Guardrails and the logical shallowness of Guardrails AI. Real-world deployments of Lean 4 at AWS (Cedar) and in DeFi (AMM formalization) substantiate the technical and enterprise-scale viability of the approach.

The three-phase roadmap provides a structured path from shadow verification MVP to a production-ready, zero-trust mathematical AI infrastructure—one that enables financial institutions to deploy autonomous agentic AI at scale while remaining absolutely impervious to regulatory violations.

## Acknowledgments

V. Rashi led the formal mapping of SEC Rule 15c3-5 and FINRA Rule 3110 regulatory mandates into the Lean-Agent logical framework, providing the regulatory analysis that underpins Sections 3.1 and 3.2 of this paper.

## References (집필 인용용 핵심 목록)

- Amazon Web Services (2023). How we designed Cedar to be intuitive to use, fast, and safe. AWS Security Blog.
- Amazon Web Services (2026). Lean into verified software development. AWS Open Source Blog.
- Breen et al. (2025). Ax-Prover: a deep reasoning agentic framework for theorem proving. arXiv:2510.12787.
- Carneiro (2024). Lean4Lean: verifying a typechecker for Lean, in Lean. arXiv:2403.14064.
- Chen et al. (2026). FastTTS: accelerating test-time scaling for edge LLM reasoning. arXiv:2509.00195.
- Christodorescu et al. (2026). Systems security foundations for agentic computing. arXiv:2512.01295.
- Dessalvi, Bartoletti, Lluch-Lafuente (2026). A formal approach to AMM fee mechanisms with Lean 4. arXiv:2602.00101.
- Doshi et al. (2026). Towards verifiably safe tool use for LLM agents. arXiv:2601.08012.
- Fang et al. (2025). NL2Lean: translating natural language into Lean 4 through multi-aspect reinforcement learning. EMNLP 2025.
- Gao et al. (2025). Herald: a natural language annotated Lean 4 dataset. arXiv:2410.10878.
- Harmonic AI (2025). Aristotle: IMO-level automated theorem proving. arXiv:2510.01346.
- Li et al. (2025). Are LLMs stable formal logic translators in logical reasoning across linguistically diversified texts? (MenTaL) arXiv:2506.04575.
- Lu et al. (2024). Process-driven autoformalization in Lean 4. arXiv:2406.01940.
- Miculicich et al. (2025). VeriGuard: enhancing LLM agent safety via verified code generation. arXiv:2510.05156.
- Ospanov, Farnia, Yousefzadeh (2025). APOLLO: automated LLM and Lean collaboration for advanced formal reasoning. arXiv:2505.05758.
- Peng et al. (2025). Logic jailbreak: efficiently unlocking LLM safety restrictions through formal logical expression. arXiv:2505.13527.
- Pusceddu, Bartoletti (2024). Formalizing automated market makers in the Lean 4 theorem prover. FMBC 2024, OASIcs Vol. 118.
- Zhang et al. (2024). The fusion of large language models and formal methods for trustworthy AI agents: a roadmap. arXiv:2412.06512.
- Zou et al. (2025). QueryAttack: jailbreaking aligned large language models using structured non-natural query language. ACL 2025 Findings.
