

## One-command setup + smoke test
From project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_and_smoke_test.ps1
```

Expected:
- Conda env at `.conda` is created (or reused).
- Dependencies install.
- PCA demo runs and prints:
  - Input data summary
  - Transformed train/test shape
  - Model summary
  - Train and test Precision/Recall/F1

## Manual run of demos
From project root:

```powershell
Push-Location .\demo
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_pca_baseline.py
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_logreg_baseline.py
C:\Users\rajes\anaconda3\Scripts\conda.exe run -p ..\.conda --no-capture-output python project_iforest_baseline.py
Pop-Location
```

