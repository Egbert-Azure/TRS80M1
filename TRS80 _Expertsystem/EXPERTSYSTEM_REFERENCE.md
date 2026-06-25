# Expert system — one-page reference

An **educational expert system** for the TRS-80 Model I — built to *teach* how an
expert system works, demonstrating the **recursive BASIC technique** for an inference
engine. Original concept by Dr. H.-J. Soll (1987); ported and extended for the TRS-80
Model I by Egbert Schröer (1989–1990).

It is **not** an advisor product. The radio-repair knowledge base (`testen`) is only a
sample domain to show the method working — the actual subject of the program is the
inference mechanism itself.

## What the whole thing is

The system has two halves that share a data file:

- An **editor** builds a *knowledge base* (objects, questions, rules, constraints) and
  saves it to disk.
- An **inference engine** loads that knowledge base, asks the user questions, and uses
  **backward chaining** to confirm one or more diagnoses.

### The inference type: backward only

The engine `w.bas` is a **pure backward-chaining (goal-driven) inference engine**. It is
*not* forward-chaining and not hybrid. Evidence from the code:

- It seeds the stack with **only the diagnosis rules** (`IF TYP%(N%)=1`, line 1130) —
  it starts from the goals it wants to prove, not from known data.
- When it needs an unknown fact, it looks for another rule that *concludes* that fact
  and proves that rule first as a sub-goal (line 3030); only if no rule yields it does
  it ask the user (line 3050).
- There is **no forward sweep** — no loop firing every applicable rule from known facts.
  The constraint routine (the one mildly forward element) lives only in the editors and
  is absent from `w.bas`.

### The recursive BASIC technique (the point of the exercise)

Soll's teaching idea was to express backward chaining as **recursion**: to prove a goal,
the routine calls itself on each sub-goal. The TRS-80 Model I's Level II BASIC has no
user-defined recursive subroutines, so this port re-implements that recursion with an
**explicit manual stack**:

- `SRNR%(STACK%)` — which rule this stack frame is working on
- `PZAEHLER%(STACK%)` — which premise (1–5) of that rule is being checked
- `STACK%` — the current depth; `MSTACK%=100` is the limit

Mechanics: lines 3220–3250 **push** a frame, line 2030 **pops** one, and line 3030 is
the recursive heart — when a premise's object is itself the conclusion of another rule,
that rule is pushed and worked first (a sub-goal interrupting the current goal), exactly
as a recursive call would behave. The technique is preserved; only its *implementation*
changed from language-recursion to a hand-rolled stack, because the hardware forced it.

## The files — what is latest

| File | Role | Status |
|------|------|--------|
| `w.bas` | Inference engine (`'Expertensystem / Inferenzkomponente`, 1990). Source of the compiled `WC/CMD`. | **Current — the engine you run** |
| `wbedit.bas` | Knowledge-base editor (`'Wissenserwerbskomponente`, 1989). Full-screen input mask; both save-bugs already fixed. | **Current — the editor you use** |
| `maskgen.bas` | Generates the input-mask screens used by `wbedit`. | Current — build-time tool |
| `maske1.dum`, `maske2.dum` | Saved screen images of the question form and rule form. | Current — data for `wbedit` |
| `testen` | A complete knowledge base: the radio-repair rule set. | Current — sample/working KB |
| `wedit.bas`, `fremedit.bas` | Older editor versions. Inline (line-by-line) input instead of the mask; still contain two save-bugs. | Superseded |
| `druck.bas` | A 3-line `LPRINT` printer fragment, not a standalone program. | Fragment |
| `WC/CMD` | Compiled binary of `w.bas`. Runs without BASIC; this is what the startup screenshots show. | Current — compiled engine |

Newest working pair: **`wbedit.bas` (edit) + `w.bas` / `WC/CMD` (consult)**.

## Dependencies

- `wbedit.bas` → loads `maske1/dum` and `maske2/dum` at runtime via `CMD"load …"`
  (lines 4010 and 7010). Those `.dum` files are produced by `maskgen.bas`. Without
  them, `wbedit` cannot draw its entry forms.
- `w.bas` / `WC/CMD` → needs a **knowledge-base file** (e.g. `testen`), entered at the
  `Name der Wissensbasis` prompt. No knowledge base = nothing to reason over.
- `wedit.bas` / `fremedit.bas` → self-contained (inline mask), need only a KB file.
- `w.bas` reads only objects, questions, and rules from the KB; it reads the constraint
  and entry-question counts but **does not load or apply them**. Constraints are an
  editor-side feature.

## How the editor captures input (the "Maske" difference)

- `wbedit.bas` (latest): loads a pre-drawn full-screen form (`maske*/dum`), lets you
  fill in the fields, then reads your answers back out of video memory with `PEEK`
  (line 4140 onward). This is the improved input mask.
- `wedit.bas` / `fremedit.bas` (older): just `PRINT` the field labels and collect
  answers with sequential `INPUT` statements — no external mask.

## Knowledge-base file format (sequential ASCII)

Header: `OBJEKTE%`, `FRAGEN%`, `REGELN%`, `CO%` (constraints), `NQ%` (entry questions).
Then, in order:

- per **object**: name `OA$`, status `OSTATUS%` (0/±1), diagnosis flag `ODIAG%`
- per **question**: text `FTEXT$`, answer 1 `FA$(1)`, answer 2 `FA$(2)`, status
  `FSTATUS%`, bound object `FOBJEKT$`
- per **rule**: `RSTATUS%`, then 5×(premise `WENN$`, weight `WF%`), conclusion `DANN$`,
  diagnosis flag `TYP%`
- per **constraint**: antecedent `CN$(1)`, consequent `CN$(2)`, forced status `CS%`
- per **entry question**: object `QU$`

Status codes: `0` unknown, `+1` true, `-1` false. Rule weight `WF%`: `+1` normal,
`-1` negated. An OR-rule is marked by the sentinel `"- oder -"` in premise slot 1.

## What is in `testen` (the sample knowledge base)

`testen` is the demonstration knowledge base — a radio-fault example used to show the
inference engine reasoning over a real rule set. It is sample teaching content, not the
purpose of the program.

35 objects, 13 questions, 16 rules, 5 constraints, 4 entry questions.

Sample questions in it: does the reception indicator deflect on a tuned station; is
music or speech audible; is there hiss at full volume; does the sound seem dull;
reception quality on medium-wave and on FM; is anything audible through headphones;
crackling when turning the volume; volume only ever quiet; can weak stations be
received; are the batteries full.

Sample diagnoses (objects flagged as diagnosis): pre-amplifier defective; tone control
mis-set (no treble); antenna defective; speaker or output stage defective; batteries
empty; no battery contact; batteries exhausted; interference from electrical devices;
poor local reception location; range-selector switch oxidised; volume control dirty.

A session demonstrates the technique: the learner answers a few yes/no questions, and
the engine works backward from each candidate goal — asking only the questions a goal
needs, recursing into sub-rules via the manual stack — until it confirms the goal(s)
the evidence supports.
