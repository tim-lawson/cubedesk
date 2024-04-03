"""
A simple Python script to generate an animated plot from a CubeDesk data export.
"""

import datetime as dt
from math import ceil

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.stats import norm

from data import load

df = load()
df["started_at"] = (df["started_at"] / 1000).apply(dt.datetime.fromtimestamp)
df = df.set_index("started_at")

fig, ax = plt.subplots()

BATCH_SIZE = 100


def update(frame):
    """
    Update the histogram.
    """
    plt.cla()

    n = (frame + 1) * BATCH_SIZE
    imin, imax = max(n - 1000, 0), n + 1
    times = df["time"].iloc[imin:imax]
    (mu, sigma) = norm.fit(times)

    print(
        ", ".join(
            [
                f"{n}".rjust(4),
                f"avg = {mu:.3f}",
                f"std = {sigma:.3f}",
                f"95% = {mu - 1.96 * sigma:.3f}-{mu + 1.96 * sigma:.3f}",
            ]
        )
    )

    _, bins, _ = plt.hist(times, 50, density=True, color="tab:blue", alpha=0.75)
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, "tab:orange", linewidth=2)

    ax.set_xlim(10, 50)
    ax.set_ylim(0, 0.16)

    plt.title(
        r"$\mathrm{Last\ 1000\ times:}\ \mu=%.3f,\ \sigma=%.3f,\ n=%d$" % (mu, sigma, n)
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Density")


ani = FuncAnimation(
    fig,
    update,  # type: ignore
    frames=ceil(len(df) / BATCH_SIZE),
)

ani.save("figures/animation.gif", writer="imagemagick", fps=5)
