import numpy as np
import pandas as pd
from pathlib import Path

from pgmpy.inference import VariableElimination

try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianModel
    from pgmpy.parameter_estimator import DiscreteMLE
    MLE_ESTIMATOR = DiscreteMLE()
except ImportError:
    from pgmpy.models import BayesianModel
    from pgmpy.estimators import MaximumLikelihoodEstimator
    MLE_ESTIMATOR = MaximumLikelihoodEstimator

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "datasets"
HEART_CSV = DATA_DIR / "heart.csv"

def load_heart():
    """Return the Cleveland data frame, or None (after printing instructions) if it cannot be obtained."""
    if not HEART_CSV.exists():
        import sys
        sys.path.insert(0, str(BASE_DIR))
        from download_heart import download_heart_csv
        try:
            download_heart_csv(HEART_CSV)
        except Exception as exc:
            print(f"Could not obtain datasets/heart.csv automatically ({type(exc).__name__}: {exc}).")
            print("Download  processed.cleveland.data  from the UCI repository (URL in download_heart.py),")
            print("or run  python download_heart.py  on a machine with internet, and put heart.csv in datasets/.")
            return None
    return pd.read_csv(HEART_CSV).replace('?', np.nan)


heartDisease = load_heart()

if heartDisease is not None:
    print('Few examples from the dataset are given below')
    print(heartDisease.head())

    print('\n Attributes and datatypes')
    print(heartDisease.dtypes)

if heartDisease is not None:
    model = BayesianModel([('age', 'heartdisease'), ('sex', 'heartdisease'),
                           ('exang', 'heartdisease'), ('cp', 'heartdisease'),
                           ('heartdisease', 'restecg'), ('heartdisease', 'chol')])

    print('\nLearning CPD using Maximum likelihood estimators')
    model.fit(heartDisease, estimator=MLE_ESTIMATOR)

if heartDisease is not None:
    print('\n Inferencing with Bayesian Network:')
    HeartDiseasetest_infer = VariableElimination(model)

    print('\n 1. Probability of HeartDisease given evidence= restecg')
    q1 = HeartDiseasetest_infer.query(variables=['heartdisease'], evidence={'restecg': 1}, show_progress=False)
    print(q1)

    print('\n 2. Probability of HeartDisease given evidence= cp')
    q2 = HeartDiseasetest_infer.query(variables=['heartdisease'], evidence={'cp': 2}, show_progress=False)
    print(q2)

if __name__ == "__main__":
    import sys
    if heartDisease is None and "ipykernel" not in sys.modules:
        sys.exit(2)
