# Learning Beast

A research playground for exploring **adaptive, game-inspired learning experiences**. The repository currently stores early strategy
documents that define the product direction, onboarding styles, and functional scope of the MVP.

## Repository map

| Path | Description |
| --- | --- |
| `PRV.md` | Product requirements document that defines the long-term vision, roadmap, and KPIs. |
| `onboarding_questions.md` | Narrative and gamified approaches we are evaluating for the first-time user experience. |
| `README.md` | Practical overview (this file). |

## Product vision snapshot

* Tutoring should feel like playing a lightweight game, not like following a rigid syllabus.
* A vector of user preferences (`S_u`) guides which micro-lessons ("nodos educativos") we surface.
* Micro-activities reward curiosity with immediate feedback, then inform the next recommendation.

These principles map directly to the **MVP checkpoints** listed in `PRV.md`:

1. Motor de preguntas iniciales (10–15 prompts).
2. Vector de preferencias que evoluciona tras cada respuesta.
3. Catálogo compacto de nodos educativos (3–8 min). 
4. API FastAPI mínima para sesiones, nodos y respuestas.
5. Persistencia ligera en memoria.

## Getting started

Even though there is no executable backend yet, keeping the following conventions now will save time later:

1. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt  # file coming in a future commit
   ```
2. **Follow module boundaries** outlined in the PRD: `sessions`, `nodes`, `profiles`, and `recommendations`.
3. **Write documentation-first**: when adding a new feature, sketch the intended UX or API in Markdown before shipping code.

## Decision log

| Date | Decision |
| --- | --- |
| 2025-01-08 | Consolidated strategy docs into a single repository and formalized onboarding explorations. |
| 2025-01-09 | Added this README to clarify vision, MVP checklist, and conventions for upcoming backend work. |

## Next steps

1. Convert the onboarding experiments into JSON schemas that a backend can serve dynamically.
2. Prototype the FastAPI service described in the PRD with in-memory persistence.
3. Define how rewards update the `S_u` vector (initial idea: epsilon-greedy policy with softmax weights).

## Working agreement

To keep collaboration predictable, follow this lightweight git workflow:

1. Create a feature branch off `work` for every change.
2. Commit locally with descriptive messages once the docs and code are tidy.
3. Run `git push origin <branch-name>` immediately after a successful commit so reviewers can see the update.
4. Open a PR that links back to the relevant PRD checkpoints or onboarding experiments.

---

If you are contributing, open an issue describing the learning mechanic you want to explore and how it maps back to the PRD
objectives before submitting a PR.
