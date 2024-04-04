import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet

from data import load

df = load()
df["started_at"] = (df["started_at"] / 1000).apply(dt.datetime.fromtimestamp)
df = df.rename(columns={"started_at": "ds", "time": "y"})

df["floor"] = 0
df["cap"] = df["y"].max()

model = Prophet(growth="logistic", interval_width=0.95)
model.fit(df)

future = model.make_future_dataframe(periods=30)

future["floor"] = 0
future["cap"] = df["y"].max()

forecast = model.predict(future)

model.plot(forecast)

# Find the first time the forecast is below 20s.
idx = forecast[forecast["yhat"] < 20]["ds"].idxmin()

# Add a vertical line at that time.
plt.axvline(x=forecast["ds"][idx], color="k", linestyle="--")

# Annotate the line.
plt.text(
    forecast["ds"][idx] + pd.Timedelta(days=1),
    20 + 1,
    f"Forecast < 20s\n{forecast['ds'][idx].strftime('%Y-%m-%d')}",
    verticalalignment="bottom",
    horizontalalignment="left",
)

plt.xlabel("Date")
plt.ylabel("Time (s)")
plt.ylim(10, 50)

plt.legend()
plt.tight_layout()

plt.savefig("figures/prophet.png")
