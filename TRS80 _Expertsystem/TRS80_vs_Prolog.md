# TRS‑80 Expert System vs. Prolog
## A Side‑by‑Side Comparison of Backward‑Chaining Inference

This document compares the inference model of the TRS‑80 Model I expert‑system engine
(`wc.bas`, Soll 1987 / Schröer 1989–1990) with Prolog's SLD‑resolution mechanism. The
goal is to show how the TRS‑80 engine manually re‑implements the core ideas of logic
programming using BASIC, explicit stacks, and three‑valued logic — and, just as usefully,
where it stops short of full Prolog.

**Why compare it to Prolog at all?** Prolog is used here as a *familiar reference point*
for backward‑chaining resolution, not as the program's historical source. The TRS‑80
engine descends from the expert‑system‑shell tradition (Soll's book, in the lineage of
MYCIN and rule‑based production systems), which developed largely in parallel with logic
programming rather than from it. The two arrive at the same core mechanism — goal‑driven,
recursively reduce a goal to sub‑goals, succeed when you reach known facts — from
different directions. That shared mechanism is exactly what makes the comparison
informative: it lets us name precisely what this engine is, in terms a reader already
understands, and measure where it matches Prolog and where it deliberately does not.
The comparison is therefore a *lens*, not a claim of descent.

---

## 1. Core Inference Paradigm

| Concept | TRS‑80 Engine | Prolog |
|--------|----------------|--------|
| Inference type | Backward chaining | Backward chaining (SLD resolution) |
| Starting point | Push all diagnosis rules (`TYP%=1`) as goals | Start with user query |
| Goal expansion | Evaluate rule premises 1–5 | Expand predicate body goals |
| Sub‑goals | Manual stack push (`GOSUB 3220`) | Recursive predicate calls |
| Unknown facts | Try a rule that concludes it → else **ask the user** | Try clauses → else **fail and backtrack** |
| Termination | Stack empty → diagnoses printed | Goal list empty → success |

**Summary.** The TRS‑80 engine is a hand‑built backward‑chaining resolver in the SLD
*tradition*. The key qualifier — developed in §8 — is that it does **not backtrack**: it
commits to the first resolution and gathers missing facts by asking the user, rather than
searching alternative proofs.

---

## 2. Recursion Model

| Feature | TRS‑80 Engine | Prolog |
|--------|----------------|--------|
| Recursion support | None (Level II BASIC) | Native recursion |
| Implementation | Explicit stack (`SRNR%`, `PZAEHLER%`, `STACK%`) | Implicit call stack |
| Push frame | `GOSUB 3220` | Predicate call |
| Pop frame | `STACK%=STACK%-1` | Return from predicate |
| Sub‑goal | Push the rule whose conclusion matches the needed fact | Select clause and recurse |

**Key idea.** The TRS‑80 engine *re‑implements recursion as a data structure* — two
parallel arrays acting as call frames — because the language offers no recursive
subroutines.

---

## 3. Rule Representation

| Element | TRS‑80 Engine | Prolog |
|--------|----------------|--------|
| Rule structure | Up to 5 premises + 1 conclusion | Arbitrary number of body goals |
| AND‑rules | Default (all premises must hold) | Comma: `A, B, C` |
| OR‑rules | Sentinel `"- oder -"` flips one rule to OR‑mode | Multiple clauses with the same head |
| Negation | Premise weight `WF% = -1` | `\+ Goal` (negation as failure) |
| Truth values | `+1`, `-1`, `0` (three‑valued) | true / false (two‑valued) |

**Key difference.** TRS‑80 uses **three‑valued logic** (a fact can be explicitly
*unknown*); Prolog uses **two‑valued logic plus negation‑as‑failure**, where "not proven"
is treated as false. Note also that the TRS‑80 OR is *within a single rule* (one of the
five premise slots switches the rule to OR‑mode), whereas Prolog expresses OR as several
separate clauses sharing a head.

---

## 4. Fact Acquisition

| Behavior | TRS‑80 Engine | Prolog |
|----------|----------------|--------|
| Unknown fact | Try a rule → else ask the user | Try clauses → else fail |
| User interaction | Built‑in question/dialog system | None (pure resolution) |
| Fact storage | `OSTATUS%(N%)` (per‑object status) | Static facts or dynamic `assert/1` |

**Key point.** The TRS‑80 engine is **interactive** — it acquires unknown facts from the
user during inference. Prolog resolves against a fixed (or programmatically asserted)
database and does not consult a user.

---

## 5. Constraint Propagation

| Feature | TRS‑80 Engine | Prolog |
|---------|----------------|--------|
| Constraints | `CN$(1) ⇒ CN$(2)` with forced status `CS%` | Must be encoded manually |
| Propagation | One‑directional forward propagation (line 5000) | None built in |
| Retraction | None — only fills *unknown* facts, never revises | n/a (CLP extensions add this) |

**Key point.** When a fact becomes true, the engine forces dependent facts via the
constraint table — a **lightweight forward propagation step** layered on the backward
chainer. It is *not* a truth‑maintenance system: it never retracts or revises a belief
when support is withdrawn (the routine at line 5070 only writes facts that are still
unknown). It is a one‑shot consistency aid, not dependency‑directed backtracking.

---

## 6. Explanation / Tracer System

| Feature | TRS‑80 Engine | Prolog |
|---------|----------------|--------|
| Tracer | Custom trace log (`TRACER$()`, writer at 2810) | Optional `trace/0` |
| Explanation | Human‑readable justifications (blocks 6000–8300) | Execution trace only |
| Output | Why a rule fired, why a fact holds, printout | Step‑by‑step goal trace |

**Key point.** The TRS‑80 engine includes a genuine **explanation facility** — the
*Begründungskomponente*. It logs tagged records during inference and decodes them to
explain *why* each conclusion was reached. This is the same class of feature that made
MYCIN notable, and it belongs to the expert‑system explanation tradition that prefigured
today's **Explainable AI**. Prolog's `trace/0` shows *how* execution proceeded but does
not, by itself, produce a human‑oriented justification.

---

## 7. Execution Model

| Step | TRS‑80 Engine | Prolog |
|------|----------------|--------|
| 1 | Push all diagnosis rules as goals | Start with the query |
| 2 | Pop a rule, evaluate its premises | Select a clause |
| 3 | Unknown premise → push sub‑goal | Recurse into the clause body |
| 4 | No rule yields it → ask the user | Goal fails |
| 5 | Mark the rule true / false | Success / failure (backtrack on failure) |
| 6 | Continue until the stack is empty | Continue until the goal list is empty |

---

## 8. What Prolog Has That This Engine Does Not

A fair comparison has to name the things that make Prolog *Prolog* — the features the
TRS‑80 engine does not attempt:

- **Backtracking.** Prolog's defining mechanism. On failure it returns to the most recent
  choice point and tries an alternative clause, searching the whole proof tree. The TRS‑80
  engine has **no backtracking**: it commits to the first resolution of each goal and, for
  unknown facts, asks the user instead of exploring alternatives. (A full status reset
  exists only *between* runs, at line 1000 — not during a proof.)
- **Unification.** Prolog matches goals against clause heads by unifying logic terms,
  binding variables in the process. The TRS‑80 engine does plain **string equality** on
  object names (`DANN$(K%)=OA$(N%)`); there are no variables to bind.
- **Logic variables and arbitrary terms.** Prolog reasons over compound terms of any arity
  with variables. The TRS‑80 knowledge base is fixed‑shape: named objects, up to five
  premises per rule, one conclusion.
- **A general-purpose language.** Prolog is a programming language; this is a single
  special‑purpose inference engine for one rule/question/diagnosis schema.

These are not shortcomings of the port so much as the boundary between an *expert‑system
shell* and a *logic‑programming language*. The TRS‑80 engine implements the
backward‑chaining core of the latter, without the search and unification machinery.

---

## 9. Final Summary

The TRS‑80 inference engine is a **hand‑built backward‑chaining resolver in the SLD
tradition** — with three‑valued logic, forward constraint propagation, and a full
explanation subsystem — implemented entirely in 1980s BASIC, with recursion simulated by
an explicit stack. It commits to its first resolution (no backtracking) and gathers
unknown facts interactively from the user.

It is an unusually complete and faithful implementation of expert‑system theory for the
hardware and language it runs on: not a toy, but a working teaching machine for inference
theory.
