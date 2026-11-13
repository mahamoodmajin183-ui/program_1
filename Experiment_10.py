import numpy as np
from pathlib import Path
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.layouts import gridplot

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

try:
    IN_NOTEBOOK = get_ipython().__class__.__name__ == "ZMQInteractiveShell"
except NameError:
    IN_NOTEBOOK = False
if IN_NOTEBOOK:
    output_notebook()
else:
    output_file(str(OUT_DIR / "ml_ex10_lwr.html"), title="Locally Weighted Regression", mode="inline")

np.random.seed(42)

def local_regression(x0, X, Y, tau):
    x0 = np.r_[1, x0]
    X = np.c_[np.ones(len(X)), X]

    xw = X.T * radial_kernel(x0, X, tau)
    beta = np.linalg.pinv(xw @ X) @ xw @ Y

    return x0 @ beta


def radial_kernel(x0, X, tau):
    return np.exp(np.sum((X - x0) ** 2, axis=1) / (-2 * tau * tau))

n = 1000
X = np.linspace(-3, 3, num=n)
print("The Data Set ( 10 Samples) X :\n", X[1:10])
Y = np.log(np.abs(X ** 2 - 1) + .5)
print("The Fitting Curve Data Set (10 Samples) Y :\n", Y[1:10])

X += np.random.normal(scale=.1, size=n)
print("Normalised (10 Samples) X :\n", X[1:10])

domain = np.linspace(-3, 3, num=300)
print(" Xo Domain Space(10 Samples) :\n", domain[1:10])

def plot_lwr(tau):
    prediction = [local_regression(x0, X, Y, tau) for x0 in domain]
    plot = figure(width=400, height=400)
    plot.title.text = 'tau=%g' % tau
    plot.scatter(X, Y, alpha=.3)
    plot.line(domain, prediction, line_width=2, color='red')
    return plot, prediction


if __name__ == "__main__":
    taus = [10., 1., 0.1, 0.01]
    plots_and_preds = [plot_lwr(t) for t in taus]
    show(gridplot([[plots_and_preds[0][0], plots_and_preds[1][0]],
                   [plots_and_preds[2][0], plots_and_preds[3][0]]]))
    for t, (_, pred) in zip(taus, plots_and_preds):
        print(f"tau={t:<5g} fitted curve: min={min(pred):.3f} max={max(pred):.3f}")
