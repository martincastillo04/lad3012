"""
Dashboard Superstore — LAD3012 D09 (version mejorada)
=====================================================
1) Cambia TU_NOMBRE y TU_ID por los tuyos.
2) Escribe TU_INSIGHT con TUS palabras despues de explorar el dashboard.
Las secciones extra (diagnostico, descuento, Pareto) se calculan solas
y se ajustan si tu dataset no trae alguna columna.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIGURACION DE PAGINA
# ============================================================
st.set_page_config(page_title="Superstore Dashboard", page_icon="🏪", layout="wide")

# ============================================================
# PASO 1 — TUS DATOS (CAMBIA ESTO)
# ============================================================
TU_NOMBRE = "Martin Santiago Castillo"
TU_ID     = "181689"

# ============================================================
# PASO 2 — TU INSIGHT
# ============================================================
TU_INSIGHT = """
Lo que mas me salto al revisar el tablero fue el margen: la tienda vende $1.78M pero solo se queda con 3.1% de utilidad, casi 9 puntos abajo del 12% esperado. Buscando a donde se iba el dinero, encontre que el problema no son las ventas sino los descuentos: las 384 ordenes con mas de 20% de descuento (el 38% del total) en vez de aportar restan unos $90,000, y al cruzarlo por categoria, Furniture es la mas golpeada con margen negativo de -6%. Si tuviera 10 segundos para decidir como gerente, mi recomendacion seria poner un tope de 20% al descuento y que cualquier excepcion la autorice un gerente, empezando por Furniture; con eso la utilidad sube bastante sin vender una sola unidad mas.
"""

# ============================================================
# COLORES
# ============================================================
AZUL   = "#6C7BFF"
ROJO   = "#F96167"
VERDE  = "#21A179"
MORADO = "#1E2761"

# ============================================================
# CARGAR DATOS
# ============================================================
@st.cache_data
def cargar_datos():
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"]  = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = cargar_datos()

# columnas opcionales (por si el dataset modificado no las trae)
HAY_SEGMENT  = "Segment" in df.columns
HAY_DISCOUNT = "Discount" in df.columns
HAY_STATE    = "State" in df.columns

# ============================================================
# TITULO Y AUTOR
# ============================================================
st.title("🏪 Superstore — Tablero Ejecutivo de Rentabilidad")
st.caption(f"Por **{TU_NOMBRE}** · ID {TU_ID} · LAD3012 · UDLAP Verano I 2026")
st.markdown(
    "Diagnostico de **donde se gana y donde se pierde dinero**, con foco en las "
    "palancas que un gerente puede mover esta semana. Usa los filtros del panel "
    "izquierdo; todas las metricas y graficas se recalculan al instante."
)
st.markdown("---")

# ============================================================
# FILTROS (sidebar)
# ============================================================
st.sidebar.header("🔎 Filtros")
regiones = st.sidebar.multiselect(
    "Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)
categorias = st.sidebar.multiselect(
    "Categoria", sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
if HAY_SEGMENT:
    segmentos = st.sidebar.multiselect(
        "Segmento", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique())
    )
anios = st.sidebar.multiselect(
    "Anio", sorted(df["Year"].unique()), default=sorted(df["Year"].unique())
)

# aplicar filtros
mask = df["Region"].isin(regiones) & df["Category"].isin(categorias) & df["Year"].isin(anios)
if HAY_SEGMENT:
    mask = mask & df["Segment"].isin(segmentos)
df_f = df[mask]

if len(df_f) == 0:
    st.warning("No hay datos con esos filtros. Selecciona al menos una opcion en cada filtro.")
    st.stop()

# ============================================================
# FUNCION PARA CALCULAR METRICAS
# ============================================================
def metricas(d):
    ventas   = d["Sales"].sum()
    ganancia = d["Profit"].sum()
    margen   = 100 * ganancia / ventas if ventas else 0
    ticket   = ventas / len(d) if len(d) else 0
    perdida  = 100 * (d["Profit"] < 0).mean() if len(d) else 0
    desc     = 100 * d["Discount"].mean() if HAY_DISCOUNT else None
    return ventas, ganancia, margen, ticket, perdida, desc

v_f, g_f, m_f, t_f, p_f, d_f = metricas(df_f)   # filtrado
v_h, g_h, m_h, t_h, p_h, d_h = metricas(df)     # historico (todo)

# ============================================================
# KPIs (6 tarjetas en 2 filas)
# ============================================================
c1, c2, c3 = st.columns(3)
c1.metric("Ventas totales", f"${v_f:,.0f}", help="Suma de Sales con los filtros aplicados")
c2.metric("Ganancia total", f"${g_f:,.0f}")
c3.metric("Margen %", f"{m_f:.1f}%", delta=f"{m_f - 12:.1f} pp vs benchmark 12%")

c4, c5, c6 = st.columns(3)
c4.metric("Ticket promedio", f"${t_f:,.0f}", delta=f"{t_f - t_h:+,.0f} vs historico")
c5.metric("Lineas con perdida", f"{p_f:.1f}%",
          delta=f"{p_f - p_h:+.1f} pp vs historico", delta_color="inverse")
if d_f is not None:
    c6.metric("Descuento promedio", f"{d_f:.1f}%",
              delta=f"{d_f - d_h:+.1f} pp vs historico", delta_color="inverse")

st.markdown("---")

# ============================================================
# 🚨 DIAGNOSTICO AUTOMATICO
# ============================================================
st.subheader("🚨 Diagnostico automatico")
da1, da2 = st.columns(2)

with da1:
    if HAY_DISCOUNT:
        agr  = df_f[df_f["Discount"] > 0.20]
        n    = len(agr)
        pct  = 100 * n / len(df_f) if len(df_f) else 0
        util = agr["Profit"].sum()
        st.error(
            f"**Descuentos agresivos:** las {n} lineas con descuento mayor a 20% "
            f"({pct:.0f}% del total) acumulan ${util:,.0f} de utilidad. "
            f"Es dinero que se regala."
        )
    else:
        st.info("Esta version del dataset no trae columna de descuento.")

with da2:
    cm = df_f.groupby("Category").agg(s=("Sales", "sum"), p=("Profit", "sum"))
    cm["margen"] = 100 * cm["p"] / cm["s"]
    peor   = cm["margen"].idxmin()
    peor_m = cm["margen"].min()
    st.error(
        f"**Categoria de bajo margen:** {peor} deja apenas {peor_m:.1f}% de margen "
        f"en el periodo filtrado — por debajo del resto. "
        f"Candidata a revision de precio y descuentos."
    )

st.markdown("---")

# ============================================================
# 🗺️ ¿DONDE ESTA EL DINERO? (Ventas vs Ganancia)
# ============================================================
st.subheader("🗺️ ¿Donde esta el dinero?")
gd1, gd2 = st.columns(2)

with gd1:
    st.markdown("**Por categoria de producto**")
    cat = df_f.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
    fig = go.Figure()
    fig.add_bar(x=cat["Category"], y=cat["Sales"],  name="Ventas",   marker_color=AZUL)
    fig.add_bar(x=cat["Category"], y=cat["Profit"], name="Ganancia", marker_color=VERDE)
    fig.update_layout(barmode="group", height=380, template="plotly_dark",
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

with gd2:
    if HAY_SEGMENT:
        st.markdown("**Por segmento de cliente**")
        seg = df_f.groupby("Segment")[["Sales", "Profit"]].sum().reset_index()
        fig = go.Figure()
        fig.add_bar(x=seg["Segment"], y=seg["Sales"],  name="Ventas",   marker_color=AZUL)
        fig.add_bar(x=seg["Segment"], y=seg["Profit"], name="Ganancia", marker_color=VERDE)
        fig.update_layout(barmode="group", height=380, template="plotly_dark",
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("**Por region**")
        reg = df_f.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
        fig = go.Figure()
        fig.add_bar(x=reg["Region"], y=reg["Sales"],  name="Ventas",   marker_color=AZUL)
        fig.add_bar(x=reg["Region"], y=reg["Profit"], name="Ganancia", marker_color=VERDE)
        fig.update_layout(barmode="group", height=380, template="plotly_dark",
                          legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 💸 EL FACTOR DESCUENTO
# ============================================================
if HAY_DISCOUNT:
    st.markdown("---")
    st.subheader("💸 El factor descuento: donde se rompe la rentabilidad")
    fd1, fd2 = st.columns(2)

    with fd1:
        st.markdown("**Margen por tramo de descuento**")
        bins   = [-0.01, 0.001, 0.10, 0.20, 0.30, 0.50, 0.80]
        labels = ["Sin desc.", "1-10%", "11-20%", "21-30%", "31-50%", "51-80%"]
        d2 = df_f.copy()
        d2["tramo"] = pd.cut(d2["Discount"], bins=bins, labels=labels)
        agg = d2.groupby("tramo", observed=True).agg(
            s=("Sales", "sum"),
            p=("Profit", "sum"),
            perdida=("Profit", lambda x: 100 * (x < 0).mean()),
        ).reset_index()
        agg["margen"] = 100 * agg["p"] / agg["s"]

        fig = go.Figure()
        fig.add_bar(x=agg["tramo"], y=agg["margen"], name="Margen %",
                    marker_color=[VERDE if v >= 0 else ROJO for v in agg["margen"]])
        fig.add_trace(go.Scatter(x=agg["tramo"], y=agg["perdida"],
                                 name="% lineas con perdida", yaxis="y2",
                                 line=dict(color=AZUL)))
        fig.update_layout(
            height=400, template="plotly_dark",
            yaxis=dict(title="Margen %"),
            yaxis2=dict(title="% lineas con perdida", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 El margen aguanta hasta ~20% de descuento; despues se desploma "
                   "y casi todas las ordenes pierden dinero. Conclusion: tope de 20%.")

    with fd2:
        if HAY_STATE:
            st.markdown("**La prueba por estado** (cada punto = un estado)")
            est = df_f.groupby("State").agg(
                ventas=("Sales", "sum"),
                ganancia=("Profit", "sum"),
                desc=("Discount", "mean"),
                region=("Region", "first"),
            ).reset_index()
            est["margen"] = 100 * est["ganancia"] / est["ventas"]
            est["desc"]   = 100 * est["desc"]
            fig = px.scatter(est, x="desc", y="margen", size="ventas", color="region",
                             hover_name="State", size_max=40, template="plotly_dark")
            fig.add_hline(y=0, line_dash="dash", line_color=ROJO)
            fig.update_layout(height=400, xaxis_title="Descuento promedio (%)",
                              yaxis_title="Margen (%)", legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig, use_container_width=True)
            st.caption("💡 A mas descuento promedio, menos margen: la relacion es casi "
                       "una linea recta. No es mala suerte, es la politica de descuentos.")

# ============================================================
# 📊 CONCENTRACION DE VENTAS POR ESTADO (PARETO)
# ============================================================
if HAY_STATE:
    st.markdown("---")
    st.subheader("📊 Concentracion de ventas por estado (analisis de Pareto)")
    par = df_f.groupby("State")["Sales"].sum().sort_values(ascending=False).reset_index()
    par["acum"] = 100 * par["Sales"].cumsum() / par["Sales"].sum()
    par15 = par.head(15)

    fig = go.Figure()
    fig.add_bar(x=par15["State"], y=par15["Sales"], name="Ventas", marker_color=AZUL)
    fig.add_trace(go.Scatter(x=par15["State"], y=par15["acum"],
                             name="% acumulado de ventas", yaxis="y2",
                             line=dict(color=VERDE)))
    fig.update_layout(
        height=420, template="plotly_dark",
        yaxis=dict(title="Ventas ($)"),
        yaxis2=dict(title="% acumulado", overlaying="y", side="right", range=[0, 100]),
        legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig, use_container_width=True)

    n20   = max(1, int(len(par) * 0.20))
    pct20 = par["acum"].iloc[n20 - 1]
    st.caption(f"💡 El 20% de los estados concentra el {pct20:.0f}% de las ventas. "
               f"El esfuerzo comercial y de inventario deberia priorizar ese puñado de mercados.")

# ============================================================
# 📈 VENTAS MENSUALES
# ============================================================
st.markdown("---")
st.subheader("📈 Ventas mensuales")
mensual = df_f.groupby("Month")["Sales"].sum().reset_index()
fig = px.line(mensual, x="Month", y="Sales", markers=True, template="plotly_dark")
fig.update_traces(line_color=AZUL)
fig.update_layout(height=380)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TABLA: TOP 10 ORDENES
# ============================================================
st.markdown("---")
st.subheader("Top 10 ordenes por venta")
top10 = (
    df_f.sort_values("Sales", ascending=False)
        .head(10)[["Order ID", "Order Date", "Category", "Region", "Sales", "Profit"]]
)
st.dataframe(top10, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================================
# PREGUNTAS GUIA
# ============================================================
with st.expander("🔍 Preguntas guia para encontrar tu insight"):
    st.markdown("""
**Juega con los filtros del sidebar mientras te haces estas preguntas:**

1. **Region menos rentable.** Deja solo una region a la vez. ¿Cual tiene el margen mas bajo?
2. **Categoria problema.** ¿Que categoria tiene margen sospechosamente bajo? ¿Que harias como gerente?
3. **Patron temporal.** En "Ventas mensuales", ¿hay meses pico o valle? ¿Que implica para inventario o staffing?
4. **Reto extra.** Si fueras CEO con 10 segundos para UNA decision, ¿cual seria y por que?

---
**Tu insight ideal:** una frase con TU hallazgo + una frase con TU recomendacion.
*"Descubri que [HALLAZGO con un dato concreto]. Recomiendo [ACCION concreta] para [RESULTADO esperado]."*
    """)

# ============================================================
# 💡 INSIGHT DE NEGOCIO
# ============================================================
st.subheader("💡 Insight de negocio")
st.info(TU_INSIGHT)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption("Dashboard preparado con pandas + plotly + Streamlit · LAD3012 D09")
