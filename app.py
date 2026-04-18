import streamlit as st
import anthropic
import random
import json
import uuid
from datetime import datetime
from pathlib import Path

from banco_preguntas import BANCO, NIVELES, CATEGORIAS

st.set_page_config(
    page_title="Anatomía UCV — Banco de Preguntas",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FALLOS_PATH = Path(__file__).parent / "fallos.json"

# ── CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  .stApp { background: #0f1117; }
  .pregunta-card {
    background: #1a1d2e;
    border: 1px solid #3a3f5c;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
  }
  .nivel-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 8px;
  }
  .n1 { background:#7c3aed22; color:#a78bfa; border:1px solid #7c3aed55; }
  .n2 { background:#1d4ed822; color:#60a5fa; border:1px solid #1d4ed855; }
  .n3 { background:#05966922; color:#34d399; border:1px solid #05966955; }
  .concepto-tag {
    display: inline-block;
    background: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 11px;
  }
  .fallo-card {
    background: #1a1218;
    border: 1px solid #7f1d1d44;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
  }
  .flashcard-front {
    background: #1a1d2e;
    border: 2px solid #7c3aed;
    border-radius: 16px;
    padding: 30px 24px;
    text-align: center;
    min-height: 140px;
  }
  .flashcard-back {
    background: #0f1a12;
    border: 2px solid #10b981;
    border-radius: 16px;
    padding: 24px;
    min-height: 140px;
  }
  .stat-box {
    background: #1a1d2e;
    border: 1px solid #3a3f5c;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
  }
  .pregunta-num { color:#a78bfa; font-size:13px; font-weight:600; }
  div[data-testid="stProgress"] > div { background: #7c3aed44; }
</style>
""", unsafe_allow_html=True)

# ── Persistencia de fallos ───────────────────────────────────────
def cargar_fallos() -> list:
    if FALLOS_PATH.exists():
        try:
            return json.loads(FALLOS_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def guardar_fallos(fallos: list):
    try:
        FALLOS_PATH.write_text(json.dumps(fallos, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def registrar_fallo(pregunta: dict, tema: str, respuesta_dada: str, generada_ia: bool = False):
    fallos = st.session_state.fallos
    pid = pregunta["id"]
    for f in fallos:
        if f["pregunta_id"] == pid and not f.get("aprendida"):
            f["veces_fallada"] += 1
            f["ultima_fecha"] = datetime.now().strftime("%Y-%m-%d")
            guardar_fallos(fallos)
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
    guardar_fallos(fallos)

# ── Session state ────────────────────────────────────────────────
defaults = {
    "fallos": cargar_fallos(),
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
    """Muestra correcto/incorrecto + explicación breve tras cada pregunta."""
    if letra == p["correcta"]:
        st.success("✅  ¡Correcto!")
    else:
        st.error(f"❌  Incorrecto — era  **{p['correcta']})** {p['opciones'][p['correcta']]}")
    st.info(f"💬  {p['exp']}")

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
            model="claude-opus-4-7",
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
#  CABECERA
# ════════════════════════════════════════════════════════════════
portada = Path(__file__).parent / "portada.jpg"
if portada.exists():
    st.image(portada.read_bytes(), use_container_width=True)

st.markdown("## 🧠 Anatomía UCV — Banco de Preguntas")
st.caption("MS · MI · Cráneo · Vértebras  |  1º Medicina")

n_fallos_activos = sum(1 for f in st.session_state.fallos if not f.get("aprendida"))
col_a, col_b, col_c = st.columns(3)
with col_a:
    total_q = sum(len(v["preguntas"]) for v in BANCO.values())
    st.metric("Total preguntas", total_q)
with col_b:
    st.metric("Preguntas falladas", n_fallos_activos)
with col_c:
    temas_fallados = len({f["tema"] for f in st.session_state.fallos if not f.get("aprendida")})
    st.metric("Temas con fallos", temas_fallados)

# ════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════
tab_test, tab_revision, tab_fallos, tab_flash, tab_tfallo, tab_chat = st.tabs([
    "📚 Test", "📝 Revisión Test", "❌ Mis Fallos", "🃏 Flashcards", "🔁 Test de Fallos", "💬 Chat IA"
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
            pool = [(sel_key := temas_disp[sel], p) for p in BANCO[temas_disp[sel]]["preguntas"]]
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
                feedback_breve(p, st.session_state.test_last_letra)
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
    errores_rev = st.session_state.get("test_errores", []) + st.session_state.get("ft_errores", [])
    if not errores_rev:
        st.info("Aquí aparecerán los errores del último test realizado. ¡Haz un test primero!")
    else:
        st.markdown(f"### Errores del último test — {len(errores_rev)} pregunta(s) fallada(s)")
        st.caption("Repasa cada error con su explicación antes de continuar estudiando.")
        st.divider()
        for i, e in enumerate(errores_rev, 1):
            tema_nombre = BANCO.get(e.get("tema",""), {}).get("nombre", "")
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
                        guardar_fallos(st.session_state.fallos)
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
                    guardar_fallos(datos)
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

        n_ft = st.slider("Preguntas:", 3, min(20, len(pool_ft)), min(10, len(pool_ft)), key="n_ft")

        if ordenar_ft == "Más falladas primero":
            pool_ft_sorted = sorted(pool_ft, key=lambda x: x["veces_fallada"], reverse=True)
            muestra_ft = pool_ft_sorted[:n_ft]
        else:
            muestra_ft = random.sample(pool_ft, n_ft)

        st.info(f"**{len(pool_ft)} preguntas** en el banco de fallos para este filtro.")

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
#  TAB 5 — CHAT IA
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
                    model="claude-opus-4-7",
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
