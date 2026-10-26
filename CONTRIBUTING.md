# Contributing to Motion Pilot

Thanks for considering a contribution to Motion Pilot, created and maintained by Taiwo David Dayomola.

Motion Pilot is a steering document as much as it is code: every sentence in `SKILL.md` and `references/` changes what an agent makes. Changes are judged on whether they make the work measurably better, so taste, precision and evidence matter more than volume. Opening a pull request does not imply that it will be merged.

## What helps most

- **Genre playbooks** for kinds of piece the skill does not cover yet, written as numbers and decisions rather than adjectives.
- **References with analysis**: a film you can share the rights to, run through `scripts/analyze_reference.py`, with the grammar written down and what you measured marked apart from what you judged.
- **Lessons**: a correction that turned a draft into approved work, in the format of `references/taste/lessons.md`.
- **Engine components and scripts** that keep every frame a pure function of time.
- **Fixes** to anything that is wrong, unclear or out of date.

## Before you start

For a fix with a clear reproduction, open an issue or go straight to a pull request. For a new playbook, a change to `SKILL.md`, a new dependency or a change to the engine's contract, open an issue first so the approach can be discussed.

## Fork workflow

1. Fork `Tee-David/Motion-Pilot` into your own GitHub account.
2. Clone your fork and create a focused branch from the latest `main`.
3. Make one coherent change.
4. Run the checks below.
5. Push to your fork and open a pull request against `main`.

## Checks

```bash
python -m py_compile skills/motion-pilot/scripts/*.py
node --check skills/motion-pilot/engine/*.js skills/motion-pilot/templates/*.js
python .github/scripts/check_skill.py
```

If your change affects rendering, render a short piece and run `scripts/qc.py` and `scripts/review.py` on it, and say in the pull request what you measured.

## Writing rules

- Numbers over adjectives. "Arrivals on `cubic-bezier(.16,1,.3,1)` over 400 ms", not "smooth arrivals".
- Plain, specific sentences. Sentence case. No marketing language.
- Name no product, brand or person as the source of an idea unless it is a reference in the style library with analysis.
- Keep `SKILL.md` short; depth belongs in `references/`.
- No invented numbers, clients or testimonials anywhere, including examples.

## Rights

Only submit material you have the right to share. Do not commit contact sheets or frames of third-party films; describe them in writing instead. Fonts must be under an open licence with the licence text included.

## Pull request bar

Focused, explained, checked, and documented where behaviour changes. Maintainers may request changes or decline contributions that do not fit the project's direction.
