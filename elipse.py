import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Figuras 3D", layout="wide")
st.title("Elipsoide, esfera y plano en 3D")

# Selector fuera del formulario para cambiar de figura inmediatamente
figura = st.sidebar.selectbox(
    "Selecciona una figura",
    ["Elipsoide", "Esfera", "Plano"]
)

# Cada figura conserva sus últimos parámetros aplicados
iniciales = {
    "Elipsoide": dict(a=5.0, b=3.0, c=2.0),
    "Esfera": dict(a=4.0, b=4.0, c=4.0),
    "Plano": dict(a=8.0, b=6.0, c=1.0)
}

clave = f"datos_{figura}"

if clave not in st.session_state:
    st.session_state[clave] = {
        **iniciales[figura],
        "cx": 0.0,
        "cy": 0.0,
        "cz": 0.0,
        "angulo": 0.0
    }

datos = st.session_state[clave]

# El formulario evita recalcular mientras editas
with st.sidebar.form(f"formulario_{figura}"):
    st.subheader("Editar valores")

    if figura == "Elipsoide":
        a = st.number_input(
            "Semieje a", min_value=0.1, value=datos["a"]
        )
        b = st.number_input(
            "Semieje b", min_value=0.1, value=datos["b"]
        )
        c = st.number_input(
            "Semieje c", min_value=0.1, value=datos["c"]
        )

    elif figura == "Esfera":
        a = st.number_input(
            "Radio", min_value=0.1, value=datos["a"]
        )
        b = c = a

    else:
        a = st.number_input(
            "Ancho", min_value=0.1, value=datos["a"]
        )
        b = st.number_input(
            "Alto", min_value=0.1, value=datos["b"]
        )
        c = 1.0

    cx = st.number_input("Centro X", value=datos["cx"])
    cy = st.number_input("Centro Y", value=datos["cy"])
    cz = st.number_input("Centro Z", value=datos["cz"])

    angulo = st.number_input(
        "Inclinación alrededor de X (°)",
        value=datos["angulo"]
    )

    aplicar = st.form_submit_button("Actualizar gráfica")

if aplicar:
    nuevos = dict(
        a=a, b=b, c=c,
        cx=cx, cy=cy, cz=cz,
        angulo=angulo
    )

    if all(np.isfinite(valor) for valor in nuevos.values()):
        st.session_state[clave] = nuevos
    else:
        st.sidebar.error("Ingresa valores finitos.")

datos = st.session_state[clave]

a, b, c = datos["a"], datos["b"], datos["c"]
cx, cy, cz = datos["cx"], datos["cy"], datos["cz"]
angulo = np.radians(datos["angulo"] % 360)

if figura == "Plano":
    # Porción rectangular de un plano
    x, y = np.meshgrid(
        np.linspace(-a / 2, a / 2, 10),
        np.linspace(-b / 2, b / 2, 10)
    )
    z = np.zeros_like(x)
    limite = np.hypot(a / 2, b / 2) * 1.2
    color = "#f59e0b"

else:
    u, v = np.meshgrid(
        np.linspace(0, 2 * np.pi, 50),
        np.linspace(0, np.pi, 32)
    )

    x = a * np.sin(v) * np.cos(u)
    y = b * np.sin(v) * np.sin(u)
    z = c * np.cos(v)

    limite = max(a, b, c) * 1.2
    color = "#4169e1" if figura == "Elipsoide" else "#22a06b"

# Rotar y trasladar la superficie
xr = x + cx
yr = y * np.cos(angulo) - z * np.sin(angulo) + cy
zr = y * np.sin(angulo) + z * np.cos(angulo) + cz

grafica = go.Figure(
    data=[
        go.Surface(
            x=xr,
            y=yr,
            z=zr,
            surfacecolor=np.zeros_like(zr),
            colorscale=[[0, color], [1, color]],
            showscale=False,
            opacity=0.9
        )
    ]
)

grafica.update_layout(
    title=f"{figura} en 3D",
    height=700,
    margin=dict(l=0, r=0, t=50, b=0),
    uirevision=figura,
    scene=dict(
        xaxis=dict(title="X", range=[cx - limite, cx + limite]),
        yaxis=dict(title="Y", range=[cy - limite, cy + limite]),
        zaxis=dict(title="Z", range=[cz - limite, cz + limite]),
        aspectmode="cube"
    )
)

st.plotly_chart(grafica, use_container_width=True)

st.caption(
    "Arrastra la figura para girarla y usa la rueda para acercarte. "
    "Edita los valores del panel izquierdo y pulsa Actualizar gráfica."
)

if figura == "Plano":
    st.info("Se muestra una porción del plano; el plano matemático es infinito.")