import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression

from data import load

df = load()

# Remove the first two weeks of data.
df = df[df["started_at"] > df["started_at"].min() + pd.Timedelta(days=14).value / 1e6]

X = df["started_at"].to_numpy().reshape(-1, 1)
y = df["time"].to_numpy().reshape(-1, 1)

xmin = X.min()
xmax = X.max()
xrange = xmax - xmin

model = TransformedTargetRegressor(
    regressor=LinearRegression(), func=np.log, inverse_func=np.exp
)

model.fit(X, y)

X_ = np.linspace(xmin, xmin + 2 * xrange, 1000).reshape(-1, 1)
y_ = model.predict(X_)

# Transform X and X_ into timestamps.
X = pd.to_datetime(X.flatten(), unit="ms")
X_ = pd.to_datetime(X_.flatten(), unit="ms")

plt.scatter(X, y, color="tab:blue", label="data", alpha=0.5, s=1)

plt.plot(X_, y_, color="tab:orange", label="linear regression")

# Find the first time the forecast is below 20s.
idx = np.argmax(y_ < 20)

# Add a vertical line at that time.
plt.axvline(x=X_[idx], color="k", linestyle="--")

# Annotate the line.
plt.text(
    X_[idx] + pd.Timedelta(days=1),
    20 + 1,
    f"Forecast < 20s\n{X_[idx].strftime('%Y-%m-%d')}",
    verticalalignment="bottom",
    horizontalalignment="left",
)

plt.xlabel("Date")
plt.xticks(rotation=45)
plt.ylabel("Time (s)")

plt.legend()
plt.tight_layout()

plt.savefig("figures/regression.png")
