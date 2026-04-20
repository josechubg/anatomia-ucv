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


def get_existing_enunciados(banco_path: Path) -> set:
    content = banco_path.read_text(encoding="utf-8")
    return set(re.findall(r'"enunciado":\s*"([^"]+)"', content))


def generar_preguntas(tema_key: str, tema_nombre: str, n: int, existentes: set) -> list:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    muestra_existentes = json.dumps(list(existentes)[:15], ensure_ascii=False)
    prompt = f"""Eres un profesor experto en Anatomía Humana para estudiantes de 1º de Medicina en España.

Genera exactamente {n} preguntas NUEVAS tipo test estilo MIR sobre: **{tema_nombre}**.

Requisitos:
- 4 opciones (A, B, C, D), solo una correcta
- Dificultad alta: clínica aplicada, lesiones nerviosas, variantes anatómicas, topografía
- NO uses estos enunciados ya existentes: {muestra_existentes}
- Campo "exp": máx 2 frases, preciso anatómicamente
- La respuesta correcta debe ser 100% correcta

Responde SOLO con un array JSON válido, sin texto adicional:
[
  {{
    "id": "auto_001",
    "concepto": "concepto evaluado",
    "enunciado": "Pregunta completa...",
    "opciones": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correcta": "A",
    "exp": "Explicación breve y precisa..."
  }}
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
                if all(k in p for k in ["enunciado", "opciones", "correcta", "exp"]):
                    if p["correcta"] in p["opciones"]:
                        if p["enunciado"] not in existentes:
                            validas.append(p)
            return validas
    except Exception as e:
        print(f"Error generando preguntas para {tema_key}: {e}")
    return []


def validar_pregunta(p: dict) -> bool:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    opciones_texto = "\n".join(f"{k}) {v}" for k, v in p["opciones"].items())
    prompt = f"""Verifica si esta respuesta anatómica es correcta:

PREGUNTA: {p['enunciado']}
OPCIONES:
{opciones_texto}
RESPUESTA MARCADA: {p['correcta']}) {p['opciones'][p['correcta']]}

Responde SOLO con JSON: {{"correcta": true/false, "razon": "breve"}}"""

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
                print(f"  ⚠️  Rechazada: {result.get('razon', '')}")
                return False
        return True
    except Exception:
        return True


def append_to_banco(banco_path: Path, tema_key: str, nuevas: list) -> int:
    for p in nuevas:
        p["id"] = f"{tema_key}_auto_{str(uuid.uuid4())[:8]}"

    content = banco_path.read_text(encoding="utf-8")

    bloque = f"\n# AUTO {date.today()} — {tema_key}\n"
    for p in nuevas:
        bloque += (
            f'if "{tema_key}" in BANCO and '
            f'not any(q["enunciado"] == {json.dumps(p["enunciado"], ensure_ascii=False)} '
            f'for q in BANCO["{tema_key}"]["preguntas"]):\n'
            f'    BANCO["{tema_key}"]["preguntas"].append({json.dumps(p, ensure_ascii=False)})\n'
        )

    insert_pos = content.rfind("\nNIVELES")
    if insert_pos == -1:
        insert_pos = len(content)

    content = content[:insert_pos] + bloque + content[insert_pos:]
    banco_path.write_text(content, encoding="utf-8")
    return len(nuevas)


def main():
    banco_path = Path(__file__).parent.parent / "banco_preguntas.py"
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

    try:
        ast.parse(banco_path.read_text(encoding="utf-8"))
        print("✅ Sintaxis correcta")
    except SyntaxError as e:
        print(f"❌ ERROR DE SINTAXIS: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
