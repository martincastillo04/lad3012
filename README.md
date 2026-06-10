# Superstore Dashboard — Plantilla LAD3012 D09

Plantilla mínima para tu primer dashboard publicado.

## 📁 Qué hay en esta carpeta

| Archivo | Para qué |
|---|---|
| `app.py` | Tu dashboard Streamlit. Cambia las 3 variables marcadas y listo. |
| `requirements.txt` | Las 3 librerías que Streamlit Cloud necesita instalar. |
| `superstore.csv` | El dataset (descárgalo desde Kaggle si no está aquí). |

## ⚡ Correr local (probar antes de desplegar)

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre `http://localhost:8501` en tu navegador. Ahí ves tu dashboard.

## 🚀 Desplegar en `streamlit.io/cloud`

1. **Crea cuenta GitHub** gratis con tu correo institucional (`@udlap.mx`).
2. **Crea un repo público nuevo** llamado `lad3012-d09-dashboard` (o el nombre que quieras).
3. **Sube estos 3 archivos** al repo:
   - `app.py`
   - `requirements.txt`
   - `superstore.csv`
4. **Ve a [share.streamlit.io](https://share.streamlit.io)** → "Sign in with GitHub".
5. **Click "New app"** → selecciona tu repo → branch `main` → main file `app.py` → **Deploy**.
6. **Espera 2 minutos** mientras se instalan las librerías.
7. Te dará una URL tipo:
   ```
   https://TU-USUARIO-lad3012-d09-dashboard.streamlit.app
   ```
8. **Copia ESA URL** y pégala en Blackboard como tu entregable.

## 📥 Descargar el dataset Superstore

Si no tienes el CSV:

1. Cuenta gratis en [kaggle.com](https://kaggle.com) con tu correo UDLAP.
2. Busca **"Sample Superstore"** en el buscador.
3. Datasets recomendados:
   - `vivek468/superstore-dataset-final` (el más usado)
   - `rohitsahoo/sales-forecasting`
4. Click **Download**. Descomprime. Renómbralo a `superstore.csv` y ponlo junto a `app.py`.

## 🎯 Lo que califica (10 puntos)

Antes de entregar, valida que tu dashboard tenga:

- [ ] Link `.streamlit.app` funcional (2 pts)
- [ ] 3 KPIs con `st.metric()` (2 pts)
- [ ] 2 gráficos con `plotly` (2 pts)
- [ ] 1 filtro lateral con `st.sidebar` (1 pt)
- [ ] Tu insight de negocio escrito en `TU_INSIGHT` (2 pts)
- [ ] Defensa oral aleatoria (1 pt — solo si te toca)

## 🆘 Si algo falla

- **"ModuleNotFoundError: streamlit"** → falta `pip install streamlit`
- **"File not found: superstore.csv"** → el CSV no está en la carpeta donde corres `streamlit run app.py`
- **El dashboard se queda cargando** → revisa `requirements.txt` que tenga las 3 librerías
- **Streamlit Cloud no despliega** → revisa que el repo sea **público** y `app.py` esté en la raíz

## 🤖 Tip pro: usa la IA

Si no sabes cómo hacer algún cambio, pídele a Gemini/ChatGPT/Copilot:

> *"En Streamlit, ¿cómo agrego un selectbox lateral que filtre mi DataFrame `df` por la columna `Segment`?"*

Y pégale tu código actual. Ellos saben Streamlit muy bien.

---

**Dr. Francisco G. Rodríguez González** · LAD3012 · UDLAP Verano I 2026
