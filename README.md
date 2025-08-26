# Algorithme.ai — BlackSwanClassifier 🦢 (Library API)

Predictive modeling toolkit that talks to Algorithme.ai’s hosted engine through a thin Python client. This repository includes a minimal Python package (`algorithmeai`) and a **quickstart** showing how to build, evaluate, improve, and export a model using CSV files.

> **Heads‑up (privacy/IO):** Most calls send your CSV content or individual items to a hosted API (AWS Lambda) and receive results back. **Do not** send sensitive or personally identifiable data unless you have approval to do so and the data is anonymized.

---

## Contents

```
BlackSwanClassifier/
├─ algorithmeai/                 # Python client package
│  ├─ __init__.py
│  └─ algorithmeai.py            # BlackSwanClassifier client
├─ quickstart/
│  ├─ quickstart.ipynb           # End-to-end example
│  ├─ train.csv                  # Example training set (binary target in col 0)
│  ├─ backtest.csv               # Example evaluation set
│  └─ blackswan-api.json         # Example saved model handle (hash + log)
├─ pyproject.toml
└─ algorithmeai.egg-info/
```

---

## Installation

You can install the package locally in editable mode. The client depends on `requests`.

```bash
# from the repo root (this folder)
pip install algorithmeai
pip install requests  # if not already present
```

Python 3.8+ recommended.

---

## Quickstart (from `quickstart/quickstart.ipynb`)

Below mirrors the notebook and covers the main workflow:

```python
from algorithmeai import BlackSwanClassifier

# 1) Build a remote model from a CSV (target is at index 0 by default)
model = BlackSwanClassifier("quickstart/train.csv", target_index=0)

# 2) Rehydrate/ping an existing remote model by its 64-char hash
new_model = BlackSwanClassifier("bc0ad6c0d46f32551bda63fb70e6186bdad6cb66bd39958d40a99beee4ae5bde")

# 3) Evaluate AUC on a backtest set
auc = new_model.get_auc("quickstart/backtest.csv")

# 4) Optimize the model (server-side)
new_model.improvePrecision()   # bias toward precision
new_model.improveRecall()      # bias toward recall
new_model.improve()            # balanced improvement

# 5) Re-evaluate
auc = new_model.get_auc("quickstart/backtest.csv")

# 6) Find the optimal threshold and its AUC
auc, opt = new_model.get_auc_opt("quickstart/backtest.csv")

# 7) Inspect global feature importance on a dataset
gfi = new_model.get_global_feature_importance("quickstart/backtest.csv")

# 8) Get per-row confidence scores and filter indexes above a threshold
conf = new_model.get_confidence("quickstart/backtest.csv")
idx = new_model.filter("quickstart/backtest.csv", opt)  # opt from step 6

# 9) Work with a "population" of sample items for item-level exploration
population = new_model.make_population("quickstart/backtest.csv")
item = population[0]  # pick one item

# Item-level introspection
fi_item = new_model.get_feature_importance(item)   # feature contributions for this item
conf_item = new_model.get_item_confidence(item)    # confidence for this item
audit = new_model.get_audit(item)                  # returns a dictionary audit with lookalikes csv confidence and feature importance for this item

# 10) Export a portable handle and re-load later
new_model.to_json("quickstart/blackswan-api.json")
final_model = BlackSwanClassifier("quickstart/blackswan-api.json")
print(final_model.log)  # server log / trace from last call
```

> **Notes:**
> - Most methods update both `self.hash` (the remote model handle) and `self.log` (a textual server log).

---

## Data format

- **CSV files** with a header row.
- **Binary target** column by default at **index 0** (`0/1`). You can choose a different target via the `target_index` argument.
- Other columns are treated as **features**. Numeric floats/ints are supported; 0/1 columns work as booleans.
- You can exclude features by their positional index: `excluded_features_index=[...]` when constructing the classifier.

Example (from `quickstart/train.csv` and `backtest.csv`):

```
Diagnosis,Age,Gender,BMI,Smoking,GeneticRisk,PhysicalActivity,AlcoholIntake,CancerHistory
1,58,1,16.0853,0,1,8.1463,4.1482,1
0,71,0,30.8288,0,1,9.3616,3.1983,0
...
```

---

## Python API

All calls below contact the hosted service and may take time depending on data size and network.

### Constructor
```python
BlackSwanClassifier(filepath, target_index=0, excluded_features_index=[])
```
- **`filepath`** accepts one of:
  - Path to a **CSV file** → builds/initializes a remote model.
  - A **64-character hash** string → attaches to an existing remote model.
  - Path to a **JSON file** created by `to_json` → reloads a saved handle.
- Side-effects: sets/updates `.hash` and `.log`.

### Model lifecycle
- `improve()` → server-side balanced improvement; updates `.hash`, `.log`.
- `improvePrecision()` → bias toward precision; updates `.hash`, `.log`.
- `improveRecall()` → bias toward recall; updates `.hash`, `.log`.

### Evaluation
- `get_auc(csv_path) -> float`  
  Returns AUC on the provided dataset.
- `get_auc_opt(csv_path) -> (float auc, float opt)`  
  Returns the AUC and the optimal decision threshold used to achieve it.

### Introspection (dataset-level)
- `get_global_feature_importance(csv_path) -> dict[str, float]`  
  Global feature importance computed over the given dataset.
- `get_confidence(csv_path) -> dict[int, float]`  
  Per-row confidence (keyed by row index).
- `filter(csv_path, opt=0.5) -> list[int]`  
  Convenience wrapper that returns indexes whose confidence ≥ `opt`.

### Introspection (item-level)
- `make_population(csv_path) -> list[item]`  
  Returns a collection of item payloads suitable for per-item analysis.
- `get_feature_importance(item) -> dict[str, float]`  
  Feature contributions for a specific item.
- `get_item_confidence(item) -> float`  
  Confidence for a specific item.
- `get_audit(item) -> None`  
  Retrieves and logs an audit trail for the item (printed, and appended to `self.log`).

### Persistence
- `to_json(fileout="blackswan-api.json") -> None`  
  Writes a minimal JSON with the current `hash` and `log`. You can later rehydrate with `BlackSwanClassifier(fileout)`.

---

## Networking, privacy & security

- The client sends your CSV text and/or item payloads to a hosted endpoint (AWS Lambda) and receives JSON responses.
- **Do not** include PII or sensitive data unless it is anonymized and you have permission to process it off-device.
- Keep your `blackswan-api.json` and model **hash** private if your project requires access control—possession of the hash re-attaches to the remote model.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'requests'`**  
  Install it: `pip install requests`.

- **Network/HTTP errors (non-200, timeouts):**  
  Check connectivity, retry, and inspect `print` output and `final_model.log` for server-side messages.

- **Unexpected results / wrong target column:**  
  Make sure the target is 0/1 and pass the correct `target_index` when building the model.

- **CSV parsing issues:**  
  Ensure UTF-8 encoding and a single header row. Avoid stray commas/quotes.

---

## Development

- Code style is simple and dependency-light. Contributions that improve robustness (typing, retries, docstrings) are welcome.
- Before opening PRs that change network protocols or add telemetry, please open an issue to discuss.

---

## License

MIT Licence. Assume **all rights reserved** © Algorithme.ai / Charles Dana (2025). For commercial use, contact the author.

---

## Contact

- Author: **Charles Dana** — <charles@algorithme.ai>
- Product: **BlackSwanClassifier** (Algorithme.ai)

