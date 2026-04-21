# banco_ucv.py — Preguntas reales y del temario UCV
# Fuente 1: banco_UCV_por_temas.json (90 preguntas, Temas 1-9)
# Fuente 2: banco_UCV_temas_3_4_5_REAL.json (35 preguntas reales de examen)

import json
from pathlib import Path

# ── Convertir formato UCV al formato interno de la app ──────────
# Formato interno: {"id", "concepto", "enunciado", "opciones": {A,B,C,D}, "correcta", "exp"}

def _conv(raw_id: str, pregunta: str, opciones: list, correcta_idx: int, exp: str, concepto: str) -> dict:
    letras = ["A", "B", "C", "D"]
    return {
        "id": raw_id,
        "concepto": concepto,
        "enunciado": pregunta,
        "opciones": {letras[i]: opt for i, opt in enumerate(opciones[:4])},
        "correcta": letras[correcta_idx],
        "exp": exp,
    }

# ════════════════════════════════════════════════════════════════
#  BANCO UCV — organizado por temas del temario oficial
# ════════════════════════════════════════════════════════════════
BANCO_UCV = {

    "ucv_t1_histologia": {
        "nombre": "Tema 1: Histología humana",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t1_01","¿Cuál es la función del tejido conectivo?",["Solo transportar oxígeno","Formar los huesos únicamente","Generar fibras proteicas como colágeno y elastina","Ninguna de las anteriores"],2,"El tejido conectivo está compuesto por células especializadas (fibroblastos) que generan fibras proteicas como colágeno y elastina.","tejido conectivo"),
            _conv("ucv_t1_02","¿Cuál es el único tejido conectivo líquido?",["El hígado","La sangre","El músculo","El riñón"],1,"La sangre es el único tejido conectivo líquido. Contiene millones de células, cada una con su función.","tejido conectivo líquido"),
            _conv("ucv_t1_03","¿Qué órganos NO tienen epitelio?",["Hígado y corazón","Piel y estómago","Pulmones e intestino","Vejiga y uréteres"],0,"El hígado y el corazón son las excepciones: NO tienen epitelio. Los epitelios tapizan la superficie del cuerpo, órganos huecos y glándulas.","epitelio"),
            _conv("ucv_t1_04","¿Cuál es la función de la queratina en la epidermis?",["Dar elasticidad","Impermeabilizar","Nutrir la piel","Protección solar"],1,"La queratina impermeabiliza. Por eso está presente en zonas como la planta de los pies y la palma de las manos.","queratina"),
            _conv("ucv_t1_05","¿Cuál es la función del colágeno en la dermis?",["Impermeabilidad","Elasticidad","Producir melanina","Protección solar"],1,"La dermis es muy rica en colágeno, le confiere elasticidad. La edad colabora a la pérdida de colágeno.","colágeno"),
            _conv("ucv_t1_06","¿Qué células producen la melanina?",["Fibroblastos","Adipocitos","Melanocitos","Miocitos"],2,"Los melanocitos segregan melanina, proteína que protege la piel contra la radiación ultravioleta. Se encuentran en la interfase epidermis-dermis.","melanocitos"),
            _conv("ucv_t1_07","¿Qué tipo de músculo forma el miocardio?",["Músculo liso involuntario","Músculo esquelético voluntario","Músculo estriado de movimiento involuntario","Músculo liso voluntario"],2,"El miocardio es músculo estriado que escapa del control voluntario. Reúne características del músculo esquelético (estrías) y del liso (involuntario).","músculo cardíaco"),
            _conv("ucv_t1_08","¿Dónde se vierte el producto de una glándula endocrina?",["A la superficie de la piel","A la sangre","A una estructura hueca","Al conducto glandular"],1,"Las glándulas endocrinas vierten su producto (hormonas) a la sangre. En 2-3 segundos está por todo el cuerpo. Ej: glándula tiroides.","glándulas endocrinas"),
            _conv("ucv_t1_09","¿Qué órgano es un ejemplo de glándula mixta (endocrina y exocrina)?",["Tiroides","Hígado","Páncreas","Glándula sudorípara"],2,"El páncreas es mixto: parte endocrina (segrega insulina a la sangre) y parte exocrina (segrega enzimas digestivas al duodeno).","glándula mixta"),
            _conv("ucv_t1_10","¿Qué capa de la piel contiene el tejido adiposo?",["Epidermis","Dermis","Hipodermis","Todas las anteriores"],2,"La hipodermis es el tejido celular subcutáneo, formado por adipocitos (tejido adiposo). Es la capa más profunda.","capas de la piel"),
        ]
    },

    "ucv_t2_anatomia_gral": {
        "nombre": "Tema 2: Conceptos generales de anatomía",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t2_01","¿Cuál NO es un requisito de la posición anatómica?",["Bipedestación o decúbito supino","Palmas mirando anteriormente","Ojos y pies dirigidos anteriormente","MMSS cruzados sobre el tórax"],3,"En posición anatómica los MMSS van con las palmas mirando anteriormente, NO cruzados. Además: bipedestación, cabeza y pies dirigidos anteriormente.","posición anatómica"),
            _conv("ucv_t2_02","El plano sagital divide al cuerpo en:",["Anterior y posterior","Mitades derecha e izquierda","Superior e inferior","Interno y externo"],1,"Los planos sagitales son longitudinales imaginarios que dividen al cuerpo en mitades derecha e izquierda.","planos anatómicos"),
            _conv("ucv_t2_03","¿Qué afirmación es correcta sobre el plano medio?",["Todos los planos sagitales son medios","Todos los planos medios son sagitales","El plano medio es horizontal","El plano medio divide en anterior y posterior"],1,"Todos los planos medios son sagitales, pero NO todos los planos sagitales son medios. El plano medio pasa exactamente por la mitad del cuerpo.","plano medio"),
            _conv("ucv_t2_04","El plano coronal o frontal divide el cuerpo en:",["Derecha e izquierda","Superior e inferior","Anterior y posterior","Proximal y distal"],2,"El plano coronal o frontal es longitudinal imaginario perpendicular al plano medio y divide el cuerpo en anterior y posterior.","plano coronal"),
            _conv("ucv_t2_05","El plano horizontal o transversal divide al cuerpo en:",["Anterior y posterior","Superior e inferior","Derecha e izquierda","Medial y lateral"],1,"El plano transversal pasa perpendicular al eje longitudinal y divide al cuerpo en porción inferior y superior.","plano transversal"),
            _conv("ucv_t2_06","¿Cuántas cavidades corporales existen?",["2","3","4","5"],1,"Existen 3 cavidades corporales: craneal, torácica y abdominopélvica.","cavidades corporales"),
            _conv("ucv_t2_07","¿Qué estructura separa la cavidad torácica de la abdominopélvica?",["Peritoneo","Diafragma","Mediastino","Esternón"],1,"El diafragma es el límite entre tórax y abdomen. No hay frontera equivalente entre abdomen y pelvis.","diafragma"),
            _conv("ucv_t2_08","En la región epigástrica, un dolor agudo puede sugerir:",["Cólico biliar","Pancreatitis","Apendicitis","Litiasis renal"],1,"Dolor agudo en epigastrio: pancreatitis. Dolor subagudo: úlcera duodenal (se calma con leche al equilibrar el pH).","regiones abdominales"),
            _conv("ucv_t2_09","¿Qué órganos se encuentran en el hipocondrio derecho?",["Estómago y bazo","Hígado y vesícula biliar","Riñón derecho y ciego","Colon sigmoide"],1,"En el hipocondrio derecho se encuentran el hígado y la vesícula biliar. Un traumatismo fuerte puede causar lesión hepática o cólico biliar.","regiones abdominales"),
            _conv("ucv_t2_10","¿En qué región se sitúa el apéndice?",["Fosa ilíaca izquierda","Hipogastrio","Fosa ilíaca derecha","Epigastrio"],2,"El apéndice está en la fosa ilíaca derecha, colgado del ciego. Apendicitis: náuseas, vómitos, anorexia, febrícula.","regiones abdominales"),
        ]
    },

    "ucv_t3_locomotor": {
        "nombre": "Tema 3: Aparato locomotor",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t3_01","¿Cuáles son los 4 elementos necesarios para que se produzca el movimiento?",["Huesos, tendones, nervios y sangre","Huesos, cartílagos, articulaciones y músculos","Músculos, ligamentos, articulaciones y arterias","Huesos, vasos, nervios y músculos"],1,"Los 4 elementos íntegros necesarios son: huesos, cartílagos, articulaciones y músculos (esquelético o estriado).","aparato locomotor"),
            _conv("ucv_t3_02","¿Cuáles son las partes de un hueso largo?",["Epífisis, diáfisis y metáfisis","Cabeza, cuello y cuerpo","Periostio, endostio y médula","Proximal, medial y distal"],0,"Huesos largos: EPÍFISIS (extremos), DIÁFISIS (parte intermedia, con médula ósea) y METÁFISIS (unión con cartílago de crecimiento).","huesos largos"),
            _conv("ucv_t3_03","¿Cuántos huesos forman el cráneo?",["6","8","10","12"],1,"El cráneo tiene 8 huesos: 2 pares (parietal y temporal) y 4 impares (frontal, etmoides, esfenoides y occipital).","huesos del cráneo"),
            _conv("ucv_t3_04","¿Cuál es la función del foramen magno?",["Paso del nervio óptico","Salida del bulbo raquídeo que continúa con la médula espinal","Articular con la mandíbula","Alojar el oído interno"],1,"El foramen magno (agujero occipital) permite la salida del bulbo raquídeo, que continúa con la médula espinal.","foramen magno"),
            _conv("ucv_t3_05","¿Qué hueso tiene forma de alas de mariposa y es la piedra angular de la base del cráneo?",["Frontal","Etmoides","Esfenoides","Occipital"],2,"El esfenoides tiene forma de alas de mariposa y es la piedra angular porque articula todos los huesos del cráneo manteniéndolos unidos.","esfenoides"),
            _conv("ucv_t3_06","La silla turca se encuentra en el esfenoides. ¿Qué glándula se inserta en ella?",["Tiroides","Hipófisis","Paratiroides","Timo"],1,"La silla turca del esfenoides aloja la hipófisis (glándula endocrina).","silla turca"),
            _conv("ucv_t3_07","El músculo esternocleidomastoideo (ECM) se inserta en:",["Apófisis cigomática del temporal","Apófisis estiloides","Apófisis mastoides del temporal","Cóndilos occipitales"],2,"El ECM: inserción proximal en esternón y clavícula, inserción distal (por tendón) en apófisis mastoides del hueso temporal.","ECM"),
            _conv("ucv_t3_08","¿Cuál es el único hueso móvil del macizo craneofacial?",["Maxilar","Cigomático","Mandíbula","Hioides"],2,"La mandíbula es el único hueso móvil. Se articula con la fosa mandibular del temporal formando la ATM.","mandíbula"),
            _conv("ucv_t3_09","¿Qué particularidad tiene el hueso hioides?",["Es el hueso más pequeño del cuerpo","No se articula con ningún otro hueso","Es un hueso par","Se fusiona al crecer"],1,"El hioides es un componente del esqueleto axial que NO se articula con ningún otro hueso. Ubicado en el cuello entre mandíbula y laringe, sostiene la lengua.","hioides"),
            _conv("ucv_t3_10","¿Qué tipo de articulación corresponde con las sinoviales?",["Sinartrosis","Anfiartrosis","Diartrosis","Sindesmosis"],2,"Sinartrosis = fibrosas (inmóviles). Anfiartrosis = cartilaginosas (semimóviles). Diartrosis = sinoviales (muñeca, codo, hombro, cadera, rodilla, tobillo).","articulaciones"),
        ]
    },

    "ucv_t4_columna_torax": {
        "nombre": "Tema 4: Columna vertebral y tórax",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t4_01","¿Cuántas vértebras tiene la columna vertebral en total?",["24","26","33","35"],2,"33 vértebras: 7 cervicales + 12 dorsales + 5 lumbares + 5 sacras (fusionadas en sacro) + 4 coxígeas (fusionadas en cóccix).","vértebras totales"),
            _conv("ucv_t4_02","¿Qué vértebras forman la porción INMÓVIL de la columna?",["Cervicales y dorsales","Dorsales y lumbares","Sacras y coxígeas","Lumbares y sacras"],2,"Móvil: 7 cervicales + 12 dorsales + 5 lumbares. Inmóvil (movimiento muy reducido): sacro + cóccix.","columna inmóvil"),
            _conv("ucv_t4_03","¿Qué estructura tiene el axis que no tiene ninguna otra vértebra?",["Agujero transverso","Apófisis odontoides (pestillo de seguridad)","Carillas articulares","Apófisis espinosa bífida"],1,"El axis (C2) presenta la apófisis odontoides, una especie de 'pestillo de seguridad' que refuerza la articulación con el atlas.","axis y odontoides"),
            _conv("ucv_t4_04","¿Cuál es el rasgo propio de las vértebras torácicas (dorsales)?",["Agujero transverso para la arteria vertebral","Apófisis transversas con carillas articulares laterales para las costillas","Apófisis espinosas bífidas","Cuerpo muy voluminoso"],1,"Las vértebras torácicas presentan carillas articulares laterales en las apófisis transversas para articular con las costillas.","vértebras torácicas"),
            _conv("ucv_t4_05","¿Qué forma la pelvis?",["Solo el sacro","Sacro + 2 coxales","Solo los 2 coxales","Sacro + cóccix + coxales"],1,"La pelvis está formada por el sacro (fusión de las 5 vértebras sacras) + 2 huesos coxales.","pelvis"),
            _conv("ucv_t4_06","¿Cuáles son las 3 partes del esternón?",["Cabeza, cuerpo y cola","Manubrio, cuerpo y apéndice xifoides","Diáfisis, epífisis y metáfisis","Superior, medio e inferior"],1,"El esternón consta de: manubrio (parte superior), cuerpo y apéndice xifoides (donde se inserta el diafragma y los rectos anteriores del abdomen).","esternón"),
            _conv("ucv_t4_07","Las costillas 8-10 se denominan:",["Verdaderas o esternales","Falsas","Flotantes","Flotantes auxiliares"],1,"Costillas 1-7: verdaderas (con cartílago costal propio). 8-10: falsas (usan el cartílago de las verdaderas). 11-12: flotantes (no llegan al esternón).","costillas"),
            _conv("ucv_t4_08","¿Cuál es la acción principal del diafragma en la inspiración?",["Se eleva y se relaja","Se contrae y aplana, aumentando el volumen torácico","Se mantiene inmóvil","Disminuye el volumen torácico"],1,"En inspiración: el diafragma se contrae y aplana, los pilares tiran de él, desciende, aumenta el volumen torácico. En espiración: se relaja y eleva.","diafragma"),
            _conv("ucv_t4_09","¿Qué nervio lleva el impulso motor al diafragma?",["Vago","Frénico","Intercostal","Torácico"],1,"El impulso motor al diafragma lo canaliza el nervio frénico (uno para cada hemidiafragma). El hipo incoercible es una hiperestimulación del frénico.","nervio frénico"),
            _conv("ucv_t4_10","¿Qué músculos son antagonistas en la movilización de la escápula?",["Pectoral mayor y dorsal ancho","Pectoral menor (desciende) y trapecio (asciende)","Trapecio y dorsal ancho","Pectoral mayor y trapecio"],1,"Tomando las costillas como punto fijo: el pectoral menor desciende la escápula y el trapecio la asciende. Son antagonistas.","escápula"),
        ]
    },

    "ucv_t5_mmss": {
        "nombre": "Tema 5: Miembro superior",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t5_01","¿Cuál es la función principal de la clavícula?",["Proteger los pulmones","Separar los miembros superiores del esqueleto axial","Sostener el cráneo","Permitir la rotación del hombro"],1,"La clavícula separa los MMSS del esqueleto axial (tronco). Al separarlos se aumenta la capacidad torácica y permite acciones más complejas.","clavícula"),
            _conv("ucv_t5_02","¿Con qué hueso se articula la clavícula en su extremo externo?",["Apófisis coracoides de la escápula","Acromion de la escápula","Cavidad glenoidea","Cabeza del húmero"],1,"La clavícula articula desde el esternón hasta la escápula (en el acromion). La apófisis coracoides es otro accidente anatómico de la escápula.","articulación clavícula"),
            _conv("ucv_t5_03","¿Qué músculos se insertan en la apófisis coracoides de la escápula?",["Deltoides y supraespinoso","Bíceps braquial y pectoral menor","Tríceps y pectoral mayor","Subescapular y redondo menor"],1,"En la apófisis coracoides se insertan el bíceps braquial (cabeza corta) y el pectoral menor.","coracoides"),
            _conv("ucv_t5_04","¿En qué se inserta el deltoides?",["Acromion","Clavícula","Tuberosidad deltoidea del húmero","Troquíter"],2,"El deltoides se inserta en la tuberosidad deltoidea (rugosidad anterolateral del húmero). Origen: clavícula, acromion y espina de la escápula.","deltoides"),
            _conv("ucv_t5_05","La corredera bicipital (surco intertubercular) está situada entre:",["El troquíter y el acromion","El troquíter y el troquín","La diáfisis y la epífisis","El epicóndilo y la epitróclea"],1,"La corredera bicipital está entre el troquíter (mayor) y el troquín (menor). Por ella discurre el tendón de la cabeza larga del bíceps braquial.","corredera bicipital"),
            _conv("ucv_t5_06","¿Cuántos huesos forman el carpo?",["6","8","10","5"],1,"El carpo está formado por 8 huesos en 2 filas. Proximal: escafoides, semilunar, piramidal, pisiforme. Distal: trapecio, trapezoide, grande, ganchoso.","carpo"),
            _conv("ucv_t5_07","¿Qué ligamento es el más resistente de la articulación de la muñeca?",["Ligamento anular del carpo","Ligamento colateral radial","Ligamento radiocarpal palmar","Retináculo flexor"],2,"El ligamento radiocarpal palmar es el más resistente de la muñeca. El retináculo flexor forma el techo del canal carpiano.","muñeca"),
            _conv("ucv_t5_08","¿Qué estructura atraviesa el canal carpiano?",["Arteria radial y nervio radial","Nervio mediano y tendones flexores","Nervio cubital y arteria cubital","Solo tendones extensores"],1,"Por el canal carpiano pasan: nervio mediano + 9 tendones flexores. La compresión del mediano aquí produce el síndrome del túnel carpiano.","canal carpiano"),
            _conv("ucv_t5_09","La arteria braquial se divide en el codo en:",["Radial y cubital","Radial y axilar","Braquial profunda y braquial superficial","Interósea y cubital"],0,"La arteria braquial (continuación de la axilar) se divide a nivel del pliegue del codo en arteria radial y arteria cubital (ulnar).","arteria braquial"),
            _conv("ucv_t5_10","¿Qué nervio se lesiona en la fractura del cuello quirúrgico del húmero?",["Nervio radial","Nervio mediano","Nervio axilar","Nervio musculocutáneo"],2,"El nervio axilar (C5-C6) rodea el cuello quirúrgico del húmero. Su lesión paraliza el deltoides y el teres minor → pérdida de abducción.","nervio axilar"),
        ]
    },

    "ucv_t6_mmii": {
        "nombre": "Tema 6: Miembro inferior",
        "nivel": 1,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t6_01","¿Qué hueso es el más largo del cuerpo humano?",["Tibia","Peroné","Fémur","Húmero"],2,"El fémur es el hueso más largo y resistente del cuerpo. Forma la articulación de la cadera (acetábulo) y la rodilla.","fémur"),
            _conv("ucv_t6_02","¿Qué músculo es el principal flexor de la cadera?",["Glúteo mayor","Cuádriceps","Iliopsoas","Sartorio"],2,"El iliopsoas (psoas mayor + ilíaco) es el principal flexor de la cadera. Se inserta en el trocánter menor del fémur.","flexores cadera"),
            _conv("ucv_t6_03","¿Cuál es el músculo más potente del cuerpo?",["Bíceps braquial","Glúteo mayor","Cuádriceps femoral","Tríceps sural"],1,"El glúteo mayor es el más potente, aunque el cuádriceps también se considera el más grande. El glúteo mayor realiza extensión y rotación externa de cadera.","glúteo mayor"),
            _conv("ucv_t6_04","La rótula es un tipo de hueso:",["Largo","Corto","Plano","Sesamoideo"],3,"La rótula es el hueso sesamoideo más grande del cuerpo. Está incluida en el tendón del cuádriceps y mejora su brazo de palanca.","rótula"),
            _conv("ucv_t6_05","¿Cuántos huesos tiene el tarso?",["5","6","7","8"],2,"El tarso tiene 7 huesos: calcáneo, astrágalo, navicular, cuboides y 3 cuneiformes (medial, intermedio, lateral).","tarso"),
            _conv("ucv_t6_06","¿Qué nervio puede lesionarse al fracturar el cuello del peroné?",["Nervio tibial","Nervio femoral","Nervio peroneo común","Nervio ciático"],2,"El nervio peroneo común rodea el cuello del peroné. Su lesión produce pie caído (incapacidad para la dorsiflexión del pie).","nervio peroneo"),
            _conv("ucv_t6_07","¿De qué raíces se origina el nervio ciático?",["L2-L3-L4","L3-L4-L5","L4-L5-S1-S2-S3","L2-L3-L4-L5"],2,"El nervio ciático (L4-L5-S1-S2-S3) es el nervio más largo del cuerpo. Sale por el agujero ciático mayor y desciende por la cara posterior del muslo.","nervio ciático"),
            _conv("ucv_t6_08","La arteria femoral se palpa en:",["El trocánter mayor","El punto medio del ligamento inguinal","La cara interna del muslo","El espacio poplíteo"],1,"El pulso femoral se palpa en el punto medio del ligamento inguinal. En el triángulo de Scarpa: NAV de lateral a medial (nervio-arteria-vena).","arteria femoral"),
            _conv("ucv_t6_09","¿Qué músculo estabiliza la pelvis durante la marcha monopodal?",["Glúteo mayor","Glúteo medio","Iliopsoas","Cuádriceps"],1,"El glúteo medio estabiliza la pelvis durante la fase monopodal de la marcha. Su parálisis → marcha de Trendelenburg (caída pélvica contralateral).","glúteo medio"),
            _conv("ucv_t6_10","El tendón de Aquiles corresponde al músculo:",["Tibial anterior","Peroneo largo","Tríceps sural (gemelos + sóleo)","Flexor largo de los dedos"],2,"El tendón de Aquiles es el tendón del tríceps sural (gastrocnemios + sóleo). Se inserta en el calcáneo. Es el tendón más grueso del cuerpo.","tendón de Aquiles"),
        ]
    },

    "ucv_t7_corazon": {
        "nombre": "Tema 7: Anatomía del corazón",
        "nivel": 2,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t7_01","¿En qué cavidad del tórax se sitúa el corazón?",["Cavidad pleural derecha","Mediastino","Cavidad pleural izquierda","Cavidad abdominal"],1,"El corazón se sitúa en el mediastino (espacio entre los pulmones). El mediastino medio contiene el corazón y grandes vasos.","localización corazón"),
            _conv("ucv_t7_02","¿Cuántas capas tiene la pared del corazón?",["2","3","4","5"],1,"La pared cardíaca tiene 3 capas: epicardio (externa), miocardio (capa muscular, la más gruesa) y endocardio (interna, en contacto con la sangre).","capas del corazón"),
            _conv("ucv_t7_03","¿Qué membrana recubre externamente el corazón?",["Pleura","Peritoneo","Pericardio","Meninges"],2,"El pericardio es el saco fibroso que rodea el corazón. Tiene dos capas: fibrosa (externa) y serosa (interna, con líquido pericárdico lubricante).","pericardio"),
            _conv("ucv_t7_04","La válvula mitral separa:",["VD y arteria pulmonar","VI y aorta","AI y VI","AD y VD"],2,"La válvula mitral (bicúspide, 2 valvas) está entre la aurícula izquierda (AI) y el ventrículo izquierdo (VI). La tricúspide entre AD y VD.","válvulas cardíacas"),
            _conv("ucv_t7_05","¿Qué arteria irriga el corazón?",["Arteria carótida","Arteria pulmonar","Arterias coronarias","Arteria aorta"],2,"Las arterias coronarias (derecha e izquierda) nacen de la raíz de la aorta e irrigan el miocardio. Su obstrucción causa infarto agudo de miocardio.","arterias coronarias"),
            _conv("ucv_t7_06","¿Cuántas cavidades tiene el corazón?",["2","3","4","5"],2,"El corazón tiene 4 cavidades: 2 aurículas (reciben sangre) y 2 ventrículos (bombean sangre). El tabique interventricular las separa izquierda de derecha.","cavidades cardíacas"),
            _conv("ucv_t7_07","¿Qué ventrículo tiene la pared más gruesa y por qué?",["VD, porque bombea al cuerpo","VI, porque bombea sangre a todo el cuerpo (mayor resistencia)","Ambos igual","AD, por el retorno venoso"],1,"El ventrículo izquierdo tiene pared más gruesa (8-12mm vs 3-4mm del VD) porque debe vencer la resistencia sistémica para bombear sangre a todo el cuerpo.","ventrículos"),
            _conv("ucv_t7_08","La sangre del ventrículo derecho va hacia:",["La aorta","Las arterias coronarias","La arteria pulmonar","La vena cava"],2,"El VD bombea sangre venosa (desoxigenada) a la arteria pulmonar → pulmones → oxigenación. Esta es la circulación pulmonar (menor).","circulación pulmonar"),
            _conv("ucv_t7_09","¿Qué estructura genera el impulso eléctrico que inicia el latido cardíaco?",["Nódulo AV","Haz de His","Nódulo sinusal (SA)","Fibras de Purkinje"],2,"El nódulo sinusal (SA), en la aurícula derecha, es el marcapasos natural. Genera el impulso → nódulo AV → haz de His → Purkinje → contracción ventricular.","sistema de conducción"),
            _conv("ucv_t7_10","¿Qué son las válvulas sigmoideas?",["Las válvulas AV (mitral y tricúspide)","Las válvulas de la aorta y arteria pulmonar","Las válvulas venosas","Los anillos fibrosos"],1,"Las válvulas sigmoideas (semilunares) son la válvula aórtica y la pulmonar. Tienen 3 valvas en forma de nido de golondrina. Impiden el reflujo ventricular.","válvulas sigmoideas"),
        ]
    },

    "ucv_t8_arterias": {
        "nombre": "Tema 8: Grandes vasos arteriales",
        "nivel": 2,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t8_01","¿Cuáles son las 3 capas de la pared arterial?",["Epidermis, dermis e hipodermis","Íntima (endotelio), media (músculo liso) y adventicia","Solo íntima y adventicia","Media, externa e interna"],1,"Arterias: túnica íntima (endotelio), túnica media (músculo liso + elastina, más gruesa cuanto más cerca del corazón) y túnica adventicia (colágeno).","capas arteriales"),
            _conv("ucv_t8_02","¿Qué zonas NO tienen arterias?",["Músculos y huesos","Cartílago, córnea, cristalino, epidermis, uñas y cabello","Vísceras abdominales","SNC"],1,"Las arterias están en todo el organismo EXCEPTO en: cartílago, córnea, cristalino, epidermis, uñas, cabello y faneras (avasculares).","zonas avasculares"),
            _conv("ucv_t8_03","¿Qué arteria se origina en el ventrículo izquierdo y es la única a la que NO se le añade 'arteria' delante?",["Carótida","Subclavia","Aorta","Pulmonar"],2,"La AORTA es la única arteria a la que no se le añade 'arteria' delante (ej: 'arteria femoral', pero solo 'aorta'). Sale del VI.","aorta"),
            _conv("ucv_t8_04","Los troncos supraaórticos emergen del cayado de la aorta. ¿Cuáles son?",["Tronco braquiocefálico, arteria carótida izquierda y subclavia izquierda","Arterias pulmonares","Arterias coronarias","Aorta abdominal y torácica"],0,"Del cayado aórtico emergen 3 troncos supraaórticos: tronco braquiocefálico (carótida derecha + subclavia derecha), carótida izquierda y subclavia izquierda.","cayado aórtico"),
            _conv("ucv_t8_05","¿Por qué las arterias más alejadas del corazón tienen una capa muscular más delgada?",["Porque se desgastan con el tiempo","Porque no tienen que soportar tanta presión","Porque son más jóvenes","Por una anomalía genética"],1,"Las arterias se van bifurcando y disminuyendo su calibre. Dado que las más alejadas no soportan tanta presión, su capa muscular se adelgaza progresivamente.","estructura arterial"),
            _conv("ucv_t8_06","¿En qué se bifurca la aorta abdominal a nivel de las últimas vértebras lumbares?",["Arterias renales","Arterias ilíacas comunes (bifurcación ilíaca)","Arterias femorales","Arterias mesentéricas"],1,"La aorta abdominal se bifurca en 2 arterias ilíacas comunes (bifurcación ilíaca) a nivel de las últimas vértebras lumbares.","bifurcación aórtica"),
            _conv("ucv_t8_07","¿Qué arteria irriga el cerebro junto con la carótida interna?",["Arteria vertebral","Arteria temporal","Arteria facial","Arteria occipital"],0,"Las arterias vertebrales ascienden por los agujeros transversos cervicales, entran al cráneo y forman la arteria basilar. Junto con las carótidas internas forman el polígono de Willis.","irrigación cerebral"),
            _conv("ucv_t8_08","La arteria femoral es continuación de:",["Arteria poplítea","Arteria ilíaca externa","Arteria ilíaca interna","Arteria obturatriz"],1,"La arteria ilíaca externa pasa bajo el ligamento inguinal y se convierte en arteria femoral. Esta pasa por el triángulo de Scarpa y el canal de Hunter.","arteria femoral"),
            _conv("ucv_t8_09","¿Qué arteria se palpa en la cara lateral de la muñeca para tomar el pulso radial?",["Arteria cubital","Arteria interósea","Arteria radial","Arteria braquial"],2,"La arteria radial se palpa en la cara anterolateral de la muñeca (entre el tendón del flexor radial del carpo y el proceso estiloides del radio).","pulso radial"),
            _conv("ucv_t8_10","¿Qué es un aneurisma?",["Obstrucción arterial","Dilatación anormal y localizada de una arteria","Inflamación de la vena","Coágulo en la arteria"],1,"Un aneurisma es una dilatación anormal y localizada de la pared arterial. El más frecuente y peligroso es el de la aorta abdominal (riesgo de rotura).","aneurisma"),
        ]
    },

    "ucv_t9_venas": {
        "nombre": "Tema 9: Grandes vasos venosos y linfáticos",
        "nivel": 2,
        "categoria": "UCV Temario",
        "preguntas": [
            _conv("ucv_t9_01","¿Por qué las venas NO presentan pulso?",["Porque no tienen sangre","Porque no soportan la presión del VI (es amortiguada por las arterias)","Porque están obstruidas","Porque tienen válvulas"],1,"Los pulsos son manifestaciones de la sístole ventricular izquierda. Las venas no soportan esa presión (la amortiguan las arterias), por eso su capa media es menos gruesa.","pulso venoso"),
            _conv("ucv_t9_02","¿Cómo sangran las venas comparadas con las arterias?",["Las venas sangran intermitentemente, las arterias 'en sábana'","Las arterias sangran brutalmente pero intermitentemente, las venas sangran 'en sábana' (homogéneamente)","Ambas igual","Las venas no sangran"],1,"Las arterias sangran de forma brutal pero intermitente (al ritmo de los latidos). Las venas sangran 'en sábana', de forma homogénea y continua.","hemorragia arterial vs venosa"),
            _conv("ucv_t9_03","¿Qué son las válvulas venosas?",["Repliegues del músculo liso","Repliegues del endotelio que obstruyen periódicamente la luz venosa","Válvulas similares a las cardíacas","Estructuras óseas"],1,"Las válvulas venosas son repliegues del endotelio. Suelen tener 2 valvas: una adherida a la pared y otra libre orientada al corazón. Favorecen el retorno venoso.","válvulas venosas"),
            _conv("ucv_t9_04","¿Qué sucede con el número de válvulas venosas?",["Aumenta con el calibre","Aumenta con la disminución del calibre","Es siempre el mismo","Solo hay en las venas grandes"],1,"El número de válvulas AUMENTA cuando DISMINUYE el calibre. Las grandes venas (cava, femoral, subclavia, yugular) NO poseen válvulas.","válvulas venosas calibre"),
            _conv("ucv_t9_05","¿Por qué las grandes venas no tienen válvulas?",["Porque no son importantes","Por el volumen de sangre que tienen, que ejerce presión suficiente","Por evolución","Porque son cortas"],1,"Las grandes venas (cava, femoral, subclavia, yugular) no tienen válvulas porque el volumen de sangre que transportan ejerce la presión necesaria.","grandes venas sin válvulas"),
            _conv("ucv_t9_06","¿Qué porcentaje del volumen sanguíneo transportan las venas profundas?",["20%","50%","80%","100%"],2,"El sistema venoso profundo transporta el 80% del volumen sanguíneo. Acompañan a los grandes vasos arteriales (coronarias, yugulares).","venas profundas"),
            _conv("ucv_t9_07","¿Cuál es un ejemplo de vena superficial del miembro inferior?",["Vena femoral","Vena poplítea","Vena safena","Vena cava"],2,"Las venas SAFENAS (mayor y menor) son el sistema superficial del MMII. La basílica y cefálica son las superficiales del MMSS. Drenan al sistema profundo.","venas safenas"),
            _conv("ucv_t9_08","¿Qué enfermedad afecta al sistema valvular venoso, típicamente en las piernas?",["Arteriosclerosis","Tromboflebitis (varices)","Hemorroides","Aneurisma"],1,"La tromboflebitis (varices) ocurre cuando el sistema valvular venoso se inflama, normalmente en las piernas.","varices"),
            _conv("ucv_t9_09","¿Qué elementos comprende el sistema linfático?",["Solo los ganglios","Vasos y ganglios linfáticos, bazo y timo","Bazo e hígado","Solo los vasos linfáticos"],1,"Sistema linfático = vasos linfáticos + ganglios linfáticos + bazo + timo.","sistema linfático"),
            _conv("ucv_t9_10","¿Dónde drenan los vasos linfáticos?",["En el corazón directamente","En el sistema venoso","En el sistema arterial","En el sistema digestivo"],1,"Los vasos linfáticos transportan linfa (líquido claro con linfocitos) y drenan en el sistema venoso. Presentan ensanchamientos llamados ganglios linfáticos.","vasos linfáticos"),
        ]
    },

    "ucv_reales_3_4_5": {
        "nombre": "🎓 Preguntas Reales de Examen UCV",
        "nivel": 1,
        "categoria": "UCV Examen Real",
        "preguntas": [
            _conv("ucv_r_01","¿Quién genera el líquido sinovial?",["Membrana sinovial","Cartílago articular","Cápsula articular","Cavidad articular"],0,"La membrana sinovial (interna a la cápsula articular) produce el líquido sinovial que lubrica la articulación.","líquido sinovial"),
            _conv("ucv_r_02","¿Qué articulación es anfiartrosis?",["Sincondrosis","Si todas son correctas indica esta opción","Sindesmosis","Gonfosis"],1,"Las anfiartrosis (articulaciones semimóviles) incluyen sincondrosis (cartilaginosas), sindesmosis (fibrosas) y gonfosis (dientes en alvéolos). Todas son correctas.","anfiartrosis"),
            _conv("ucv_r_03","El hueso que tiene forma de alas de mariposa:",["Etmoides","Esfenoides","Maxilar","Nasal"],1,"El esfenoides tiene forma de mariposa con alas mayores y menores. Está en la base del cráneo y articula con todos los huesos craneales.","esfenoides"),
            _conv("ucv_r_04","¿Cómo se denomina la articulación que permite todos los movimientos?",["Gínglimo","Enartrosis","Deslizante","Condílea"],1,"La enartrosis (esferoidea) permite los 3 ejes de movimiento. Ejemplos: articulación del hombro y de la cadera.","enartrosis"),
            _conv("ucv_r_05","¿Cuál de las siguientes funciones es correcta con respecto a la piel?",["Almacena agua y grasa","Impide la pérdida de agua","Regula la temperatura del cuerpo","Todas son correctas"],3,"La piel almacena agua y grasa (hipodermis), actúa como barrera impermeable y regula la temperatura (sudoración y vasodilatación). Todas son correctas.","funciones de la piel"),
            _conv("ucv_r_06","El músculo de la sonrisa se denomina:",["Cigomático mayor","Cigomático menor","Risorio","Buccinador"],2,"El músculo risorio es el músculo de la sonrisa: tira de las comisuras labiales hacia los lados. El cigomático mayor eleva el labio superior.","músculo risorio"),
            _conv("ucv_r_07","La capa más externa de la piel es:",["Dermis","Epidermis","Ninguna de ellas","Hipodermis"],1,"De superficial a profundo: epidermis (más externa) - dermis - hipodermis (más interna/profunda).","capas de la piel"),
            _conv("ucv_r_08","¿Cómo se llama la parte superior del esternón?",["Cuerpo","Ninguna","Mango","Apófisis xifoides"],2,"El esternón se divide en: manubrio (mango, parte superior), cuerpo y apófisis xifoides (inferior, inserción del diafragma).","esternón manubrio"),
            _conv("ucv_r_09","La membrana que cubre las fibras musculares se denomina:",["Perimisio","Fascia","Epimisio","Endomisio"],3,"Endomisio: cubre cada fibra muscular. Perimisio: rodea fascículos (grupos de fibras). Epimisio: recubre todo el músculo. Fascia: envuelve grupos musculares.","membranas musculares"),
            _conv("ucv_r_10","Función del psoas:",["Abducción de cadera","Flexión de cadera","Aducción de cadera","Extensión de cadera"],1,"El psoas (parte del iliopsoas) es el principal flexor de la cadera. El iliopsoas = psoas mayor + ilíaco. Se inserta en el trocánter menor del fémur.","psoas"),
            _conv("ucv_r_11","Los extremos de un hueso largo se denominan:",["Diáfisis","Epífisis","Metáfisis","Compacto"],1,"Epífisis: extremos del hueso. Diáfisis: parte central. Metáfisis: zona de unión entre ambas (cartílago de crecimiento en edad pediátrica).","epífisis"),
            _conv("ucv_r_12","¿Cuántas vértebras cervicales hay?",["7","6","5","8"],0,"7 cervicales + 12 dorsales + 5 lumbares + 5 sacras + 4 coccígeas = 33 vértebras totales.","vértebras cervicales"),
            _conv("ucv_r_13","Las apófisis que salen de las vértebras a ambos lados se denominan:",["Pedículos","Láminas","Espinosas","Transversas"],3,"Apófisis transversas: salen lateralmente a ambos lados. La espinosa es posterior única. Pedículos y láminas forman el arco vertebral posterior.","apófisis vertebrales"),
            _conv("ucv_r_14","La capa que envuelve el hueso en su interior se denomina:",["Cartílago articular","Cavidad medular","Periostio","Endostio"],3,"Endostio: cubre la superficie interna del canal medular. Periostio: cubre la superficie externa del hueso. Ambos contienen células osteoprogenitoras.","endostio"),
            _conv("ucv_r_15","El tejido epitelio cúbico simple tiene la función de:",["Ninguna de ellas","Revestimiento","Protección","Absorción"],3,"El epitelio cúbico simple tiene función de absorción y secreción (ej: túbulos renales, glándulas tiroides, ovarios).","epitelio cúbico"),
            _conv("ucv_r_16","La parte de la neurona que recoge el estímulo de una parte del cuerpo se denomina:",["Axón","Dendrita","Soma","Núcleo"],1,"Las dendritas reciben el estímulo hacia el soma (cuerpo neuronal). El axón conduce el impulso eléctrico hacia otra neurona o efector.","dendritas"),
            _conv("ucv_r_17","Los glóbulos blancos que migran a sitios de infección parasitaria y donde se desarrollan respuestas alérgicas se denominan:",["Neutrófilos","Adipocitos","Eosinófilos","Mastocitos"],2,"Eosinófilos: responden a parásitos y reacciones alérgicas (IgE). Neutrófilos: infecciones bacterianas (primera línea). Mastocitos: hipersensibilidad tipo I.","eosinófilos"),
            _conv("ucv_r_18","El nervio que inerva el músculo elevador del párpado superior es el par craneal:",["3","5","7","4"],0,"El III par craneal (oculomotor común) inerva el elevador del párpado superior. Su lesión produce ptosis palpebral (párpado caído).","par craneal III"),
            _conv("ucv_r_19","Inserción del esternocleidomastoideo:",["Esternón","Mastoides","Clavícula","Costilla 1"],1,"El ECM se INSERTA en la apófisis mastoides del temporal y la línea nucal superior. Sus ORÍGENES son el esternón y la clavícula.","ECM inserción"),
            _conv("ucv_r_20","Otro nombre de la articulación troclear:",["Pivote","Bisagra","Condílea","Trocoide"],1,"Troclear = bisagra (gínglimo). Un solo eje de movimiento (flexo-extensión). Ejemplo clásico: articulación humerocubital del codo.","articulación troclear"),
            _conv("ucv_r_21","¿Qué vértebras tienen las apófisis transversas con agujeros?",["Lumbares","Dorsales","Cervicales","Sacro"],2,"Solo las vértebras cervicales tienen agujero transverso (foramen transversarium), por donde asciende la arteria vertebral hacia el cerebro.","vértebras cervicales agujero"),
            _conv("ucv_r_22","¿Dónde encontramos la carilla costal, en qué vértebras?",["Sacro","Cervicales","Lumbares","Dorsales"],3,"Las vértebras dorsales (torácicas) tienen carillas costales en sus cuerpos y apófisis transversas para articularse con las cabezas y tubérculos de las costillas.","carilla costal"),
            _conv("ucv_r_23","¿En qué región vertebral encontramos el atlas?",["Lumbares","Sacro","Dorsales","Cervicales"],3,"Atlas = C1, primera vértebra cervical. Sostiene el cráneo articulándose con los cóndilos occipitales. Carece de cuerpo vertebral.","atlas C1"),
            _conv("ucv_r_24","¿Cómo se llama el agujero por donde salen los nervios espinales?",["Vertebral","Todas son correctas","Raquídeo","Conjunción"],3,"Agujero de conjunción (o intervertebral): paso de los nervios espinales entre vértebras adyacentes. El agujero vertebral forma el canal raquídeo.","agujero de conjunción"),
            _conv("ucv_r_25","Entre los orígenes del pectoral mayor se encuentra:",["Clavícula","Costillas","Húmero","Escápula"],0,"Orígenes del pectoral mayor: porción clavicular (clavícula), porción esternocostal (esternón y cartílagos costales 1-6). Inserción: labio externo del surco bicipital del húmero.","pectoral mayor"),
            _conv("ucv_r_26","¿Entre qué estructuras encontramos el disco intervertebral?",["Entre los pedículos","Entre los cuerpos","Entre las transversas","Entre las láminas"],1,"Los discos intervertebrales (fibrocartilaginosos, formados por anillo fibroso + núcleo pulposo) están entre los cuerpos vertebrales adyacentes. Amortiguan cargas axiales.","disco intervertebral"),
            _conv("ucv_r_27","Función de los intercostales internos:",["Todas son correctas","Descender la escápula","Inspiración","Espiración"],3,"Intercostales internos: descienden costillas → espiración. Intercostales externos: elevan costillas → inspiración. Son antagonistas.","intercostales"),
            _conv("ucv_r_28","Costillas de la 8ª a la 10ª:",["Flotantes","Enteras","Verdaderas","Falsas"],3,"Verdaderas (1-7): llegan al esternón con cartílago propio. Falsas (8-10): se unen al cartílago de la 7ª. Flotantes (11-12): extremo libre sin conexión anterior.","costillas falsas"),
            _conv("ucv_r_29","¿Cuál es un músculo suprahioideo?",["Digástrico","Esternohioideo","Omohioideo","Tirohioideo"],0,"Suprahioideos (por encima del hioides): digástrico, estilohioideo, milohioideo, genihioideo. Infrahioideos (por debajo): esternohioideo, omohioideo, tirohioideo, esternotitoideo.","músculos hioideos"),
            _conv("ucv_r_30","¿Cuál es el huesecillo más externo del oído?",["Yunque","Caracol","Martillo","Estribo"],2,"De externo a interno: Martillo (unido a la membrana timpánica) - Yunque - Estribo (en contacto con la ventana oval). El caracol NO es huesecillo (es parte del oído interno).","huesecillos del oído"),
            _conv("ucv_r_31","De entre los tejidos conectivos maduros, el que regula la temperatura y es reserva de energía se denomina:",["Tejido adiposo","Tejido conectivo areolar","Tejido conectivo reticular","Tejido conectivo denso irregular"],0,"El tejido adiposo almacena grasa (reserva energética, 9 kcal/g) y actúa como aislante térmico. También protege órganos mecánicamente.","tejido adiposo"),
            _conv("ucv_r_32","¿En qué hueso encontramos el conducto auditivo externo?",["Parietal","Esfenoides","Occipital","Temporal"],3,"El conducto auditivo externo (CAE) está en la porción timpánica del hueso temporal. El temporal también aloja el oído medio e interno y la apófisis mastoides.","conducto auditivo externo"),
            _conv("ucv_r_33","Función correcta del dorsal ancho:",["Rotación interna","Rotación externa","Abducción","Flexión"],0,"Dorsal ancho: aducción, extensión y rotación INTERNA del hombro. Es el 'músculo del nadador'. Se origina en las vértebras torácicas bajas, lumbares y cresta ilíaca.","dorsal ancho"),
            _conv("ucv_r_34","El músculo esplenio tiene como inserción:",["Apófisis espinosas de las primeras dorsales","Costillas primeras","Occipital","Mastoides"],3,"El esplenio de la cabeza se inserta en la apófisis mastoides y la línea nucal superior del occipital. Función: extensión y rotación ipsilateral del cuello.","esplenio"),
            _conv("ucv_r_35","Si vemos la columna desde la posición anatómica, ¿cómo se denomina cuando vemos la columna torcida (lateralizada)?",["Hipercifosis","Escoliosis","Hiperlordosis","Ninguna de ellas"],1,"Escoliosis: desviación lateral de la columna (en el plano frontal). Hipercifosis: aumento de la curvatura dorsal. Hiperlordosis: aumento de la curvatura lumbar o cervical.","escoliosis"),
        ]
    },

}

# ── Índices auxiliares ───────────────────────────────────────────
NIVELES_UCV = {
    1: [k for k, v in BANCO_UCV.items() if v["nivel"] == 1],
    2: [k for k, v in BANCO_UCV.items() if v["nivel"] == 2],
}

CATEGORIAS_UCV = {
    "UCV Temario": [k for k, v in BANCO_UCV.items() if v["categoria"] == "UCV Temario"],
    "UCV Examen Real": [k for k, v in BANCO_UCV.items() if v["categoria"] == "UCV Examen Real"],
}
