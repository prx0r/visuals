Yes. The synthesis is:

> **Truthcore should not mean “the single truth.”**
> It should mean **a scoped claim node with provenance, status, contradictions, and residue.**

Multiple Truthcores can contradict. That is not a bug. The graph should preserve contradiction instead of flattening it.

Here is the agent-ready build brief.

# Build Brief: Imaginarium Conversation Geometry Engine

## 0. Core Goal

Build a LangGraph-based system that turns every user conversation into a reusable path through:

```txt
Compression → Truthcore retrieval/checking → Meta strategy → Pedagogy move → Response → Evaluation → Saved path
```

The system should not start as a LoRA or monolithic fine-tune. It should be a graph-orchestrated pathway engine that learns which conversational geometries work for which user inputs.

LangGraph should be used because it provides stateful graph execution with nodes, edges, conditional routing, persistence, checkpoints, memory, human-in-the-loop, and time-travel/replay-style debugging. ([Docs by LangChain][1])

---

## 1. What We Already Have

The project has four existing assets:

1. **Conversation geometry traces**
   Around 50 “Pythagoras/string theory” style conversations. These contain:

   * user prompt
   * HXRMXS response
   * `n1_compression`
   * `n2_truthcore`
   * `n3_meta`
   * turn intention / phase / stance / progress

2. **Pedagogy datasets**
   Large labelled datasets for Socratic, Buddhist, therapeutic, Gurdjieff-style, etc. These contain:

   * lineage
   * phase
   * function ID
   * student state
   * behavior tags
   * mechanism shape
   * teaching actions
   * register
   * intent
   * predicted response

3. **Lean / Sanskrit Proof Engine basics**
   Existing system for classifying claims as PROVED, OUTSIDE_FORMAL, HOLLOW, UNPROVED, PARTIAL, etc. The Sanskrit Proof Engine thesis already frames claims as graph nodes with statuses, primitives, bridges, divergences, and residues. 

4. **Formal primitive schema**
   Current primitives include things like `CausalPower`, `Integration`, `Composition`, `Exclusion`, `Particularity`, `Broadcast`, `Threshold`, and `Normativity`, with cross-mappings across IIT, PyPhi, Dharmakīrti, GWT, and FEP. 

---

## 2. Truthcore Definition

Do **not** treat Truthcore as “the truth.”

A Truthcore is:

```txt
a scoped, source-grounded claim object with provenance, status, relations, contradiction edges, and residue.
```

Truthcores can disagree.

Example:

```json
{
  "id": "dharmakirti_arthakriya_exists",
  "claim": "A thing is real insofar as it has causal efficacy.",
  "scope": {
    "tradition": "Dharmakirti / Buddhist epistemology",
    "domain": "epistemology / ontology",
    "source_refs": ["dharmakirti_arthakriya_node"]
  },
  "status": "AXIOMATIC_WITHIN_TRADITION",
  "formal_status": "PARTIAL",
  "primitive_refs": ["CausalPower"],
  "residue": "This does not automatically equal IIT causal power or modern physical causation.",
  "relations": [
    {
      "type": "OVERLAPS",
      "target": "iit_causal_power",
      "reason": "Both use causal efficacy/power as a primitive."
    },
    {
      "type": "DIVERGES_FROM",
      "target": "nyaya_pramana_factivity",
      "reason": "Different account of valid cognition and reality."
    }
  ]
}
```

Truthcore exists to prevent hallucination by forcing every claim into one of these statuses:

```txt
PROVED
AXIOMATIC_WITHIN_TRADITION
EMPIRICAL
PARTIAL
UNPROVED
OUTSIDE_FORMAL
HOLLOW
CONTESTED
CONTRADICTED
```

The Build Order doc already uses a tiered structure: Tier 1 proved items from Mathlib/PhysLean, Tier 2 functional primitives, Tier 3 tradition-anchored claim files. The decompositions table maps claim components to primitives and leaves residue when something does not fit. 

---

## 3. The Key Design Rule

Never collapse contradiction.

Contradiction must be represented as a graph relation:

```txt
SUPPORTS
CONTRADICTS
OVERLAPS
DIVERGES_FROM
REFINES
DEPENDS_ON
USES_PRIMITIVE
LEAVES_RESIDUE
ANALOGOUS_TO
NOT_IDENTICAL_TO
```

If two claims contradict, store both with source scope.

Bad:

```txt
Truthcore says X is true.
```

Good:

```txt
Truthcore A says X under Buddhist epistemology.
Truthcore B says not-X under Nyāya.
They CONTRADICT at primitive Y or axiom Z.
```

This is how Truthcore avoids becoming a hallucinated mess.

---

## 4. Minimal Tech Stack

Use:

```txt
Python
LangGraph
FastAPI
Postgres + pgvector or Qdrant
SQLite/Postgres for graph tables
Lean 4 / lake / Pantograph integration
Pydantic schemas
LLM provider of choice
```

LangGraph should orchestrate the runtime. It can store short-term conversation state and long-term memories; the current docs describe short-term memory as part of agent state and long-term memory as user/application-level storage across sessions. ([Docs by LangChain][2])

Use LangGraph checkpoints/persistence so every run can be inspected, resumed, forked, and corrected. ([Docs by LangChain][3])

---

## 5. Repository Structure

Create:

```txt
imaginarium-engine/
  app/
    main.py
    api/
      chat.py
      ingest.py
      eval.py

  graph/
    state.py
    build_graph.py
    nodes/
      input_normalizer.py
      compression.py
      path_retrieval.py
      truthcore_retrieval.py
      formal_boundary.py
      meta_strategy.py
      pedagogy_router.py
      response_generator.py
      judge.py
      save_trace.py

  schemas/
    compression.py
    truthcore.py
    pedagogy.py
    meta.py
    path.py
    user_profile.py
    evaluation.py

  ingest/
    ingest_conversation_geometries.py
    ingest_pedagogy_packs.py
    normalize_pedagogy_labels.py
    build_embeddings.py

  storage/
    db.py
    vector.py
    graph_store.py
    migrations/

  lean/
    lean_tool.py
    templates/
    scratch/
    lakefile.lean

  prompts/
    compression.md
    meta_strategy.md
    pedagogy_router.md
    response_generator.md
    judge.md
    truthcore_extractor.md

  evals/
    golden_router_cases.jsonl
    negative_controls.jsonl
    path_replay_tests.py
    truthcore_hallucination_tests.py

  data/
    raw/
    processed/
    embeddings/
```

---

## 6. Core State Schema

Create a single LangGraph state object.

```python
from typing import TypedDict, List, Dict, Any, Optional

class EngineState(TypedDict, total=False):
    thread_id: str
    user_id: str

    raw_input: str
    normalized_input: str
    conversation_window: List[Dict[str, str]]

    compression: Dict[str, Any]
    active_compression_nodes: List[str]

    retrieved_paths: List[Dict[str, Any]]
    retrieved_truthcores: List[Dict[str, Any]]
    truthcore_conflicts: List[Dict[str, Any]]

    formal_checks: List[Dict[str, Any]]

    meta_strategy: Dict[str, Any]
    pedagogy_plan: Dict[str, Any]

    draft_response: str
    final_response: str

    judge_result: Dict[str, Any]
    path_trace: Dict[str, Any]

    user_profile: Dict[str, Any]
    errors: List[str]
```

---

## 7. Data Schemas

### 7.1 Compression

```python
class CompressionResult(BaseModel):
    surface_question: str
    actual_question: str
    hidden_assumptions: list[str]
    category_errors: list[str]
    confusion_type: str
    user_intention: str
    compression_nodes: list[str]
    confidence: float
```

Compression is **not** pedagogy. Compression is diagnostic decomposition.

---

### 7.2 Truthcore

```python
class TruthcoreNode(BaseModel):
    id: str
    claim: str
    scope: dict
    source_refs: list[str]
    status: str
    formal_status: str
    primitive_refs: list[str]
    evidence_refs: list[str]
    residue: str
    confidence: float
    relations: list[dict]
```

Required rule:

```txt
No TruthcoreNode may be promoted without at least one of:
- source_ref
- human_verified = true
- formal_status = PROVED
- explicitly marked as HYPOTHESIS
```

---

### 7.3 Pedagogy Move

```python
class PedagogyMove(BaseModel):
    id: str
    lineage: str
    phase: str
    function_id: str
    mechanism_shape: str
    teaching_actions: list[str]
    register: dict
    intent: str
    approach: str
    avoid: list[str]
```

Pedagogy is the move library. Meta chooses from it.

---

### 7.4 Meta Strategy

```python
class MetaStrategy(BaseModel):
    phase: str
    stance: str
    reason: str
    selected_truthcore_mode: str
    selected_pedagogy_moves: list[str]
    response_arc: list[str]
    avoid: list[str]
    should_call_lean: bool
    should_interrupt_for_human: bool
```

---

### 7.5 Conversation Path

```python
class ConversationPath(BaseModel):
    id: str
    title: str
    input_pattern: str
    compression_nodes: list[str]
    truthcore_nodes: list[str]
    pedagogy_moves: list[str]
    meta_phases: list[str]
    response_steps: list[dict]
    outcome_score: float | None
    failure_notes: str | None
    embedding: list[float] | None
```

---

## 8. Ingestion Step 1: Conversation Geometries

Input: the 50 Pythagoras-style conversations.

For each turn, extract:

```txt
user text
hxrmxs answer
n1_compression
n2_truthcore
n3_meta
turn intention
phase
stance
category errors
mechanisms
correspondences
evidence
```

Store as:

```txt
ConversationPath
PathStep
CompressionNode
TruthcoreCandidate
MetaPhase
```

Important: Do **not** trust all generated Truthcores. Import them as:

```txt
status = HYPOTHESIS
verification_status = UNVERIFIED
```

until they are source-grounded, human-verified, or Lean/formal checked.

---

## 9. Ingestion Step 2: Pedagogy Packs

Input: Buddha, Socrates, therapy, Gurdjieff, etc.

For each assistant turn, extract:

```txt
lineage
phase
function_id
student_state
behavior_tags
mechanism_shape
teaching_actions
register
intent
approach
predicted_response
assistant text
```

Store as:

```txt
PedagogyMoveNode
PedagogyExample
```

Then normalize move IDs.

Example:

```txt
socratic_constraint_collapse
buddhist_view_clinging_cut
therapeutic_projection_check
gurdjieff_mechanicality_exposure
corbin_symbolic_re_elevation
levin_level_mapping
```

The point is to make lineage-specific moves reusable across content domains.

---

## 10. Ingestion Step 3: Truthcore Seeds

Do not build the full Truthcore layer yet. Seed only the primitives and a few core boundary claims.

Start with 20–50 primitives:

```txt
CausalPower
Integration
Broadcast
Particularity
Normativity
PredictionError
AnalogyVsIdentity
SymbolicVsPhysicalCausation
FormalVsEmpirical
ViewClinging
SelfView
CategoryError
MechanismBoundary
Residue
```

Each primitive must have:

```txt
definition
allowed uses
forbidden uses
source/domain notes
example claims
negative controls
```

Example:

```json
{
  "id": "AnalogyVsIdentity",
  "claim": "A structural analogy between two systems does not establish ontological identity.",
  "status": "AXIOMATIC_SYSTEM_RULE",
  "formal_status": "PARTIAL",
  "primitive_refs": ["CategoryDistinction"],
  "forbidden_use": "Do not use analogy as proof of physical causation.",
  "negative_controls": [
    "String theory proves Pythagorean music of the spheres.",
    "Quantum entanglement proves amulet luck."
  ]
}
```

---

## 11. LangGraph Runtime

Build these nodes:

```txt
START
→ input_normalizer
→ parallel:
    compression_node
    path_retrieval_node
    truthcore_retrieval_node
    user_profile_node
→ meta_strategy_node
→ conditional:
    formal_boundary_node if should_call_lean
→ pedagogy_router_node
→ response_generator_node
→ judge_node
→ save_trace_node
→ END
```

LangGraph supports nodes and conditional edges, so implement the formal check as a conditional edge from `meta_strategy_node`. ([Docs by LangChain][4])

---

## 12. Node Responsibilities

### 12.1 `input_normalizer`

Clean user input.

Output:

```txt
normalized_input
conversation_window
```

---

### 12.2 `compression_node`

Prompt the LLM to produce strict JSON:

```json
{
  "surface_question": "...",
  "actual_question": "...",
  "hidden_assumptions": [],
  "category_errors": [],
  "confusion_type": "...",
  "user_intention": "...",
  "compression_nodes": [],
  "confidence": 0.0
}
```

This is the first major prediction target.

---

### 12.3 `path_retrieval_node`

Embed:

```txt
normalized_input + actual_question + compression_nodes
```

Retrieve similar prior paths by:

```txt
semantic similarity
+ matching compression nodes
+ matching phase
+ high outcome score
```

Return top 3–5 paths.

---

### 12.4 `truthcore_retrieval_node`

Retrieve candidate Truthcores by:

```txt
actual_question
compression_nodes
truthcore refs from similar paths
primitive refs
```

Return:

```txt
supporting truthcores
contradicting truthcores
boundary truthcores
unknowns
```

Important: if no grounded Truthcore exists, return:

```json
{
  "truthcore_mode": "INSUFFICIENT_GROUNDING",
  "allowed_response": "provisional framing only"
}
```

---

### 12.5 `formal_boundary_node`

Call Lean only when the meta strategy says the claim is formalizable or primitive-related.

Do not use Lean for poetry, symbol, ritual, or existential claims unless they are being formalized as structure.

Input:

```json
{
  "claim": "...",
  "candidate_primitives": [],
  "candidate_lean_type": "optional"
}
```

Output:

```json
{
  "called_lean": true,
  "formal_status": "PROVED | UNPROVED | TYPE_ERROR | OUTSIDE_FORMAL | PARTIAL",
  "lean_output": "...",
  "residue": "...",
  "human_review_required": false
}
```

Lean should verify the formal spine, not decide metaphysical truth.

---

### 12.6 `meta_strategy_node`

Input:

```txt
compression
retrieved paths
retrieved truthcores
formal checks
user profile
```

Output:

```json
{
  "phase": "DISSECTION | FRAMEWORKS | MECHANISM | BOUNDARIES | INTEGRATION | UNMAKING | REMAKING | SELF_MAKING | META",
  "stance": "iron_wall | direct | exploratory | imaginal | gentle",
  "reason": "...",
  "selected_truthcore_mode": "support_only | contrast | contradiction_map | insufficient_grounding",
  "selected_pedagogy_moves": [],
  "response_arc": [],
  "avoid": [],
  "should_call_lean": false,
  "should_interrupt_for_human": false
}
```

---

### 12.7 `pedagogy_router_node`

Choose concrete moves from the pedagogy dataset.

Example:

```json
{
  "primary_move": "socratic_definition_pressure",
  "secondary_move": "buddhist_binary_refusal",
  "mechanism_shape": "constraint_collapse",
  "register": {
    "pressure": 3,
    "intimacy": 2,
    "attunement": 3
  },
  "avoid": ["existential_choice_ending", "generic_spiritual_synthesis"]
}
```

---

### 12.8 `response_generator_node`

Generate final response using:

```txt
actual question
truthcore map
formal boundaries
meta strategy
pedagogy plan
similar path examples
```

Hard rule:

```txt
The response must not invent Truthcore claims.
If grounding is insufficient, it must say so.
If traditions contradict, it must preserve the contradiction.
```

---

### 12.9 `judge_node`

Score the response.

Metrics:

```txt
compression_accuracy
truthcore_fidelity
contradiction_preservation
pedagogy_fit
non_repetition
source_grounding
formal_boundary_respect
user_helpfulness
```

Output:

```json
{
  "score": 0.0,
  "passed": false,
  "failure_modes": [],
  "rewrite_needed": true,
  "recommended_fix": "..."
}
```

If score is low, either regenerate once or save as failure trace.

---

### 12.10 `save_trace_node`

Save:

```txt
input
compression
retrieved paths
truthcores used
formal checks
meta strategy
pedagogy move
response
judge result
```

This becomes future training data.

---

## 13. Human Correction Loop

Use LangGraph interrupts for uncertain or dangerous graph writes. Interrupts allow the graph to pause for human input and resume after updates. ([Docs by LangChain][5])

Interrupt when:

```txt
Truthcore is about to be promoted from HYPOTHESIS to GROUNDED
Lean result is TYPE_ERROR but model wants to use it
contradiction is detected between high-confidence nodes
judge score is low twice
new primitive is proposed
```

Human correction should save:

```json
{
  "bad_prediction": {},
  "why_bad": "...",
  "corrected_prediction": {},
  "correction_type": "compression | truthcore | meta | pedagogy | response"
}
```

---

## 14. Truthcore Anti-Hallucination Rules

These are mandatory.

### Rule 1: No source, no promotion

A Truthcore can exist as `HYPOTHESIS`, but cannot become `GROUNDED` without:

```txt
source citation
human verification
Lean proof
or explicit system axiom
```

### Rule 2: Contradiction is stored, not solved

If two Truthcores conflict:

```txt
do not average them
do not choose one automatically
do not synthesize them poetically
```

Instead:

```txt
create CONTRADICTS edge
name the scope
name the primitive or axiom where they diverge
```

### Rule 3: Every bridge needs residue

If the system says two things overlap, it must also say what does **not** carry over.

Example:

```json
{
  "bridge": "Dharmakirti arthakriyā ↔ IIT causal power",
  "shared_primitive": "CausalPower",
  "residue": "Different domains, aims, and axiom systems."
}
```

### Rule 4: Use negative controls

Maintain a file:

```txt
negative_controls.jsonl
```

Examples:

```txt
String theory proves Pythagorean music of the spheres.
Quantum entanglement proves amulet luck.
All traditions say the same thing.
Dharmakīrti proves IIT.
Astrology is empirically validated by symbolic usefulness.
```

If the system produces these as true bridges, the build fails.

### Rule 5: Truthcore confidence is not truth

Confidence only means:

```txt
confidence in extraction / mapping / source support
```

not cosmic truth.

---

## 15. How Lean Fits

Lean should be a tool node, not the main runtime.

Use Lean for:

```txt
formalizable primitives
claim equivalence
dependency checks
contradiction under fixed axioms
proof status
type-checking
```

Do not use Lean for:

```txt
mythic meaning
symbolic resonance
personal advice
unformalized metaphysics
aesthetic synthesis
```

Lean result should update Truthcore as:

```txt
PROVED
UNPROVED
TYPE_ERROR
OUTSIDE_FORMAL
PARTIAL
```

The Sanskrit Proof Engine already says the boundary between formal and non-formal is itself a finding. Keep that principle. 

---

## 16. Training/Evaluation Later

Do not train LoRA first.

First generate a dataset:

```txt
input → compression → truthcore refs → meta strategy → pedagogy move → outcome
```

Then train:

```txt
router model: input → compression/meta/pedagogy labels
```

Later use DPO/preference training on:

```txt
good path vs bad path
```

The important correction target is not only the answer. It is the chosen geometry.

---

## 17. MVP Milestones

### Milestone 1: Ingest and normalize

* Ingest 50 conversation geometry traces.
* Ingest pedagogy packs.
* Create node tables.
* Build embeddings for paths and moves.

Done when:

```txt
Given a new input, system retrieves 3 similar paths and 5 candidate pedagogy moves.
```

---

### Milestone 2: LangGraph runtime

* Build the LangGraph state.
* Implement nodes.
* Implement conditional Lean call.
* Save full traces.

Done when:

```txt
One user input produces compression, path retrieval, truthcore candidates, meta strategy, pedagogy plan, final response, and saved trace.
```

---

### Milestone 3: Truthcore discipline

* Add primitive seeds.
* Add statuses.
* Add contradiction edges.
* Add negative controls.
* Prevent ungrounded promotion.

Done when:

```txt
The system can say “this is only a hypothesis” instead of hallucinating certainty.
```

---

### Milestone 4: Human correction loop

* Add interrupts for Truthcore promotion and low judge scores.
* Store corrections.

Done when:

```txt
A bad response can be corrected and replayed as a better path.
```

LangGraph time-travel/forking is useful here because earlier state can be replayed or modified and later nodes rerun. ([Docs by LangChain][5])

---

### Milestone 5: Router training dataset

* Export all successful and failed traces.
* Create labelled router examples.
* Train/evaluate a small router.

Done when:

```txt
Given raw user input, router predicts compression/meta/pedagogy labels close to human choice.
```

---

## 18. Final System Principle

The system should never answer from one flattened truth layer.

It should answer from:

```txt
1. what the user is actually asking
2. what prior pathways resemble this
3. what sourced claims are relevant
4. what contradictions exist
5. what can be formalized
6. what residue remains
7. what pedagogical move fits
```

That is the engine.

Not a guru model.

Not a hallucinated graph.

Not one mega-LoRA.

A reusable conversation-path system with formal boundaries and contradiction-preserving Truthcore.

The main thing to protect: **Truthcore must remain plural, scoped, and contradiction-preserving**. A contradiction edge is often the most valuable output, not a failure.

[1]: https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com "LangGraph overview - Docs by LangChain"
[2]: https://docs.langchain.com/oss/python/langgraph/add-memory?utm_source=chatgpt.com "Memory - Docs by LangChain"
[3]: https://docs.langchain.com/oss/python/langgraph/persistence?utm_source=chatgpt.com "Persistence - Docs by LangChain"
[4]: https://docs.langchain.com/oss/python/langgraph/graph-api?utm_source=chatgpt.com "Graph API overview - Docs by LangChain"
[5]: https://docs.langchain.com/oss/python/langgraph/use-time-travel?utm_source=chatgpt.com "Use time-travel - Docs by LangChain"
