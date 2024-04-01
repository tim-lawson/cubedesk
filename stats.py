"""
A simple Python script to generate plots from a CubeDesk data export.
"""

import matplotlib.pyplot as plt
import pandas as pd

from data import load, remove_outliers

df = load()

# Create a PB column.
df["pbtime"] = df["time"].cummin()


def _mean(series: pd.Series):
    return remove_outliers(series).mean()


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

    _, ylim = plt.ylim()

    plt.axvline(df[ao].mean(), color="k", linestyle="dashed", linewidth=1)
    text = plt.text(df[ao].mean() + 1, ylim * 0.9, f"global {MU} = {df[ao].mean():.3f}")
    text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

    plt.axvline(last_1000.mean(), color="k", linestyle="dashed", linewidth=1)
    text = plt.text(
        last_1000.mean() + 1, ylim * 0.8, f"last 1000 {MU} = {last_1000.mean():.3f}"
    )
    text.set_bbox(dict(facecolor="white", edgecolor="white", alpha=1))

    plt.savefig(f"figures/hist_{ao}.png")
    plt.clf()

# Plot the time and PB.
plt.scatter(df.index, df["time"], label="time", color="tab:blue", alpha=0.5, s=1)
plt.plot(df.index, df["pbtime"], label="pb", color="tab:orange")

pb = df["pbtime"].iloc[-1]
xlim, _ = plt.xlim()
ylim, _ = plt.ylim()
plt.axhline(pb, color="k", linestyle="dashed", linewidth=1)
text = plt.text(xlim + 1, ylim + 5, f"pb = {pb:.3f}")

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

    xlim, _ = plt.xlim()
    ylim, _ = plt.ylim()
    plt.axhline(pb, color="k", linestyle="dashed", linewidth=1)
    text = plt.text(xlim + 1, ylim + 5, f"pb{ao} = {pb:.3f}")

    plt.gcf().autofmt_xdate()
    plt.ylabel("Time (s)")
    plt.legend()

    plt.savefig(f"figures/time_{ao}.png")
    plt.clf()
    plt.clf()
