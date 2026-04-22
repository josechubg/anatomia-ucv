import streamlit as st
import anthropic
import random
import json
import uuid
import base64
from datetime import datetime
from pathlib import Path
from streamlit_js_eval import streamlit_js_eval

from banco_preguntas import BANCO, NIVELES, CATEGORIAS
from banco_ucv import BANCO_UCV, NIVELES_UCV, CATEGORIAS_UCV

st.set_page_config(
    page_title="CarloTest — Anatomía UCV",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FALLOS_DIR = Path(__file__).parent / "usuarios"
FALLOS_DIR.mkdir(exist_ok=True)

def get_fallos_path(usuario: str) -> Path:
    nombre_seguro = "".join(c for c in usuario.lower().strip() if c.isalnum() or c in "_-")
    return FALLOS_DIR / f"{nombre_seguro}.json"

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #07090f !important;
  }
  .block-container { padding-top: 1.5rem !important; max-width: 860px !important; }

  /* ── HERO ── */
  .hero {
    display: flex;
    align-items: center;
    gap: 28px;
    background: linear-gradient(135deg, #10142a 0%, #0c0f1e 100%);
    border: 1px solid #1e2540;
    border-radius: 24px;
    padding: 32px 36px;
    margin-bottom: 28px;
    box-shadow: 0 24px 60px rgba(124,58,237,0.12);
  }
  .hero-text { flex: 1; min-width: 0; }
  .hero-badge {
    display: inline-block;
    background: #7c3aed18;
    color: #a78bfa;
    border: 1px solid #7c3aed44;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 14px;
  }
  .hero-title {
    font-size: 34px;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 6px 0;
    line-height: 1.1;
    letter-spacing: -0.5px;
  }
  .hero-sub {
    color: #64748b;
    font-size: 13px;
    font-weight: 500;
    margin: 0 0 22px 0;
  }
  .hero-stats { display: flex; gap: 10px; flex-wrap: wrap; }
  .stat-pill {
    border-radius: 12px;
    padding: 10px 18px;
    text-align: center;
    min-width: 72px;
  }
  .sp-purple { background:#7c3aed18; border:1px solid #7c3aed44; }
  .sp-blue   { background:#1d4ed818; border:1px solid #1d4ed844; }
  .sp-red    { background:#ef444418; border:1px solid #ef444444; }
  .stat-num  { display:block; font-size:22px; font-weight:800; line-height:1; margin-bottom:2px; }
  .sp-purple .stat-num { color:#a78bfa; }
  .sp-blue   .stat-num { color:#60a5fa; }
  .sp-red    .stat-num { color:#f87171; }
  .stat-label { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:#475569; }
  .update-badge {
    display: inline-block;
    margin-top: 12px;
    background: #0f172a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 5px 12px;
    font-size: 11px;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: 0.3px;
  }
  .hero-img-wrap { flex: 0 0 190px; }
  .hero-img-wrap img {
    width: 100%;
    border-radius: 18px;
    box-shadow: 0 16px 48px rgba(124,58,237,0.35);
    display: block;
  }
  @media (max-width: 640px) {
    .block-container { padding: 0.5rem 0.75rem !important; }
    .hero { flex-direction: column-reverse; padding: 20px 18px; gap: 16px; border-radius: 18px; }
    .hero-img-wrap { flex: none; width: 110px; align-self: center; }
    .hero-img-wrap img { border-radius: 14px; }
    .hero-title { font-size: 24px; }
    .hero-sub { font-size: 11px; margin-bottom: 14px; }
    .hero-badge { font-size: 10px; padding: 3px 10px; }
    .stat-pill { padding: 8px 12px; min-width: 60px; }
    .stat-num { font-size: 18px; }
    .stTabs [data-baseweb="tab"] { font-size: 11px !important; padding: 7px 8px !important; }
    .stButton > button { font-size: 14px !important; padding: 10px 8px !important; min-height: 46px !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { font-size: 14px !important; }
    div[data-testid="stRadio"] label { font-size: 14px !important; min-height: 44px !important; display: flex !important; align-items: center !important; }
    .fallo-card { padding: 12px 14px; }
    .flashcard-front { padding: 24px 16px; }
    .flashcard-back { padding: 18px 16px; }
  }

  /* ── NIVELES ── */
  .nivel-badge {
    display: inline-block; padding: 3px 11px; border-radius: 20px;
    font-size: 11px; font-weight: 700; margin-right: 6px; letter-spacing: 0.2px;
  }
  .n1 { background:#7c3aed1a; color:#a78bfa; border:1px solid #7c3aed55; }
  .n2 { background:#1d4ed81a; color:#60a5fa; border:1px solid #1d4ed855; }
  .n3 { background:#0596691a; color:#34d399; border:1px solid #05966955; }

  /* ── CONCEPTO TAG ── */
  .concepto-tag {
    display: inline-block; background: #1a2035; color: #94a3b8;
    border: 1px solid #2a3050; border-radius: 6px;
    padding: 2px 9px; font-size: 11px; font-weight: 500;
  }

  /* ── PREGUNTA ── */
  .pregunta-num { color:#a78bfa; font-size:12px; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; }

  /* ── FALLO CARD ── */
  .fallo-card {
    background: #100d14;
    border: 1px solid #2a1a1a;
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
  }

  /* ── FLASHCARD ── */
  .flashcard-front {
    background: linear-gradient(135deg, #13182e, #0f1220);
    border: 2px solid #7c3aed66;
    border-radius: 20px; padding: 36px 28px;
    text-align: center; min-height: 160px;
    box-shadow: 0 8px 32px rgba(124,58,237,0.15);
  }
  .flashcard-back {
    background: linear-gradient(135deg, #0d1a14, #0a1510);
    border: 2px solid #10b98166;
    border-radius: 20px; padding: 28px;
    min-height: 140px;
    box-shadow: 0 8px 32px rgba(16,185,129,0.10);
    margin-top: 12px;
  }

  /* ── REVISIÓN ── */
  .rev-card {
    background: #0e1120;
    border: 1px solid #1e2540;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
  }
  .rev-wrong { color: #f87171; font-size: 13px; font-weight: 600; }
  .rev-right { color: #34d399; font-size: 13px; font-weight: 600; }
  .rev-neutral { color: #475569; font-size: 13px; }

  /* ── BUTTONS ── */
  .stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
  }
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.35) !important;
  }
  .stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 20px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
  }

  /* ── PROGRESS ── */
  div[data-testid="stProgressBar"] > div { background: #1e2540 !important; border-radius: 99px; }
  div[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #7c3aed, #a78bfa) !important; border-radius: 99px; }

  /* ── TABS ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #0c0f1e !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid #1e2540 !important;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 8px 12px !important;
  }
  .stTabs [aria-selected="true"] {
    background: #7c3aed22 !important;
    color: #a78bfa !important;
    border: 1px solid #7c3aed44 !important;
  }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 20px !important; }

  /* ── INPUTS ── */
  .stRadio > label { color: #94a3b8 !important; font-size: 13px !important; }
  .stSelectbox > label, .stSlider > label { color: #94a3b8 !important; font-size: 13px !important; }
  div[data-testid="stMarkdownContainer"] p { color: #cbd5e1; }


  /* ── EXPANDER texto visible ── */
  .streamlit-expanderContent {
    background: #0e1120 !important;
    border: 1px solid #1e2540 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
  }
  .streamlit-expanderContent p,
  .streamlit-expanderContent li,
  .streamlit-expanderContent strong,
  .streamlit-expanderContent em,
  .streamlit-expanderContent span {
    color: #cbd5e1 !important;
  }
  .streamlit-expanderContent h1,
  .streamlit-expanderContent h2,
  .streamlit-expanderContent h3 {
    color: #e2e8f0 !important;
  }
  .streamlit-expanderContent code {
    color: #a78bfa !important;
    background: #1e1a2e !important;
  }
  /* Header del expander */
  .streamlit-expanderHeader {
    background: #0c0f1e !important;
    border: 1px solid #1e2540 !important;
    border-radius: 10px !important;
    color: #a78bfa !important;
    font-weight: 600 !important;
  }
  .streamlit-expanderHeader:hover {
    border-color: #7c3aed !important;
    color: #c4b5fd !important;
  }
  /* ── DIVIDER ── */
  hr { border-color: #1e2540 !important; margin: 16px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Persistencia de fallos ───────────────────────────────────────
def cargar_fallos(usuario: str = "default") -> list:
    path = get_fallos_path(usuario)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def _ls_key(usuario: str) -> str:
    nombre = "".join(c for c in usuario.lower().strip() if c.isalnum() or c in "_-")
    return f"carlotest_v1_{nombre}"

def guardar_fallos(fallos: list, usuario: str = "default"):
    # Guardar en archivo local (funciona en desarrollo local)
    try:
        path = get_fallos_path(usuario)
        path.write_text(json.dumps(fallos, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
    # Guardar en localStorage del navegador (persiste en Streamlit Cloud)
    try:
        payload = base64.b64encode(
            json.dumps(fallos, ensure_ascii=False).encode()
        ).decode()
        st.session_state._ls_save_n = st.session_state.get("_ls_save_n", 0) + 1
        streamlit_js_eval(
            js_expressions=(
                f"(function(){{"
                f"localStorage.setItem('{_ls_key(usuario)}', atob('{payload}'));"
                f"return true;}})();"
            ),
            key=f"ls_save_{usuario}_{st.session_state._ls_save_n}",
        )
    except Exception:
        pass

def registrar_fallo(pregunta: dict, tema: str, respuesta_dada: str, generada_ia: bool = False):
    fallos = st.session_state.fallos
    usuario = st.session_state.get("usuario", "default")
    pid = pregunta["id"]
    for f in fallos:
        if f["pregunta_id"] == pid and not f.get("aprendida"):
            f["veces_fallada"] += 1
            f["ultima_fecha"] = datetime.now().strftime("%Y-%m-%d")
            guardar_fallos(fallos, usuario)
            return
    fallos.append({
        "uid": str(uuid.uuid4())[:8],
        "pregunta_id": pid,
        "tema": tema,
        "tema_nombre": BANCO[tema]["nombre"],
        "nivel": BANCO[tema]["nivel"],
        "concepto": pregunta.get("concepto", ""),
        "enunciado": pregunta["enunciado"],
        "opciones": pregunta["opciones"],
        "correcta": pregunta["correcta"],
        "exp": pregunta["exp"],
        "respuesta_dada": respuesta_dada,
        "veces_fallada": 1,
        "primera_fecha": datetime.now().strftime("%Y-%m-%d"),
        "ultima_fecha": datetime.now().strftime("%Y-%m-%d"),
        "aprendida": False,
        "generada_ia": generada_ia,
    })
    guardar_fallos(fallos, st.session_state.get("usuario", "default"))

# ── Session state ────────────────────────────────────────────────
defaults = {
    "fallos": [],
    "usuario": "",
    "usuario_confirmado": False,
    "chat_history": [],
    "test_active": False,
    "test_tema": None,
    "test_pregs": [],
    "test_idx": 0,
    "test_results": [],
    "test_answered": False,
    "test_last_letra": None,
    "test_errores": [],
    "test_revision": False,
    "ft_active": False,
    "ft_pregs": [],
    "ft_idx": 0,
    "ft_results": [],
    "ft_answered": False,
    "ft_last_letra": None,
    "ft_errores": [],
    "ft_revision": False,
    "flash_idx": 0,
    "flash_revealed": False,
    "gen_loading": False,
    # ── UCV ──
    "ucv_active": False,
    "ucv_pregs": [],
    "ucv_idx": 0,
    "ucv_results": [],
    "ucv_answered": False,
    "ucv_last_letra": None,
    "ucv_errores": [],
    "ucv_n_fallos": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Cliente Anthropic ────────────────────────────────────────────
@st.cache_resource
def get_client():
    return anthropic.Anthropic()

# ── Helpers ──────────────────────────────────────────────────────
def badge(nivel):
    etiq = {1: "⭐⭐⭐ Nivel 1", 2: "⭐⭐ Nivel 2", 3: "⭐ Nivel 3"}
    return f'<span class="nivel-badge n{nivel}">{etiq[nivel]}</span>'

def mostrar_pregunta(p, idx, total, key_prefix):
    st.markdown(f'<p class="pregunta-num">Pregunta {idx+1} / {total}</p>', unsafe_allow_html=True)
    tema_key = key_prefix.split("_")[0] if "_" in key_prefix else None
    nivel_n = BANCO.get(tema_key, {}).get("nivel", 1) if tema_key else 1
    st.markdown(
        f'{badge(nivel_n)} <span class="concepto-tag">🔑 {p.get("concepto","")}</span>',
        unsafe_allow_html=True
    )
    st.markdown(f"**{p['enunciado']}**")
    opciones = [f"{k})  {v}" for k, v in p["opciones"].items()]
    return st.radio("", opciones, index=None, key=f"{key_prefix}_{idx}")

def feedback(p, letra):
    """Muestra correcto/incorrecto + explicación extendida con Claude."""
    acertada = letra == p["correcta"]
    if acertada:
        st.success("✅  ¡Correcto!")
    else:
        st.error(f"❌  Incorrecto — era  **{p['correcta']})** {p['opciones'][p['correcta']]}")

    opciones_texto = "\n".join(f"  {k}) {v}" for k, v in p["opciones"].items())
    falsas = [k for k in p["opciones"] if k != p["correcta"]]
    falsas_str = ", ".join(falsas)

    prompt = f"""Eres profesor de Anatomía Humana para estudiantes de 1º de Medicina UCV. Acaban de responder esta pregunta tipo test:

PREGUNTA: {p['enunciado']}
OPCIONES:
{opciones_texto}
RESPUESTA CORRECTA: {p['correcta']}) {p['opciones'][p['correcta']]}
RESPUESTA DEL ALUMNO: {letra}) {p['opciones'].get(letra, '—')}
EXPLICACIÓN BASE: {p['exp']}

Genera una explicación didáctica con este formato EXACTO. Usa markdown con texto en color claro. Sé conciso pero completo:

**✅ Por qué {p['correcta']}) es correcta**
[1-2 frases explicando el mecanismo anatómico clave. Texto en color normal, visible.]

**❌ Por qué las otras opciones son incorrectas**
- **{falsas[0] if len(falsas)>0 else ""}**) [una frase explicando por qué es incorrecta]
- **{falsas[1] if len(falsas)>1 else ""}**) [una frase explicando por qué es incorrecta]
- **{falsas[2] if len(falsas)>2 else ""}**) [una frase explicando por qué es incorrecta]

**🧠 Truco para memorizar**
[nemotecnia, analogía clínica o regla práctica — máx 2 frases]

**📌 Otras preguntas posibles**
- [pregunta 1 sobre este mismo concepto que podría aparecer en examen]
- [pregunta 2]
- [pregunta 3]"""

    client = get_client()
    with st.expander("💬 Explicación detallada", expanded=True):
        placeholder = st.empty()
        texto = ""
        try:
            with client.messages.stream(
                model="claude-sonnet-4-5",
                max_tokens=700,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                for chunk in stream.text_stream:
                    texto += chunk
                    placeholder.markdown(texto + "▌")
            placeholder.markdown(texto)
        except Exception:
            placeholder.info(f"💬 {p['exp']}")

    # ── Preguntas similares con botón Ver respuesta ──
    p_id = p.get("id", "")
    key_sim = f"sim_{p_id}_{letra}"
    if f"pregs_sim_{key_sim}" not in st.session_state:
        st.session_state[f"pregs_sim_{key_sim}"] = None
    if f"resp_sim_{key_sim}" not in st.session_state:
        st.session_state[f"resp_sim_{key_sim}"] = {}

    with st.expander("🔁 Practica con preguntas similares", expanded=False):
        if st.session_state[f"pregs_sim_{key_sim}"] is None:
            if st.button("🤖 Generar 2 preguntas similares", key=f"btn_sim_{key_sim}", use_container_width=True):
                with st.spinner("Generando preguntas..."):
                    prompt_sim = f"""Genera exactamente 2 preguntas tipo test de anatomía sobre el mismo concepto: "{p.get('concepto','')}"
Basadas en: {p['enunciado']}

Responde SOLO con JSON válido, sin texto extra:
[
  {{
    "enunciado": "...",
    "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correcta": "A",
    "exp": "explicación breve"
  }},
  {{
    "enunciado": "...",
    "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correcta": "B",
    "exp": "explicación breve"
  }}
]"""
                    try:
                        resp = client.messages.create(
                            model="claude-sonnet-4-5",
                            max_tokens=800,
                            messages=[{"role": "user", "content": prompt_sim}]
                        )
                        raw = resp.content[0].text.strip()
                        start = raw.find("[")
                        end = raw.rfind("]") + 1
                        pregs_sim = json.loads(raw[start:end])
                        st.session_state[f"pregs_sim_{key_sim}"] = pregs_sim
                        st.rerun()
                    except Exception:
                        st.error("No se pudieron generar. Inténtalo de nuevo.")
        else:
            pregs_sim = st.session_state[f"pregs_sim_{key_sim}"]
            for i, ps in enumerate(pregs_sim):
                st.markdown(f"**Pregunta {i+1}:** {ps['enunciado']}")
                for k, v in ps["opciones"].items():
                    st.markdown(f"&nbsp;&nbsp;**{k})** {v}")
                resp_key = f"resp_sim_{key_sim}_{i}"
                if st.session_state[f"resp_sim_{key_sim}"].get(i) is None:
                    if st.button(f"👁️ Ver respuesta", key=f"ver_{key_sim}_{i}", use_container_width=False):
                        st.session_state[f"resp_sim_{key_sim}"][i] = True
                        st.rerun()
                else:
                    st.success(f"✅ Correcta: **{ps['correcta']})** {ps['opciones'][ps['correcta']]}")
                    st.caption(f"💬 {ps['exp']}")
                if i < len(pregs_sim) - 1:
                    st.divider()

def pantalla_final(results, n_fallos_nuevos=0):
    c = sum(results)
    t = len(results)
    pct = int(c / t * 100) if t else 0
    if pct >= 80:
        st.balloons()
        st.success(f"🎉  {c}/{t} — {pct}%  ¡Excelente!")
    elif pct >= 60:
        st.warning(f"👍  {c}/{t} — {pct}%  Sigue practicando")
    else:
        st.error(f"📚  {c}/{t} — {pct}%  A repasar")
    st.progress(pct / 100)
    if n_fallos_nuevos:
        st.caption(f"⚠️ {n_fallos_nuevos} preguntas guardadas en 'Mis Fallos'")

def generar_pregunta_ia(pregunta_original: dict, tema: str) -> dict | None:
    client = get_client()
    prompt = f"""Genera UNA sola pregunta tipo test de anatomía humana (4 opciones A/B/C/D) sobre el mismo concepto que esta:

CONCEPTO: {pregunta_original.get('concepto','')}
PREGUNTA ORIGINAL: {pregunta_original['enunciado']}
RESPUESTA CORRECTA: {pregunta_original['correcta']}) {pregunta_original['opciones'][pregunta_original['correcta']]}

La nueva pregunta debe:
- Ser diferente pero evaluar el mismo concepto anatómico
- Tener dificultad similar
- Incluir una explicación clínica breve

Responde SOLO con JSON válido en este formato exacto:
{{
  "id": "ia_{tema}_001",
  "concepto": "{pregunta_original.get('concepto','')}",
  "enunciado": "...",
  "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correcta": "A",
  "exp": "..."
}}"""

    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.content[0].text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(text[start:end])
            data["id"] = f"ia_{tema}_{str(uuid.uuid4())[:6]}"
            return data
    except Exception:
        pass
    return None

# ════════════════════════════════════════════════════════════════
#  PANTALLA DE LOGIN — Nombre de usuario
# ════════════════════════════════════════════════════════════════
if not st.session_state.get("usuario_confirmado"):
    st.markdown("""
    <div style="max-width:420px;margin:80px auto 0;text-align:center;">
      <div style="font-size:60px;margin-bottom:16px;">💀</div>
      <h1 style="font-family:sans-serif;font-size:36px;color:#e2e8f0;margin-bottom:4px;">
        Carlo<span style="color:#a78bfa;">Test</span>
      </h1>
      <p style="color:#64748b;font-size:14px;margin-bottom:32px;">
        Anatomía UCV · 1º Medicina
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown("**¿Cómo te llamas?**")
        nombre = st.text_input(
            "", placeholder="Escribe tu nombre...",
            key="input_nombre",
            label_visibility="collapsed"
        )
        if st.button("▶️ Entrar", type="primary", use_container_width=True):
            if nombre.strip():
                st.session_state.usuario = nombre.strip()
                st.session_state.usuario_confirmado = True
                st.session_state.fallos = cargar_fallos(nombre.strip())
                st.session_state._ls_loaded = False  # forzar carga desde localStorage
                st.rerun()
            else:
                st.warning("Escribe tu nombre para continuar")

        # Mostrar usuarios existentes
        usuarios_existentes = []
        if FALLOS_DIR.exists():
            usuarios_existentes = [
                f.stem for f in FALLOS_DIR.glob("*.json")
                if f.stat().st_size > 2
            ]
        if usuarios_existentes:
            st.divider()
            st.caption("👥 Acceso rápido:")
            for u in sorted(usuarios_existentes):
                if st.button(f"👤 {u.capitalize()}", use_container_width=True, key=f"quick_{u}"):
                    st.session_state.usuario = u
                    st.session_state.usuario_confirmado = True
                    st.session_state.fallos = cargar_fallos(u)
                    st.session_state._ls_loaded = False
                    st.rerun()
    st.stop()

# ── Carga desde localStorage (Streamlit Cloud no persiste archivos) ──
# streamlit_js_eval devuelve None la primera vez (JS aún no ejecutó)
# y el valor real en el siguiente rerun. El flag _ls_loaded evita
# sobreescribir datos una vez cargados.
if not st.session_state.get("_ls_loaded"):
    _usuario = st.session_state.get("usuario", "")
    if _usuario:
        _raw_ls = streamlit_js_eval(
            js_expressions=f"localStorage.getItem('{_ls_key(_usuario)}')",
            key=f"ls_load_{_usuario}",
        )
        if _raw_ls is not None:
            # JS ejecutó: puede ser null (sin datos) o un JSON string
            if isinstance(_raw_ls, str) and _raw_ls.strip() and _raw_ls != "null":
                try:
                    _desde_ls = json.loads(_raw_ls)
                    # Usar localStorage si tiene más fallos que el archivo local
                    if len(_desde_ls) > len(st.session_state.fallos):
                        st.session_state.fallos = _desde_ls
                except Exception:
                    pass
            st.session_state._ls_loaded = True

# ════════════════════════════════════════════════════════════════
#  HERO
# ════════════════════════════════════════════════════════════════
# Botón cerrar sesión en sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.get('usuario','').capitalize()}")
    st.caption("Tu progreso se guarda automáticamente")
    st.divider()
    if st.button("🚪 Cambiar usuario", use_container_width=True):
        st.session_state.usuario = ""
        st.session_state.usuario_confirmado = False
        st.session_state.fallos = []
        st.session_state._ls_loaded = False
        st.rerun()

total_q   = sum(len(v["preguntas"]) for v in BANCO.values())
n_fallos  = sum(1 for f in st.session_state.fallos if not f.get("aprendida"))
n_temas   = len(BANCO)

# Leer log de última actualización automática
UPDATE_LOG_PATH = Path(__file__).parent / "update_log.json"
update_info = {"fecha": "—", "nuevas": 0}
if UPDATE_LOG_PATH.exists():
    try:
        update_info = json.loads(UPDATE_LOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass

update_badge = ""
if update_info.get("nuevas", 0) > 0:
    update_badge = f'<div class="update-badge">🔄 {update_info["fecha"]} &nbsp;·&nbsp; +{update_info["nuevas"]} nuevas</div>'

# ── Cargar imagen portada (compatible con Streamlit Cloud) ──
portada = Path(__file__).parent / "portada.jpg"
img_b64 = ""
if portada.exists():
    try:
        img_b64 = base64.b64encode(portada.read_bytes()).decode()
    except Exception:
        img_b64 = ""

img_html = f'<img src="data:image/jpeg;base64,{img_b64}" alt="Anatomía UCV">' if img_b64 else \
           '<div style="width:100%;height:160px;background:linear-gradient(135deg,#1e1040,#0f0820);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:48px;">🧠</div>'

st.markdown(f"""
<div class="hero">
  <div class="hero-text">
    <span class="hero-badge">🎓 Universidad Católica de Valencia</span>
    <h1 class="hero-title">Carlo<span style="color:#a78bfa;">Test</span></h1>
    <p class="hero-sub">Anatomía · 1º Medicina &nbsp;·&nbsp; MS · MI · Cráneo · Vértebras</p>
    <div class="hero-stats">
      <div class="stat-pill sp-purple">
        <span class="stat-num">{total_q}</span>
        <span class="stat-label">preguntas</span>
      </div>
      <div class="stat-pill sp-blue">
        <span class="stat-num">{n_temas}</span>
        <span class="stat-label">temas</span>
      </div>
      <div class="stat-pill sp-red">
        <span class="stat-num">{n_fallos}</span>
        <span class="stat-label">errores</span>
      </div>
    </div>
    {update_badge}
  </div>
  <div class="hero-img-wrap">{img_html}</div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════
tab_test, tab_revision, tab_fallos, tab_flash, tab_tfallo, tab_ucv, tab_chat, tab_real, tab_temas, tab_temario = st.tabs([
    "📚 Test", "📝 Revisión Test", "❌ Mis Fallos", "🃏 Flashcards", "🔁 Test de Fallos", "🎓 Preguntas UCV", "💬 Chat IA",
    "🏆 Preguntas reales UCV", "📖 Repaso por temas", "🗂️ Consultar temario"
])

# ────────────────────────────────────────────────────────────────
#  TAB 1 — TEST
# ────────────────────────────────────────────────────────────────
with tab_test:
    if not st.session_state.test_active:
        st.markdown("### Configurar test")

        c1, c2 = st.columns(2)
        with c1:
            modo_sel = st.radio("Modo:", ["Por tema", "Por categoría", "Por nivel"], key="modo_sel")
        with c2:
            n_pregs = st.slider("Preguntas:", 5, 20, 10, key="n_pregs_test")

        if modo_sel == "Por tema":
            temas_disp = {f"{'⭐'*BANCO[k]['nivel']}  {BANCO[k]['nombre']}": k for k in BANCO}
            sel = st.selectbox("Tema:", list(temas_disp.keys()), key="sel_tema")
            pool = [(temas_disp[sel], p) for p in BANCO[temas_disp[sel]]["preguntas"]]
        elif modo_sel == "Por categoría":
            cat_sel = st.selectbox("Categoría:", list(CATEGORIAS.keys()), key="sel_cat")
            pool = [(k, p) for k in CATEGORIAS[cat_sel] for p in BANCO[k]["preguntas"]]
        else:
            nivel_sel = st.radio("Nivel:", ["⭐⭐⭐ 1", "⭐⭐ 2", "⭐ 3", "Todos"], horizontal=True, key="nivel_test")
            if "1" in nivel_sel:
                keys = NIVELES[1]
            elif "2" in nivel_sel:
                keys = NIVELES[2]
            elif "3" in nivel_sel:
                keys = NIVELES[3]
            else:
                keys = list(BANCO.keys())
            pool = [(k, p) for k in keys for p in BANCO[k]["preguntas"]]

        if st.button("▶️  Empezar test", type="primary", use_container_width=True):
            muestra = random.sample(pool, min(n_pregs, len(pool)))
            st.session_state.test_active = True
            st.session_state.test_pregs = muestra
            st.session_state.test_idx = 0
            st.session_state.test_results = []
            st.session_state.test_answered = False
            st.session_state.test_last_letra = None
            st.session_state.test_n_fallos = 0
            st.session_state.test_errores = []
            st.session_state.test_revision = False
            st.rerun()
    else:
        pregs = st.session_state.test_pregs
        idx = st.session_state.test_idx

        # ── Preguntas del test ──
        if idx < len(pregs):
            tema_k, p = pregs[idx]
            st.progress(idx / len(pregs), text=f"Progreso: {idx}/{len(pregs)}")
            st.markdown(f"**Tema:** {BANCO[tema_k]['nombre']}  |  **Categoría:** {BANCO[tema_k]['categoria']}")

            if not st.session_state.test_answered:
                resp = mostrar_pregunta(p, idx, len(pregs), f"{tema_k}_test")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔ Confirmar", type="primary", disabled=resp is None, use_container_width=True, key="conf_test"):
                        letra = resp[0]
                        correcto = letra == p["correcta"]
                        st.session_state.test_results.append(correcto)
                        st.session_state.test_answered = True
                        st.session_state.test_last_letra = letra
                        if not correcto:
                            registrar_fallo(p, tema_k, letra)
                            st.session_state.test_n_fallos = st.session_state.get("test_n_fallos", 0) + 1
                            st.session_state.test_errores.append({"p": p, "letra": letra, "tema": tema_k})
                        st.rerun()
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True, key="skip_test"):
                        st.session_state.test_idx += 1
                        st.rerun()
            else:
                feedback(p, st.session_state.test_last_letra)
                if st.button("Siguiente →", type="primary", use_container_width=True, key="next_test"):
                    st.session_state.test_idx += 1
                    st.session_state.test_answered = False
                    st.rerun()

        # ── Test terminado ──
        else:
            pantalla_final(st.session_state.test_results, st.session_state.get("test_n_fallos", 0))
            n_err = len(st.session_state.test_errores)
            if n_err:
                st.info(f"💡 Ve a la pestaña **📝 Revisión Test** para ver los {n_err} errores con explicación.")
            if st.button("🔁 Nuevo test", type="primary", use_container_width=True):
                st.session_state.test_active = False
                st.rerun()

# ────────────────────────────────────────────────────────────────
#  TAB 2 — REVISIÓN TEST
# ────────────────────────────────────────────────────────────────
with tab_revision:
    errores_rev = (
        st.session_state.get("test_errores", []) +
        st.session_state.get("ft_errores", []) +
        st.session_state.get("ucv_errores", [])
    )
    if not errores_rev:
        st.info("Aquí aparecerán los errores del último test realizado. ¡Haz un test primero!")
    else:
        st.markdown(f"### Errores del último test — {len(errores_rev)} pregunta(s) fallada(s)")
        st.caption("Repasa cada error con su explicación antes de continuar estudiando.")
        st.divider()
        for i, e in enumerate(errores_rev, 1):
            tema_e = e.get("tema", "")
            tema_nombre = BANCO.get(tema_e, BANCO_UCV.get(tema_e, {})).get("nombre", "")
            concepto = e["p"].get("concepto", "")
            with st.expander(f"❌ {i}.  {e['p']['enunciado'][:80]}{'...' if len(e['p']['enunciado'])>80 else ''}", expanded=True):
                st.markdown(f"**{e['p']['enunciado']}**")
                st.markdown("")
                for letra, texto in e["p"]["opciones"].items():
                    if letra == e["letra"]:
                        st.markdown(f"🔴 **{letra})** {texto}  ← *tu respuesta*")
                    elif letra == e["p"]["correcta"]:
                        st.markdown(f"🟢 **{letra})** {texto}  ← *correcta*")
                    else:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;{letra}) {texto}")
                st.divider()
                st.info(f"💬 {e['p']['exp']}")
                if tema_nombre or concepto:
                    st.caption(f"📚 {tema_nombre}  |  🔑 {concepto}")

# ────────────────────────────────────────────────────────────────
#  TAB 3 — MIS FALLOS
# ────────────────────────────────────────────────────────────────
with tab_fallos:
    fallos = [f for f in st.session_state.fallos if not f.get("aprendida")]

    if not fallos:
        st.info("🎉 ¡Sin fallos registrados! Haz un test para comenzar.")
    else:
        col1, col2 = st.columns([3, 1])
        with col1:
            temas_con_fallos = sorted({f["tema"] for f in fallos})
            opciones_tema = ["Todos los temas"] + [BANCO[t]["nombre"] for t in temas_con_fallos]
            filtro = st.selectbox("Filtrar por tema:", opciones_tema, key="fallos_filtro")
        with col2:
            ordenar = st.selectbox("Ordenar:", ["Más falladas", "Recientes", "Tema"], key="fallos_orden")

        if filtro != "Todos los temas":
            tema_fil = next(k for k in temas_con_fallos if BANCO[k]["nombre"] == filtro)
            fallos_vis = [f for f in fallos if f["tema"] == tema_fil]
        else:
            fallos_vis = fallos

        if ordenar == "Más falladas":
            fallos_vis = sorted(fallos_vis, key=lambda x: x["veces_fallada"], reverse=True)
        elif ordenar == "Recientes":
            fallos_vis = sorted(fallos_vis, key=lambda x: x["ultima_fecha"], reverse=True)
        else:
            fallos_vis = sorted(fallos_vis, key=lambda x: x["tema"])

        st.markdown(f"**{len(fallos_vis)} pregunta(s)** {'en este tema' if filtro != 'Todos los temas' else 'en total'}")
        st.divider()

        for i, f in enumerate(fallos_vis):
            with st.container():
                st.markdown(
                    f'<div class="fallo-card">'
                    f'{badge(f["nivel"])} <span class="concepto-tag">🔑 {f["concepto"]}</span>'
                    f'<span style="color:#64748b;font-size:11px;margin-left:8px;">📚 {f["tema_nombre"]}</span>'
                    f'<br><br><b>{f["enunciado"]}</b>'
                    f'<br><span style="color:#ef4444;font-size:12px;">Tu respuesta: {f["respuesta_dada"]}) {f["opciones"][f["respuesta_dada"]]}</span>'
                    f'<br><span style="color:#10b981;font-size:12px;">Correcta: {f["correcta"]}) {f["opciones"][f["correcta"]]}</span>'
                    f'<br><span style="color:#64748b;font-size:11px;margin-top:4px;display:block;">💬 {f["exp"]}</span>'
                    f'<br><span style="color:#94a3b8;font-size:10px;">Fallada {f["veces_fallada"]}x · última vez {f["ultima_fecha"]}'
                    + (' · 🤖 IA' if f.get("generada_ia") else '') +
                    '</span></div>',
                    unsafe_allow_html=True
                )
                btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])
                with btn_col1:
                    if st.button("✅ Marcar como aprendida", key=f"apr_{f['uid']}_{i}", use_container_width=True):
                        for ff in st.session_state.fallos:
                            if ff["uid"] == f["uid"]:
                                ff["aprendida"] = True
                        guardar_fallos(st.session_state.fallos, st.session_state.get("usuario", "default"))
                        st.rerun()
                with btn_col2:
                    if st.button("🤖 Generar pregunta similar", key=f"gen_{f['uid']}_{i}", use_container_width=True):
                        with st.spinner("Generando pregunta con IA..."):
                            nueva = generar_pregunta_ia(f, f["tema"])
                        if nueva:
                            if f["tema"] not in BANCO:
                                pass
                            else:
                                BANCO[f["tema"]]["preguntas"].append(nueva)
                            st.success("✅ Pregunta generada añadida al banco de test")
                        else:
                            st.error("No se pudo generar la pregunta. Inténtalo de nuevo.")

        st.divider()
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            datos_json = json.dumps(st.session_state.fallos, ensure_ascii=False, indent=2)
            st.download_button("⬇️ Exportar fallos (JSON)", datos_json, "fallos_anatomia.json", "application/json", use_container_width=True)
        with col_d2:
            uploaded = st.file_uploader("⬆️ Importar fallos", type="json", key="import_fallos", label_visibility="collapsed")
            if uploaded:
                try:
                    datos = json.load(uploaded)
                    st.session_state.fallos = datos
                    guardar_fallos(datos, st.session_state.get("usuario", "default"))
                    st.success("Fallos importados correctamente")
                    st.rerun()
                except Exception:
                    st.error("Archivo inválido")

# ────────────────────────────────────────────────────────────────
#  TAB 3 — FLASHCARDS
# ────────────────────────────────────────────────────────────────
with tab_flash:
    fallos_flash = [f for f in st.session_state.fallos if not f.get("aprendida")]

    if not fallos_flash:
        st.info("No hay fallos registrados para las flashcards.")
    else:
        temas_flash = sorted({f["tema"] for f in fallos_flash})
        filtro_flash = st.selectbox("Tema:", ["Todos"] + [BANCO[t]["nombre"] for t in temas_flash], key="flash_filtro")

        if filtro_flash != "Todos":
            tema_fl = next(k for k in temas_flash if BANCO[k]["nombre"] == filtro_flash)
            pool_flash = [f for f in fallos_flash if f["tema"] == tema_fl]
        else:
            pool_flash = fallos_flash

        conceptos_unicos = {}
        for f in pool_flash:
            if f["concepto"] not in conceptos_unicos:
                conceptos_unicos[f["concepto"]] = f

        lista_conceptos = list(conceptos_unicos.values())
        if not lista_conceptos:
            st.info("Sin conceptos para mostrar.")
        else:
            idx_flash = st.session_state.flash_idx % len(lista_conceptos)
            concepto_act = lista_conceptos[idx_flash]

            st.markdown(f"**Flashcard {idx_flash + 1} / {len(lista_conceptos)}** — {BANCO.get(concepto_act['tema'], {}).get('nombre', '')}")
            st.progress((idx_flash + 1) / len(lista_conceptos))

            st.markdown(
                f'<div class="flashcard-front">'
                f'<p style="color:#a78bfa;font-size:13px;margin-bottom:8px;">🔑 CONCEPTO</p>'
                f'<h3 style="color:#e2e8f0;margin:0;">{concepto_act["concepto"].upper()}</h3>'
                f'<p style="color:#64748b;font-size:12px;margin-top:12px;">{BANCO.get(concepto_act["tema"],{}).get("nombre","")}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

            if st.session_state.flash_revealed:
                st.markdown(
                    f'<div class="flashcard-back">'
                    f'<p style="color:#10b981;font-size:12px;margin-bottom:8px;">✅ EXPLICACIÓN</p>'
                    f'<p style="color:#e2e8f0;">{concepto_act["exp"]}</p>'
                    f'<p style="color:#64748b;font-size:12px;margin-top:12px;">📝 <b>{concepto_act["correcta"]})</b> {concepto_act["opciones"][concepto_act["correcta"]]}</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ Ver respuesta" if not st.session_state.flash_revealed else "🙈 Ocultar", use_container_width=True, key="reveal_flash"):
                    st.session_state.flash_revealed = not st.session_state.flash_revealed
                    st.rerun()
            with col2:
                if st.button("← Anterior", use_container_width=True, key="prev_flash"):
                    st.session_state.flash_idx = (st.session_state.flash_idx - 1) % len(lista_conceptos)
                    st.session_state.flash_revealed = False
                    st.rerun()
            with col3:
                if st.button("Siguiente →", use_container_width=True, key="next_flash", type="primary"):
                    st.session_state.flash_idx = (st.session_state.flash_idx + 1) % len(lista_conceptos)
                    st.session_state.flash_revealed = False
                    st.rerun()

# ────────────────────────────────────────────────────────────────
#  TAB 4 — TEST DE FALLOS
# ────────────────────────────────────────────────────────────────
with tab_tfallo:
    fallos_test = [f for f in st.session_state.fallos if not f.get("aprendida")]

    if not fallos_test:
        st.info("Sin fallos registrados. Haz tests primero para llenar este banco.")
    elif not st.session_state.ft_active:
        st.markdown("### Test solo con tus preguntas falladas")

        temas_ft = sorted({f["tema"] for f in fallos_test})
        c1, c2 = st.columns(2)
        with c1:
            opciones_ft = ["Todos los temas"] + [BANCO[t]["nombre"] for t in temas_ft]
            filtro_ft = st.selectbox("Tema:", opciones_ft, key="ft_filtro")
        with c2:
            ordenar_ft = st.radio("Orden:", ["Aleatorio", "Más falladas primero"], key="ft_orden")

        if filtro_ft != "Todos los temas":
            tema_ft_k = next(k for k in temas_ft if BANCO[k]["nombre"] == filtro_ft)
            pool_ft = [f for f in fallos_test if f["tema"] == tema_ft_k]
        else:
            pool_ft = fallos_test

        st.info(f"**{len(pool_ft)} preguntas** en el banco de fallos para este filtro.")

        if len(pool_ft) > 2:
            _ft_max = min(20, len(pool_ft))
            n_ft = st.slider("Preguntas:", 2, _ft_max, min(_ft_max, 10), key="n_ft")
        else:
            n_ft = len(pool_ft)

        if ordenar_ft == "Más falladas primero":
            pool_ft_sorted = sorted(pool_ft, key=lambda x: x["veces_fallada"], reverse=True)
            muestra_ft = pool_ft_sorted[:n_ft]
        else:
            muestra_ft = random.sample(pool_ft, n_ft)

        if st.button("▶️ Empezar test de fallos", type="primary", use_container_width=True):
            st.session_state.ft_active = True
            st.session_state.ft_pregs = muestra_ft
            st.session_state.ft_idx = 0
            st.session_state.ft_results = []
            st.session_state.ft_answered = False
            st.session_state.ft_last_letra = None
            st.session_state.ft_n_nuevos = 0
            st.session_state.ft_errores = []
            st.session_state.ft_revision = False
            st.rerun()
    else:
        pregs_ft = st.session_state.ft_pregs
        idx_ft = st.session_state.ft_idx

        if idx_ft < len(pregs_ft):
            f_act = pregs_ft[idx_ft]
            p_ft = {
                "id": f_act["pregunta_id"],
                "concepto": f_act["concepto"],
                "enunciado": f_act["enunciado"],
                "opciones": f_act["opciones"],
                "correcta": f_act["correcta"],
                "exp": f_act["exp"],
            }
            st.progress(idx_ft / len(pregs_ft), text=f"Progreso: {idx_ft}/{len(pregs_ft)}")
            st.markdown(f"**Tema:** {f_act['tema_nombre']}  |  Fallada **{f_act['veces_fallada']}x**")

            if not st.session_state.ft_answered:
                st.markdown(f'<p class="pregunta-num">Pregunta {idx_ft+1} / {len(pregs_ft)}</p>', unsafe_allow_html=True)
                st.markdown(f'{badge(f_act["nivel"])} <span class="concepto-tag">🔑 {f_act["concepto"]}</span>', unsafe_allow_html=True)
                st.markdown(f"**{p_ft['enunciado']}**")
                opciones_ft2 = [f"{k})  {v}" for k, v in p_ft["opciones"].items()]
                resp_ft = st.radio("", opciones_ft2, index=None, key=f"ft_{idx_ft}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔ Confirmar", type="primary", disabled=resp_ft is None, use_container_width=True, key="conf_ft"):
                        letra_ft = resp_ft[0]
                        correcto_ft = letra_ft == p_ft["correcta"]
                        st.session_state.ft_results.append(correcto_ft)
                        st.session_state.ft_answered = True
                        st.session_state.ft_last_letra = letra_ft
                        if not correcto_ft:
                            registrar_fallo(p_ft, f_act["tema"], letra_ft)
                            st.session_state.ft_n_nuevos = st.session_state.get("ft_n_nuevos", 0) + 1
                            st.session_state.ft_errores.append({"p": p_ft, "letra": letra_ft, "tema": f_act["tema"]})
                        st.rerun()
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True, key="skip_ft"):
                        st.session_state.ft_idx += 1
                        st.rerun()
            else:
                feedback(p_ft, st.session_state.ft_last_letra)
                if st.button("Siguiente →", type="primary", use_container_width=True, key="next_ft"):
                    st.session_state.ft_idx += 1
                    st.session_state.ft_answered = False
                    st.rerun()

        else:
            c = sum(st.session_state.ft_results)
            t = len(st.session_state.ft_results)
            pct = int(c / t * 100) if t else 0
            if pct >= 80:
                st.balloons()
                st.success(f"🎉  {c}/{t} — {pct}%  ¡Excelente!")
            elif pct >= 60:
                st.warning(f"👍  {c}/{t} — {pct}%  Sigue practicando")
            else:
                st.error(f"📚  {c}/{t} — {pct}%  A repasar")
            st.progress(pct / 100)
            n_err_ft = len(st.session_state.ft_errores)
            if n_err_ft:
                st.info(f"💡 Ve a la pestaña **📝 Revisión Test** para ver los {n_err_ft} errores con explicación.")
            if st.button("🔁 Nuevo test", type="primary", use_container_width=True):
                st.session_state.ft_active = False
                st.rerun()

# ────────────────────────────────────────────────────────────────
#  TAB 6 — PREGUNTAS UCV
# ────────────────────────────────────────────────────────────────
with tab_ucv:
    if not st.session_state.ucv_active:
        st.markdown("### 🎓 Preguntas del temario UCV")
        st.caption("Preguntas del temario oficial + preguntas reales de examen de la UCV")

        total_ucv = sum(len(v["preguntas"]) for v in BANCO_UCV.values())
        reales_ucv = len(BANCO_UCV["ucv_reales_3_4_5"]["preguntas"])
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total preguntas UCV", total_ucv)
        with c2:
            st.metric("Preguntas reales examen", reales_ucv)
        with c3:
            st.metric("Temas", len(BANCO_UCV))

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            modo_ucv = st.radio("Modo:", ["Por tema", "Por categoría", "Solo preguntas reales"], key="modo_ucv")
        with col2:
            n_ucv = st.slider("Nº preguntas:", 5, 20, 10, key="n_ucv")

        if modo_ucv == "Por tema":
            temas_ucv_disp = {f"{BANCO_UCV[k]['nombre']}": k for k in BANCO_UCV}
            sel_ucv = st.selectbox("Tema:", list(temas_ucv_disp.keys()), key="sel_ucv_tema")
            tema_sel_key = temas_ucv_disp[sel_ucv]
            pool_ucv = [(tema_sel_key, p) for p in BANCO_UCV[tema_sel_key]["preguntas"]]
            # Mostrar imagen del tema si existe
            img_url = BANCO_UCV[tema_sel_key].get("imagen_tema")
            if img_url:
                col_img, col_txt = st.columns([1, 3])
                with col_img:
                    st.image(img_url, use_container_width=True)
                with col_txt:
                    st.caption(f"📖 {BANCO_UCV[tema_sel_key]['nombre']}")
        elif modo_ucv == "Por categoría":
            cat_ucv = st.selectbox("Categoría:", list(CATEGORIAS_UCV.keys()), key="sel_ucv_cat")
            pool_ucv = [(k, p) for k in CATEGORIAS_UCV[cat_ucv] for p in BANCO_UCV[k]["preguntas"]]
        else:
            pool_ucv = [("ucv_reales_3_4_5", p) for p in BANCO_UCV["ucv_reales_3_4_5"]["preguntas"]]

        st.info(f"**{len(pool_ucv)} preguntas disponibles** para este filtro.")

        if st.button("▶️ Empezar test UCV", type="primary", use_container_width=True):
            muestra_ucv = random.sample(pool_ucv, min(n_ucv, len(pool_ucv)))
            st.session_state.ucv_active = True
            st.session_state.ucv_pregs = muestra_ucv
            st.session_state.ucv_idx = 0
            st.session_state.ucv_results = []
            st.session_state.ucv_answered = False
            st.session_state.ucv_last_letra = None
            st.session_state.ucv_errores = []
            st.session_state.ucv_n_fallos = 0
            st.rerun()

    else:
        pregs_ucv = st.session_state.ucv_pregs
        idx_ucv = st.session_state.ucv_idx

        if idx_ucv < len(pregs_ucv):
            tema_k_ucv, p_ucv = pregs_ucv[idx_ucv]
            tema_info = BANCO_UCV.get(tema_k_ucv, {})
            nivel_ucv = tema_info.get("nivel", 1)

            st.progress(idx_ucv / len(pregs_ucv), text=f"Progreso: {idx_ucv}/{len(pregs_ucv)}")
            st.markdown(f"**Tema:** {tema_info.get('nombre','')}  |  **Categoría:** {tema_info.get('categoria','')}")

            if not st.session_state.ucv_answered:
                st.markdown(f'<p class="pregunta-num">Pregunta {idx_ucv+1} / {len(pregs_ucv)}</p>', unsafe_allow_html=True)
                st.markdown(
                    f'{badge(nivel_ucv)} <span class="concepto-tag">🔑 {p_ucv.get("concepto","")}</span>',
                    unsafe_allow_html=True
                )
                st.markdown(f"**{p_ucv['enunciado']}**")
                opciones_ucv = [f"{k})  {v}" for k, v in p_ucv["opciones"].items()]
                resp_ucv = st.radio("", opciones_ucv, index=None, key=f"ucv_{idx_ucv}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✔ Confirmar", type="primary", disabled=resp_ucv is None,
                                 use_container_width=True, key="conf_ucv"):
                        letra_ucv = resp_ucv[0]
                        correcto_ucv = letra_ucv == p_ucv["correcta"]
                        st.session_state.ucv_results.append(correcto_ucv)
                        st.session_state.ucv_answered = True
                        st.session_state.ucv_last_letra = letra_ucv
                        if not correcto_ucv:
                            registrar_fallo(p_ucv, tema_k_ucv, letra_ucv)
                            st.session_state.ucv_n_fallos += 1
                            st.session_state.ucv_errores.append({
                                "p": p_ucv, "letra": letra_ucv, "tema": tema_k_ucv
                            })
                        st.rerun()
                with col2:
                    if st.button("⏭ Saltar", use_container_width=True, key="skip_ucv"):
                        st.session_state.ucv_idx += 1
                        st.rerun()
            else:
                # ── Feedback inline con explicación ──
                feedback(p_ucv, st.session_state.ucv_last_letra)
                if st.button("Siguiente →", type="primary", use_container_width=True, key="next_ucv"):
                    st.session_state.ucv_idx += 1
                    st.session_state.ucv_answered = False
                    st.rerun()

        else:
            # ── Pantalla final ──
            pantalla_final(st.session_state.ucv_results, st.session_state.ucv_n_fallos)
            n_err_ucv = len(st.session_state.ucv_errores)
            if n_err_ucv:
                st.markdown(f"### 📝 Revisión de errores — {n_err_ucv} pregunta(s) fallada(s)")
                st.caption("Repasa cada error con su explicación completa.")
                st.divider()
                for i, e in enumerate(st.session_state.ucv_errores, 1):
                    tema_nombre_ucv = BANCO_UCV.get(e.get("tema", ""), {}).get("nombre", "")
                    concepto_ucv = e["p"].get("concepto", "")
                    with st.expander(
                        f"❌ {i}.  {e['p']['enunciado'][:80]}{'...' if len(e['p']['enunciado']) > 80 else ''}",
                        expanded=True
                    ):
                        st.markdown(f"**{e['p']['enunciado']}**")
                        st.markdown("")
                        for letra, texto in e["p"]["opciones"].items():
                            if letra == e["letra"]:
                                st.markdown(f"🔴 **{letra})** {texto}  ← *tu respuesta*")
                            elif letra == e["p"]["correcta"]:
                                st.markdown(f"🟢 **{letra})** {texto}  ← *correcta*")
                            else:
                                st.markdown(f"&nbsp;&nbsp;&nbsp;{letra}) {texto}")
                        st.divider()
                        st.info(f"💬 {e['p']['exp']}")
                        if tema_nombre_ucv or concepto_ucv:
                            st.caption(f"📚 {tema_nombre_ucv}  |  🔑 {concepto_ucv}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔁 Nuevo test UCV", type="primary", use_container_width=True):
                    st.session_state.ucv_active = False
                    st.rerun()
            with col2:
                if st.button("❌ Ver todos mis fallos", use_container_width=True):
                    st.session_state.ucv_active = False
                    st.rerun()

# ────────────────────────────────────────────────────────────────
#  TAB 7 — CHAT IA
# ────────────────────────────────────────────────────────────────
with tab_chat:
    st.caption("Pregunta cualquier duda sobre anatomía del temario")

    SYSTEM_PROMPT = """Eres un profesor experto en anatomía humana para estudiantes de 1º de Medicina de la Universidad Católica de Valencia (UCV).
El temario de examen cubre: Miembro Superior, Miembro Inferior, Cráneo y Vértebras.
Los exámenes son tipo test de 60-80 preguntas. Responde en español, de forma clara y concisa.
Usa nemotecnias cuando sea útil. Incluye perlas clínicas relevantes."""

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if pregunta := st.chat_input("Escribe tu duda de anatomía..."):
        with st.chat_message("user"):
            st.write(pregunta)
        st.session_state.chat_history.append({"role": "user", "content": pregunta})

        mensajes_api = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[-20:]]
        client = get_client()

        with st.chat_message("assistant"):
            def stream_gen():
                with client.messages.stream(
                    model="claude-sonnet-4-5",
                    max_tokens=700,
                    system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
                    messages=mensajes_api,
                ) as stream:
                    yield from stream.text_stream

            respuesta = st.write_stream(stream_gen())
        st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    if st.session_state.chat_history:
        if st.button("🗑️ Limpiar conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ── Carga de bancos JSON externos ────────────────────────────────
@st.cache_data
def cargar_banco_real():
    p = Path(__file__).parent / "banco_UCV_temas_3_4_5_REAL.json"
    return json.loads(p.read_text(encoding="utf-8"))

@st.cache_data
def cargar_banco_por_temas():
    p = Path(__file__).parent / "banco_UCV_por_temas.json"
    return json.loads(p.read_text(encoding="utf-8"))

@st.cache_data
def cargar_temario():
    p = Path(__file__).parent / "temario_UCV_anatomia.json"
    return json.loads(p.read_text(encoding="utf-8"))

def _contexto_temario(pregunta: str, opciones: list[str]) -> str:
    """Extrae hasta ~1200 chars de las secciones del temario más relevantes."""
    try:
        tm = cargar_temario()
        palabras = set(
            w for w in (pregunta + " " + " ".join(opciones)).lower().split()
            if len(w) > 4
        )
        fragmentos = []
        for tema_t in tm["temas"]:
            for sec in tema_t.get("secciones", []):
                texto = sec["contenido"].lower()
                if sum(1 for w in palabras if w in texto) >= 2:
                    fragmentos.append(
                        f"**{tema_t['titulo']} › {sec['titulo']}**\n{sec['contenido'][:400]}"
                    )
        ctx = "\n\n".join(fragmentos[:4])
        return ctx[:1400] if ctx else ""
    except Exception:
        return ""

def saber_mas(p_data: dict, campo_valor: str, key_prefix: str):
    """Expander 'Saber más' con IA: explicación ampliada, preguntas, esquema y nemotecnia."""
    sm_key = f"sm__{key_prefix}__{p_data['id']}"
    if sm_key not in st.session_state:
        st.session_state[sm_key] = None

    with st.expander("💡 Saber más", expanded=False):
        if st.session_state[sm_key] is None:
            if st.button(
                "🤖 Ampliar con IA — explicación, preguntas, esquema y nemotecnia",
                key=f"btn_{sm_key}",
                use_container_width=True,
            ):
                correcta_idx = p_data["respuesta_correcta"]
                correcta_txt = p_data["opciones"][correcta_idx]
                falsas = [op for i, op in enumerate(p_data["opciones"]) if i != correcta_idx]
                ctx = _contexto_temario(p_data["pregunta"], p_data["opciones"])

                prompt = f"""Eres profesor de Anatomía Humana de 1º de Medicina UCV (Universidad Católica de Valencia).
El alumno acaba de responder esta pregunta tipo test:

PREGUNTA: {p_data["pregunta"]}
RESPUESTA CORRECTA: {chr(65 + correcta_idx)}) {correcta_txt}
OPCIONES INCORRECTAS: {" | ".join(falsas)}
BLOQUE/TEMA: {campo_valor}
EXPLICACIÓN BREVE: {p_data["explicacion"]}

CONTEXTO DEL TEMARIO UCV:
{ctx if ctx else "(no hay contexto adicional disponible)"}

Genera la respuesta con este formato EXACTO en markdown, sin introducción:

## 📚 Explicación ampliada
[2-3 párrafos. Explica el mecanismo anatómico, función, localización y relevancia clínica usando el contexto del temario. Conecta con lo que el alumno debe dominar para el examen.]

## 🧪 Preguntas relacionadas
Escribe 3 preguntas tipo test diferentes sobre el mismo concepto, que podrían aparecer en el examen UCV:

**Pregunta 1:** [enunciado]
A) ... &nbsp; B) ... &nbsp; C) ... &nbsp; D) ...
✅ **Correcta: [letra])** [opción] — [explicación en 1 línea]

**Pregunta 2:** [enunciado]
A) ... &nbsp; B) ... &nbsp; C) ... &nbsp; D) ...
✅ **Correcta: [letra])** [opción] — [explicación en 1 línea]

**Pregunta 3:** [enunciado]
A) ... &nbsp; B) ... &nbsp; C) ... &nbsp; D) ...
✅ **Correcta: [letra])** [opción] — [explicación en 1 línea]

## 🗂️ Esquema — lo que debes saber
[Lista jerárquica con bullets (•) de todos los puntos clave examinables sobre este concepto. Máx 10 puntos, concretos y directos.]

## 🧠 Regla nemotécnica
[Una regla, analogía clínica o truco visual para no olvidar este concepto. Si no existe una regla natural, inventa una que funcione. Nunca dejes esta sección vacía.]"""

                client = get_client()
                placeholder = st.empty()
                texto = ""
                try:
                    with client.messages.stream(
                        model="claude-sonnet-4-5",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}],
                    ) as stream:
                        for chunk in stream.text_stream:
                            texto += chunk
                            placeholder.markdown(texto + "▌")
                    placeholder.markdown(texto)
                    st.session_state[sm_key] = texto
                except Exception as e:
                    placeholder.error(f"Error al conectar con IA: {e}")
        else:
            st.markdown(st.session_state[sm_key])

# ────────────────────────────────────────────────────────────────
#  TAB 8 — PREGUNTAS REALES UCV
# ────────────────────────────────────────────────────────────────
with tab_real:
    banco_real = cargar_banco_real()
    preguntas_real = banco_real["preguntas"]

    bloques_real = sorted({p["bloque"] for p in preguntas_real})
    bloque_sel = st.selectbox(
        "Filtrar por bloque:",
        ["Todos los bloques"] + bloques_real,
        key="real_bloque_sel"
    )

    pool_real = preguntas_real if bloque_sel == "Todos los bloques" else [
        p for p in preguntas_real if p["bloque"] == bloque_sel
    ]

    st.caption(f"**{len(pool_real)} preguntas** disponibles en este bloque")
    st.divider()

    if "real_idx" not in st.session_state:
        st.session_state.real_idx = 0
    if "real_orden" not in st.session_state:
        st.session_state.real_orden = list(range(len(preguntas_real)))
    if "real_respondidas" not in st.session_state:
        st.session_state.real_respondidas = {}

    if st.button("🔀 Mezclar preguntas", key="real_shuffle"):
        import random as _r
        orden = list(range(len(pool_real)))
        _r.shuffle(orden)
        st.session_state.real_orden = orden
        st.session_state.real_idx = 0
        st.session_state.real_respondidas = {}
        st.rerun()

    if not pool_real:
        st.info("No hay preguntas para este bloque.")
    else:
        orden_real = [i for i in range(len(pool_real))]
        idx_r = st.session_state.real_idx % len(pool_real)
        p_r = pool_real[idx_r]

        st.markdown(f'<p class="pregunta-num">Pregunta {idx_r + 1} / {len(pool_real)}</p>', unsafe_allow_html=True)
        st.progress((idx_r + 1) / len(pool_real))
        st.markdown(f'<span class="concepto-tag">📂 {p_r["bloque"]}</span>', unsafe_allow_html=True)
        st.markdown(f"**{p_r['pregunta']}**")

        opciones_r = [f"{chr(65+i)})  {op}" for i, op in enumerate(p_r["opciones"])]
        resp_r = st.radio("", opciones_r, index=None, key=f"real_radio_{idx_r}_{bloque_sel}")

        resp_key = f"real_resp_{idx_r}_{bloque_sel}"
        if resp_key not in st.session_state:
            st.session_state[resp_key] = None

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔ Confirmar", type="primary", disabled=(resp_r is None or st.session_state[resp_key] is not None),
                         use_container_width=True, key=f"real_conf_{idx_r}_{bloque_sel}"):
                letra_idx = ord(resp_r[0]) - 65
                st.session_state[resp_key] = letra_idx
                st.rerun()
        with col2:
            if st.button("Siguiente →", use_container_width=True, key=f"real_next_{idx_r}_{bloque_sel}"):
                st.session_state.real_idx = (idx_r + 1) % len(pool_real)
                st.rerun()

        if st.session_state[resp_key] is not None:
            elegida = st.session_state[resp_key]
            correcta = p_r["respuesta_correcta"]
            if elegida == correcta:
                st.success("✅ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto — era **{chr(65+correcta)})** {p_r['opciones'][correcta]}")
            with st.expander("💬 Explicación", expanded=True):
                st.markdown(p_r["explicacion"])
            saber_mas(p_r, p_r["bloque"], f"real_{idx_r}_{bloque_sel}")

# ────────────────────────────────────────────────────────────────
#  TAB 9 — REPASO POR TEMAS
# ────────────────────────────────────────────────────────────────
with tab_temas:
    banco_temas = cargar_banco_por_temas()
    preguntas_temas = banco_temas["preguntas"]

    temas_disp = sorted({p["tema"] for p in preguntas_temas})
    tema_sel = st.selectbox(
        "Filtrar por tema:",
        ["Todos los temas"] + temas_disp,
        key="temas_tema_sel"
    )

    pool_temas = preguntas_temas if tema_sel == "Todos los temas" else [
        p for p in preguntas_temas if p["tema"] == tema_sel
    ]

    st.caption(f"**{len(pool_temas)} preguntas** disponibles en este tema")
    st.divider()

    if "temas_idx" not in st.session_state:
        st.session_state.temas_idx = 0

    if st.button("🔀 Mezclar preguntas", key="temas_shuffle"):
        import random as _r2
        st.session_state.temas_idx = 0
        st.rerun()

    if not pool_temas:
        st.info("No hay preguntas para este tema.")
    else:
        idx_t = st.session_state.temas_idx % len(pool_temas)
        p_t = pool_temas[idx_t]

        st.markdown(f'<p class="pregunta-num">Pregunta {idx_t + 1} / {len(pool_temas)}</p>', unsafe_allow_html=True)
        st.progress((idx_t + 1) / len(pool_temas))
        st.markdown(f'<span class="concepto-tag">📚 {p_t["tema"]}</span>', unsafe_allow_html=True)
        st.markdown(f"**{p_t['pregunta']}**")

        opciones_t = [f"{chr(65+i)})  {op}" for i, op in enumerate(p_t["opciones"])]
        resp_t = st.radio("", opciones_t, index=None, key=f"temas_radio_{idx_t}_{tema_sel}")

        tresp_key = f"temas_resp_{idx_t}_{tema_sel}"
        if tresp_key not in st.session_state:
            st.session_state[tresp_key] = None

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✔ Confirmar", type="primary", disabled=(resp_t is None or st.session_state[tresp_key] is not None),
                         use_container_width=True, key=f"temas_conf_{idx_t}_{tema_sel}"):
                letra_idx_t = ord(resp_t[0]) - 65
                st.session_state[tresp_key] = letra_idx_t
                st.rerun()
        with col2:
            if st.button("Siguiente →", use_container_width=True, key=f"temas_next_{idx_t}_{tema_sel}"):
                st.session_state.temas_idx = (idx_t + 1) % len(pool_temas)
                st.rerun()

        if st.session_state[tresp_key] is not None:
            elegida_t = st.session_state[tresp_key]
            correcta_t = p_t["respuesta_correcta"]
            if elegida_t == correcta_t:
                st.success("✅ ¡Correcto!")
            else:
                st.error(f"❌ Incorrecto — era **{chr(65+correcta_t)})** {p_t['opciones'][correcta_t]}")
            with st.expander("💬 Explicación", expanded=True):
                st.markdown(p_t["explicacion"])
            saber_mas(p_t, p_t["tema"], f"temas_{idx_t}_{tema_sel}")

# ────────────────────────────────────────────────────────────────
#  TAB 10 — CONSULTAR TEMARIO
# ────────────────────────────────────────────────────────────────
with tab_temario:
    temario = cargar_temario()
    st.markdown("### 🗂️ Temario oficial UCV — Anatomía Humana y Funcional")
    st.caption("9 temas del temario oficial. Embriología excluida.")
    st.divider()

    for tema_t in temario["temas"]:
        st.markdown(f"#### {tema_t['numero']}: {tema_t['titulo']}")
        st.caption(tema_t.get("descripcion", ""))
        for sec in tema_t.get("secciones", []):
            with st.expander(f"📌 {sec['titulo']}", expanded=False):
                st.markdown(sec["contenido"])
                conceptos = sec.get("conceptos_clave", [])
                if conceptos:
                    st.markdown("**Conceptos clave:** " + " · ".join(f"`{c}`" for c in conceptos))
        st.divider()
