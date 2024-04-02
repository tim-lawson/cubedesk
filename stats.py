"""
A simple Python script to generate plots from a CubeDesk data export.
"""

import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd

from data import load, remove_outliers

df = load()

df["started_at"] = (df["started_at"] / 1000).apply(dt.datetime.fromtimestamp)
df = df.set_index("started_at")

# Create a PB column.
df["pbtime"] = df["time"].cummin()


def _mean(series: pd.Series):
    return remove_outliers(series).mean()


XOFFSET = 0.05
YOFFSET = 0.1


# Create AO columns.
for ao in [3, 5, 12, 50, 100, 1000]:
    # Remove 5% of the best and worst times before computing the mean.
    df[f"ao{ao}"] = df["time"].rolling(window=ao).apply(_mean)
    df[f"pb{ao}"] = df[f"ao{ao}"].cummin()

MU = r"$\mu$"

# For each time and AO column, plot a histogram.
for ao in ["time", "ao3", "ao5", "ao12", "ao50", "ao100", "ao1000"]:
    last_1000 = df.iloc[-1000:][ao]

    plt.hist(
        df[ao],
        bins=100,
        density=True,
        color="tab:blue",
        alpha=0.5,
        label="global",
    )
    plt.hist(
        last_1000,
        bins=100,
        density=True,
        color="tab:orange",
        alpha=0.5,
        label="last 1000",
    )

    plt.title(f"{ao} histogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Density")
    plt.legend()

    xmin, xmax = plt.xlim()
    xrange = xmax - xmin
    ymin, ymax = plt.ylim()
    yrange = ymax - ymin

    ao_mean = df[ao].mean()

    plt.axvline(ao_mean, color="k", linestyle="dashed", linewidth=1)

    text = plt.text(
        ao_mean + XOFFSET * xrange,
        ymax * (1 - YOFFSET),
        f"global {MU} = {ao_mean:.3f}",
    )

    text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

    last_1000_mean = last_1000.mean()

    plt.axvline(last_1000_mean, color="k", linestyle="dashed", linewidth=1)

    text = plt.text(
        last_1000_mean + XOFFSET * xrange,
        ymax * (1 - 2 * YOFFSET),
        f"last 1000 {MU} = {last_1000_mean:.3f}",
    )

    text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

    plt.savefig(f"figures/hist_{ao}.png")
    plt.clf()

# Plot the time and PB.
plt.scatter(df.index, df["time"], label="time", color="tab:blue", alpha=0.5, s=1)
plt.plot(df.index, df["pbtime"], label="pb", color="tab:orange")

pb = df["pbtime"].iloc[-1]

xmin, xmax = plt.xlim()
xrange = xmax - xmin
ymin, ymax = plt.ylim()
yrange = ymax - ymin

plt.axhline(pb, color="k", linestyle="dashed", linewidth=1)

text = plt.text(xmin + XOFFSET * xrange, ymin + YOFFSET * yrange, f"pb = {pb:.3f}")

text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

plt.gcf().autofmt_xdate()
plt.ylabel("Time (s)")
plt.legend()

plt.savefig("figures/time.png")
plt.clf()

# For each AO column, plot the AO, standard deviation, and PB.
for ao in [3, 5, 12, 50, 100, 1000]:
    plt.scatter(
        df.index, df[f"ao{ao}"], label=f"ao{ao}", color="tab:blue", alpha=0.5, s=1
    )

    plt.plot(df.index, df[f"pb{ao}"], label=f"pb{ao}", color="tab:orange")

    pb = df[f"pb{ao}"].iloc[-1]

    xmin, xmax = plt.xlim()
    xrange = xmax - xmin
    ymin, ymax = plt.ylim()
    yrange = ymax - ymin

    plt.axhline(pb, color="k", linestyle="dashed", linewidth=1)

    text = plt.text(
        xmin + XOFFSET * xrange, ymin + YOFFSET * yrange, f"pb{ao} = {pb:.3f}"
    )

    text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

    plt.gcf().autofmt_xdate()
    plt.ylabel("Time (s)")
    plt.legend()

    plt.savefig(f"figures/time_{ao}.png")
    plt.clf()
