import io
import streamlit as st


st.set_page_config(page_title="Napkin Radar - Astella", page_icon="📈", layout="wide")

st.title("Napkin Radar - Astella")
st.caption("Defina os dados da sua startup e visualize a comparação com o benchmark Napkin.")

import io
import numpy as np
import matplotlib.pyplot as plt


# -------------------------------
# Configuração de página e fontes
# -------------------------------
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Open Sans', 'Intelo', 'Montserrat', 'Arial', 'Helvetica', 'DejaVu Sans']


# -------------------------------
# Paleta de cores (Astella)
# -------------------------------
COLORS = {
    # Primary Colors (Cyan-Turquoise Gradient)
    'deep_ocean': '#225379',      # Dark text, contrasts
    'marine_blue': '#3981A4',     # Mid-tone elements
    'turquoise': '#56BBC2',       # PRIMARY brand accent, CTAs, highlights
    'soft_aqua': '#B7E7DC',       # Light backgrounds, subtle accents
    'mint_whisper': '#E6F7E8',    # Very light backgrounds
    'pale_sage': '#E2ECCB',       # Neutral light backgrounds

    # Secondary Colors (Use sparingly)
    'coral': '#E05145',           # Error states, urgent CTAs
    'peach': '#F3AF8A',           # Warm accents, success states
}


# -------------------------------
# Benchmarks do Napkin por estágio
# -------------------------------
NAPKIN_BENCHMARKS = {
    'Pre-Seed': {
        'low':   {'ARR': 0.0,   'Growth': 0, 'Round Size': 0.460, 'Valuation': 2.750, 'Cap Table': 90, 'Gross Margin': 70},
        'high':  {'ARR': 0.180, 'Growth': 0, 'Round Size': 0.920, 'Valuation': 6.410, 'Cap Table': 90, 'Gross Margin': 70},
    },
    'Seed': {
        'low':   {'ARR': 0.64, 'Growth': 200, 'Round Size': 1.46, 'Valuation': 5.86, 'Cap Table': 80, 'Gross Margin': 70},
        'high':  {'ARR': 1.83, 'Growth': 200, 'Round Size': 3.66, 'Valuation': 10.9, 'Cap Table': 80, 'Gross Margin': 70},
    },
    'Series A': {
        'low':   {'ARR': 3.300, 'Growth': 150, 'Round Size': 4.580, 'Valuation': 13.730, 'Cap Table': 65, 'Gross Margin': 70},
        'high':  {'ARR': 5.490, 'Growth': 150, 'Round Size': 9.150, 'Valuation': 36.620, 'Cap Table': 65, 'Gross Margin': 70},
    },
    'Series B': {
        'low':   {'ARR': 9.150, 'Growth': 100, 'Round Size': 13.730, 'Valuation': 45.700, 'Cap Table': 50, 'Gross Margin': 70},
        'high':  {'ARR': 36.620, 'Growth': 100, 'Round Size': 27.450, 'Valuation': 91.550, 'Cap Table': 50, 'Gross Margin': 70},
    },
}

metrics = ['ARR', 'Growth', 'Round Size', 'Cap Table', 'Valuation', 'Gross Margin']
metric_labels = ['ARR', 'Growth', 'Round Size', 'Cap Table', 'Valuation', 'Gross Margin']


# -------------------------------
# Normalização e utilitários
# -------------------------------
def normalize_value(value: float, benchmark: float, metric_type: str = 'higher_better') -> float:
    """
    Normaliza valores para escala 0-100.
    Para métricas 'higher_better', 70 é a referência (benchmark médio).
    """
    if metric_type == 'higher_better':
        ratio = value / benchmark if benchmark != 0 else 0
        if ratio >= 1.5:
            return 100
        elif ratio <= 0.5:
            return 40
        else:
            return 40 + (ratio - 0.5) * 60
    else:
        return (value / benchmark) * 100 if benchmark != 0 else 0


def check_label_overlap(purple_value: float, napkin_value: float, threshold: float = 12):
    """Detecta sobreposição entre labels e calcula offsets necessários (radial e angular)."""
    distance = abs(purple_value - napkin_value)
    if distance < threshold:
        if distance < 7:
            radial_offset = (threshold - distance) * 1.3 + 8
        elif distance < 9:
            radial_offset = (threshold - distance) * 1.1 + 6
        else:
            radial_offset = (threshold - distance) * 0.9 + 4
        direction = 'down' if napkin_value < purple_value else 'up'
        if distance < 7:
            angular_offset = 0.18 if napkin_value < purple_value else -0.18
        elif distance < 9:
            angular_offset = 0.12 if napkin_value < purple_value else -0.12
        else:
            angular_offset = 0.08 if napkin_value < purple_value else -0.08
        return radial_offset, angular_offset, direction
    return 0, 0, None


# -------------------------------
# Geração do gráfico radar
# -------------------------------
def generate_radar_chart(startup_metrics: dict, startup_name: str = "Startup"):
    # Normalização
    purple_normalized = []
    napkin_low_normalized = []
    napkin_high_normalized = []

    for metric in metrics:
        benchmark_mid = (napkin_low[metric] + napkin_high[metric]) / 2
        if metric == 'Cap Table':
            purple_norm = normalize_value(startup_metrics[metric], benchmark_mid, 'percentage')
            low_norm = normalize_value(napkin_low[metric], benchmark_mid, 'percentage')
            high_norm = normalize_value(napkin_high[metric], benchmark_mid, 'percentage')
        else:
            purple_norm = normalize_value(startup_metrics[metric], benchmark_mid, 'higher_better')
            low_norm = normalize_value(napkin_low[metric], benchmark_mid, 'higher_better')
            high_norm = normalize_value(napkin_high[metric], benchmark_mid, 'higher_better')

        purple_normalized.append(min(100, purple_norm))
        napkin_low_normalized.append(min(100, low_norm))
        napkin_high_normalized.append(min(100, high_norm))

    # Plot
    fig = plt.figure(figsize=(14, 14), facecolor='white')
    ax = fig.add_subplot(111, projection='polar', facecolor='white')

    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    purple_plot = purple_normalized + [purple_normalized[0]]
    napkin_low_plot = napkin_low_normalized + [napkin_low_normalized[0]]
    napkin_high_plot = napkin_high_normalized + [napkin_high_normalized[0]]
    angles += angles[:1]

    ax.set_ylim(0, 100)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_yticklabels([])
    ax.grid(True, color='#E0E0E0', linestyle='-', linewidth=1.2, alpha=0.6)
    theta_circle = np.linspace(0, 2*np.pi, 200)
    r_circle = np.full_like(theta_circle, 100)
    ax.plot(theta_circle, r_circle, color='#C0C0C0', linewidth=2.5, alpha=0.7, zorder=1)

    # Área entre Low e High
    ax.fill_between(angles, napkin_low_plot, napkin_high_plot,
                    color=COLORS['marine_blue'], alpha=0.15, zorder=1)

    # Low
    ax.plot(angles, napkin_low_plot, color=COLORS['marine_blue'], linewidth=1.8,
            linestyle=':', alpha=0.5, zorder=2)
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], napkin_low_normalized, metrics)):
        purple_value = purple_normalized[i]
        radial_offset, angular_offset, direction = check_label_overlap(purple_value, value)
        label_distance = (max(0, value - radial_offset) if direction == 'down'
                          else min(100, value + radial_offset)) if radial_offset > 0 else value
        adjusted_angle = angle + angular_offset
        if metric == 'ARR':
            napkin_text = f'${napkin_low["ARR"]}M'
        elif metric == 'Growth':
            napkin_text = f'{int(napkin_low["Growth"])}%'
        elif metric == 'Round Size':
            napkin_text = f'${napkin_low["Round Size"]}M'
        elif metric == 'Valuation':
            napkin_text = f'${napkin_low["Valuation"]}M'
        elif metric == 'Cap Table':
            napkin_text = f'{int(napkin_low["Cap Table"])}%'
        else:
            napkin_text = f'{int(napkin_low["Gross Margin"])}%'
        ha_align = 'left' if angular_offset > 0 else ('right' if angular_offset < 0 else 'center')
        ax.text(adjusted_angle, label_distance, napkin_text,
                ha=ha_align, va='center', fontsize=14, fontweight='500',
                color=COLORS['marine_blue'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS['marine_blue'], linewidth=1.2, alpha=0.85),
                zorder=5)

    # High
    ax.plot(angles, napkin_high_plot, color=COLORS['marine_blue'], linewidth=1.8,
            linestyle=':', alpha=0.5, zorder=2)
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], napkin_high_normalized, metrics)):
        purple_value = purple_normalized[i]
        radial_offset, angular_offset, direction = check_label_overlap(purple_value, value)
        label_distance = (max(0, value - radial_offset) if direction == 'down'
                          else min(100, value + radial_offset)) if radial_offset > 0 else value
        adjusted_angle = angle + angular_offset
        if metric == 'ARR':
            napkin_text = f'${napkin_high["ARR"]}M'
        elif metric == 'Growth':
            napkin_text = f'{int(napkin_high["Growth"])}%'
        elif metric == 'Round Size':
            napkin_text = f'${napkin_high["Round Size"]}M'
        elif metric == 'Valuation':
            napkin_text = f'${napkin_high["Valuation"]}M'
        elif metric == 'Cap Table':
            napkin_text = f'{int(napkin_high["Cap Table"])}%'
        else:
            napkin_text = f'{int(napkin_high["Gross Margin"])}%'
        ha_align = 'left' if angular_offset > 0 else ('right' if angular_offset < 0 else 'center')
        ax.text(adjusted_angle, label_distance, napkin_text,
                ha=ha_align, va='center', fontsize=14, fontweight='500',
                color=COLORS['marine_blue'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS['marine_blue'], linewidth=1.2, alpha=0.85),
                zorder=5)

    # Série da startup (linha principal)
    ax.plot(angles, purple_plot, color=COLORS['turquoise'], linewidth=4.5, linestyle='-', zorder=4)
    ax.fill(angles, purple_plot, color=COLORS['turquoise'], alpha=0.25, zorder=3)
    for i, (angle, value, metric) in enumerate(zip(angles[:-1], purple_normalized, metrics)):
        ax.plot(angle, value, 'o', color=COLORS['turquoise'], markersize=18,
                markeredgewidth=3.5, markeredgecolor='white', zorder=5)
        ax.plot(angle, value, 'o', color=COLORS['turquoise'], markersize=18, alpha=0.35, zorder=4.5)
        if metric == 'ARR':
            label_text = f'${startup_metrics["ARR"]}M'
        elif metric == 'Growth':
            label_text = f'{startup_metrics["Growth"]}%'
        elif metric == 'Round Size':
            label_text = f'${startup_metrics["Round Size"]}M'
        elif metric == 'Valuation':
            label_text = f'${startup_metrics["Valuation"]}M'
        elif metric == 'Cap Table':
            label_text = f'{startup_metrics["Cap Table"]}%'
        else:
            label_text = f'{int(startup_metrics["Gross Margin"])}%'
        ax.text(angle, value, label_text, ha='center', va='center',
                fontsize=15, fontweight='bold', color=COLORS['deep_ocean'],
                bbox=dict(boxstyle='round,pad=0.45', facecolor='white',
                          edgecolor=COLORS['turquoise'], linewidth=2.5, alpha=0.98),
                zorder=6)

    # Eixos (labels externos)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])
    for angle, label in zip(angles[:-1], metric_labels):
        rotation = np.rad2deg(angle)
        if label == 'ARR':
            ha, distance_mul = 'center', 1.10
        elif angle == 0:
            ha, distance_mul = 'center', 1.13
        elif 0 < angle < np.pi:
            ha, distance_mul = 'left', 1.13
        elif angle == np.pi:
            ha, distance_mul = 'center', 1.17
        else:
            ha, distance_mul = 'right', 1.13
        ax.text(angle, 100 * distance_mul, label, ha=ha, va='center',
                fontsize=18, fontweight='bold', color=COLORS['deep_ocean'], linespacing=1.3)

    ax.spines['polar'].set_visible(False)

    # Legenda e rodapé
    legend_y = 0.09
    legend_x_start = 0.18
    fig.patches.append(plt.Rectangle((legend_x_start, legend_y), 0.025, 0.012,
                                     transform=fig.transFigure, facecolor=COLORS['turquoise'],
                                     edgecolor='white', linewidth=2.5))
    fig.text(legend_x_start + 0.035, legend_y + 0.006, f'{startup_name} Metrics',
             transform=fig.transFigure, fontsize=16, fontweight='700',
             color=COLORS['deep_ocean'], va='center')

    napkin_low_x = legend_x_start + 0.20
    fig.patches.append(plt.Rectangle((napkin_low_x, legend_y), 0.025, 0.012,
                                     transform=fig.transFigure, facecolor=COLORS['marine_blue'],
                                     edgecolor='white', linewidth=1.2, alpha=0.35))
    fig.text(napkin_low_x + 0.035, legend_y + 0.006, 'Napkin Low',
             transform=fig.transFigure, fontsize=16, fontweight='700',
             color=COLORS['deep_ocean'], va='center')

    napkin_high_x = legend_x_start + 0.35
    fig.patches.append(plt.Rectangle((napkin_high_x, legend_y), 0.025, 0.012,
                                     transform=fig.transFigure, facecolor=COLORS['marine_blue'],
                                     edgecolor='white', linewidth=1.2, alpha=0.35))
    fig.text(napkin_high_x + 0.035, legend_y + 0.006, 'Napkin High',
             transform=fig.transFigure, fontsize=16, fontweight='700',
             color=COLORS['deep_ocean'], va='center')

    # Nota de rodapé dinâmica conforme estágio selecionado (sem f-strings aninhadas)
    growth_suffix = "" if napkin_low["Growth"] == napkin_high["Growth"] else ("-" + str(int(napkin_high["Growth"])) + "%")
    cap_suffix = "" if napkin_low["Cap Table"] == napkin_high["Cap Table"] else ("-" + str(int(napkin_high["Cap Table"])) + "%")
    gm_low = int(napkin_low.get("Gross Margin", 70))
    gm_high = int(napkin_high.get("Gross Margin", 70))
    gm_suffix = "" if gm_low == gm_high else ("-" + str(gm_high) + "%")
    footnote_text = (
        f"Napkin Benchmark: ARR ${napkin_low['ARR']}M-${napkin_high['ARR']}M | "
        f"Growth {int(napkin_low['Growth'])}%{growth_suffix} | "
        f"Round ${napkin_low['Round Size']}M-${napkin_high['Round Size']}M | "
        f"Valuation ${napkin_low['Valuation']}M-${napkin_high['Valuation']}M | "
        f"Cap Table {int(napkin_low['Cap Table'])}%{cap_suffix} | "
        f"Gross Margin {gm_low}%{gm_suffix}"
    )
    fig.text(0.5, 0.04, footnote_text, ha='center', va='center', fontsize=13.5,
             color=COLORS['marine_blue'], style='italic', transform=fig.transFigure)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.93, bottom=0.20)

    # Buffer de imagem para download
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white',
                edgecolor='none', pad_inches=0.3)
    buffer.seek(0)
    return fig, buffer


# -------------------------------
# Interface Streamlit
# -------------------------------
st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">
      <div style="width:10px;height:26px;border-radius:4px;background:{COLORS['turquoise']}"></div>
      <h2 style="margin:0;color:{COLORS['deep_ocean']}">Napkin Radar • Astella</h2>
    </div>
    <p style="margin-top:0;color:{COLORS['marine_blue']}">Atualiza em tempo real conforme você altera os dados.</p>
    """,
    unsafe_allow_html=True,
)

# Layout: nome da startup, estágio e inputs
c_name, c_stage, _ = st.columns([2, 1.3, 0.7])
with c_name:
    col_name = st.text_input("Nome da startup", value="Startup")
with c_stage:
    stage = st.selectbox("Estágio da rodada", options=["Seed", "Pre-Seed", "Series A", "Series B"], index=0)
selected_bench = NAPKIN_BENCHMARKS[stage]
napkin_low = selected_bench['low']
napkin_high = selected_bench['high']

c1, c2, c3 = st.columns(3)
with c1:
    arr = st.number_input("ARR (em milhões de USD)", min_value=0.0, step=0.1, value=1.1)
    round_size = st.number_input("Round Size (em milhões de USD)", min_value=0.0, step=0.1, value=3.5)
with c2:
    growth = st.number_input("Growth (%)", min_value=0.0, step=10.0, value=389.0)
    valuation = st.number_input("Valuation (em milhões de USD)", min_value=0.0, step=0.5, value=13.0)
with c3:
    cap_table = st.number_input("Cap Table (%)", min_value=0.0, max_value=100.0, step=1.0, value=72.0)
    gross_margin = st.number_input("Gross Margin (%)", min_value=0.0, max_value=100.0, step=1.0, value=82.0)

# Gera o gráfico automaticamente (tempo real) a cada alteração
startup_metrics = {
    'ARR': float(arr),
    'Growth': float(growth),
    'Round Size': float(round_size),
    'Valuation': float(valuation),
    'Cap Table': float(cap_table),
    'Gross Margin': float(gross_margin),
}

fig, buffer = generate_radar_chart(startup_metrics, startup_name=col_name or "Startup")

tab1, tab2 = st.tabs(["Gráfico", "Dados"])
with tab1:
    st.pyplot(fig, use_container_width=True)
    st.download_button(
        label="Baixar gráfico (PNG)",
        data=buffer,
        file_name=f"napkin_radar_{(col_name or 'startup').lower().replace(' ', '_')}.png",
        mime="image/png"
    )
with tab2:
    st.write("Entradas atuais")
    st.dataframe(
        {
            "Métrica": metrics,
            "Valor Startup": [
                startup_metrics['ARR'],
                startup_metrics['Growth'],
                startup_metrics['Round Size'],
                startup_metrics['Cap Table'],
                startup_metrics['Valuation'],
                startup_metrics['Gross Margin'],
            ],
            "Napkin Low": [napkin_low[m] for m in metrics],
            "Napkin High": [napkin_high[m] for m in metrics],
        },
        use_container_width=True
    )


