import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, send_file
import os
from flask_cors import CORS  # Importa CORS para manejar las solicitudes de distintos orígenes

from data import get_closest_to_24h, get_RSI, get_top_vol_coins

app = Flask(__name__)
CORS(app)  # Habilita CORS para tu aplicación Flask

FIGURE_SIZE = (12, 10)
BACKGROUND_COLOR = "#0d1117"
RANGES = {
    "Overbought": (70, 100),
    "Strong": (60, 70),
    "Neutral": (40, 60),
    "Weak": (30, 40),
    "Oversold": (0, 30),
}
COLORS_LABELS = {
    "Oversold": "#1d8b7a",
    "Weak": "#144e48",
    "Neutral": "#0d1117",
    "Strong": "#681f28",
    "Overbought": "#c32e3b",
}
SCATTER_COLORS = {
    "Oversold": "#1e9884",
    "Weak": "#165952",
    "Neutral": "#78797a",
    "Strong": "#79212c",
    "Overbought": "#cf2f3d",
}

def get_color_for_rsi(rsi_value: float) -> dict:
    for label, (low, high) in RANGES.items():
        if low <= rsi_value < high:
            return SCATTER_COLORS[label]
    return None

def plot_rsi_heatmap(num_coins: int = 100, time_frame: str = "1d") -> str:
    top_vol = get_top_vol_coins(num_coins)
    rsi_data = get_RSI(top_vol, time_frame=time_frame)
    old_rsi_data = get_closest_to_24h(time_frame=time_frame)

    rsi_symbols = list(rsi_data.keys())
    rsi_values = list(rsi_data.values())

    average_rsi = np.mean(rsi_values)

    fig, ax = plt.subplots(figsize=FIGURE_SIZE)

    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(BACKGROUND_COLOR)

    color_map = []
    for k in RANGES:
        color_map.append((*RANGES[k], COLORS_LABELS[k], k))

    for i, (start, end, color, symbol) in enumerate(color_map):
        ax.fill_between([0, len(rsi_symbols) + 2], start, end, color=color, alpha=0.35)

        if i == 0:
            y_pos = start + 5
        elif i == len(color_map) - 1:
            y_pos = end - 5
        else:
            y_pos = (start + end) / 2

        ax.text(
            len(rsi_symbols) + 1.5,
            y_pos,
            symbol.upper(),
            va="center",
            ha="right",
            fontsize=15,
            color="grey",
        )

    for i, symbol in enumerate(rsi_symbols):
        ax.scatter(
            i + 1,
            rsi_values[i],
            color=get_color_for_rsi(rsi_values[i]),
            s=100,
        )
        ax.annotate(
            symbol,
            (i + 1, rsi_values[i]),
            color="#b9babc",
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

        if symbol in old_rsi_data:
            rsi_diff = rsi_values[i] - old_rsi_data[symbol]
            line_color = "#1f9986" if rsi_diff > 0 else "#e23343"
            ax.plot(
                [i + 1, i + 1],
                [old_rsi_data[symbol], rsi_values[i]],
                color=line_color,
                linestyle="--",
                linewidth=0.75,
            )

    ax.axhline(
        xmin=0, xmax=1, y=average_rsi, color="#d58c3c", linestyle="--", linewidth=0.75
    )
    ax.text(
        len(rsi_symbols) + 1.5,
        average_rsi,
        f"AVG RSI: {average_rsi:.2f}",
        color="#d58c3c",
        va="bottom",
        ha="right",
        fontsize=15,
    )

    ax.tick_params(colors="#a9aaab", which="both", length=0)
    ax.set_ylim(20, 80)
    ax.set_xlim(0, len(rsi_symbols) + 2)
    ax.set_xticks([])

    add_legend(ax)

    for spine in ax.spines.values():
        spine.set_edgecolor(BACKGROUND_COLOR)

    plt.text(
        -0.025,
        1.125,
        "Crypto Market RSI Heatmap",
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment="top",
        horizontalalignment="left",
        color="white",
        weight="bold",
    )

    image_path = os.path.join(os.path.dirname(__file__), "rsi_heatmap.png")
    plt.savefig(image_path, bbox_inches="tight")
    plt.close(fig)
    return image_path

def add_legend(ax: plt.Axes) -> None:
    adjusted_colors = list(COLORS_LABELS.values())
    adjusted_colors[2] = "#808080"
    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="s",
            color=BACKGROUND_COLOR,
            markerfacecolor=color,
            markersize=10,
            label=label,
        )
        for color, label in zip(
            adjusted_colors,
            [label.upper() for label in list(COLORS_LABELS.keys())],
        )
    ]

    legend = ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.05),
        ncol=len(legend_handles),
        frameon=False,
        fontsize="small",
        labelcolor="white",
    )

    for text in legend.get_texts():
        text.set_fontweight("bold")

    plt.subplots_adjust(left=0.05, right=0.95, top=0.875, bottom=0.1)

@app.route("/")
def serve_rsi_heatmap():
    image_path = plot_rsi_heatmap(num_coins=100, time_frame="1d")
    return send_file(image_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
