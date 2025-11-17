# Learning Beast Architecture Overview

This document expands on the core concepts already implemented in the MVP so that future contributors understand what each component does and how they interact.

## 1. FastAPI backend with secure session handling

The backend is structured around FastAPI and exposes endpoints for:

- **Session creation** – a `/sessions` endpoint provisions a new learning session, returns a unique `session_id`, and initializes the in-memory state needed to track the learner’s progress.
- **Conversational onboarding** – once a session exists, `/sessions/{session_id}/onboarding` presents curated questions that gather learner goals, prior knowledge, and preferred modalities. Responses are sanitized before storage to prevent code injection or log poisoning.
- **Node progression using `X-Session-Id`** – all node and micro-lesson endpoints require the `X-Session-Id` header. The backend resolves the session, validates it against the session manager, and only then delivers the next node payload so that private progress data never leaks between users.
- **Profile retrieval** – `/sessions/{session_id}/profile` aggregates sanitized answers and computed preference vectors so that clients can render a snapshot of the learner’s current state.

Every free-form response passes through the text sanitization helper before being persisted or echoed in responses, which neutralizes HTML/JS payloads when using chat-based UI surfaces.

## 2. Dedicated security helpers

Two core helpers underpin the security posture:

1. **Session token generation** – the helper produces cryptographically strong, unguessable identifiers used both for the `session_id` and the session header. Tokens are never reused and are stored only in memory, limiting exposure.
2. **HTML-escaped input** – a utility wraps Python’s `html.escape` to normalize whitespace, strip control characters, and escape HTML entities. This guarantees that any user-authored text rendered later in the UI cannot execute scripts.

These helpers are imported wherever user data is accepted, ensuring that new endpoints automatically benefit from the same protections.

## 3. Adaptive session manager

The in-memory session manager performs several coordinated tasks:

- **Answer logging** – sanitized onboarding or lesson answers are appended to a chronological log along with timestamps so we can analyze how preferences evolve during a session.
- **Preference vector updates** – after each response, heuristics update a lightweight vector (e.g., format preference, difficulty tolerance, pacing). This enables adaptive sequencing without heavyweight ML infrastructure.
- **Learning node sequencing** – the manager tracks which node (question, micro-lesson, or exercise) should be served next. It guarantees that nodes are delivered in a safe order, avoids repetition, and prevents clients from requesting arbitrary content out of sequence.
- **Timeout + cleanup hooks** – sessions that have been idle beyond a configurable threshold are purged, freeing memory and invalidating stale tokens.

Although the store is currently in-memory for MVP simplicity, the abstraction makes it straightforward to swap in a persistent backend later.

## 4. Curated conversational datasets and refreshed documentation

- **Onboarding question set** – a curated list of conversational prompts helps the system capture learner motivations, habits, and blockers in a friendly tone. Each question is tagged with metadata so the UI can render hints or fallback choices.
- **Micro-lesson catalog** – a lightweight dataset maps each learning node to the skills it reinforces, prerequisites, and suggested follow-up content. This data drives the adaptive sequencing logic inside the session manager.
- **Documentation + dependency pins** – the README and supporting docs describe how to run the FastAPI server, outline the security posture (session tokens, sanitization, HTTP headers), and pin critical dependencies for reproducible installs. Contributors can follow the documented flow to bootstrap local development quickly.

Together, these components deliver a privacy-aware onboarding flow, resilient session handling, and a curated learning experience suited for early product validation while leaving room for future scaling.
