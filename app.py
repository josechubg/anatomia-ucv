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

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background: #0f1117; }
  .schema-card {
    background: #1a1d2e;
    border: 1px solid #3a3f5c;
    border-radius: 12px;
    padding: 18px 20px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.5;
    color: #e2e8f0;
    white-space: pre;
    overflow-x: auto;
    margin-bottom: 12px;
  }
  .nivel-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  .nivel-1 { background:#7c3aed22; color:#a78bfa; border:1px solid #7c3aed55; }
  .nivel-2 { background:#1d4ed822; color:#60a5fa; border:1px solid #1d4ed855; }
  .nivel-3 { background:#05966922; color:#34d399; border:1px solid #05966955; }
  .img-title {
    background: #1a1d2e;
    border-radius: 12px 12px 0 0;
    padding: 10px 16px;
    color: #a78bfa;
    font-weight: 600;
    font-size: 15px;
    border: 1px solid #3a3f5c;
    border-bottom: none;
  }
  .img-box {
    background: #13152a;
    border-radius: 0 0 12px 12px;
    padding: 16px;
    border: 1px solid #3a3f5c;
    border-top: none;
    text-align: center;
    margin-bottom: 20px;
  }
  .img-caption {
    color: #64748b;
    font-size: 11px;
    margin-top: 8px;
  }
  .pregunta-num {
    color: #a78bfa;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 4px;
  }
</style>
""", unsafe_allow_html=True)

# ── Imágenes por tema ─────────────────────────────────────────
# Todas de Wikipedia Commons (licencia libre)
_BASE = "https://commons.wikimedia.org/w/index.php?title=Special:Redirect/file/"
IMAGENES = {
    "manguito_rotador": {
        "url": _BASE + "Shoulderjoint.PNG&width=600",
        "titulo": "🦴 Manguito rotador — articulación del hombro",
        "caption": "Vista anterior. Identifica los 4 músculos del SITS: Supraespinoso, Infraespinoso, Teres minor, Subescapular."
    },
    "plexo_braquial": {
        "url": _BASE + "Brachial_plexus_color.svg&width=700",
        "titulo": "🧠 Plexo braquial (C5–T1)",
        "caption": "Raíces → Troncos → Divisiones → Fascículos → Nervios terminales"
    },
    "huesos_ms": {
        "url": _BASE + "Gray207.png&width=500",
        "titulo": "🦴 Húmero — hueso del miembro superior",
        "caption": "Cabeza, cuello anatómico, troquíter, troquín, surco bicipital, epicóndilos"
    },
    "huesos_mi": {
        "url": _BASE + "Gray243.png&width=500",
        "titulo": "🦴 Fémur — hueso del miembro inferior",
        "caption": "Cabeza, cuello, trocánteres, cóndilos medial y lateral"
    },
    "rodilla": {
        "url": _BASE + "Knee_diagram.svg&width=600",
        "titulo": "🦵 Articulación de la rodilla",
        "caption": "LCA, LCP, LCM, LCL y meniscos medial y lateral"
    },
    "huesos_craneo": {
        "url": _BASE + "Human_skull_side_simplified_%28bones%29.svg&width=650",
        "titulo": "💀 Huesos del cráneo — vista lateral",
        "caption": "Neurocráneo (8 huesos): frontal, parietales, occipital, temporales, esfenoides, etmoides"
    },
    "craneo_foramenes": {
        "url": _BASE + "Gray193.png&width=650",
        "titulo": "💀 Base del cráneo — forámenes",
        "caption": "Fosa anterior, media y posterior con sus forámenes"
    },
    "nervios_craneales": {
        "url": _BASE + "Cranial_nerve_components_english.svg&width=700",
        "titulo": "🧠 Los 12 nervios craneales",
        "caption": "Origen y función de cada par craneal"
    },
    "columna": {
        "url": _BASE + "Human_vertebral_column.svg&width=400",
        "titulo": "🦴 Columna vertebral",
        "caption": "Regiones cervical (7), torácica (12), lumbar (5), sacra y coccígea"
    },
    "atlas_axis": {
        "url": _BASE + "Gray86.png&width=500",
        "titulo": "🦴 Atlas (C1) y Axis (C2)",
        "caption": "C1 = flexoextensión (decir SÍ) · C2 = rotación (decir NO)"
    },
    "carpo_tarso": {
        "url": _BASE + "Gray219.png&width=500",
        "titulo": "🦴 Huesos del carpo",
        "caption": "Fila proximal: E-S-P-P / Fila distal: T-T-G-G (Escafoides, Semilunar, Piramidal, Pisiforme)"
    },
    "nervios_mmii": {
        "url": _BASE + "Gray826and831.PNG&width=550",
        "titulo": "🧠 Nervios del miembro inferior",
        "caption": "Plexo lumbar (femoral, obturador) y plexo sacro (ciático, tibial, peroneo)"
    },
    "articulacion_hombro": {
        "url": _BASE + "Gray327.png&width=550",
        "titulo": "🦴 Articulación glenohumeral",
        "caption": "Cabeza del húmero, cavidad glenoidea, labrum y ligamentos"
    },
    "musculos_ms": {
        "url": _BASE + "Gray413.png&width=500",
        "titulo": "💪 Músculos del brazo — compartimento anterior",
        "caption": "Bíceps braquial (cabeza larga y corta), braquial anterior, coracobraquial"
    },
    "musculos_mi": {
        "url": _BASE + "Gray430.png&width=500",
        "titulo": "🦵 Músculos del muslo — compartimento anterior",
        "caption": "Cuádriceps femoral: recto femoral, vasto medial, lateral e intermedio"
    },
    "arterias_ms_mi": {
        "url": _BASE + "Gray549.png&width=500",
        "titulo": "🩸 Arterias del miembro inferior",
        "caption": "Ilíaca externa → Femoral → Poplítea → Tibial anterior y posterior"
    },
    "ligamentos_columna": {
        "url": _BASE + "Gray301.png&width=550",
        "titulo": "🦴 Ligamentos de la columna vertebral",
        "caption": "LLA, LLP, ligamento amarillo, interespinosos y supraespinoso"
    },
    "disco_intervertebral": {
        "url": _BASE + "Gray_111_-_Vertebral_column.png&width=500",
        "titulo": "🦴 Disco intervertebral y vértebra",
        "caption": "Núcleo pulposo y anillo fibroso. Hernia posterolateral."
    },
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

# ── Helpers visuales ─────────────────────────────────────────
def badge_nivel(n):
    labels = {1: "⭐⭐⭐ Muy importante", 2: "⭐⭐ Importante", 3: "⭐ Poco preguntado"}
    return f'<span class="nivel-badge nivel-{n}">{labels[n]}</span>'

def mostrar_imagen(clave):
    """Muestra la imagen anatómica real del tema si existe."""
    if clave not in IMAGENES:
        return
    img = IMAGENES[clave]
    st.markdown(f'<div class="img-title">{img["titulo"]}</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="img-box">', unsafe_allow_html=True)
        try:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                st.image(img["url"], use_container_width=True)
            st.markdown(f'<p class="img-caption">📖 {img["caption"]}</p>',
                        unsafe_allow_html=True)
        except Exception:
            st.warning("⚠️ Imagen no disponible en este momento.")
        st.markdown('</div>', unsafe_allow_html=True)

def mostrar_esquema_texto(clave):
    """Muestra el esquema ASCII con estilo."""
    e = ESQUEMAS[clave]
    st.markdown(badge_nivel(e["nivel"]), unsafe_allow_html=True)
    st.markdown(f'<div class="schema-card">{e["esquema"]}</div>',
                unsafe_allow_html=True)

def mostrar_pregunta(p, idx, total, key_prefix):
    """Renderiza una pregunta con radio buttons."""
    st.markdown(f'<p class="pregunta-num">Pregunta {idx+1} de {total}</p>',
                unsafe_allow_html=True)
    st.markdown(f"**{p['enunciado']}**")
    opciones = [f"{k})  {v}" for k, v in p["opciones"].items()]
    return st.radio("", opciones, index=None, key=f"{key_prefix}_{idx}")

def feedback_respuesta(p, letra):
    """Muestra si la respuesta es correcta o no."""
    if letra == p["correcta"]:
        st.success(f"✅  ¡Correcto!")
    else:
        st.error(f"❌  Incorrecto — era  **{p['correcta']})** {p['opciones'][p['correcta']]}")
    st.info(f"💬  {p['exp']}")

def pantalla_final(results):
    c = sum(results)
    t = len(results)
    pct = int(c / t * 100) if t > 0 else 0
    if pct >= 80:
        st.balloons()
        st.success(f"🎉  {c}/{t} correctas — {pct}%  ¡Excelente!")
    elif pct >= 60:
        st.warning(f"👍  {c}/{t} correctas — {pct}%  Bien, sigue practicando")
    else:
        st.error(f"📚  {c}/{t} correctas — {pct}%  A repasar este tema")
    st.progress(pct / 100)

# ════════════════════════════════════════════════════════════
#  CABECERA
# ════════════════════════════════════════════════════════════
st.markdown("## 🧠 Anatomía UCV — 1º Medicina")
st.caption("MS · MI · Cráneo · Vértebras")

# ════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════
tab_esq, tab_test, tab_repaso, tab_chat = st.tabs(
    ["📋 Esquemas", "✏️ Test", "🔀 Repaso", "💬 Chat IA"]
)

# ────────────────────────────────────────────────────────────
#  TAB 1 — ESQUEMAS
# ────────────────────────────────────────────────────────────
with tab_esq:
    nivel_fil = st.radio(
        "Filtrar por nivel:",
        ["Todos", "⭐⭐⭐ Nivel 1", "⭐⭐ Nivel 2", "⭐ Nivel 3"],
        horizontal=True,
        key="esq_fil",
    )
    if "1" in nivel_fil:
        claves_fil = NIVELES[1]["claves"]
    elif "2" in nivel_fil:
        claves_fil = NIVELES[2]["claves"]
    elif "3" in nivel_fil:
        claves_fil = NIVELES[3]["claves"]
    else:
        claves_fil = list(ESQUEMAS.keys())

    mapa = {f"{'⭐'*ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k for k in claves_fil}
    sel = st.selectbox("Elige un tema:", list(mapa.keys()), key="esq_sel")
    clave_esq = mapa[sel]

    # Imagen anatómica real primero
    mostrar_imagen(clave_esq)

    # Luego el esquema ASCII como resumen
    with st.expander("📝 Ver esquema de texto"):
        mostrar_esquema_texto(clave_esq)

# ────────────────────────────────────────────────────────────
#  TAB 2 — TEST (imagen + preguntas)
# ────────────────────────────────────────────────────────────
with tab_test:
    mapa_t = {f"{'⭐'*ESQUEMAS[k]['nivel']}  {ESQUEMAS[k]['nombre']}": k for k in ESQUEMAS}
    sel_t = st.selectbox("Elige un tema:", list(mapa_t.keys()), key="test_sel")
    clave_t = mapa_t[sel_t]

    # Resetear si cambia el tema
    if st.session_state.test_clave != clave_t:
        st.session_state.test_active = False
        st.session_state.test_clave = clave_t
        st.session_state.test_idx = 0
        st.session_state.test_results = []
        st.session_state.test_answered = False

    # ── Imagen anatómica siempre visible ──
    mostrar_imagen(clave_t)

    # ── Esquema ASCII colapsable ──
    with st.expander("📝 Ver esquema de texto"):
        mostrar_esquema_texto(clave_t)

    st.divider()

    if not st.session_state.test_active:
        n = len(ESQUEMAS[clave_t]["preguntas"])
        st.info(f"**{n} preguntas** sobre este tema. Estudia la imagen de arriba antes de empezar.")
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
            st.progress(idx / len(pregs), text=f"Progreso: {idx}/{len(pregs)}")
            p = pregs[idx]

            if not st.session_state.test_answered:
                resp = mostrar_pregunta(p, idx, len(pregs), "test")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔ Confirmar", type="primary",
                                 disabled=resp is None, use_container_width=True):
                        letra = resp[0]
                        st.session_state.test_answered = True
                        st.session_state.test_last_letra = letra
                        st.session_state.test_results.append(letra == p["correcta"])
                        st.rerun()
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True):
                        st.session_state.test_idx += 1
                        st.rerun()
            else:
                feedback_respuesta(p, st.session_state.test_last_letra)
                if st.button("Siguiente →", type="primary", use_container_width=True):
                    st.session_state.test_idx += 1
                    st.session_state.test_answered = False
                    st.rerun()
        else:
            pantalla_final(st.session_state.test_results)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁 Repetir", use_container_width=True):
                    st.session_state.test_idx = 0
                    st.session_state.test_results = []
                    st.session_state.test_answered = False
                    st.rerun()
            with col2:
                if st.button("← Elegir otro tema", use_container_width=True):
                    st.session_state.test_active = False
                    st.rerun()

# ────────────────────────────────────────────────────────────
#  TAB 3 — REPASO ALEATORIO
# ────────────────────────────────────────────────────────────
with tab_repaso:
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

        if st.button("▶️ Empezar repaso", type="primary", use_container_width=True):
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
        pregs_r = st.session_state.repaso_pregs
        idx_r = st.session_state.repaso_idx

        if idx_r < len(pregs_r):
            st.progress(idx_r / len(pregs_r), text=f"{idx_r}/{len(pregs_r)}")
            clave_r, p_r = pregs_r[idx_r]

            # Imagen del tema actual en el repaso
            mostrar_imagen(clave_r)

            st.caption(f"📌  {ESQUEMAS[clave_r]['nombre']}")

            if not st.session_state.repaso_answered:
                resp_r = mostrar_pregunta(p_r, idx_r, len(pregs_r), "rep")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔ Confirmar", type="primary",
                                 disabled=resp_r is None,
                                 use_container_width=True, key="conf_r"):
                        letra_r = resp_r[0]
                        st.session_state.repaso_answered = True
                        st.session_state.repaso_last_letra = letra_r
                        st.session_state.repaso_results.append(letra_r == p_r["correcta"])
                        st.rerun()
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True, key="skip_r"):
                        st.session_state.repaso_idx += 1
                        st.rerun()
            else:
                feedback_respuesta(p_r, st.session_state.repaso_last_letra)
                if st.button("Siguiente →", type="primary",
                             use_container_width=True, key="next_r"):
                    st.session_state.repaso_idx += 1
                    st.session_state.repaso_answered = False
                    st.rerun()
        else:
            pantalla_final(st.session_state.repaso_results)
            if st.button("🔁 Nuevo repaso", type="primary", use_container_width=True):
                st.session_state.repaso_active = False
                st.rerun()

# ────────────────────────────────────────────────────────────
#  TAB 4 — CHAT CON IA
# ────────────────────────────────────────────────────────────
with tab_chat:
    st.caption("Pregunta cualquier duda sobre el temario de anatomía")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if pregunta := st.chat_input("Escribe tu duda de anatomía..."):
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
        if st.button("🗑️ Limpiar conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
