import streamlit as st
import anthropic
import random

from agente_anatomia import ESQUEMAS, NIVELES, SYSTEM_PROMPT

# ────────────────────────────────────────────────────────────
#  Configuración de página
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Anatomía UCV",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────
#  Session state
# ────────────────────────────────────────────────────────────
for key, default in {
    "chat_history": [],
    "test_active": False,
    "test_clave": None,
    "test_idx": 0,
    "test_results": [],
    "test_answered": False,
    "test_last_letra": None,
    "repaso_active": False,
    "repaso_pregs": [],
    "repaso_idx": 0,
    "repaso_results": [],
    "repaso_answered": False,
    "repaso_last_letra": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ────────────────────────────────────────────────────────────
#  Cliente Anthropic (cacheado por sesión)
# ────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()

# ────────────────────────────────────────────────────────────
#  Streaming para el chat
# ────────────────────────────────────────────────────────────
def stream_respuesta(messages):
    client = get_client()
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=600,
        system=[{"type": "text", "text": SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral"}}],
        messages=messages,
    ) as stream:
        yield from stream.text_stream

# ────────────────────────────────────────────────────────────
#  SIDEBAR
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🧠 Anatomía UCV")
    st.caption("1º Medicina · MS · MI · Cráneo · Vértebras")
    st.divider()

    modo = st.radio(
        "Modo de estudio:",
        ["📋 Esquemas", "✏️ Test por tema", "🔀 Repaso aleatorio", "💬 Chat con IA"],
    )

    st.divider()
    st.caption("**TEMAS DISPONIBLES**")
    for n, datos in NIVELES.items():
        st.caption(f"{'⭐' * n} Nivel {n}")
        for clave in datos["claves"]:
            st.caption(f"  · {ESQUEMAS[clave]['nombre'][:34]}")

# ────────────────────────────────────────────────────────────
#  MODO: ESQUEMAS
# ────────────────────────────────────────────────────────────
if modo == "📋 Esquemas":
    st.header("📋 Esquemas anatómicos")

    nivel_sel = st.radio(
        "Filtrar por nivel:",
        ["Todos", "⭐⭐⭐ Nivel 1 — Muy importantes",
         "⭐⭐ Nivel 2 — Importantes", "⭐ Nivel 3 — Poco preguntados"],
        horizontal=True,
    )

    if "Nivel 1" in nivel_sel:
        claves_filtradas = NIVELES[1]["claves"]
    elif "Nivel 2" in nivel_sel:
        claves_filtradas = NIVELES[2]["claves"]
    elif "Nivel 3" in nivel_sel:
        claves_filtradas = NIVELES[3]["claves"]
    else:
        claves_filtradas = list(ESQUEMAS.keys())

    opciones_nombre = {
        f"{'⭐' * ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k
        for k in claves_filtradas
    }
    sel = st.selectbox("Elige un tema:", list(opciones_nombre.keys()))
    clave = opciones_nombre[sel]
    esquema = ESQUEMAS[clave]

    col1, col2 = st.columns([3, 1])
    with col2:
        st.metric("Preguntas", len(esquema["preguntas"]))
        st.metric("Nivel", "⭐" * esquema["nivel"])

    st.code(esquema["esquema"], language=None)

    st.divider()
    if st.button("▶️ Hacer el test de este tema", type="primary", use_container_width=True):
        st.session_state.test_active = True
        st.session_state.test_clave = clave
        st.session_state.test_idx = 0
        st.session_state.test_results = []
        st.session_state.test_answered = False
        # Cambiar al modo test
        st.info("Cambia a **✏️ Test por tema** en el menú lateral para empezar.")

# ────────────────────────────────────────────────────────────
#  MODO: TEST POR TEMA
# ────────────────────────────────────────────────────────────
elif modo == "✏️ Test por tema":
    st.header("✏️ Test por tema")

    opciones_nombre = {
        f"{'⭐' * ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k
        for k in ESQUEMAS
    }
    sel = st.selectbox("Elige un tema:", list(opciones_nombre.keys()))
    clave_sel = opciones_nombre[sel]

    # Si cambia el tema, resetear el test
    if st.session_state.test_clave != clave_sel:
        st.session_state.test_active = False
        st.session_state.test_clave = clave_sel
        st.session_state.test_idx = 0
        st.session_state.test_results = []
        st.session_state.test_answered = False

    # Botón para ver esquema
    with st.expander("👁️ Ver esquema del tema"):
        st.code(ESQUEMAS[clave_sel]["esquema"], language=None)

    # Iniciar test
    if not st.session_state.test_active:
        n_pregs = len(ESQUEMAS[clave_sel]["preguntas"])
        st.info(f"Este tema tiene **{n_pregs} preguntas**.")
        if st.button("▶️ Empezar test", type="primary", use_container_width=True):
            st.session_state.test_active = True
            st.session_state.test_clave = clave_sel
            st.session_state.test_idx = 0
            st.session_state.test_results = []
            st.session_state.test_answered = False
            st.rerun()
    else:
        pregs = ESQUEMAS[st.session_state.test_clave]["preguntas"]
        idx = st.session_state.test_idx

        if idx < len(pregs):
            # Barra de progreso
            st.progress(idx / len(pregs),
                        text=f"Pregunta {idx + 1} de {len(pregs)}")

            p = pregs[idx]
            st.subheader(f"Pregunta {idx + 1}")
            st.write(p["enunciado"])
            st.divider()

            if not st.session_state.test_answered:
                opciones_lista = [f"**{k})** {v}" for k, v in p["opciones"].items()]
                respuesta_sel = st.radio(
                    "Selecciona tu respuesta:",
                    opciones_lista,
                    index=None,
                    key=f"test_q_{idx}",
                )

                col1, col2 = st.columns(2)
                with col1:
                    confirmar = st.button(
                        "✔ Confirmar",
                        type="primary",
                        disabled=respuesta_sel is None,
                        use_container_width=True,
                    )
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True):
                        st.session_state.test_idx += 1
                        st.rerun()

                if confirmar and respuesta_sel:
                    letra = respuesta_sel.split(")")[0].replace("**", "").strip()
                    st.session_state.test_answered = True
                    st.session_state.test_last_letra = letra
                    st.session_state.test_results.append(letra == p["correcta"])
                    st.rerun()
            else:
                letra = st.session_state.test_last_letra
                if letra == p["correcta"]:
                    st.success(f"✅ ¡CORRECTO!")
                else:
                    respuesta_correcta = p["opciones"][p["correcta"]]
                    st.error(f"❌ Incorrecto — La respuesta era: **{p['correcta']})** {respuesta_correcta}")

                st.info(f"💬 {p['exp']}")

                if st.button("Siguiente →", type="primary", use_container_width=True):
                    st.session_state.test_idx += 1
                    st.session_state.test_answered = False
                    st.rerun()
        else:
            # Pantalla de resultados
            results = st.session_state.test_results
            correctas = sum(results)
            total = len(results)
            pct = int(correctas / total * 100) if total > 0 else 0

            st.divider()
            if pct >= 80:
                st.balloons()
                st.success(f"🎉 ¡Excelente! {correctas}/{total} correctas ({pct}%)")
            elif pct >= 60:
                st.warning(f"👍 Bien. {correctas}/{total} correctas ({pct}%)")
            else:
                st.error(f"📚 A repasar. {correctas}/{total} correctas ({pct}%)")

            st.progress(pct / 100)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁 Repetir test", use_container_width=True):
                    st.session_state.test_idx = 0
                    st.session_state.test_results = []
                    st.session_state.test_answered = False
                    st.rerun()
            with col2:
                if st.button("📋 Ver esquema del tema", use_container_width=True):
                    st.session_state.test_active = False
                    st.rerun()

# ────────────────────────────────────────────────────────────
#  MODO: REPASO ALEATORIO
# ────────────────────────────────────────────────────────────
elif modo == "🔀 Repaso aleatorio":
    st.header("🔀 Repaso aleatorio")

    if not st.session_state.repaso_active:
        col1, col2 = st.columns(2)
        with col1:
            nivel_repaso = st.radio(
                "¿Qué nivel quieres repasar?",
                ["Todos los niveles", "⭐⭐⭐ Solo Nivel 1", "⭐⭐ Solo Nivel 2", "⭐ Solo Nivel 3"],
            )
        with col2:
            n_pregs = st.slider("Número de preguntas:", 5, 25, 12)

        if st.button("▶️ Empezar repaso", type="primary", use_container_width=True):
            if "Nivel 1" in nivel_repaso:
                claves = NIVELES[1]["claves"]
            elif "Nivel 2" in nivel_repaso:
                claves = NIVELES[2]["claves"]
            elif "Nivel 3" in nivel_repaso:
                claves = NIVELES[3]["claves"]
            else:
                claves = list(ESQUEMAS.keys())

            pool = [(k, p) for k in claves for p in ESQUEMAS[k]["preguntas"]]
            muestra = random.sample(pool, min(n_pregs, len(pool)))

            st.session_state.repaso_active = True
            st.session_state.repaso_pregs = muestra
            st.session_state.repaso_idx = 0
            st.session_state.repaso_results = []
            st.session_state.repaso_answered = False
            st.rerun()
    else:
        pregs = st.session_state.repaso_pregs
        idx = st.session_state.repaso_idx

        if idx < len(pregs):
            clave_p, p = pregs[idx]
            st.progress(idx / len(pregs),
                        text=f"Pregunta {idx + 1} de {len(pregs)}")
            st.caption(f"📌 Tema: *{ESQUEMAS[clave_p]['nombre']}*")
            st.subheader(f"Pregunta {idx + 1}")
            st.write(p["enunciado"])
            st.divider()

            if not st.session_state.repaso_answered:
                opciones_lista = [f"**{k})** {v}" for k, v in p["opciones"].items()]
                respuesta_sel = st.radio(
                    "Selecciona tu respuesta:",
                    opciones_lista,
                    index=None,
                    key=f"rep_q_{idx}",
                )

                col1, col2 = st.columns(2)
                with col1:
                    confirmar = st.button(
                        "✔ Confirmar",
                        type="primary",
                        disabled=respuesta_sel is None,
                        use_container_width=True,
                        key="confirm_rep",
                    )
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True, key="skip_rep"):
                        st.session_state.repaso_idx += 1
                        st.rerun()

                if confirmar and respuesta_sel:
                    letra = respuesta_sel.split(")")[0].replace("**", "").strip()
                    st.session_state.repaso_answered = True
                    st.session_state.repaso_last_letra = letra
                    st.session_state.repaso_results.append(letra == p["correcta"])
                    st.rerun()
            else:
                letra = st.session_state.repaso_last_letra
                if letra == p["correcta"]:
                    st.success("✅ ¡CORRECTO!")
                else:
                    resp_correcta = p["opciones"][p["correcta"]]
                    st.error(f"❌ Era: **{p['correcta']})** {resp_correcta}")

                st.info(f"💬 {p['exp']}")

                if st.button("Siguiente →", type="primary",
                             use_container_width=True, key="next_rep"):
                    st.session_state.repaso_idx += 1
                    st.session_state.repaso_answered = False
                    st.rerun()
        else:
            # Resultados del repaso
            results = st.session_state.repaso_results
            correctas = sum(results)
            total = len(results)
            pct = int(correctas / total * 100) if total > 0 else 0

            st.divider()
            if pct >= 80:
                st.balloons()
                st.success(f"🎉 ¡Excelente! {correctas}/{total} correctas ({pct}%)")
            elif pct >= 60:
                st.warning(f"👍 Bien. {correctas}/{total} correctas ({pct}%)")
            else:
                st.error(f"📚 A repasar. {correctas}/{total} correctas ({pct}%)")

            st.progress(pct / 100)

            if st.button("🔁 Nuevo repaso", type="primary", use_container_width=True):
                st.session_state.repaso_active = False
                st.rerun()

# ────────────────────────────────────────────────────────────
#  MODO: CHAT CON IA
# ────────────────────────────────────────────────────────────
elif modo == "💬 Chat con IA":
    st.header("💬 Chat con el profesor de Anatomía")
    st.caption("Pregunta cualquier duda sobre el temario: MS · MI · Cráneo · Vértebras")

    # Mostrar historial de mensajes
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input del usuario
    if pregunta := st.chat_input("Escribe tu pregunta de anatomía..."):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.write(pregunta)

        st.session_state.chat_history.append({"role": "user", "content": pregunta})

        # Preparar mensajes para la API
        mensajes_api = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history[-20:]
        ]

        # Mostrar respuesta con streaming
        with st.chat_message("assistant"):
            respuesta = st.write_stream(stream_respuesta(mensajes_api))

        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    # Botón para limpiar el chat
    if st.session_state.chat_history:
        if st.button("🗑️ Limpiar conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
