#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agente Anatomía UCV — Miembro Superior, Miembro Inferior, Cráneo, Vértebras"""

import anthropic
import sys
import random

ESQUEMAS = {

    # ══════════════════════════════════════════════════════
    #  NIVEL 1 — MUY IMPORTANTES  ⭐⭐⭐
    # ══════════════════════════════════════════════════════

    "huesos_ms": {
        "nombre": "HUESOS DEL MIEMBRO SUPERIOR",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║           HUESOS DEL MIEMBRO SUPERIOR                        ║
╠══════════════════════════════════════════════════════════════╣
║  CLAVÍCULA: extremo esternal (articulación esternoclavicular)║
║             extremo acromial (articulación acromioclavicular)║
║                                                              ║
║  ESCÁPULA:  Espina → acromion · Coracoides (apófisis ant.)  ║
║             Cavidad glenoidea · Fosa supra/infra/subescapular║
║             Ángulo inferior (vértice, palpable)              ║
║                                                              ║
║  HÚMERO:    Cabeza (2/3 esfera) · Cuello anatómico          ║
║             Cuello QUIRÚRGICO (fractura + frecuente)        ║
║             Troquíter (mayor) → SITS (supra/infra/red.menor)║
║             Troquín (menor) → subescapular                   ║
║             Corredera bicipital (entre troquíter y troquín)  ║
║             Canal de torsión/radial (fractura → n. radial)  ║
║             Epicóndilo (lateral) · Epitróclea (medial)       ║
║             Cóndilo (articula radio) · Tróclea (articula cúbito)║
║                                                              ║
║  RADIO:     Cabeza (cóndilo) · Cuello · Tuberosidad bicipital║
║             Estiloides radial (más DISTAL que cubital)       ║
║                                                              ║
║  CÚBITO:    Olécranon · Apófisis coronoides                  ║
║             Escotadura troclear (articula tróclea)           ║
║             Estiloides cubital (más PROXIMAL que radial)     ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Troquíter = lateral/mayor. Troquín = medial/menor        ║
║  ⚡ Fractura cuello quirúrgico → lesión nervio axilar        ║
║     Fractura canal torsión → lesión nervio radial             ║
║     Epitróclea → nervio cubital. Cóndilo → nervio radial     ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿En qué estructura del húmero se insertan los músculos del manguito rotador supraespinoso, infraespinoso y redondo menor?",
                "opciones": {"A": "Troquín", "B": "Troquíter", "C": "Epicóndilo", "D": "Cabeza del húmero"},
                "correcta": "B",
                "exp": "Troquíter (tubérculo mayor): supraespinoso (faceta superior), infraespinoso (faceta media), redondo menor (faceta inferior). Troquín (tubérculo menor): solo el subescapular."
            },
            {
                "enunciado": "Una fractura en el canal de torsión del húmero lesiona con mayor frecuencia el nervio:",
                "opciones": {"A": "Axilar", "B": "Mediano", "C": "Radial", "D": "Cubital"},
                "correcta": "C",
                "exp": "El nervio radial discurre en el canal de torsión (surco radial) del húmero. Fractura de la diáfisis humeral → lesión del radial → caída de muñeca (wrist drop)."
            },
            {
                "enunciado": "¿Cuál es la fractura más frecuente del húmero proximal?",
                "opciones": {"A": "Fractura de la cabeza", "B": "Fractura del cuello anatómico", "C": "Fractura del cuello quirúrgico", "D": "Fractura del troquíter aislado"},
                "correcta": "C",
                "exp": "El cuello QUIRÚRGICO (por debajo de las tuberosidades) es la fractura más frecuente del húmero proximal. Riesgo de lesión del nervio axilar y arteria circunfleja humeral anterior."
            },
            {
                "enunciado": "¿La estiloides del radio es más distal o más proximal que la del cúbito?",
                "opciones": {"A": "Más proximal", "B": "Más distal", "C": "Al mismo nivel", "D": "Depende de la posición"},
                "correcta": "B",
                "exp": "La estiloides RADIAL es ~1 cm más distal que la cubital. Dato importante en fracturas: la fractura de Colles invierte esta relación (estiloides radial queda al mismo nivel o más proximal)."
            },
        ]
    },

    "plexo_braquial": {
        "nombre": "PLEXO BRAQUIAL — C5 a T1",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║              PLEXO BRAQUIAL  (C5–T1)                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RAÍCES → TRONCOS → DIVISIONES → FASCÍCULOS → NERVIOS       ║
║  "Randy Travis Drinks Cold Beer"                             ║
║                                                              ║
║  C5 ──┐                                                      ║
║       ├── SUPERIOR ───┐                                      ║
║  C6 ──┘               ├──> LATERAL ──> Musculocutáneo       ║
║                        │         (parcial) Mediano           ║
║  C7 ───── MEDIO ──────┤                                      ║
║                        ├──> POSTERIOR ──> Radial + Axilar   ║
║  C8 ──┐               │                                      ║
║       ├── INFERIOR ───┘                                      ║
║  T1 ──┘               └──> MEDIAL ──> Cubital               ║
║                                  (parcial) Mediano           ║
║                                                              ║
║  NERVIOS TERMINALES:                                         ║
║  Musculocutáneo (C5-C7) → bíceps, braquial, coracobraquial  ║
║  Mediano (C6-T1)        → flexores antebrazo, tenar, 2 lumb.║
║  Cubital (C8-T1)        → hipotenar, interóseos, 2 lumb.    ║
║  Radial (C5-T1)         → todos los extensores              ║
║  Axilar (C5-C6)         → deltoides + redondo menor         ║
║                                                              ║
║  ERB C5-C6: brazo en aducción + pronación ("dar propina")   ║
║  KLUMPKE C8-T1: mano en garra + Horner (ptosis+miosis)      ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Fascículo POSTERIOR → radial + axilar (extensores)       ║
║  ⚡ Wrist drop=radial · Garra cubital=cubital · Predicador=mediano║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuáles raíces forman la parálisis de Erb?",
                "opciones": {"A": "C5-C6", "B": "C7-C8", "C": "C8-T1", "D": "C6-C7"},
                "correcta": "A",
                "exp": "Erb-Duchenne (C5-C6): brazo en aducción, rotación interna, pronación ('posición de propina'). Klumpke (C8-T1): mano en garra + síndrome de Horner si afecta T1."
            },
            {
                "enunciado": "El nervio axilar inerva el deltoides y procede del fascículo:",
                "opciones": {"A": "Lateral", "B": "Medial", "C": "Posterior", "D": "Tronco superior"},
                "correcta": "C",
                "exp": "El fascículo POSTERIOR origina el nervio axilar (C5-C6) y el radial (C5-T1). El fascículo lateral origina el musculocutáneo y parte del mediano. El medial origina el cubital y parte del mediano."
            },
            {
                "enunciado": "'Mano de predicador' con pérdida de sensibilidad en 3,5 dedos radiales indica lesión de:",
                "opciones": {"A": "Nervio radial", "B": "Nervio cubital", "C": "Nervio mediano", "D": "Nervio axilar"},
                "correcta": "C",
                "exp": "Mediano: 'mano de predicador' (no puede flexionar índice y corazón), atrofia del tenar, pérdida de sensibilidad en los 3,5 dedos radiales. Típico del síndrome del túnel carpiano."
            },
            {
                "enunciado": "¿Qué nervio inerva TODOS los músculos extensores del miembro superior?",
                "opciones": {"A": "Nervio mediano", "B": "Nervio cubital", "C": "Nervio radial", "D": "Nervio musculocutáneo"},
                "correcta": "C",
                "exp": "El nervio RADIAL (fascículo posterior, C5-T1) inerva todos los extensores: tríceps, extensores de muñeca y dedos, supinador, braquiorradial. Lesión → wrist drop + pérdida de supinación."
            },
        ]
    },

    "manguito_rotador": {
        "nombre": "MANGUITO ROTADOR — SITS",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║           MANGUITO ROTADOR — SITS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  S — Supraespinoso   → Abducción 0-15°                       ║
║      N. supraescapular (C5-C6)                               ║
║      Inserción: faceta SUPERIOR del troquíter                ║
║      Pasa bajo el arco coracoacromial → compresión           ║
║                                                              ║
║  I — Infraespinoso   → Rotación EXTERNA                      ║
║      N. supraescapular (C5-C6)                               ║
║      Inserción: faceta MEDIA del troquíter                   ║
║                                                              ║
║  T — Redondo menor   → Rotación EXTERNA                      ║
║      N. axilar (C5-C6)                                       ║
║      Inserción: faceta INFERIOR del troquíter                ║
║                                                              ║
║  S — Subescapular    → Rotación INTERNA                      ║
║      N. subescapular (C5-C6)                                 ║
║      Inserción: TROQUÍN (cara anterior del húmero)           ║
║                                                              ║
║  Deltoides (N. axilar): abducción 15-90° y más               ║
║  Trapecio + serrato: rotan escápula >90°                     ║
╠══════════════════════════════════════════════════════════════╣
║  💡 SITS: Supra-Infra-Teres minor-Sub                        ║
║     Rot. externa = I + T (2 músculos). Rot. interna = S(sub)║
║  ⚡ Rotura supra → arco doloroso 60-120°. Prueba Neer+Hawkins║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué músculo del manguito rotador se inserta en el troquín?",
                "opciones": {"A": "Supraespinoso", "B": "Infraespinoso", "C": "Redondo menor", "D": "Subescapular"},
                "correcta": "D",
                "exp": "El subescapular (único rotador interno del manguito) se inserta en el troquín (tubérculo menor). Los otros 3 (supra, infra, redondo menor) se insertan en el troquíter."
            },
            {
                "enunciado": "El arco doloroso entre 60° y 120° de abducción indica lesión del:",
                "opciones": {"A": "Deltoides", "B": "Supraespinoso", "C": "Infraespinoso", "D": "Subescapular"},
                "correcta": "B",
                "exp": "El supraespinoso queda comprimido bajo el arco coracoacromial entre 60-120° → arco doloroso. La rotura completa produce signo de 'caída del brazo' (drop arm sign)."
            },
            {
                "enunciado": "¿Qué nervio inerva tanto el infraespinoso como el supraespinoso?",
                "opciones": {"A": "Nervio axilar", "B": "Nervio subescapular", "C": "Nervio supraescapular", "D": "Nervio radial"},
                "correcta": "C",
                "exp": "El nervio supraescapular (C5-C6, del tronco superior) inerva supraespinoso e infraespinoso. Puede lesionarse en el escotadura supraescapular → atrofia de ambos músculos."
            },
        ]
    },

    "huesos_mi": {
        "nombre": "HUESOS DEL MIEMBRO INFERIOR",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║           HUESOS DEL MIEMBRO INFERIOR                        ║
╠══════════════════════════════════════════════════════════════╣
║  COXAL (ilion + isquion + pubis):                            ║
║  Cresta ilíaca (EIAS, EIAI) · Espina isquiática             ║
║  Tuberosidad isquiática ("hueso de sentarse")                ║
║  Escotadura isquiática mayor (ciático) y menor (obturador)  ║
║  Acetábulo: confluencia de los 3 huesos                      ║
║  Línea terminal: separa pelvis mayor de menor                ║
║                                                              ║
║  FÉMUR:                                                      ║
║  Cabeza (2/3 esfera, fóvea = ligamento redondo)              ║
║  Cuello: ángulo 125-135° (coxa vara <120°, valga >135°)     ║
║  Anteversión femoral: ~15° normal                            ║
║  Trocánter MAYOR (lateral) · Trocánter MENOR (posteromedial)║
║  Glúteo mayor → trocánter mayor (vía tracto iliotibial)     ║
║  Línea áspera (posterior) → inserción aductores y vasto      ║
║  Cóndilos medial y lateral · Epicóndilos · Fosa intercondílea║
║                                                              ║
║  TIBIA: Platillo medial (mayor) + lateral · Espinas tibiales ║
║  Tuberosidad tibial anterior (inserción cuádriceps via rótula)║
║  Maléolo MEDIAL                                              ║
║                                                              ║
║  PERONÉ: Cabeza (art. tibioperonea superior) · Maléolo LAT. ║
║  Maléolo lateral más DISTAL que el medial (1-2 cm)          ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Trocánter mayor=lateral, menor=posteromedial             ║
║  ⚡ Fractura cuello fémur → necrosis avascular cabeza femoral║
║     Maléolo lateral más distal → esguince ligamentos laterales║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuál es el ángulo normal del cuello del fémur?",
                "opciones": {"A": "90-100°", "B": "110-115°", "C": "125-135°", "D": "145-150°"},
                "correcta": "C",
                "exp": "El ángulo cervicodiafisario normal es 125-135°. Coxa vara (<120°): acorta el miembro. Coxa valga (>135°): predispone a luxación. Fractura de cuello femoral → riesgo de necrosis avascular."
            },
            {
                "enunciado": "¿En qué hueso se inserta el ligamento redondo de la cadera?",
                "opciones": {"A": "Trocánter mayor", "B": "Trocánter menor", "C": "Fóvea de la cabeza femoral", "D": "Cuello del fémur"},
                "correcta": "C",
                "exp": "El ligamento redondo del fémur va desde la fóvea de la cabeza femoral hasta el acetábulo (zona de la escotadura acetabular). Transporta la arteria del ligamento redondo (rama obturadora) que irriga parte de la cabeza."
            },
            {
                "enunciado": "¿Qué maléolo es más distal?",
                "opciones": {"A": "Maléolo medial (tibial)", "B": "Maléolo lateral (peroneal)", "C": "Son el mismo nivel", "D": "Depende de la posición"},
                "correcta": "B",
                "exp": "El maléolo LATERAL (peroneo) es ~1-2 cm más distal que el medial (tibial). Esto hace que el tobillo esté más protegido lateralmente. En esguince de tobillo los ligamentos laterales son los más lesionados."
            },
            {
                "enunciado": "La tuberosidad isquiática es el punto de origen de los músculos:",
                "opciones": {"A": "Glúteos", "B": "Cuádriceps", "C": "Isquiotibiales", "D": "Aductores"},
                "correcta": "C",
                "exp": "Los isquiotibiales (bíceps femoral, semitendinoso y semimembranoso) se originan en la tuberosidad isquiática. Es el hueso sobre el que nos sentamos, de ahí su nombre. Lesión: 'hamstring injury'."
            },
        ]
    },

    "nervios_mmii": {
        "nombre": "NERVIOS MIEMBRO INFERIOR — Plexos lumbar y sacro",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          NERVIOS DEL MIEMBRO INFERIOR                        ║
╠══════════════════════════════════════════════════════════════╣
║  PLEXO LUMBAR (L1-L4):                                       ║
║  Femoral (L2-L3-L4) → cuádriceps + sensib. ant. muslo       ║
║    └─ Safeno → sensibilidad cara medial pierna y pie         ║
║  Obturador (L2-L3-L4) → aductores + sensib. medial muslo    ║
║                                                              ║
║  PLEXO SACRO (L4-S3):                                        ║
║  Ciático (L4-S3) → sale infrapiriforme (escotadura mayor)   ║
║    ├─ Tibial (L4-S3)                                         ║
║    │   → flexores plantares (gastrocnemio, sóleo)            ║
║    │   → inversión (tibial posterior)                        ║
║    │   → sensibilidad planta del pie                         ║
║    └─ Peroneo común (L4-S2)                                  ║
║        ├─ Peroneo PROFUNDO → dorsiflexión + extensión dedos  ║
║        │   → sensibilidad 1er espacio interdigital           ║
║        └─ Peroneo SUPERFICIAL → eversión (peroneos)         ║
║            → sensibilidad dorso del pie                      ║
║                                                              ║
║  LESIONES:                                                   ║
║  Femoral → no extiende rodilla, no sube escaleras            ║
║  Peroneo común (rodea cabeza peroné) → pie caído (drop foot) ║
║  Tibial → no se pone de puntillas, anestesia de la planta    ║
║  Ciático → combinación tibial + peroneo                      ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Peroneo común = muy vulnerable en cabeza del peroné      ║
║  ⚡ Lasègue (+) → irritación ciática L4-S1                   ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "Un paciente no puede dorsiflexionar el pie tras fractura de cabeza del peroné. Nervio lesionado:",
                "opciones": {"A": "Nervio tibial", "B": "Nervio safeno", "C": "Nervio peroneo común", "D": "Nervio femoral"},
                "correcta": "C",
                "exp": "El peroneo común rodea la cabeza del peroné → muy vulnerable. Se divide en profundo (dorsiflexión + extensión dedos) y superficial (eversión). Lesión del tronco → pie caído completo."
            },
            {
                "enunciado": "¿Qué movimiento se pierde con la lesión del nervio tibial?",
                "opciones": {"A": "Dorsiflexión del pie", "B": "Extensión de los dedos", "C": "Flexión plantar", "D": "Eversión del pie"},
                "correcta": "C",
                "exp": "El nervio tibial inerva los flexores plantares (gastrocnemio, sóleo → flexión plantar) y los músculos de la planta. Lesión → no puede ponerse de puntillas + anestesia de la planta."
            },
            {
                "enunciado": "¿Qué nervio inerva los músculos aductores del muslo?",
                "opciones": {"A": "Nervio femoral", "B": "Nervio obturador", "C": "Nervio ciático", "D": "Nervio glúteo superior"},
                "correcta": "B",
                "exp": "El nervio obturador (L2-L4) inerva los aductores del muslo (aductor largo, corto y mayor + gracilis). Sale por el foramen obturador. Lesión → incapacidad de aducción."
            },
            {
                "enunciado": "El nervio ciático sale de la pelvis por la escotadura isquiática mayor pasando:",
                "opciones": {"A": "Por encima del músculo piriforme", "B": "Por debajo del músculo piriforme", "C": "A través del músculo piriforme", "D": "Por el foramen obturador"},
                "correcta": "B",
                "exp": "El ciático sale por el foramen infrapiriforme (escotadura isquiática mayor, debajo del piriforme) en el 90% de los casos. En el 10%, el peroneo común perfora el piriforme → síndrome del piriforme."
            },
        ]
    },

    "rodilla": {
        "nombre": "ARTICULACIÓN DE LA RODILLA — Meniscos y ligamentos",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║         ARTICULACIÓN DE LA RODILLA                           ║
╠══════════════════════════════════════════════════════════════╣
║  MENISCOS:                                                   ║
║  Medial: forma de C (semiluna) · menos móvil · MÁS LESIONADO║
║          unido al ligamento colateral medial (LCM)           ║
║  Lateral: forma de O · más móvil · menos lesionado           ║
║                                                              ║
║  LIGAMENTOS CRUZADOS:                                        ║
║  LCA (anterior): tibia ant-lat → fémur post-lat              ║
║       Evita traslación ANTERIOR de la tibia                  ║
║       Prueba: cajón anterior (+) · Lachman (+)               ║
║       Lesión: pivote + desaceleración (deporte)              ║
║                                                              ║
║  LCP (posterior): tibia post-med → fémur ant-med             ║
║       Evita traslación POSTERIOR de la tibia                 ║
║       Prueba: cajón posterior (+)                            ║
║       Lesión: golpe en tibia proximal (parachoque de coche)  ║
║                                                              ║
║  LIGAMENTOS COLATERALES:                                     ║
║  LCM (medial/tibial): rodilla laxa al VALGO forzado         ║
║       Unido al menisco medial → lesión combinada             ║
║  LCL (lateral/peroneo): rodilla laxa al VARO forzado        ║
║                                                              ║
║  TRÍADA DESGRACIADA (O'Donoghue): LCA + LCM + menisco medial║
╠══════════════════════════════════════════════════════════════╣
║  💡 Cajón anterior = LCA · Cajón posterior = LCP             ║
║  ⚡ McMurray (+) → lesión de menisco (clic doloroso)         ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuál de los dos meniscos se lesiona con más frecuencia y por qué?",
                "opciones": {
                    "A": "El lateral, por ser más móvil",
                    "B": "El medial, por ser menos móvil y estar unido al LCM",
                    "C": "El lateral, porque tiene forma de O",
                    "D": "El medial, porque es más grande"
                },
                "correcta": "B",
                "exp": "El menisco MEDIAL es menos móvil (está unido al LCM) y tiene forma de C semiluna. Al ser menos móvil, queda atrapado con más facilidad entre los cóndilos femoral y tibial durante movimientos bruscos."
            },
            {
                "enunciado": "¿Qué ligamento evita la traslación anterior de la tibia sobre el fémur?",
                "opciones": {"A": "LCP", "B": "LCM", "C": "LCA", "D": "LCL"},
                "correcta": "C",
                "exp": "El LCA (ligamento cruzado anterior) evita la traslación ANTERIOR de la tibia. Prueba del cajón anterior y de Lachman. El LCP evita la traslación posterior (cajón posterior)."
            },
            {
                "enunciado": "La 'tríada desgraciada' de O'Donoghue incluye:",
                "opciones": {
                    "A": "LCA + LCP + rótula",
                    "B": "LCA + LCM + menisco medial",
                    "C": "LCP + LCL + menisco lateral",
                    "D": "LCA + LCL + menisco lateral"
                },
                "correcta": "B",
                "exp": "Tríada desgraciada (O'Donoghue): LCA + LCM + menisco MEDIAL. Mecanismo: valgus + rotación externa + flexión (típica en fútbol). El menisco medial se lesiona porque está unido al LCM."
            },
        ]
    },

    "huesos_craneo": {
        "nombre": "HUESOS DEL CRÁNEO — Neurocráneo y viscerocráneo",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║            HUESOS DEL CRÁNEO                                 ║
╠══════════════════════════════════════════════════════════════╣
║  NEUROCRÁNEO (8 huesos):                                     ║
║  ┌─────────────────────────────────────────┐                 ║
║  │  1 Frontal    │ 2 Parietales            │                 ║
║  │  1 Occipital  │ 2 Temporales            │                 ║
║  │  1 Esfenoides │ 1 Etmoides              │                 ║
║  └─────────────────────────────────────────┘                 ║
║  Regla: 1-2-1-2-1-1 (F-P-O-T-Esf-Etm)                      ║
║                                                              ║
║  VISCEROCRÁNEO (14 huesos):                                  ║
║  Par (×2 cada uno = 12): Maxilar · Palatino · Cigomático    ║
║                          Nasal · Lagrimal · Cornete inf.     ║
║  Impares (×1 = 2):       Vómer · Mandíbula                   ║
║                                                              ║
║  PUNTOS DE REFERENCIA:                                       ║
║  Bregma    → sutura coronal + sagital (ant.)                 ║
║  Lambda    → sutura sagital + lambdoidea (post.)             ║
║  Ptérion   → unión frontal+parietal+temporal+esfenoides      ║
║              = zona MÁS DELGADA del cráneo                   ║
║              cubre arteria meníngea media → hematoma epidural║
║  Asterión  → unión parietal+occipital+temporal               ║
║                                                              ║
║  SUTURAS: Coronal · Sagital · Lambdoidea · Escamosa          ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Ptérion = zona débil → fractura → hematoma epidural       ║
║  ⚡ Fontanela anterior (bregma) cierra a los 18-24 meses     ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuántos huesos forman el neurocráneo?",
                "opciones": {"A": "6", "B": "7", "C": "8", "D": "14"},
                "correcta": "C",
                "exp": "8 huesos del neurocráneo: frontal (1), parietales (2), occipital (1), temporales (2), esfenoides (1), etmoides (1). Regla 1-2-1-2-1-1."
            },
            {
                "enunciado": "¿Qué punto craneal es el más delgado y cubre la arteria meníngea media?",
                "opciones": {"A": "Bregma", "B": "Lambda", "C": "Pterion", "D": "Asterión"},
                "correcta": "C",
                "exp": "El ptérion (unión de frontal, parietal, temporal y ala mayor del esfenoides) es la zona más delgada del cráneo. Un golpe aquí → fractura → rotura de la arteria meníngea media → hematoma epidural con intervalo lúcido."
            },
            {
                "enunciado": "La sutura que une los dos huesos parietales es:",
                "opciones": {"A": "Sutura coronal", "B": "Sutura sagital", "C": "Sutura lambdoidea", "D": "Sutura escamosa"},
                "correcta": "B",
                "exp": "Sutura sagital = entre los dos parietales (en la línea media). Coronal = frontal + parietales. Lambdoidea = parietales + occipital. Escamosa = parietal + temporal."
            },
            {
                "enunciado": "¿Cuáles son los únicos huesos impares del viscerocráneo?",
                "opciones": {"A": "Maxilar y palatino", "B": "Vómer y mandíbula", "C": "Cigomático y nasal", "D": "Lagrimal y cornete"},
                "correcta": "B",
                "exp": "Los únicos huesos impares del viscerocráneo son el vómer (tabique nasal inferior) y la mandíbula. El resto son pares (×2): maxilar, palatino, cigomático, nasal, lagrimal, cornete inferior."
            },
        ]
    },

    "craneo_foramenes": {
        "nombre": "FORÁMENES DE LA BASE DEL CRÁNEO",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║        FORÁMENES DE LA BASE DEL CRÁNEO                       ║
╠══════════════════════════════════════════════════════════════╣
║  FOSA ANTERIOR:                                              ║
║    Lámina cribosa (etmoides) → NC I (olfatorio)              ║
║                                                              ║
║  FOSA MEDIA:                                                 ║
║    Canal óptico          → NC II + a. oftálmica              ║
║    Fisura orbitaria sup. → NC III, IV, V1, VI + v. oftálmica ║
║    Foramen rotundum      → NC V2 (maxilar)                   ║
║    Foramen oval          → NC V3 (mandibular)                ║
║    Foramen espinoso      → arteria meníngea media            ║
║    Foramen lacerum       → cubierto por cartílago (en vivo)  ║
║                                                              ║
║  FOSA POSTERIOR:                                             ║
║    Meato auditivo interno→ NC VII + VIII                     ║
║    Foramen yugular       → NC IX, X, XI + v. yugular int.   ║
║    Canal hipogloso       → NC XII                            ║
║    Foramen magno         → bulbo raquídeo + NC XI + aa.      ║
║                                                              ║
║  REGLA: Rotundum=V2 · oVal=V3 · Yugular=9+10+11             ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Foramen espinoso → a. meníngea media → hematoma epidural ║
║  ⚡ Síndrome del agujero rasgado posterior = lesión IX+X+XI  ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Por qué foramen pasa el nervio mandibular (V3)?",
                "opciones": {"A": "Foramen rotundum", "B": "Foramen oval", "C": "Fisura orbitaria superior", "D": "Canal óptico"},
                "correcta": "B",
                "exp": "Regla: Rotundum=V2 (maxilar), oVal=V3 (mandibular). Por la fisura orbitaria superior pasan III+IV+V1+VI. Por el canal óptico pasan NC II y la arteria oftálmica."
            },
            {
                "enunciado": "¿Qué nervios craneales pasan por el foramen yugular?",
                "opciones": {"A": "VII + VIII", "B": "IX + X + XI", "C": "X + XI + XII", "D": "IX + X + XII"},
                "correcta": "B",
                "exp": "Foramen yugular (agujero rasgado posterior): NC IX (glosofaríngeo) + X (vago) + XI (espinal accesorio) + vena yugular interna. Síndrome = parálisis IX+X+XI."
            },
            {
                "enunciado": "¿Qué estructura pasa por el meato auditivo interno?",
                "opciones": {"A": "NC V + VI", "B": "NC VII + VIII", "C": "NC IX + X", "D": "NC XI + XII"},
                "correcta": "B",
                "exp": "El meato auditivo interno (en el peñasco del temporal): NC VII (facial) + NC VIII (vestibulococlear). El schwannoma del VIII puede comprimir ambos → hipoacusia + parálisis facial."
            },
        ]
    },

    "nervios_craneales": {
        "nombre": "NERVIOS CRANEALES — Los 12 pares",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║              NERVIOS CRANEALES — Los 12 pares                ║
╠══════════════════════════════════════════════════════════════╣
║  I   Olfatorio     → Olfato (S)                              ║
║  II  Óptico        → Visión (S)                              ║
║  III Motor oc. com.→ Todos los músculos ojo salvo IV y VI   ║
║                      + elevador párpado + constric. pupila   ║
║  IV  Troclear      → Oblicuo SUPERIOR (M)                   ║
║  V   Trigémino     → Sensib. cara + masticación (S+M)        ║
║        V1 Oftálmico · V2 Maxilar · V3 Mandibular            ║
║  VI  Motor oc. ext.→ Recto LATERAL (M)                      ║
║  VII Facial        → Mímica + gusto 2/3 ant. + glándulas    ║
║  VIII Vestibulococlear→ Audición + equilibrio (S)            ║
║  IX  Glosofaríngeo → Gusto 1/3 post + deglución (S+M+PS)   ║
║  X   Vago          → Vísceras tórax y abdomen (S+M+PS)      ║
║  XI  Espinal       → ECM + trapecio (M)                      ║
║  XII Hipogloso     → Musculatura de la lengua (M)            ║
║                                                              ║
║  LR6SO4: Recto Lateral=VI · Oblicuo Superior=IV · resto=III ║
╠══════════════════════════════════════════════════════════════╣
║  💡 NC único que emerge dorsal: IV (troclear)                ║
║     NC más largo intracraneal: IV                            ║
║  ⚡ Ptosis+midriasis → NC III. Parálisis facial periférica  ║
║     (hemicara completa) vs central (solo hemiboca inferior). ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "Un paciente no puede abducir el ojo (mirar hacia afuera). ¿Qué nervio está lesionado?",
                "opciones": {"A": "NC III", "B": "NC IV", "C": "NC VI", "D": "NC VII"},
                "correcta": "C",
                "exp": "NC VI (motor ocular externo) inerva únicamente el recto lateral → abducción del ojo. Lesión → estrabismo convergente. LR6SO4: Recto Lateral=VI, Oblicuo Superior=IV, el resto=III."
            },
            {
                "enunciado": "Parálisis facial periférica (Bell) afecta todo el hemicara porque:",
                "opciones": {
                    "A": "El NC VII cruza en la protuberancia",
                    "B": "La frente tiene inervación bilateral cortical, pero en la periferia depende solo del NC VII ipsilateral",
                    "C": "La corteza motora controla solo la mitad inferior de la cara",
                    "D": "El NC VII tiene dos raíces"
                },
                "correcta": "B",
                "exp": "La frente tiene representación BILATERAL en la corteza → lesión central del VII (ACV) solo afecta hemiboca inferior. Lesión PERIFÉRICA del NC VII → todo el hemicara (incluyendo frente) ipsilateral."
            },
            {
                "enunciado": "¿Qué nervio craneal inerva el músculo esternocleidomastoideo?",
                "opciones": {"A": "NC X", "B": "NC XI", "C": "NC XII", "D": "NC IX"},
                "correcta": "B",
                "exp": "NC XI (espinal o accesorio) inerva el ECM y el trapecio. Lesión → cabeza desviada al lado contrario (ECM contralateral la gira) + hombro caído ipsilateral (trapecio)."
            },
            {
                "enunciado": "¿Cuál es el único nervio craneal que emerge por la cara DORSAL del tronco encefálico?",
                "opciones": {"A": "NC III", "B": "NC IV", "C": "NC VI", "D": "NC VIII"},
                "correcta": "B",
                "exp": "El NC IV (troclear) es el único que emerge por la cara DORSAL del mesencéfalo (debajo del colículo inferior). También es el más delgado y el de mayor recorrido intracraneal. Lesión → diplopía al bajar escaleras."
            },
        ]
    },

    "columna": {
        "nombre": "COLUMNA VERTEBRAL — Regiones y características",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║              COLUMNA VERTEBRAL                               ║
╠══════════════════════════════════════════════════════════════╣
║  REGIONES:                                                   ║
║  Cervical  C1-C7  (7)  → Lordosis (cóncava post.)           ║
║  Torácica  T1-T12 (12) → Cifosis  (convexa post.)           ║
║  Lumbar    L1-L5  (5)  → Lordosis (cóncava post.)           ║
║  Sacra     S1-S5  (5)  → Cifosis (fusionadas = sacro)       ║
║  Coccígea  Co1-Co4(4)                                        ║
║                                                              ║
║  VÉRTEBRA TIPO (torácica):                                   ║
║  Cuerpo + Arco vertebral (pedículos + láminas)               ║
║  Apófisis espinosa (posterior) + 2 transversas               ║
║  4 carillas articulares (2 sup + 2 inf)                      ║
║  Foramen vertebral → canal raquídeo                          ║
║                                                              ║
║  PARTICULARIDADES:                                           ║
║  Cervicales: foramen transverso (arteria vertebral)          ║
║              apófisis espinosas bífidas (C3-C6)              ║
║              C7 = vértebra prominente (no bífida, palpable)  ║
║  Torácicas:  facetas costales en cuerpo y transversas        ║
║              espinosas largas inclinadas (cubren espacio inf.)║
║  Lumbares:   más grandes · sin foramen transverso ni facetas ║
║              espinosas cortas y horizontales (acceso epidural)║
╠══════════════════════════════════════════════════════════════╣
║  💡 Solo cervicales tienen foramen transverso (art. vertebral)║
║  ⚡ Hernia L4-L5 → peroneo profundo. L5-S1 → reflejo aquíleo║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué característica tienen SOLO las vértebras cervicales?",
                "opciones": {
                    "A": "Facetas costales",
                    "B": "Apófisis espinosas largas",
                    "C": "Foramen transverso por donde pasa la arteria vertebral",
                    "D": "Son las más grandes del raquis"
                },
                "correcta": "C",
                "exp": "Las 7 vértebras cervicales tienen foramen transverso (foramen transversario). Por los de C1-C6 pasa la arteria vertebral (no por C7). Las torácicas tienen facetas costales y las lumbares son las más grandes."
            },
            {
                "enunciado": "La curvatura lumbar normal es:",
                "opciones": {"A": "Cifosis", "B": "Lordosis", "C": "Escoliosis", "D": "Sin curvatura"},
                "correcta": "B",
                "exp": "Lordosis (convexa anterior, cóncava posterior): cervical y lumbar. Cifosis (convexa posterior): torácica y sacra. Las lordosis cervical y lumbar son secundarias (se desarrollan con la bipedestación)."
            },
            {
                "enunciado": "¿Cuántas vértebras lumbares hay?",
                "opciones": {"A": "4", "B": "5", "C": "6", "D": "7"},
                "correcta": "B",
                "exp": "5 lumbares (L1-L5). Son las más grandes del raquis. Sus apófisis espinosas son cortas y horizontales, lo que facilita el acceso epidural/intratecal entre ellas (punción lumbar en L3-L4 o L4-L5)."
            },
        ]
    },

    "atlas_axis": {
        "nombre": "ATLAS y AXIS — C1 y C2",
        "nivel": 1,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║              ATLAS (C1) y AXIS (C2)                          ║
╠══════════════════════════════════════════════════════════════╣
║  ATLAS (C1):                                                 ║
║  NO tiene cuerpo vertebral (ni apófisis espinosa propia)     ║
║  Tiene: Masas laterales (2) · Arco anterior · Arco posterior ║
║         Tubérculo anterior (donde articula el odontoides)    ║
║         Tubérculo posterior (vestigio de apófisis espinosa)  ║
║  Art. atlanto-occipital → FLEXO-EXTENSIÓN ("decir SÍ")       ║
║                                                              ║
║  AXIS (C2):                                                  ║
║  Tiene ODONTOIDES (proceso odontoideo = "diente")            ║
║  Proyección superior del cuerpo del atlas que se fusionó     ║
║  Ligamento TRANSVERSO del atlas: retiene el odontoides       ║
║  Ligamentos ALARES: odontoides → occipital (estabilizan rot.)║
║  Art. atlanto-axoidea → ROTACIÓN ("decir NO")                ║
║                                                              ║
║  FRACTURAS IMPORTANTES:                                      ║
║  Jefferson (C1): compresión axial → fractura en 4 partes     ║
║                  del arco del atlas                          ║
║  Ahorcado (C2):  hiperextensión → fractura de los pedículos  ║
║                  del axis (espondilolistesis traumática)      ║
║  Odontoides:     Tipo I (punta), II (base=+ frecuente),      ║
║                  III (cuerpo del axis)                       ║
╠══════════════════════════════════════════════════════════════╣
║  💡 C1=SÍ (flex-ext) · C2=NO (rotación)                     ║
║  ⚡ Ruptura lig. transverso → odontoides comprime bulbo      ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué movimiento realiza principalmente la articulación atlanto-axoidea?",
                "opciones": {"A": "Flexo-extensión", "B": "Rotación", "C": "Inclinación lateral", "D": "Circunducción"},
                "correcta": "B",
                "exp": "La articulación atlanto-axoidea (C1-C2) permite la ROTACIÓN de la cabeza (~50% de toda la rotación cervical) = 'decir que NO'. La atlanto-occipital (cráneo-C1) permite la flexo-extensión = 'decir que SÍ'."
            },
            {
                "enunciado": "El atlas (C1) se diferencia del resto de vértebras porque:",
                "opciones": {
                    "A": "Tiene foramen transverso",
                    "B": "No tiene cuerpo vertebral",
                    "C": "Tiene apófisis espinosa muy larga",
                    "D": "No tiene carillas articulares"
                },
                "correcta": "B",
                "exp": "El atlas es la única vértebra SIN CUERPO vertebral. Tiene masas laterales y dos arcos (anterior y posterior). El 'cuerpo' del atlas se fusionó con el axis y se convirtió en el odontoides."
            },
            {
                "enunciado": "La fractura de Jefferson afecta a:",
                "opciones": {"A": "El odontoides del axis", "B": "Los pedículos del axis", "C": "El arco del atlas por compresión axial", "D": "Los ligamentos alares"},
                "correcta": "C",
                "exp": "Fractura de Jefferson (C1): compresión axial (caída sobre la cabeza) → fractura del arco anterior y posterior del atlas en 4 fragmentos. Fractura del 'ahorcado' (C2): hiperextensión → pedículos del axis."
            },
        ]
    },

    # ══════════════════════════════════════════════════════
    #  NIVEL 2 — IMPORTANTES  ⭐⭐
    # ══════════════════════════════════════════════════════

    "carpo_tarso": {
        "nombre": "CARPO y TARSO — Huesos",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║              CARPO y TARSO — Huesos                          ║
╠══════════════════════════════════════════════════════════════╣
║  CARPO (8 huesos, 2 filas, de radial a cubital):             ║
║  Proximal: Escafoides · Semilunar · Piramidal · Pisiforme    ║
║  Distal:   Trapecio · Trapezoide · Grande · Ganchoso         ║
║                                                              ║
║  "El Señor Por Ti Trae Tu Gran Gusto"                        ║
║   E    S    P   T    T    T    G    G                        ║
║                                                              ║
║  TARSO (7 huesos):                                           ║
║  Fila posterior: Calcáneo (mayor) · Astrágalo                ║
║  Fila anterior: Navicular (escafoides tarsal) · Cuboides     ║
║  Cuñas (medial, intermedia, lateral)                         ║
║                                                              ║
║  Astrágalo → articula con tibia (arriba) y peroné (lateral) ║
║  Calcáneo → forma el talón + inserción tendón de Aquiles     ║
║                                                              ║
║  TÚNEL DEL CARPO (retináculo flexor):                        ║
║  Contiene: tendones flexores + nervio MEDIANO                ║
║  Síndrome: parestesias 3,5 dedos radiales, nocturnas         ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Escafoides = fractura más frecuente del carpo            ║
║     (tabaquera anatómica dolorosa → fractura hasta demostrar ║
║      lo contrario, incluso con Rx normal)                    ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuál es el hueso del carpo con mayor riesgo de necrosis avascular tras fractura?",
                "opciones": {"A": "Semilunar", "B": "Escafoides", "C": "Grande", "D": "Ganchoso"},
                "correcta": "B",
                "exp": "El escafoides tiene irrigación retrógrada (entra por el polo distal). En la fractura de la cintura, el fragmento proximal queda sin vascularización → necrosis avascular. Dolor en tabaquera anatómica = fractura hasta que se demuestre lo contrario."
            },
            {
                "enunciado": "¿Qué hueso del tarso se articula con la tibia para formar la mortaja tibiotarsiana?",
                "opciones": {"A": "Calcáneo", "B": "Navicular", "C": "Astrágalo", "D": "Cuboides"},
                "correcta": "C",
                "exp": "El astrágalo articula con la tibia (arriba) y el peroné (lateralmente) formando la mortaja del tobillo. El calcáneo es el más grande, forma el talón y da inserción al tendón de Aquiles."
            },
            {
                "enunciado": "El síndrome del túnel del carpo produce síntomas en el territorio del nervio:",
                "opciones": {"A": "Cubital", "B": "Radial", "C": "Mediano", "D": "Musculocutáneo"},
                "correcta": "C",
                "exp": "El nervio mediano pasa por el túnel carpiano (junto con los tendones flexores) bajo el retináculo flexor. Compresión → parestesias nocturnas en 3,5 dedos radiales + atrofia del tenar en casos crónicos."
            },
        ]
    },

    "musculos_ms": {
        "nombre": "MÚSCULOS MIEMBRO SUPERIOR — Compartimentos",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          MÚSCULOS DEL MIEMBRO SUPERIOR                       ║
╠══════════════════════════════════════════════════════════════╣
║  BRAZO:                                                      ║
║  Ant.: Bíceps (supinación+flexión codo, N.musculocutáneo)   ║
║        Braquial (flexión codo pura, N.musculocutáneo)        ║
║  Post.: Tríceps (extensión codo, N.radial)                   ║
║                                                              ║
║  ANTEBRAZO:                                                  ║
║  Anterior (flexores, N.mediano principal):                   ║
║    Flexor carpi radialis · Flexor carpi ulnaris (N.cubital)  ║
║    Flexor digitorum superficialis · profundus                ║
║    Pronador redondo · Pronador cuadrado                      ║
║  Posterior (extensores, N.radial):                           ║
║    Ext. carpi radialis longus/brevis · Ext. carpi ulnaris    ║
║    Ext. digitorum · Supinador (N.radial profundo)            ║
║                                                              ║
║  MANO — Músculos intrínsecos:                                ║
║  Tenar (eminencia radial) → N.MEDIANO:                       ║
║    Abductor pollicis brevis · Oponente · Flexor pollicis br. ║
║  Hipotenar (eminencia cubital) → N.CUBITAL:                  ║
║    Abductor digiti minimi · Flexor digiti minimi · Oponente  ║
║  Interóseos (4 dorsales + 4 palmares) → N.CUBITAL            ║
║  Lumbricales: 1º-2º = N.mediano · 3º-4º = N.cubital         ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Tenar=mediano · Hipotenar+interóseos=cubital             ║
║  ⚡ Atrofia tenar = lesión mediano (STC). Atrofia hipotenar  ║
║     = lesión cubital (canal de Guyón o epitróclea).          ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué nervio inerva los músculos de la eminencia tenar?",
                "opciones": {"A": "Nervio radial", "B": "Nervio cubital", "C": "Nervio mediano", "D": "Nervio musculocutáneo"},
                "correcta": "C",
                "exp": "La eminencia tenar (abductor corto, oponente y flexor corto del pulgar) está inervada por el nervio mediano. El aductor del pulgar y la parte profunda del flexor corto están inervados por el cubital."
            },
            {
                "enunciado": "¿Qué músculo del antebrazo es el flexor puro del codo (sin supinación)?",
                "opciones": {"A": "Bíceps braquial", "B": "Braquial", "C": "Braquiorradial", "D": "Pronador redondo"},
                "correcta": "B",
                "exp": "El braquial es el flexor puro del codo (independiente de la posición de pronación/supinación). El bíceps es más potente en supinación. Ambos inervados por el nervio musculocutáneo."
            },
            {
                "enunciado": "Los músculos interóseos de la mano están inervados por el nervio:",
                "opciones": {"A": "Mediano", "B": "Radial", "C": "Cubital", "D": "Musculocutáneo"},
                "correcta": "C",
                "exp": "Todos los interóseos (4 dorsales + 4 palmares) están inervados por el nervio CUBITAL. Función: interóseos dorsales = ABducción de dedos, palmares = ADducción. Regla DAB/PAD."
            },
        ]
    },

    "musculos_mi": {
        "nombre": "MÚSCULOS MIEMBRO INFERIOR — Compartimentos",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          MÚSCULOS DEL MIEMBRO INFERIOR                       ║
╠══════════════════════════════════════════════════════════════╣
║  CINTURA PÉLVICA:                                            ║
║  Glúteo mayor → extensión + rotación ext. cadera (N.glúteo inf)║
║  Glúteo med+menor → abducción cadera (N.glúteo superior)     ║
║    → evitan caída de pelvis al caminar (signo de Trendelenburg)║
║  Piriforme → rotación externa (N.directo del sacro)          ║
║                                                              ║
║  MUSLO (compartimentos):                                     ║
║  Anterior: Cuádriceps = recto femoral + vastos (extensión    ║
║             rodilla, N.femoral) + Sartorio (N.femoral)       ║
║  Posterior: Isquiotibiales = bíceps femoral + semitend. +    ║
║              semimembranoso (flexión rodilla, N.ciático)     ║
║  Medial: Aductores + Gracilis (N.obturador)                  ║
║                                                              ║
║  PIERNA (compartimentos):                                    ║
║  Anterior (N.peroneo profundo):                              ║
║    Tibial anterior → dorsiflexión + inversión                ║
║    Extensor digitorum/hallucis longus → extensión dedos      ║
║  Lateral (N.peroneo superficial):                            ║
║    Peroneos largo y corto → eversión                         ║
║  Posterior (N.tibial):                                       ║
║    Gastrocnemio + Sóleo → flexión plantar (Aquiles)          ║
║    Tibial posterior → inversión + flexión plantar            ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Trendelenburg(+) → glúteo medio débil (n.glúteo sup.)   ║
║  ⚡ Ruptura tendón Aquiles → no puede ponerse de puntillas   ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "El signo de Trendelenburg positivo indica debilidad del:",
                "opciones": {"A": "Glúteo mayor", "B": "Glúteo medio", "C": "Cuádriceps", "D": "Piriforme"},
                "correcta": "B",
                "exp": "El glúteo medio (y menor) abducen la cadera y estabilizan la pelvis al caminar. En monopodal, si el glúteo medio es débil (lesión del n. glúteo superior), la pelvis cae al lado contrario → Trendelenburg positivo."
            },
            {
                "enunciado": "¿Qué nervio inerva el cuádriceps femoral?",
                "opciones": {"A": "Nervio obturador", "B": "Nervio femoral", "C": "Nervio ciático", "D": "Nervio glúteo superior"},
                "correcta": "B",
                "exp": "El nervio femoral (L2-L4) inerva el cuádriceps (extensión de rodilla) y sartorio. Lesión → no puede extender la rodilla ni subir escaleras. El reflejo rotuliano (L4) depende del cuádriceps."
            },
            {
                "enunciado": "¿Qué movimiento realiza el tibial anterior?",
                "opciones": {"A": "Flexión plantar + inversión", "B": "Dorsiflexión + inversión", "C": "Eversión + dorsiflexión", "D": "Flexión plantar + eversión"},
                "correcta": "B",
                "exp": "Tibial anterior (compartimento anterior, N.peroneo profundo): dorsiflexión del pie + inversión. El tibial posterior (compartimento posterior, N.tibial): inversión + flexión plantar. Peroneos: eversión."
            },
        ]
    },

    "arterias_ms_mi": {
        "nombre": "ARTERIAS DE LOS MIEMBROS — Trayecto principal",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          ARTERIAS DE LOS MIEMBROS                            ║
╠══════════════════════════════════════════════════════════════╣
║  MIEMBRO SUPERIOR:                                           ║
║  Subclavia → Axilar (en axila) → Braquial (en brazo)        ║
║  Braquial se divide a nivel del codo en:                     ║
║    → Radial → arco palmar PROFUNDO (+ arteria radial)       ║
║    → Cubital → arco palmar SUPERFICIAL (principal)           ║
║                                                              ║
║  Punto de compresión: arteria braquial en epitróclea         ║
║  Pulso braquial: cara medial del brazo                       ║
║  Pulso radial: tabaquera anatómica / cara ant. muñeca        ║
║                                                              ║
║  MIEMBRO INFERIOR:                                           ║
║  Ilíaca común → Ilíaca EXTERNA → Femoral                    ║
║  (pasa bajo el lig. inguinal, por laguna vascular)           ║
║  Femoral → Femoral profunda (irriga muslo)                   ║
║           → Poplítea (romboide del poplíteo)                 ║
║  Poplítea → Tibial anterior                                  ║
║           → Tronco tibioperoneal → Tibial posterior + Peronea║
║                                                              ║
║  Pulsos periféricos del MI:                                  ║
║  Femoral (triángulo de Scarpa) · Poplíteo (fosa poplítea)   ║
║  Tibial posterior (detrás maléolo medial)                    ║
║  Pedio (dorso del pie, entre 1º-2º metatarsiano)            ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Arteria más palpable del MS = braquial y radial          ║
║  ⚡ Claudicación intermitente → estenosis arteria femoral    ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "La arteria braquial se divide en el codo en:",
                "opciones": {
                    "A": "Arteria axilar y subclavia",
                    "B": "Arteria radial y cubital",
                    "C": "Arteria radial e interósea",
                    "D": "Arteria cubital y palmar"
                },
                "correcta": "B",
                "exp": "La arteria braquial se divide en la fosa cubital en arteria RADIAL (lateral) y CUBITAL (medial). La radial forma el arco palmar profundo y la cubital el arco palmar superficial (más importante para los dedos)."
            },
            {
                "enunciado": "¿Por dónde pasa la arteria femoral al pasar del abdomen al muslo?",
                "opciones": {
                    "A": "Por el canal obturador",
                    "B": "Por la laguna vascular (bajo el ligamento inguinal)",
                    "C": "Por la escotadura isquiática mayor",
                    "D": "Por la laguna muscular"
                },
                "correcta": "B",
                "exp": "La arteria femoral (continuación de la ilíaca externa) pasa por la LAGUNA VASCULAR, bajo el ligamento inguinal, en la parte medial. La laguna muscular (parte lateral) deja pasar el nervio femoral y el músculo iliopsoas."
            },
            {
                "enunciado": "¿Dónde se palpa el pulso tibial posterior?",
                "opciones": {
                    "A": "Dorso del pie",
                    "B": "Detrás del maléolo medial",
                    "C": "Detrás del maléolo lateral",
                    "D": "En la fosa poplítea"
                },
                "correcta": "B",
                "exp": "Pulso tibial posterior: detrás del maléolo MEDIAL. Pulso pedio: dorso del pie (1º-2º metatarsiano). Ambos se evalúan en el examen vascular del pie diabético o en arteriopatía periférica."
            },
        ]
    },

    "articulacion_hombro": {
        "nombre": "ARTICULACIÓN DEL HOMBRO — Glenohumeral y estabilizadores",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║         ARTICULACIÓN DEL HOMBRO                              ║
╠══════════════════════════════════════════════════════════════╣
║  ARTICULACIONES DEL COMPLEJO DEL HOMBRO:                     ║
║  1. Glenohumeral (principal) — más móvil del cuerpo          ║
║  2. Acromioclavicular                                        ║
║  3. Esternoclavicular                                        ║
║  4. Escapulotorácica (no es articulación verdadera)          ║
║                                                              ║
║  ARTICULACIÓN GLENOHUMERAL:                                  ║
║  Cabeza del húmero (grande) vs cavidad glenoidea (pequeña)   ║
║  Profundizada por el labrum glenoideo (rodete glenoideo)      ║
║  Articulación más inestable del cuerpo → + luxada            ║
║                                                              ║
║  ESTABILIZADORES:                                            ║
║  Estáticos: labrum + cápsula + ligamentos glenohumerales     ║
║  Dinámicos: manguito rotador (SITS) + deltoides + bíceps     ║
║                                                              ║
║  LUXACIÓN GLENOHUMERAL:                                      ║
║  Anterior (95%): mecanismo = abducción + rotación externa    ║
║    Lesión de Bankart (labrum ant.) + Hill-Sachs (cabeza húm.)║
║    Riesgo de lesión del nervio AXILAR                        ║
║  Posterior (5%): convulsiones / descarga eléctrica           ║
║    Mano en rotación interna que no puede supinar             ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Luxación ant. → lesión axilar → deltoides paralizado     ║
║  ⚡ Test de aprehensión (+) → inestabilidad anterior         ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Cuál es la articulación más frecuentemente luxada del cuerpo?",
                "opciones": {"A": "Cadera", "B": "Rodilla", "C": "Glenohumeral", "D": "Acromioclavicular"},
                "correcta": "C",
                "exp": "La articulación glenohumeral es la más móvil y la más inestable → más frecuentemente luxada. La luxación anterior (95%) ocurre por abducción + rotación externa. Riesgo de lesión del nervio axilar."
            },
            {
                "enunciado": "En la luxación glenohumeral anterior, ¿qué nervio puede lesionarse?",
                "opciones": {"A": "Nervio radial", "B": "Nervio mediano", "C": "Nervio axilar", "D": "Nervio musculocutáneo"},
                "correcta": "C",
                "exp": "El nervio axilar (C5-C6) rodea el cuello quirúrgico del húmero y puede dañarse en la luxación anterior. Evaluación: sensibilidad en 'charretera' (cara lateral del deltoides) + función del deltoides."
            },
        ]
    },

    "ligamentos_columna": {
        "nombre": "LIGAMENTOS DE LA COLUMNA VERTEBRAL",
        "nivel": 2,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          LIGAMENTOS DE LA COLUMNA VERTEBRAL                  ║
╠══════════════════════════════════════════════════════════════╣
║  LIGAMENTOS LONGITUDINALES (de occipital a sacro):           ║
║  ┌──────────────────────────────────────────────────────┐    ║
║  │ LLA (anterior): cara ant. cuerpos vertebrales        │    ║
║  │   → muy resistente · limita la EXTENSIÓN             │    ║
║  │                                                      │    ║
║  │ LLP (posterior): cara post. cuerpos = pared ant.     │    ║
║  │   del canal raquídeo · más ESTRECHO · menos resistente│   ║
║  │   → hernias posterolaterales (sale por los lados)    │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                              ║
║  LIGAMENTOS ENTRE ARCOS VERTEBRALES:                         ║
║  Ligamento amarillo (flavum): entre láminas · muy elástico   ║
║    → hipertrofia en espondilosis → estenosis de canal        ║
║  Ligamentos interespinosos: entre apófisis espinosas         ║
║  Ligamento supraespinoso: sur apófisis espinosas (ext.)      ║
║    → en región cervical = ligamento NUCAL                    ║
║  Ligamentos intertransversos: entre apófisis transversas     ║
║                                                              ║
║  DISCO INTERVERTEBRAL:                                       ║
║  Núcleo pulposo (gel centro) + Anillo fibroso (periférico)   ║
║  Sin discos en C0-C1, C1-C2, ni entre vértebras sacras      ║
╠══════════════════════════════════════════════════════════════╣
║  💡 LLA limita extensión. LLP limita flexión.                ║
║  ⚡ Hernia discal: núcleo pulposo rompe anillo fibroso →     ║
║     comprime raíz nerviosa posterolateral (LLP más débil)    ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué ligamento limita la extensión de la columna vertebral?",
                "opciones": {"A": "Ligamento amarillo", "B": "Ligamento longitudinal posterior", "C": "Ligamento longitudinal anterior", "D": "Ligamento supraespinoso"},
                "correcta": "C",
                "exp": "El ligamento longitudinal ANTERIOR (LLA) cubre la cara anterior de los cuerpos vertebrales y es el más resistente. Limita la EXTENSIÓN. El LLP cubre la cara posterior de los cuerpos y limita la FLEXIÓN."
            },
            {
                "enunciado": "¿Por qué las hernias discales son predominantemente posterolaterales?",
                "opciones": {
                    "A": "Porque el LLA es más débil en esa zona",
                    "B": "Porque el LLP es más estrecho y débil lateralmente",
                    "C": "Porque las raíces nerviosas están anteriores",
                    "D": "Porque el núcleo pulposo migra hacia adelante"
                },
                "correcta": "B",
                "exp": "El LLP es más estrecho (no cubre bien los bordes laterales del disco) y menos resistente que el LLA. El núcleo pulposo prolapsa posterolateralmente → comprime la raíz nerviosa que sale por el foramen intervertebral."
            },
            {
                "enunciado": "El ligamento nucal es la continuación cervical del:",
                "opciones": {"A": "Ligamento amarillo", "B": "Ligamento longitudinal anterior", "C": "Ligamento supraespinoso", "D": "Ligamento intertransverso"},
                "correcta": "C",
                "exp": "El ligamento nucal es la expansión cervical y craneal del ligamento supraespinoso. Va desde la protuberancia occipital externa hasta C7. En cuadrúpedos está muy desarrollado para soportar el peso de la cabeza."
            },
        ]
    },

    # ══════════════════════════════════════════════════════
    #  NIVEL 3 — POCO PREGUNTADOS  ⭐
    # ══════════════════════════════════════════════════════

    "articulacion_codo": {
        "nombre": "ARTICULACIÓN DEL CODO — Relaciones y lesiones",
        "nivel": 3,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║         ARTICULACIÓN DEL CODO                                ║
╠══════════════════════════════════════════════════════════════╣
║  ARTICULACIONES del codo (bajo una sola cápsula):            ║
║  1. Humerocubital: tróclea + escotadura troclear → flex/ext  ║
║  2. Humeroradial: cóndilo + cabeza del radio → flex/ext      ║
║  3. Radiocubital proximal: cabeza radio + escot. radial      ║
║                            del cúbito → prono/supinación     ║
║                                                              ║
║  TRIÁNGULO DE HUETER (codo extendido):                       ║
║  Epicóndilo · Epitróclea · Olécranon → triángulo isósceles  ║
║  En codo flexionado 90°: forman línea recta                  ║
║  En luxación posterior: relación alterada                    ║
║                                                              ║
║  RELACIONES NERVIOSAS:                                       ║
║  Epitróclea → nervio CUBITAL (canal epitrocleoolecraniano)   ║
║  Cóndilo → nervio RADIAL (zona lateral)                      ║
║                                                              ║
║  ÁNGULO DE CARGA (valgo fisiológico):                        ║
║  Hombre: ~5-10° · Mujer: ~10-15°                             ║
║  Cúbito valgo → tracción crónica del nervio cubital          ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Fractura supracondílea (niños) → lesión arteria braquial ║
║     + nervio mediano (o anterior interóseo)                  ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿Qué nervio discurre en el canal epitrocleoolecraniano y puede lesionarse en el codo?",
                "opciones": {"A": "Nervio mediano", "B": "Nervio radial", "C": "Nervio cubital", "D": "Nervio musculocutáneo"},
                "correcta": "C",
                "exp": "El nervio cubital pasa por el canal epitrocleoolecraniano (medial, detrás de la epitróclea). Es el 'funny bone'. Lesión → garra de los 4º-5º dedos, atrofia hipotenar, signo de Froment."
            },
            {
                "enunciado": "¿Cuántas articulaciones verdaderas están contenidas en la cápsula del codo?",
                "opciones": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "correcta": "C",
                "exp": "3 articulaciones en una cápsula: humerocubital (tróclea + escotadura troclear), humeroradial (cóndilo + cabeza del radio) y radiocubital proximal. Las dos primeras flexo-extienden; la tercera prona/supina."
            },
        ]
    },

    "disco_intervertebral": {
        "nombre": "DISCO INTERVERTEBRAL — Estructura y hernias",
        "nivel": 3,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║          DISCO INTERVERTEBRAL                                ║
╠══════════════════════════════════════════════════════════════╣
║  ESTRUCTURA:                                                 ║
║  ┌────────────────────────────────────────┐                  ║
║  │         ANILLO FIBROSO                 │                  ║
║  │   (fibrocartílago, láminas concéntricas│                  ║
║  │                                        │                  ║
║  │      NÚCLEO PULPOSO (centro)           │                  ║
║  │      (gel con 70-90% agua en joven)    │                  ║
║  └────────────────────────────────────────┘                  ║
║                                                              ║
║  El disco carece de vasos sanguíneos → nutrición por         ║
║  difusión desde las plataformas vertebrales                  ║
║  → deshidratación con la edad → protrusión/hernia            ║
║                                                              ║
║  HERNIA DISCAL — Niveles más frecuentes:                     ║
║  L4-L5: comprime raíz L5 → debilidad dorsiflexión pie       ║
║          pérdida sensibilidad cara lateral pierna + dorso    ║
║  L5-S1: comprime raíz S1 → pérdida reflejo aquíleo          ║
║          debilidad flexión plantar                           ║
║  C5-C6: comprime raíz C6 → pérdida reflejo bicipital        ║
║  C6-C7: comprime raíz C7 → pérdida reflejo tricipital       ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Hernia L5-S1 → reflejo aquíleo abolido (S1)              ║
║  ⚡ Signo de Lasègue → test de irritación de raíz ciática    ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "Una hernia discal L5-S1 comprime la raíz S1, produciendo:",
                "opciones": {
                    "A": "Pérdida del reflejo rotuliano",
                    "B": "Pérdida del reflejo aquíleo",
                    "C": "Debilidad en la dorsiflexión del pie",
                    "D": "Anestesia en el muslo anterior"
                },
                "correcta": "B",
                "exp": "Raíz S1 → reflejo aquíleo (tendón de Aquiles = gastrocnemio + sóleo). Hernia L5-S1 comprime S1 → reflejo aquíleo abolido + debilidad de flexión plantar + anestesia en cara lateral del pie y 5º dedo."
            },
            {
                "enunciado": "¿Por qué los discos intervertebrales se degeneran con la edad?",
                "opciones": {
                    "A": "Porque pierden su irrigación arterial",
                    "B": "Porque el disco carece de vasos y pierde capacidad de nutrición por difusión",
                    "C": "Porque el anillo fibroso se calcifica",
                    "D": "Porque el núcleo pulposo pierde células"
                },
                "correcta": "B",
                "exp": "El disco intervertebral avascular depende de la difusión desde las plataformas vertebrales. Con la edad, el núcleo pulposo pierde agua (de 90% a 70%) → menos amortiguación → fisuras del anillo → protrusión/hernia."
            },
        ]
    },

    "suturas_fosas": {
        "nombre": "SUTURAS CRANEALES Y FOSAS DE LA BASE",
        "nivel": 3,
        "esquema": r"""
╔══════════════════════════════════════════════════════════════╗
║       SUTURAS CRANEALES Y FOSAS DE LA BASE                   ║
╠══════════════════════════════════════════════════════════════╣
║  SUTURAS PRINCIPALES:                                        ║
║  Coronal    → Frontal + 2 Parietales                         ║
║  Sagital    → Parietal + Parietal (línea media)              ║
║  Lambdoidea → 2 Parietales + Occipital                       ║
║  Escamosa   → Parietal + Temporal                            ║
║                                                              ║
║  Fontanela anterior (bregma) = Coronal + Sagital             ║
║    Cierre: 18-24 meses                                       ║
║  Fontanela posterior (lambda) = Sagital + Lambdoidea         ║
║    Cierre: 2-3 meses                                         ║
║                                                              ║
║  FOSAS DE LA BASE DEL CRÁNEO:                                ║
║  Fosa anterior:  Lóbulo frontal + bulbo olfatorio            ║
║    Piso: porción orbitaria frontal + lámina cribosa + ala    ║
║    menor esfenoides                                          ║
║  Fosa media:     Lóbulo temporal + hipófisis (silla turca)   ║
║    Piso: ala mayor esfenoides + escama temporal + pared      ║
║    lateral esfenoides                                        ║
║  Fosa posterior: Cerebelo + protuberancia + bulbo            ║
║    Piso: clivus (esfenoides+occipital) + escama occipital    ║
╠══════════════════════════════════════════════════════════════╣
║  💡 Hipófisis en silla turca = fosa MEDIA                    ║
║  ⚡ Fractura base fosa anterior → anosmia (NC I) +           ║
║     "ojos de mapache". Fosa media → otorragia + "signo de    ║
║     Battle". Fosa posterior → afectación NC IX-XII           ║
╚══════════════════════════════════════════════════════════════╝""",
        "preguntas": [
            {
                "enunciado": "¿En qué fosa craneal se encuentra la silla turca (hipófisis)?",
                "opciones": {"A": "Fosa anterior", "B": "Fosa media", "C": "Fosa posterior", "D": "En el clivus"},
                "correcta": "B",
                "exp": "La silla turca (fosa hipofisaria) está en el cuerpo del esfenoides, que forma parte de la FOSA MEDIA. Los lóbulos temporales descansan en la fosa media. La fosa posterior contiene cerebelo, protuberancia y bulbo."
            },
            {
                "enunciado": "¿Cuándo se cierra la fontanela anterior (bregma)?",
                "opciones": {"A": "2-3 meses", "B": "6-9 meses", "C": "18-24 meses", "D": "3-4 años"},
                "correcta": "C",
                "exp": "La fontanela anterior (bregma, unión coronal + sagital) cierra entre los 18-24 meses. La posterior (lambda) cierra a los 2-3 meses. Fontanela abombada = hipertensión intracraneal. Hundida = deshidratación."
            },
        ]
    },
}

# ════════════════════════════════════════════════════════════════
#  CLASIFICACIÓN POR NIVELES
# ════════════════════════════════════════════════════════════════

NIVELES = {
    1: {
        "label": "⭐⭐⭐  NIVEL 1 — MUY IMPORTANTES",
        "claves": ["huesos_ms", "plexo_braquial", "manguito_rotador",
                   "huesos_mi", "nervios_mmii", "rodilla",
                   "huesos_craneo", "craneo_foramenes", "nervios_craneales",
                   "columna", "atlas_axis"],
    },
    2: {
        "label": "⭐⭐   NIVEL 2 — IMPORTANTES",
        "claves": ["carpo_tarso", "musculos_ms", "musculos_mi",
                   "arterias_ms_mi", "articulacion_hombro", "ligamentos_columna"],
    },
    3: {
        "label": "⭐    NIVEL 3 — POCO PREGUNTADOS",
        "claves": ["articulacion_codo", "disco_intervertebral", "suturas_fosas"],
    },
}

# ════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT
# ════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """Eres un profesor de Anatomía Humana de 1º de Medicina en la Universidad Católica de Valencia (UCV).
Ayudas al estudiante a preparar el examen tipo test sobre: MIEMBRO SUPERIOR, MIEMBRO INFERIOR, CRÁNEO y VÉRTEBRAS.

CONTEXTO: Examen tipo test, 60-80 preguntas, 4 opciones (A/B/C/D).

TEMAS CLAVE del temario:
- Miembro superior: huesos (húmero, cúbito, radio, carpo), plexo braquial, nervios y lesiones, manguito rotador, músculos
- Miembro inferior: huesos (fémur, tibia, peroné, tarso), plexo lumbar/sacro, rodilla (meniscos/ligamentos), músculos, arterias
- Cráneo: 8 huesos del neurocráneo, forámenes de la base, nervios craneales, suturas
- Vértebras: regiones, características por región, atlas/axis, ligamentos, disco intervertebral

RESPUESTAS: Cortas (máx 150 palabras), con nemotecnia si la hay, siempre relación clínica. En ESPAÑOL."""

# ════════════════════════════════════════════════════════════════
#  FUNCIONES
# ════════════════════════════════════════════════════════════════

def cabecera():
    print("""
╔══════════════════════════════════════════════════════════════╗
║       AGENTE ANATOMÍA UCV — 1º MEDICINA                      ║
║  Temario: MS · MI · Cráneo · Vértebras                       ║
╚══════════════════════════════════════════════════════════════╝
""")

def listar_esquemas():
    print()
    for n, datos in NIVELES.items():
        print(f"\n  {datos['label']}")
        print("  " + "─" * 58)
        for clave in datos["claves"]:
            e = ESQUEMAS[clave]
            nq = len(e["preguntas"])
            print(f"  • {clave:<28} {e['nombre'][:32]}  ({nq}p)")
    print()

def mostrar_esquema(clave):
    if clave not in ESQUEMAS:
        print(f"  ✗ '{clave}' no encontrado. Usa /esquemas para ver la lista.")
        return
    e = ESQUEMAS[clave]
    print(f"\n  {'⭐' * e['nivel']}  NIVEL {e['nivel']}")
    print(e["esquema"])

def hacer_pregunta(p, n, total):
    print(f"\n  ─── Pregunta {n}/{total} " + "─" * 40)
    print(f"  {p['enunciado']}\n")
    for letra, texto in p["opciones"].items():
        print(f"    {letra}) {texto}")
    while True:
        r = input("\n  Respuesta (A/B/C/D) o S para saltar: ").strip().upper()
        if r in ("A", "B", "C", "D", "S"):
            break
    if r == "S":
        print(f"  Saltada. Correcta: {p['correcta']}  |  {p['exp']}")
        return None
    elif r == p["correcta"]:
        print(f"  ✓ CORRECTO  |  {p['exp']}")
        return True
    else:
        print(f"  ✗ Incorrecto. Era {p['correcta']}  |  {p['exp']}")
        return False

def resultado(correctas, total):
    print(f"\n  ┌──────────────────────────────────┐")
    print(f"  │  Resultado: {correctas}/{total} correctas")
    if total > 0:
        pct = int(correctas / total * 100)
        barra = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"  │  [{barra}] {pct}%")
    print(f"  └──────────────────────────────────┘\n")

def modo_test(clave):
    if clave not in ESQUEMAS:
        print(f"  ✗ '{clave}' no encontrado.")
        return
    mostrar_esquema(clave)
    pregs = ESQUEMAS[clave]["preguntas"]
    print(f"\n  TEST: {ESQUEMAS[clave]['nombre']} — {len(pregs)} preguntas\n")
    c = s = 0
    for i, p in enumerate(pregs, 1):
        r = hacer_pregunta(p, i, len(pregs))
        if r is True: c += 1
        elif r is None: s += 1
    resultado(c, len(pregs) - s)

def modo_repaso_nivel(n):
    if n not in NIVELES:
        print(f"  ✗ Nivel {n} no existe.")
        return
    claves = NIVELES[n]["claves"]
    pool = [(k, p) for k in claves for p in ESQUEMAS[k]["preguntas"]]
    muestra = random.sample(pool, min(15, len(pool)))
    print(f"\n  {NIVELES[n]['label']} — {len(muestra)} preguntas\n")
    c = s = 0
    for i, (k, p) in enumerate(muestra, 1):
        print(f"  [{ESQUEMAS[k]['nombre'][:44]}]")
        r = hacer_pregunta(p, i, len(muestra))
        if r is True: c += 1
        elif r is None: s += 1
    resultado(c, len(muestra) - s)

def modo_repaso():
    pool = [(k, p) for k in ESQUEMAS for p in ESQUEMAS[k]["preguntas"]]
    muestra = random.sample(pool, min(12, len(pool)))
    print(f"\n  REPASO ALEATORIO — {len(muestra)} preguntas mixtas\n")
    c = s = 0
    for i, (k, p) in enumerate(muestra, 1):
        print(f"  [{ESQUEMAS[k]['nombre'][:44]}]")
        r = hacer_pregunta(p, i, len(muestra))
        if r is True: c += 1
        elif r is None: s += 1
    resultado(c, len(muestra) - s)

def chat_libre(client, historial, pregunta):
    historial.append({"role": "user", "content": pregunta})
    if len(historial) > 20:
        historial = historial[-20:]
    print("\n  ", end="", flush=True)
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=600,
        system=[{"type": "text", "text": SYSTEM_PROMPT,
                 "cache_control": {"type": "ephemeral"}}],
        messages=historial,
    ) as stream:
        texto_completo = ""
        for t in stream.text_stream:
            print(t, end="", flush=True)
            texto_completo += t
    print("\n")
    historial.append({"role": "assistant", "content": texto_completo})
    return historial

def ayuda():
    print("""
  ┌────────────────────────────────────────────────────────┐
  │  /esquemas        Lista todos los esquemas por nivel   │
  │  /ver <clave>     Muestra el esquema del tema          │
  │  /test <clave>    Test de preguntas de ese tema        │
  │  /repaso          12 preguntas aleatorias mixtas       │
  │  /nivel1          Repaso temas MUY IMPORTANTES         │
  │  /nivel2          Repaso temas IMPORTANTES             │
  │  /nivel3          Repaso temas poco preguntados        │
  │  /todo            Todos los test seguidos              │
  │  /ayuda           Este menú                            │
  │  /salir           Salir                                │
  ├────────────────────────────────────────────────────────┤
  │  O escribe cualquier pregunta de anatomía              │
  └────────────────────────────────────────────────────────┘
""")

# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8')

    client = anthropic.Anthropic()
    historial = []

    cabecera()
    total_p = sum(len(e["preguntas"]) for e in ESQUEMAS.values())
    print(f"  {len(ESQUEMAS)} esquemas · {total_p} preguntas")
    print(f"  Temario: MS · MI · Cráneo · Vértebras\n")
    print("  Escribe /ayuda para ver comandos.")
    print("  Recomendado: empieza con /nivel1\n")

    while True:
        try:
            entrada = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  ¡Ánimo con el examen!\n")
            break

        if not entrada:
            continue
        cmd = entrada.lower()

        if cmd in ("/salir", "/exit"):
            print("\n  ¡Ánimo con el examen!\n")
            break
        elif cmd in ("/ayuda", "/help"):
            ayuda()
        elif cmd == "/esquemas":
            listar_esquemas()
        elif cmd.startswith("/ver "):
            mostrar_esquema(entrada[5:].strip().lower())
        elif cmd.startswith("/test "):
            modo_test(entrada[6:].strip().lower())
        elif cmd == "/repaso":
            modo_repaso()
        elif cmd == "/nivel1":
            modo_repaso_nivel(1)
        elif cmd == "/nivel2":
            modo_repaso_nivel(2)
        elif cmd == "/nivel3":
            modo_repaso_nivel(3)
        elif cmd == "/todo":
            for clave in ESQUEMAS:
                modo_test(clave)
                if input("  Continuar? (Enter=sí / n=no): ").strip().lower() == "n":
                    break
        else:
            historial = chat_libre(client, historial, entrada)


if __name__ == "__main__":
    main()
