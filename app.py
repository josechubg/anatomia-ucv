import streamlit as st
import anthropic
import random

from agente_anatomia import ESQUEMAS, NIVELES, SYSTEM_PROMPT

st.set_page_config(
    page_title="Anatomía UCV",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS global ──────────────────────────────────────────────
st.markdown("""
<style>
  /* Fondo oscuro suave */
  .stApp { background: #0f1117; }

  /* Tarjeta de esquema */
  .schema-card {
    background: #1a1d2e;
    border: 1px solid #3a3f5c;
    border-radius: 12px;
    padding: 18px 20px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 1.5;
    color: #e2e8f0;
    white-space: pre;
    overflow-x: auto;
  }

  /* Badge de nivel */
  .nivel-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
  }
  .nivel-1 { background: #7c3aed22; color: #a78bfa; border: 1px solid #7c3aed55; }
  .nivel-2 { background: #1d4ed822; color: #60a5fa; border: 1px solid #1d4ed855; }
  .nivel-3 { background: #05966922; color: #34d399; border: 1px solid #05966955; }

  /* Tarjeta de pregunta */
  .pregunta-card {
    background: #1a1d2e;
    border-left: 4px solid #7c3aed;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
    color: #e2e8f0;
    font-size: 16px;
  }

  /* Imagen anatómica */
  .img-caption {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 6px;
  }

  /* Resultado correcto/incorrecto */
  div[data-testid="stAlert"] { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Imágenes anatómicas (Wikipedia Commons) ─────────────────
IMAGENES = {
    "plexo_braquial": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/"
        "Brachial_plexus_color.svg/800px-Brachial_plexus_color.svg.png",
        "Plexo braquial — Wikipedia Commons"
    ),
    "huesos_ms": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/"
        "Arm_bones.jpg/400px-Arm_bones.jpg",
        "Huesos del miembro superior"
    ),
    "huesos_mi": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/"
        "Leg_bones.jpg/400px-Leg_bones.jpg",
        "Huesos del miembro inferior"
    ),
    "rodilla": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/"
        "Knee_diagram.svg/600px-Knee_diagram.svg.png",
        "Articulación de la rodilla — ligamentos"
    ),
    "manguito_rotador": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/"
        "Shoulder_joint.svg/600px-Shoulder_joint.svg.png",
        "Articulación del hombro"
    ),
    "huesos_craneo": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/"
        "Head_skull.jpg/600px-Head_skull.jpg",
        "Cráneo — vista lateral"
    ),
    "craneo_foramenes": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/"
        "Cranial_bones_en.svg/800px-Cranial_bones_en.svg.png",
        "Base del cráneo — forámenes"
    ),
    "nervios_craneales": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/"
        "Cranial_nerve_components_english.svg/800px-Cranial_nerve_components_english.svg.png",
        "Nervios craneales"
    ),
    "columna": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/"
        "Human_vertebral_column.svg/300px-Human_vertebral_column.svg.png",
        "Columna vertebral — regiones y curvaturas"
    ),
    "carpo_tarso": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/"
        "Carpus.svg/400px-Carpus.svg.png",
        "Huesos del carpo"
    ),
    "nervios_mmii": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/"
        "Nerves_of_the_right_lower_extremity.jpg/400px-Nerves_of_the_right_lower_extremity.jpg",
        "Nervios del miembro inferior"
    ),
    "atlas_axis": (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/"
        "Atlas_%28C1%29_from_above_-_animation.gif/300px-Atlas_%28C1%29_from_above_-_animation.gif",
        "Atlas (C1) visto desde arriba"
    ),
}

# ── Session state ────────────────────────────────────────────
for k, v in {
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
    if k not in st.session_state:
        st.session_state[k] = v

# ── Cliente Anthropic ────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()

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

# ── Helpers ──────────────────────────────────────────────────
def badge_nivel(n):
    etiquetas = {1: "⭐⭐⭐ Muy importante", 2: "⭐⭐ Importante", 3: "⭐ Poco preguntado"}
    return f'<span class="nivel-badge nivel-{n}">{etiquetas[n]}</span>'

def mostrar_esquema_card(clave):
    e = ESQUEMAS[clave]
    st.markdown(badge_nivel(e["nivel"]), unsafe_allow_html=True)
    st.markdown(f'<div class="schema-card">{e["esquema"]}</div>', unsafe_allow_html=True)
    if clave in IMAGENES:
        url, caption = IMAGENES[clave]
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            try:
                st.image(url, use_container_width=True)
                st.markdown(f'<p class="img-caption">{caption}</p>', unsafe_allow_html=True)
            except Exception:
                pass

def mostrar_pregunta_activa(p, idx, total, prefix):
    st.markdown(f'<div class="pregunta-card">Pregunta {idx+1} de {total}<br><br>{p["enunciado"]}</div>',
                unsafe_allow_html=True)
    opciones_lista = [f"{k})  {v}" for k, v in p["opciones"].items()]
    return st.radio("", opciones_lista, index=None, key=f"{prefix}_q_{idx}")

def mostrar_resultado_pregunta(p, letra):
    if letra == p["correcta"]:
        st.success(f"✅  ¡Correcto!")
    else:
        resp_ok = p["opciones"][p["correcta"]]
        st.error(f"❌  Incorrecto — era  **{p['correcta']})** {resp_ok}")
    st.info(f"💬  {p['exp']}")

def pantalla_resultados(results, prefix):
    c = sum(results)
    t = len(results)
    pct = int(c / t * 100) if t > 0 else 0
    if pct >= 80:
        st.balloons()
        st.success(f"🎉  {c}/{t} correctas — {pct}%")
    elif pct >= 60:
        st.warning(f"👍  {c}/{t} correctas — {pct}%")
    else:
        st.error(f"📚  {c}/{t} correctas — {pct}%  · ¡A repasar!")
    st.progress(pct / 100)
    return pct

# ════════════════════════════════════════════════════════════
#  CABECERA
# ════════════════════════════════════════════════════════════
st.markdown("## 🧠 Anatomía UCV")
st.caption("1º Medicina · Miembro Superior · Miembro Inferior · Cráneo · Vértebras")
st.divider()

# ════════════════════════════════════════════════════════════
#  TABS — NAVEGACIÓN PRINCIPAL (visible en iPad)
# ════════════════════════════════════════════════════════════
tab_esq, tab_test, tab_repaso, tab_chat = st.tabs(
    ["📋  Esquemas", "✏️  Test", "🔀  Repaso", "💬  Chat IA"]
)

# ────────────────────────────────────────────────────────────
#  TAB 1 — ESQUEMAS
# ────────────────────────────────────────────────────────────
with tab_esq:
    st.subheader("Esquemas anatómicos")

    nivel_fil = st.radio(
        "Filtrar:",
        ["Todos", "⭐⭐⭐ Nivel 1", "⭐⭐ Nivel 2", "⭐ Nivel 3"],
        horizontal=True,
        key="fil_nivel",
    )
    if "1" in nivel_fil:
        claves_fil = NIVELES[1]["claves"]
    elif "2" in nivel_fil:
        claves_fil = NIVELES[2]["claves"]
    elif "3" in nivel_fil:
        claves_fil = NIVELES[3]["claves"]
    else:
        claves_fil = list(ESQUEMAS.keys())

    opciones_map = {
        f"{'⭐'*ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k
        for k in claves_fil
    }
    sel = st.selectbox("Elige un tema:", list(opciones_map.keys()), key="esq_sel")
    clave_esq = opciones_map[sel]

    mostrar_esquema_card(clave_esq)

    st.divider()
    n_pregs = len(ESQUEMAS[clave_esq]["preguntas"])
    st.caption(f"Este tema tiene **{n_pregs} preguntas** en el test.")

# ────────────────────────────────────────────────────────────
#  TAB 2 — TEST
# ────────────────────────────────────────────────────────────
with tab_test:
    st.subheader("Test por tema")

    opciones_map_t = {
        f"{'⭐'*ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k
        for k in ESQUEMAS
    }
    sel_t = st.selectbox("Elige un tema:", list(opciones_map_t.keys()), key="test_sel")
    clave_sel_t = opciones_map_t[sel_t]

    if st.session_state.test_clave != clave_sel_t:
        st.session_state.test_active = False
        st.session_state.test_clave = clave_sel_t
        st.session_state.test_idx = 0
        st.session_state.test_results = []
        st.session_state.test_answered = False

    with st.expander("👁️  Ver esquema del tema"):
        mostrar_esquema_card(clave_sel_t)

    if not st.session_state.test_active:
        n = len(ESQUEMAS[clave_sel_t]["preguntas"])
        st.info(f"**{n} preguntas** sobre este tema.")
        if st.button("▶️  Empezar test", type="primary", use_container_width=True):
            st.session_state.test_active = True
            st.session_state.test_idx = 0
            st.session_state.test_results = []
            st.session_state.test_answered = False
            st.rerun()
    else:
        pregs = ESQUEMAS[st.session_state.test_clave]["preguntas"]
        idx = st.session_state.test_idx

        if idx < len(pregs):
            st.progress(idx / len(pregs), text=f"{idx}/{len(pregs)} preguntas")
            p = pregs[idx]

            if not st.session_state.test_answered:
                resp = mostrar_pregunta_activa(p, idx, len(pregs), "test")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔  Confirmar", type="primary",
                                 disabled=resp is None, use_container_width=True):
                        letra = resp[0]
                        st.session_state.test_answered = True
                        st.session_state.test_last_letra = letra
                        st.session_state.test_results.append(letra == p["correcta"])
                        st.rerun()
                with col2:
                    if st.button("⏭  Saltar", use_container_width=True):
                        st.session_state.test_idx += 1
                        st.rerun()
            else:
                mostrar_resultado_pregunta(p, st.session_state.test_last_letra)
                if st.button("Siguiente →", type="primary", use_container_width=True):
                    st.session_state.test_idx += 1
                    st.session_state.test_answered = False
                    st.rerun()
        else:
            pantalla_resultados(st.session_state.test_results, "test")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁  Repetir", use_container_width=True):
                    st.session_state.test_idx = 0
                    st.session_state.test_results = []
                    st.session_state.test_answered = False
                    st.rerun()
            with col2:
                if st.button("📋  Volver", use_container_width=True):
                    st.session_state.test_active = False
                    st.rerun()

# ────────────────────────────────────────────────────────────
#  TAB 3 — REPASO ALEATORIO
# ────────────────────────────────────────────────────────────
with tab_repaso:
    st.subheader("Repaso aleatorio")

    if not st.session_state.repaso_active:
        col1, col2 = st.columns(2)
        with col1:
            nivel_rep = st.radio(
                "Nivel:",
                ["Todos", "⭐⭐⭐ Nivel 1", "⭐⭐ Nivel 2", "⭐ Nivel 3"],
                key="rep_nivel",
            )
        with col2:
            n_rep = st.slider("Preguntas:", 5, 25, 12, key="rep_n")

        if st.button("▶️  Empezar repaso", type="primary", use_container_width=True):
            if "1" in nivel_rep:
                claves_r = NIVELES[1]["claves"]
            elif "2" in nivel_rep:
                claves_r = NIVELES[2]["claves"]
            elif "3" in nivel_rep:
                claves_r = NIVELES[3]["claves"]
            else:
                claves_r = list(ESQUEMAS.keys())

            pool = [(k, p) for k in claves_r for p in ESQUEMAS[k]["preguntas"]]
            muestra = random.sample(pool, min(n_rep, len(pool)))
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
            st.progress(idx / len(pregs), text=f"{idx}/{len(pregs)} preguntas")
            clave_r, p = pregs[idx]
            st.caption(f"📌  {ESQUEMAS[clave_r]['nombre']}")

            if not st.session_state.repaso_answered:
                resp = mostrar_pregunta_activa(p, idx, len(pregs), "rep")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔  Confirmar", type="primary",
                                 disabled=resp is None, use_container_width=True, key="conf_r"):
                        letra = resp[0]
                        st.session_state.repaso_answered = True
                        st.session_state.repaso_last_letra = letra
                        st.session_state.repaso_results.append(letra == p["correcta"])
                        st.rerun()
                with col2:
                    if st.button("⏭  Saltar", use_container_width=True, key="skip_r"):
                        st.session_state.repaso_idx += 1
                        st.rerun()
            else:
                mostrar_resultado_pregunta(p, st.session_state.repaso_last_letra)
                if st.button("Siguiente →", type="primary",
                             use_container_width=True, key="next_r"):
                    st.session_state.repaso_idx += 1
                    st.session_state.repaso_answered = False
                    st.rerun()
        else:
            pantalla_resultados(st.session_state.repaso_results, "rep")
            if st.button("🔁  Nuevo repaso", type="primary", use_container_width=True):
                st.session_state.repaso_active = False
                st.rerun()

# ────────────────────────────────────────────────────────────
#  TAB 4 — CHAT CON IA
# ────────────────────────────────────────────────────────────
with tab_chat:
    st.subheader("Chat con el profesor")
    st.caption("Pregunta cualquier duda sobre el temario")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if pregunta := st.chat_input("Escribe tu pregunta de anatomía..."):
        with st.chat_message("user"):
            st.write(pregunta)
        st.session_state.chat_history.append({"role": "user", "content": pregunta})

        mensajes_api = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history[-20:]
        ]
        with st.chat_message("assistant"):
            respuesta = st.write_stream(stream_respuesta(mensajes_api))
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    if st.session_state.chat_history:
        if st.button("🗑️  Limpiar conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
