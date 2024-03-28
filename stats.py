"""
A simple Python script to generate plots from a CubeDesk data export.
"""

import datetime as dt
import json
import matplotlib.pyplot as plt
import pandas as pd

# Change the file path to the location of your data export.
with open("data/cubedesk_data_28_03_2024_19_41_42.txt", encoding="utf-8") as data:
    df = pd.DataFrame.from_dict(json.load(data)["solves"])

    # Filter to a cube type.
    df = df[df["cube_type"] == "333"]

    df = df[["started_at", "time"]]

    df = df.sort_values(by="started_at")
    df["started_at"] = (df["started_at"] / 1000).apply(dt.datetime.fromtimestamp)
    df = df.set_index("started_at")

    # Create a PB column.
    df["pbtime"] = df["time"].cummin()

    # Create AO and standard deviation columns.
    for ao in [3, 5, 12, 50, 100, 1000]:
        df[f"ao{ao}"] = df["time"].rolling(window=ao).mean()
        df[f"std{ao}"] = df["time"].rolling(window=ao).std()
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
        text = plt.text(
            df[ao].mean() + 1, ylim * 0.9, f"global {MU} = {df[ao].mean():.3f}"
        )
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
        plt.plot(df.index, df[f"ao{ao}"], label=f"ao{ao}", color="tab:blue")

        plt.fill_between(
            df.index,
            df[f"ao{ao}"] - 1.96 * df[f"std{ao}"],
            df[f"ao{ao}"] + 1.96 * df[f"std{ao}"],
            color="tab:blue",
            alpha=0.25,
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
