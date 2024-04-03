import datetime as dt

import matplotlib.pyplot as plt
from prophet import Prophet

from data import load

df = load()
df["started_at"] = (df["started_at"] / 1000).apply(dt.datetime.fromtimestamp)
df = df.rename(columns={"started_at": "ds", "time": "y"})
df["floor"] = 0

model = Prophet(interval_width=0.95)
model.fit(df)

future = model.make_future_dataframe(periods=60)

forecast = model.predict(future)

model.plot(forecast)

plt.savefig("figures/prophet.png")
