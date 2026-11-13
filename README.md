# Lab Practical Programs — Big Data Analytics (9) + Machine Learning (10)

All 19 experiments from the two lab manuals, converted to runnable **Python scripts** and **Jupyter notebooks**
(same program logic in both — the code in the scripts and the notebooks is identical and contains no `#` comments; the notebook headings/aims are stored in `tools/notebook_cells/` and assembled by `tools/build_notebooks.py`).

```
Lab-Practical-Programs/
├── README.md   requirements.txt   requirements-dev.txt   .gitignore
├── tools/                     build_notebooks.py  ·  run_all_checks.py
├── Machine_Learning/          Machine_Learning.ipynb · Experiment_01.py … Experiment_10.py · download_heart.py · datasets/
└── Big_Data_Analytics/        Big_Data_Analytics.ipynb · Experiment_01.py … Experiment_09.py · bda_common.py
                               mapper.py reducer.py (Exp 6) · Experiment_04.js Experiment_05.js (Mongo shell)
                               Experiment_09_mapper.py Experiment_09_hadoop_streaming.sh · Experiment_02_Hadoop/ · datasets/
```

## ⚠️ Read this first — what is and is not verified

This project was built and tested in a Linux sandbox that has **no MongoDB, no Hadoop, and no access to UCI/Kaggle**.
Everything below is what was *actually executed*; nothing is claimed beyond that.

| # | Experiment | Status | Details |
|---|---|---|---|
| **ML 1** | FIND-S | ✅ run, output identical to manual | |
| **ML 2** | Candidate-Elimination | ✅ run, output identical | final S and G match |
| **ML 3** | ID3 decision tree | ✅ run, matches manual | same tree and the same two labels (`no`, `yes`). **Dataset not in the PDF** — see *Datasets* |
| **ML 4** | Back-propagation ANN | ✅ run, close not identical | predictions ≈ 0.89 / 0.88 / 0.89 vs manual 0.897 / 0.872 / 0.900: the manual's random initial weights were unseeded, so exact digits cannot be reproduced |
| **ML 5** | Naïve Bayes (from scratch) | ✅ run, identical | `71.65354330708661 %`, 514 train / 254 test (seed 11 — see notes) |
| **ML 6** | Naïve Bayes text | ✅ run, metrics identical | accuracy 0.8, matrix `[[2,1],[0,2]]`, precision 0.6667, recall 1.0 — but see *Notes* (the manual's token list can't come from the same run) |
| **ML 7** | Bayesian network (heart) | ⚠️ **code tested, not run on real data** | needs `heart.csv` (Cleveland). Code was run only on a *synthetic stand-in* to prove it works with current pgmpy. Run `python download_heart.py` (needs internet) then the experiment |
| **ML 8** | k-Means vs EM | ✅ run | k-Means identical (0.24, same matrix). EM: same grouping as the manual (setosa pure, 45/5 split, 50 virginica) but cluster *numbers* differ (random start), so accuracy prints 0.333 instead of 0.367 |
| **ML 9** | k-NN iris | ✅ run, identical | matrix and report match (seed 497); correct *and* wrong predictions are printed |
| **ML 10** | Locally weighted regression | ✅ run, plots visually checked | four panels tau = 10, 1, 0.1, 0.01 match the manual's figure |
| **BDA 1** | Python / NumPy / pandas | ⚠️ run on **synthetic sample** | your real `crime.csv` was not available — see *Datasets* |
| **BDA 2** | Hadoop & HDFS | ⚠️ **procedure + verification script; Hadoop NOT installed/run here** | the check script ran and correctly reports "not installed" (13 FAIL). Install by hand, then re-run it |
| **BDA 3** | Plotting | ⚠️ run on **synthetic sample** | all 8 figures generated; 2 inspected visually |
| **BDA 4** | MongoDB CRUD & arrays | ⚠️ **never run on a real MongoDB** | run against an in-memory emulator (mongomock): CRUD + array steps 1–5 OK; steps 6–7 (`$[]`, `arrayFilters`) are **unverified** (emulator lacks them) |
| **BDA 5** | MongoDB count/sort/limit/skip/aggregate | ⚠️ **never run on a real MongoDB** | emulator results cross-checked against an independent pure-Python calculation |
| **BDA 6** | MapReduce word count | ✅ run, identical | all 27 counts printed in the manual reproduced; the `mapper.py | sort | reducer.py` pipeline also run |
| **BDA 7** | MapReduce on wine data | ✅ run on real wine data | matches an independent pandas calculation. **Manual's numbers (~0.50 per class) came from random dummy data**, so real data gives different (correct) numbers |
| **BDA 8** | Spark K-Means | ✅ run (local mode, PySpark 4.3, Java 21) | works; the manual's printed numbers were illustrative and can't come from its program (WSSSE 180 vs ≈ 558 for that data) |
| **BDA 9** | Store big data in MongoDB via Hadoop | ⚠️ **partly** | mapper run for real; storing into MongoDB only tested against the emulator; the **Hadoop job script is untested** |

**Test backend:** `LAB_USE_MONGOMOCK=1` swaps MongoDB for the in-memory `mongomock` library and prints a loud banner.
It exists only so the Python logic could be tested without a server. **For your practical, run a real MongoDB** — without one the
scripts stop with start-up instructions instead of pretending.

**About the notebooks:** they were executed top to bottom (Run All, 0 errors) in the sandbox, so their stored outputs reflect
those conditions: BDA 1/3 show the *synthetic sample* banner, BDA 4/5/9 show the *mongomock* banner, ML 7 shows the
"heart.csv not available" message, BDA 2 shows its FAIL list. **Re-run them on your own machine** (Run All) to get real outputs.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Machine Learning
cd Machine_Learning
python download_heart.py            # once, needs internet (only for ML Exp 7)
python Experiment_01.py             # …  or:  jupyter notebook Machine_Learning.ipynb   → Run All

# Big Data Analytics
cd ../Big_Data_Analytics
python Experiment_06.py             # …  or:  jupyter notebook Big_Data_Analytics.ipynb → Run All
```
* Open each notebook **from its own folder** (it finds `datasets/` relative to the notebook).
* Scripts can be run from any directory (IDE "Run" button, VS Code, PyCharm, IDLE). Matplotlib windows must be closed to continue; every figure is also saved to `outputs/`.
* ML Exp 10 writes `outputs/ml_ex10_lwr.html` and opens it in the browser (inside Jupyter the plots appear inline).
* `python tools/run_all_checks.py` runs all 19 scripts and shows exit codes (0 = fine, 2 = a required service/dataset is missing and the script said so, 1 = Hadoop check failed).

## Datasets — where each came from

| File | Used by | Source / status |
|---|---|---|
| `ML/datasets/enjoysport.csv` | ML 1, 2 | **Recreated from the table printed in the PDF** (4 rows) |
| `ML/datasets/data3.csv`, `data3_test.csv` | ML 3 | **Not in the PDF.** `data3.csv` is the standard 14-row Play-Tennis table (Mitchell); it reproduces the manual's tree and both test labels. The two test rows are copied from the manual's output |
| `ML/datasets/naivedata.csv` | ML 5 | Pima Indians Diabetes, 768 rows, no header (a GitHub mirror of the UCI data). Row count matches the manual's output |
| `ML/datasets/naivetext.csv` | ML 6 | **All 18 sentences + labels are printed in the PDF output**; recreated from it |
| `ML/datasets/8-dataset.csv` | ML 8 | UCI **Iris** `iris.data`, 150 rows, no header, `Iris-*` labels (GitHub mirror). Rows 35 and 38 are the UCI originals, which differ slightly from scikit-learn's corrected copy |
| ML 9 data | ML 9 | `sklearn.datasets.load_iris()` — as in the manual |
| **`ML/datasets/heart.csv`** | ML 7 | ❌ **Not shipped.** The manual needs the UCI *Cleveland* file (303 rows, `?` for missing, target 0–4). `python download_heart.py` fetches `processed.cleveland.data` from UCI and writes `heart.csv` in the right layout. (The widely-circulated Kaggle `heart.csv` is a *different* encoding and will not reproduce the manual's tables.) |
| `BDA/datasets/data.csv` | BDA 7 | UCI **Wine Quality (red)**, 1599 rows, `;`-separated (GitHub mirror) |
| `BDA/datasets/data.txt` | BDA 6 | **Reconstructed from the screenshot in the manual**; the 27 counts the manual prints are reproduced exactly from it |
| `BDA/datasets/transactions.csv` | BDA 9 | 10-row sample; rows 1–2 are the two printed in the manual, the rest are illustrative (the manual's "large CSV" is hypothetical) |
| ❌ **`BDA/datasets/crime.csv`** | BDA 1, 3 | **Not available and not recoverable from the PDF.** The manual uses one file name for two *different* tables: Exp 1's printed output is an India crime table (*Report Number, City, Crime Code, …, Police Deployed*, ~40 000 rows) but its code uses `Robbery`/`Murder` columns that table does not have; Exp 3 plots *Year, Population, Murder, Assault, Robbery, CarTheft*. **Put your lab's file(s) in `Big_Data_Analytics/datasets/`.** Exp 3 looks for `crime.csv`, then `crime_ex3.csv`, then `crime_plots.csv` (first one that has the needed columns); Exp 1 uses `crime.csv`. Until then the programs fall back to **synthetic** `SAMPLE_*.csv` files (made by `make_sample_crime.py`) and print a banner saying so |

## Setting up the external software

### Python / Anaconda (BDA Exp 1)
The manual installs *Anaconda 2019.10 (Python 3.7)* through the graphical installer: download it from anaconda.com → *Just Me* → default folder →
leave "Add to PATH" unticked, tick "Register as default Python" → Install → open **Anaconda Navigator** → launch **Jupyter Notebook**.
Today's Anaconda ships a newer Python (3.12/3.13); the programs here work on it. Check your set-up with `python -c "import numpy, pandas; print(numpy.__version__, pandas.__version__)"`.

### MongoDB (BDA 4, 5, 9) — a running server is required
```bash
# easiest, any OS with Docker:
docker run -d --name mongo -p 27017:27017 mongo:7
# Windows: install "MongoDB Community Server" (mongodb.com/try/download/community) with "Run as a Service", also install mongosh
# Ubuntu : follow https://www.mongodb.com/docs/manual/administration/install-on-linux/  then   sudo systemctl start mongod
# macOS  : brew tap mongodb/brew && brew install mongodb-community && brew services start mongodb-community
mongosh --eval "db.runCommand({ping:1})"        # prints { ok: 1 }
```
Then `python Experiment_04.py` (or `mongosh Experiment_04.js`). A different server: set `MONGODB_URI`.

### Spark (BDA 8)
```bash
# Java 17 or newer is required by PySpark 4.x   (JDK 8/11/17 for PySpark 3.x)
winget install EclipseAdoptium.Temurin.17.JDK         # Windows;   Linux: sudo apt install openjdk-17-jdk
java -version
pip install pyspark
python Experiment_08.py          # starts Spark in local mode inside the script - no service to start
```
First start takes ~20–40 s. On Windows, if Spark complains about `winutils`/`HADOOP_HOME`, see the Hadoop notes below.

### Hadoop & HDFS (BDA 2, and 9's job script)
Follow **`Big_Data_Analytics/Experiment_02_Hadoop/INSTALL_HADOOP.md`** — it keeps the manual's Windows procedure step by step, with the four XML
config files ready to copy. Then verify with `python Experiment_02.py`. Things the manual leaves out: it says "download this GitHub repo's `bin`
folder" but **the link is not in the PDF** (you need `winutils.exe`/`hadoop.dll` built for Hadoop 2.9.x), and the `hdfs-site.xml` paths in its text
(`C:\hadoop\data\…`) disagree with its screenshots (`D:\…\hadoop-2.9.2\data\…`) — use the folders you actually created. `yarn-site.xml` keeps the manual's property name and also adds the standard `yarn.nodemanager.aux-services.mapreduce_shuffle.class` (the manual's name looks like a PDF line-break dropped a dot).

## Differences from the manuals (and why)
* **Modern libraries:** `BayesianModel`→`DiscreteBayesianNetwork`/`DiscreteMLE` (ML 7, old API still supported); Bokeh `plot_width/height`→`width/height` (ML 10); seaborn keyword arguments `x=`, `y=` (BDA 3); pandas `numeric_only=True` for `skew/var/kurtosis` (BDA 1); `display()` (Jupyter-only)→`print()`.
* **Bugs fixed:** `EO = youtput` → `y - output` (ML 4); missing newline after `if len(set(lastcol)) == 1:` and `set()` iteration order made branches print in random order → `sorted()` (ML 3); `open('shuffled.pkl','ab')` appended on every run so the reducer read stale data → `'wb'` (BDA 7); ML 1 skips the CSV header row.
* **Seeds** are fixed (the manual's runs were unseeded): ML 4 → 42, ML 5 → 11, ML 6 → 81, ML 8 uses `n_init=10` (the older scikit-learn default), ML 9 → 497, ML 10 → 42, BDA 8 → 42. Seeds 11 / 81 / 497 were chosen because they give the exact figures the manual printed; any other seed is equally valid and gives slightly different numbers. They are plain constants in each file (`SEED` / `RANDOM_STATE`).
* **ML 6:** the manual's code says `test_size=0.3` but its output shows 13 train / 5 test rows (that is 0.25), and its printed 45-token vocabulary belongs to a *different* split than its printed accuracy/matrix (the only split that gives that vocabulary yields matrix `[[2,2],[0,1]]`). It cannot be reproduced as a single run; the code uses 0.25 with the seed that reproduces the metrics. Change `TEST_SIZE` / `RANDOM_STATE` to 0.3 to follow the printed code instead.
* **BDA 4:** the manual's snippets contain errors (`update` without braces, undefined `NEW_CONTENT`, a hard-coded `ObjectId` that exists only on the author's machine, a step-6 snippet missing its first line, and a step-7 filter that can't match after step 6). Corrected versions are in `Experiment_04.py/.js`. The "Output" shown in the manual for Exp 4 and Exp 5 are screenshots of unrelated things (a Python CSP program, and MongoDB server-log documents), so there is nothing to compare.
* **BDA 6:** the manual's program splits on whitespace only, but its printed counts need punctuation removed — added. `mapper.py` / `reducer.py` are referred to but not printed; standard versions are provided.
* **BDA 9:** the manual's Hadoop command is cut off in the PDF and not a valid streaming command; the output shown is an illustrative log. `Experiment_09_hadoop_streaming.sh` is a best-effort version, **untested**.

## Rebuilding the notebooks
If you edit a script, make the same edit in the matching `tools/notebook_cells/<suite>/Experiment_XX.json` code cell, otherwise the builder stops with a mismatch message.

```bash
pip install -r requirements-dev.txt
python tools/build_notebooks.py              # regenerate both .ipynb (checks the scripts still match tools/notebook_cells/)
python tools/build_notebooks.py --execute    # …and run them, storing the outputs
```
