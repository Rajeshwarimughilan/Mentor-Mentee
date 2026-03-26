# Final Review Execution Plan

## Ground Rules
- Keep academic integrity: explain what you changed and why.
- Focus on reproducibility: every claim must map to a runnable command.
- Prepare to answer both ML and security angle questions.

## Phase 1: Environment Readiness (30-45 min)
- Objective: make the project run reliably on your laptop.
- Command:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_and_smoke_test.ps1
```

- Expected outcome: dependencies install and `project_pca_baseline.py` completes with precision/recall/F1 output.

## Phase 2: Baseline Verification (45-60 min)
- Objective: verify at least 3 models run end-to-end.
- Commands:

```powershell
Push-Location .\demo
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_pca_baseline.py
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_logreg_baseline.py
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_iforest_baseline.py
Pop-Location
```

- Deliverable: screenshot or saved logs of each run.

## Phase 3: Personal Contribution (2-4 hours)
- Objective: add genuine, explainable improvements.
- Suggested items:
  - Add one evaluation script that compares model metrics in a single table.
  - Add a short threat-model note: log poisoning, concept drift, false positive handling.
  - Add one robustness test: shuffled labels or noisy windows to show failure boundaries.

## Phase 4: Review Narrative (60-90 min)
- Objective: build a confident story for viva.
- Slide flow:
  1. Problem statement and why log anomaly detection matters.
  2. Pipeline: parsing -> feature extraction -> model -> evaluation.
  3. Results: precision/recall trade-offs across models.
  4. Security relevance: detection limits, adversarial concerns.
  5. Future work: online adaptation, drift detection, model monitoring.

## Phase 5: Demo Day Checklist (15 min)
- Re-run one model before leaving.
- Keep terminal command history visible.
- Keep dataset paths ready.
- Keep one backup demo script (`project_pca_baseline.py`) as fallback.

## Current Status (as of 2026-03-26)
- Dependency issue fixed in `requirements.txt` (`sklearn` -> `scikit-learn`).
- Renamed primary demo entry files and kept compatibility launchers for original names.
