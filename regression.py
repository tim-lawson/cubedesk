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

plt.scatter(X, y, color="tab:blue", label="data", alpha=0.5, s=1)
plt.plot(X_, y_, color="tab:orange", label="mean")
plt.xlabel("Timestamp")
plt.ylabel("Time (s)")
plt.legend()
plt.show()
