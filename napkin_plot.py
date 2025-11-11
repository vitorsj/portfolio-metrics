import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Circle  # kept for potential future use


# Astella Brand Colors (Complete Palette)
COLORS = {
    # Primary Colors (Cyan-Turquoise Gradient)
    "deep_ocean": "#225379",      # Dark text, contrasts
    "marine_blue": "#3981A4",     # Mid-tone elements
    "turquoise": "#56BBC2",       # PRIMARY brand accent, CTAs, highlights
    "soft_aqua": "#B7E7DC",       # Light backgrounds, subtle accents
    "mint_whisper": "#E6F7E8",    # Very light backgrounds
    "pale_sage": "#E2ECCB",       # Neutral light backgrounds
    # Secondary Colors (Use sparingly)
    "coral": "#E05145",           # Error states, urgent CTAs
    "peach": "#F3AF8A",           # Warm accents, success states
}

# Typography preferences (non-failing, will fallback if fonts not available)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Open Sans",
    "Intelo",
    "Montserrat",
    "Arial",
    "Helvetica",
    "DejaVu Sans",
]


def _normalize_value(value: float, benchmark: float, metric_type: str = "higher_better") -> float:
    """
    Normaliza valores para escala 0-100.
    Regra: o benchmark sempre recebe score 70 (referência média).
    """
    if metric_type == "higher_better":
        if benchmark == 0:
            return 100 if value > 0 else 40
        ratio = value / benchmark if benchmark != 0 else 0
        if ratio >= 1.5:
            return 100
        elif ratio <= 0.5:
            return 40
        else:
            return 40 + (ratio - 0.5) * 60
    else:
        return (value / benchmark) * 100 if benchmark != 0 else 0


def _check_label_overlap(purple_value: float, napkin_value: float, threshold: float = 12):
    """Detecta sobreposição entre labels e calcula offsets necessários."""
    distance = abs(purple_value - napkin_value)
    if distance < threshold:
        if distance < 7:
            radial_offset = (threshold - distance) * 1.3 + 8
        elif distance < 9:
            radial_offset = (threshold - distance) * 1.1 + 6
        else:
            radial_offset = (threshold - distance) * 0.9 + 4
        direction = "down" if napkin_value < purple_value else "up"
        if distance < 7:
            angular_offset = 0.18 if napkin_value < purple_value else -0.18
        elif distance < 9:
            angular_offset = 0.12 if napkin_value < purple_value else -0.12
        else:
            angular_offset = 0.08 if napkin_value < purple_value else -0.08
        return radial_offset, angular_offset, direction
    return 0, 0, None


DEFAULT_METRIC_ORDER = ["ARR", "Growth", "Round Size", "Cap Table", "Valuation", "Gross Margin"]


def build_figure(
    startup_metrics: dict,
    napkin_low: dict,
    napkin_high: dict,
    *,
    metric_order: list | None = None,
    startup_name: str = "Startup",
) -> Figure:
    """
    Constrói e retorna a Figure do gráfico radar no tema Astella.
    Espera dicionários com chaves: 'ARR', 'Growth', 'Round Size', 'Valuation', 'Cap Table', 'Gross Margin'
    """
    order = metric_order or DEFAULT_METRIC_ORDER

    # Normalização
    purple_normalized: list[float] = []
    napkin_low_normalized: list[float] = []
    napkin_high_normalized: list[float] = []

    for metric in order:
        benchmark = (napkin_low[metric] + napkin_high[metric]) / 2
        if metric == "Cap Table":
            p_val = _normalize_value(startup_metrics[metric], benchmark, "percentage")
            l_val = _normalize_value(napkin_low[metric], benchmark, "percentage")
            h_val = _normalize_value(napkin_high[metric], benchmark, "percentage")
        else:
            p_val = _normalize_value(startup_metrics[metric], benchmark, "higher_better")
            l_val = _normalize_value(napkin_low[metric], benchmark, "higher_better")
            h_val = _normalize_value(napkin_high[metric], benchmark, "higher_better")

        purple_normalized.append(min(100, p_val))
        napkin_low_normalized.append(min(100, l_val))
        napkin_high_normalized.append(min(100, h_val))

    # Figura
    fig = plt.figure(figsize=(14, 14), facecolor="white")
    ax = fig.add_subplot(111, projection="polar", facecolor="white")

    num_vars = len(order)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    purple_plot = purple_normalized + [purple_normalized[0]]
    napkin_low_plot = napkin_low_normalized + [napkin_low_normalized[0]]
    napkin_high_plot = napkin_high_normalized + [napkin_high_normalized[0]]
    angles += angles[:1]

    # Configurações polares
    ax.set_ylim(0, 100)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.grid(True, color="#E0E0E0", linestyle="-", linewidth=1.2, alpha=0.6)

    # Linha externa mais visível
    theta_circle = np.linspace(0, 2 * np.pi, 200)
    r_circle = np.full_like(theta_circle, 100)
    ax.plot(theta_circle, r_circle, color="#C0C0C0", linewidth=2.5, alpha=0.7, zorder=1)

    # Faixa de benchmark
    ax.fill_between(
        angles, napkin_low_plot, napkin_high_plot, color=COLORS["marine_blue"], alpha=0.15, zorder=1
    )

    # Linhas Low/High
    ax.plot(
        angles,
        napkin_low_plot,
        color=COLORS["marine_blue"],
        linewidth=1.8,
        linestyle=":",
        alpha=0.5,
        zorder=2,
    )
    ax.plot(
        angles,
        napkin_high_plot,
        color=COLORS["marine_blue"],
        linewidth=1.8,
        linestyle=":",
        alpha=0.5,
        zorder=2,
    )

    # Labels Low
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], napkin_low_normalized, order)):
        purple_value = purple_normalized[i]
        radial_offset, angular_offset, direction = _check_label_overlap(purple_value, value)
        if radial_offset > 0:
            label_distance = max(0, value - radial_offset) if direction == "down" else min(100, value + radial_offset)
        else:
            label_distance = value
        adjusted_angle = angle + angular_offset

        if metric == "ARR":
            napkin_text = f'${napkin_low["ARR"]}M'
        elif metric == "Growth":
            napkin_text = f'{int(napkin_low["Growth"])}%'
        elif metric == "Round Size":
            napkin_text = f'${napkin_low["Round Size"]}M'
        elif metric == "Valuation":
            napkin_text = f'${napkin_low["Valuation"]}M'
        elif metric == "Cap Table":
            napkin_text = f'{int(napkin_low["Cap Table"])}%'
        else:
            napkin_text = f'{int(napkin_low["Gross Margin"])}%'

        ha_align = "left" if angular_offset > 0 else ("right" if angular_offset < 0 else "center")
        ax.text(
            adjusted_angle,
            label_distance,
            napkin_text,
            ha=ha_align,
            va="center",
            fontsize=14,
            fontweight="500",
            color=COLORS["marine_blue"],
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                edgecolor=COLORS["marine_blue"],
                linewidth=1.2,
                alpha=0.85,
            ),
            zorder=5,
        )

    # Labels High
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], napkin_high_normalized, order)):
        purple_value = purple_normalized[i]
        radial_offset, angular_offset, direction = _check_label_overlap(purple_value, value)
        if radial_offset > 0:
            label_distance = max(0, value - radial_offset) if direction == "down" else min(100, value + radial_offset)
        else:
            label_distance = value
        adjusted_angle = angle + angular_offset

        if metric == "ARR":
            napkin_text = f'${napkin_high["ARR"]}M'
        elif metric == "Growth":
            napkin_text = f'{int(napkin_high["Growth"])}%'
        elif metric == "Round Size":
            napkin_text = f'${napkin_high["Round Size"]}M'
        elif metric == "Valuation":
            napkin_text = f'${napkin_high["Valuation"]}M'
        elif metric == "Cap Table":
            napkin_text = f'{int(napkin_high["Cap Table"])}%'
        else:
            napkin_text = f'{int(napkin_high["Gross Margin"])}%'

        ha_align = "left" if angular_offset > 0 else ("right" if angular_offset < 0 else "center")
        ax.text(
            adjusted_angle,
            label_distance,
            napkin_text,
            ha=ha_align,
            va="center",
            fontsize=14,
            fontweight="500",
            color=COLORS["marine_blue"],
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="white",
                edgecolor=COLORS["marine_blue"],
                linewidth=1.2,
                alpha=0.85,
            ),
            zorder=5,
        )

    # Linha principal Purple
    ax.plot(angles, purple_plot, color=COLORS["turquoise"], linewidth=4.5, linestyle="-", zorder=4)
    ax.fill(angles, purple_plot, color=COLORS["turquoise"], alpha=0.25, zorder=3)

    # Pontos em destaque
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], purple_normalized, order)):
        ax.plot(angle, value, "o", color=COLORS["turquoise"], markersize=18, markeredgewidth=3.5, markeredgecolor="white", zorder=5)
        ax.plot(angle, value, "o", color=COLORS["turquoise"], markersize=18, alpha=0.35, zorder=4.5)

        if metric == "ARR":
            label_text = f'${startup_metrics["ARR"]}M'
        elif metric == "Growth":
            label_text = f'{startup_metrics["Growth"]}%'
        elif metric == "Round Size":
            label_text = f'${startup_metrics["Round Size"]}M'
        elif metric == "Valuation":
            label_text = f'${startup_metrics["Valuation"]}M'
        elif metric == "Cap Table":
            label_text = f'{startup_metrics["Cap Table"]}%'
        else:
            label_text = f'{int(startup_metrics["Gross Margin"])}%'

        ax.text(
            angle,
            value,
            label_text,
            ha="center",
            va="center",
            fontsize=15,
            fontweight="bold",
            color=COLORS["deep_ocean"],
            bbox=dict(
                boxstyle="round,pad=0.45",
                facecolor="white",
                edgecolor=COLORS["turquoise"],
                linewidth=2.5,
                alpha=0.98,
            ),
            zorder=6,
        )

    # Eixos e labels externos
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    for angle, label in zip(angles[:-1], order):
        rotation = np.rad2deg(angle)  # noqa: F841 (mantido para referência futura)
        if label == "ARR":
            ha, distance_mul = "center", 1.10
        elif angle == 0:
            ha, distance_mul = "center", 1.13
        elif 0 < angle < np.pi:
            ha, distance_mul = "left", 1.13
        elif angle == np.pi:
            ha, distance_mul = "center", 1.17
        else:
            ha, distance_mul = "right", 1.13
        ax.text(
            angle,
            100 * distance_mul,
            label,
            ha=ha,
            va="center",
            fontsize=18,
            fontweight="bold",
            color=COLORS["deep_ocean"],
            linespacing=1.3,
        )

    # Remover borda circular
    ax.spines["polar"].set_visible(False)

    # Legenda
    legend_y = 0.09
    legend_x_start = 0.18

    # Série principal (Startup)
    fig.patches.append(
        plt.Rectangle(
            (legend_x_start, legend_y),
            0.025,
            0.012,
            transform=fig.transFigure,
            facecolor=COLORS["turquoise"],
            edgecolor="white",
            linewidth=2.5,
        )
    )
    fig.text(
        legend_x_start + 0.035,
        legend_y + 0.006,
        f"{startup_name} Metrics",
        transform=fig.transFigure,
        fontsize=16,
        fontweight="700",
        color=COLORS["deep_ocean"],
        va="center",
    )

    # Napkin Low
    napkin_low_x = legend_x_start + 0.20
    fig.patches.append(
        plt.Rectangle(
            (napkin_low_x, legend_y),
            0.025,
            0.012,
            transform=fig.transFigure,
            facecolor=COLORS["marine_blue"],
            edgecolor="white",
            linewidth=1.2,
            alpha=0.35,
        )
    )
    fig.text(
        napkin_low_x + 0.035,
        legend_y + 0.006,
        "Napkin Low",
        transform=fig.transFigure,
        fontsize=16,
        fontweight="700",
        color=COLORS["deep_ocean"],
        va="center",
    )

    # Napkin High
    napkin_high_x = legend_x_start + 0.35
    fig.patches.append(
        plt.Rectangle(
            (napkin_high_x, legend_y),
            0.025,
            0.012,
            transform=fig.transFigure,
            facecolor=COLORS["marine_blue"],
            edgecolor="white",
            linewidth=1.2,
            alpha=0.35,
        )
    )
    fig.text(
        napkin_high_x + 0.035,
        legend_y + 0.006,
        "Napkin High",
        transform=fig.transFigure,
        fontsize=16,
        fontweight="700",
        color=COLORS["deep_ocean"],
        va="center",
    )

    # Nota de rodapé
    fig.text(
        0.5,
        0.04,
        "Napkin Benchmark: ARR $0.64M-$1.83M | Growth 200% | Round $1.46M-$3.66M | Valuation $5.86M-$10.9M | Cap Table 80% | Gross Margin 70%",
        ha="center",
        va="center",
        fontsize=13.5,
        color=COLORS["marine_blue"],
        style="italic",
        transform=fig.transFigure,
    )

    # Margens
    plt.subplots_adjust(left=0.1, right=0.9, top=0.93, bottom=0.20)
    return fig



