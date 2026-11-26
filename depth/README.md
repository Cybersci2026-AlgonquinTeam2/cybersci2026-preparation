# depth/: the local-model trial for depth pages

Goal: find out whether a local model, shown one good seed page, can write pages that pass the deterministic gate often enough to be worth bootstrapping a LoRA. Standards: `standards/COMPREHENSIVE-STUDY-STANDARD.md`, `CURRICULUM-BLUEPRINT.md`, `ADAPTIVE-MASTERY-METHODS.md`, `DEPTH-AND-RIGOR-STANDARD.md` in `dev/credential-content-factory`. The competition backlog and sizes are in `tracker/CONTENT-BACKLOG.md` and `tracker/DEPTH-AUDIT.md`.

| Path | What |
|---|---|
| `seed/K-GEN01-shell-pipelines.md` | the one seed page (frontier-written, 4,078 words, gate passed with every lab command run) |
| `spec/K-LOG01.json` | the trial topic: focus, sample data description, lab questions, allowed tools |
| `data/make_sample.py` | deterministic sample data (`sales.csv`, `access.log`) |
| `tools/make_pack.py` | source pack = the installed tools' own `--help` text (captured, versioned) |
| `tools/gen.py` | generates a candidate one move (section) at a time through Ollama; the seed section for that move is the format example |
| `tools/gate.py` | the gate: 15 moves, figures, banned words, cards, quiz, hints, claims register, 8-word copy limit, and **runs every lab command** in a sandbox (`--fill` writes the real outputs into model-written pages) |
| `tools/trial.sh` | generate N, fill, gate, summarise |
| `tools/summary.py` | pass rate and the checks that fail most |

Run it (server or WSL): `bash depth/tools/trial.sh depth/spec/K-LOG01.json depth/seed/K-GEN01-shell-pipelines.md qwen3:8b http://127.0.0.1:11500 10 runs/log01-8b`

Honest limits: the gate proves structure, grounding in the pack, the copy limit and that lab commands run and match; it does not prove that explanations are correct or well taught. A candidate that passes is a candidate for review, never `reviewed`. Lab commands are restricted to an allow-list of text tools and run with no network.
