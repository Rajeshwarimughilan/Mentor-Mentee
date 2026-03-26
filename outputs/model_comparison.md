# Model Comparison Report

Sorted by `security_score` (higher is better).

| rank | model | precision | recall | f1 | security_score | tp | fp | tn | fn | fit_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DecisionTree | 0.9853 | 0.4268 | 0.5956 | 53.32 | 67 | 1 | 3813 | 90 | 0.0018 |
| 2 | IsolationForest | 0.9853 | 0.4268 | 0.5956 | 53.32 | 67 | 1 | 3813 | 90 | 0.1231 |
| 3 | PCA | 0.9661 | 0.3631 | 0.5278 | 47.28 | 57 | 2 | 3812 | 100 | 0.0008 |
| 4 | LR | 1.0 | 0.2357 | 0.3814 | 35.58 | 37 | 0 | 3814 | 120 | 0.0341 |
| 5 | SVM | 1.0 | 0.2357 | 0.3814 | 35.58 | 37 | 0 | 3814 | 120 | 0.0041 |
