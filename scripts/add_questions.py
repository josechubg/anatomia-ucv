"""
Script para generar nuevas preguntas de anatomía con Claude y añadirlas al banco.
Se ejecuta diariamente vía GitHub Actions.
"""

import anthropic
import json
import re
import sys
import os
import random
import uuid
import ast
from datetime import date
from pathlib import Path

TEMAS = {
    "manguito_rotador": "Manguito Rotador",
    "plexo_braquial": "Plexo Braquial",
    "huesos_ms": "Huesos del Miembro Superior",
    "huesos_mi": "Huesos del Miembro Inferior",
    "nervios_mmii": "Nervios del Miembro Inferior",
    "rodilla": "Rodilla y Meniscos",
    "huesos_craneo": "Huesos del Cráneo",
    "craneo_foramenes": "Forámenes del Cráneo",
    "nervios_craneales": "Nervios Craneales",
    "columna": "Columna Vertebral",
    "atlas_axis": "Atlas y Axis",
    "carpo_tarso": "Carpo y Tarso",
    "musculos_ms": "Músculos del Miembro Superior",
    "musculos_mi": "Músculos del Miembro Inferior",
    "arterias_ms_mi": "Arterias de Miembro Superior e Inferior",
    "articulacion_hombro": "Articulación del Hombro",
    "ligamentos_columna": "Ligamentos de la Columna",
    "articulacion_codo": "Articulación del Codo",
    "disco_intervertebral": "Disco Intervertebral",
    "suturas_fosas": "Suturas y Fosas del Cráneo",
}

PREGUNTAS_POR_DIA = 6

# Ejemplo de estructura exacta que deben tener las preguntas
ESTRUCTURA_EJEMPLO = '''{
  "id": "mr_001",
  "concepto": "músculos SITS",
  "enunciado": "¿Cuál de los siguientes NO forma parte del manguito rotador?",
  "opciones": {"A": "Supraespinoso", "B": "Infraespinoso", "C": "Deltoides", "D": "Subescapular"},
  "correcta": "C",
  "exp": "El manguito rotador = SITS: Supraespinoso, Infraespinoso, Teres minor, Subescapular. El deltoides es extrínseco y no forma parte."
}'''


def get_existing_enunciados(banco_path: Path) -> set:
    content = banco_path.read_text(encoding="utf-8")
    return set(re.findall(r'"enunciado":\s*"([^"]+)"', content))


def generar_preguntas(tema_key: str, tema_nombre: str, n: int, existentes: set) -> list:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    muestra_existentes = json.dumps(list(existentes)[:15], ensure_ascii=False)
    prompt = f"""Eres un profesor experto en Anatomía Humana para estudiantes de 1º de Medicina en España.

Genera exactamente {n} preguntas NUEVAS tipo test estilo MIR sobre: **{tema_nombre}**.

ESTRUCTURA OBLIGATORIA (sigue este formato exacto, campo por campo):
{ESTRUCTURA_EJEMPLO}

Reglas:
- "id": usa el formato "{tema_key}_auto_NNN"
- "concepto": 2-5 palabras que identifican el concepto anatómico evaluado
- "enunciado": pregunta completa, clara, con contexto clínico cuando sea posible
- "opciones": exactamente 4 opciones A/B/C/D, todas plausibles, solo una correcta
- "correcta": solo la letra (A, B, C o D)
- "exp": máx 2 frases. Primera frase: por qué la correcta es correcta. Segunda frase (opcional): dato clave para recordar.
- Dificultad alta: lesiones nerviosas, topografía, clínica aplicada, variantes anatómicas
- NO repitas estos enunciados: {muestra_existentes}
- La respuesta correcta debe ser 100% anatómicamente correcta

Responde SOLO con un array JSON válido, sin texto adicional antes ni después:
[
  {{ ... }},
  {{ ... }}
]"""

    try:
        resp = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2000,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": prompt}]
        )
        text = ""
        for block in resp.content:
            if hasattr(block, "text"):
                text = block.text.strip()
                break

        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            preguntas = json.loads(text[start:end])
            validas = []
            for p in preguntas:
                # Validar estructura completa
                if not all(k in p for k in ["concepto", "enunciado", "opciones", "correcta", "exp"]):
                    print(f"  ⚠️  Pregunta sin estructura completa, descartada")
                    continue
                if not all(k in p["opciones"] for k in ["A", "B", "C", "D"]):
                    print(f"  ⚠️  Pregunta sin 4 opciones A/B/C/D, descartada")
                    continue
                if p["correcta"] not in ["A", "B", "C", "D"]:
                    print(f"  ⚠️  Campo 'correcta' inválido: {p['correcta']}, descartada")
                    continue
                if p["enunciado"] in existentes:
                    print(f"  ⚠️  Enunciado duplicado, descartada")
                    continue
                validas.append(p)
            return validas
    except Exception as e:
        print(f"  Error generando preguntas para {tema_key}: {e}")
    return []


def validar_pregunta(p: dict) -> bool:
    """Segunda llamada a Claude para verificar que la respuesta correcta es correcta."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    opciones_texto = "\n".join(f"{k}) {v}" for k, v in p["opciones"].items())
    prompt = f"""Como experto en Anatomía Humana, verifica si esta respuesta es correcta:

PREGUNTA: {p['enunciado']}
OPCIONES:
{opciones_texto}
RESPUESTA MARCADA COMO CORRECTA: {p['correcta']}) {p['opciones'][p['correcta']]}

Responde SOLO con JSON: {{"correcta": true/false, "razon": "explicación breve si es falsa"}}"""

    try:
        resp = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.content[0].text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(text[start:end])
            if not result.get("correcta", True):
                print(f"  ⚠️  Rechazada por validación: {result.get('razon', '')}")
                return False
        return True
    except Exception:
        return True


def append_to_banco(banco_path: Path, tema_key: str, nuevas: list) -> int:
    """Añade preguntas al banco usando append en el array del tema."""
    for p in nuevas:
        p["id"] = f"{tema_key}_auto_{str(uuid.uuid4())[:8]}"

    content = banco_path.read_text(encoding="utf-8")

    bloque = f"\n# AUTO {date.today()} — {tema_key}\n"
    for p in nuevas:
        p_json = json.dumps(p, ensure_ascii=False)
        enunciado_escaped = json.dumps(p["enunciado"], ensure_ascii=False)
        bloque += (
            f'if "{tema_key}" in BANCO and '
            f'not any(q["enunciado"] == {enunciado_escaped} '
            f'for q in BANCO["{tema_key}"]["preguntas"]):\n'
            f'    BANCO["{tema_key}"]["preguntas"].append({p_json})\n'
        )

    insert_pos = content.rfind("\nNIVELES")
    if insert_pos == -1:
        insert_pos = len(content)

    content = content[:insert_pos] + bloque + content[insert_pos:]
    banco_path.write_text(content, encoding="utf-8")
    return len(nuevas)


def save_update_log(repo_path: Path, total_nuevas: int):
    """Guarda el log de actualización para mostrar en la web."""
    log_path = repo_path / "update_log.json"
    hoy = date.today()
    fecha_str = hoy.strftime("%-d %b %Y") if os.name != "nt" else hoy.strftime("%d %b %Y").lstrip("0")
    data = {
        "fecha": fecha_str,
        "nuevas": total_nuevas,
        "total_acumuladas": total_nuevas
    }
    # Si ya existe, acumular el total
    if log_path.exists():
        try:
            prev = json.loads(log_path.read_text(encoding="utf-8"))
            data["total_acumuladas"] = prev.get("total_acumuladas", 0) + total_nuevas
        except Exception:
            pass
    log_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📝 update_log.json guardado: {data}")


def main():
    banco_path = Path(__file__).parent.parent / "banco_preguntas.py"
    repo_path = Path(__file__).parent.parent

    if not banco_path.exists():
        print(f"ERROR: No se encuentra {banco_path}")
        sys.exit(1)

    existentes = get_existing_enunciados(banco_path)
    print(f"Preguntas existentes: {len(existentes)}")

    temas_seleccionados = random.sample(list(TEMAS.items()), min(3, len(TEMAS)))
    preguntas_por_tema = max(1, PREGUNTAS_POR_DIA // len(temas_seleccionados))

    total_añadidas = 0
    for tema_key, tema_nombre in temas_seleccionados:
        print(f"\n📚 {tema_nombre}")
        nuevas = generar_preguntas(tema_key, tema_nombre, preguntas_por_tema, existentes)
        print(f"  Generadas: {len(nuevas)} — Validando...")
        validadas = [p for p in nuevas if validar_pregunta(p)]
        print(f"  Validadas: {len(validadas)}")

        if validadas:
            n = append_to_banco(banco_path, tema_key, validadas)
            total_añadidas += n
            for p in validadas:
                existentes.add(p["enunciado"])

    print(f"\n✅ Total añadidas: {total_añadidas}")

    # Verificar sintaxis
    try:
        ast.parse(banco_path.read_text(encoding="utf-8"))
        print("✅ Sintaxis de banco_preguntas.py correcta")
    except SyntaxError as e:
        print(f"❌ ERROR DE SINTAXIS: {e}")
        sys.exit(1)

    # Guardar log solo si se añadieron preguntas
    if total_añadidas > 0:
        save_update_log(repo_path, total_añadidas)


if __name__ == "__main__":
    main()
