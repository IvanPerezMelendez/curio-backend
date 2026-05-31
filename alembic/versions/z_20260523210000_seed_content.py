"""seed_content

Revision ID: z_20260523210000
Revises: z_20260523200000
Create Date: 2026-05-23 21:00:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'z_20260523210000'
down_revision: Union[str, None] = 'z_20260523200000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text("""
        INSERT INTO categories (id, name, description, lang) VALUES
        ('c1000000-0000-0000-0000-000000000001','Historia','Historia universal y civilizaciones','es'),
        ('c1000000-0000-0000-0000-000000000002','Biología','Ciencias de la vida','es'),
        ('c1000000-0000-0000-0000-000000000003','Geografía','Geografía física y política','es'),
        ('c1000000-0000-0000-0000-000000000004','Ciencia','Física y química básica','es')
    """))

    op.execute(sa.text("""
        INSERT INTO topics (id, category_id, name, description) VALUES
        ('aa000000-0000-0000-0000-000000000001','c1000000-0000-0000-0000-000000000001','Antigua Roma','El Imperio y la República romana'),
        ('aa000000-0000-0000-0000-000000000002','c1000000-0000-0000-0000-000000000001','Segunda Guerra Mundial','El mayor conflicto bélico de la historia'),
        ('aa000000-0000-0000-0000-000000000003','c1000000-0000-0000-0000-000000000002','Células y ADN','Biología celular y molecular'),
        ('aa000000-0000-0000-0000-000000000004','c1000000-0000-0000-0000-000000000002','Evolución','Selección natural y teoría evolutiva'),
        ('aa000000-0000-0000-0000-000000000005','c1000000-0000-0000-0000-000000000003','Europa','Geografía del continente europeo'),
        ('aa000000-0000-0000-0000-000000000006','c1000000-0000-0000-0000-000000000004','Física Básica','Mecánica clásica y leyes fundamentales'),
        ('aa000000-0000-0000-0000-000000000007','c1000000-0000-0000-0000-000000000004','Química','Elementos y tabla periódica')
    """))

    op.execute(sa.text("""
        INSERT INTO subtopics (id, topic_id, name, subtitle, position) VALUES
        ('bb000000-0000-0000-0000-000000000001','aa000000-0000-0000-0000-000000000001','El Senado Romano','Poder y política en la República romana',1),
        ('bb000000-0000-0000-0000-000000000002','aa000000-0000-0000-0000-000000000001','Las Guerras Púnicas','El choque entre Roma y Cartago',2),
        ('bb000000-0000-0000-0000-000000000003','aa000000-0000-0000-0000-000000000001','Julio César','El dictador que transformó Roma',3),
        ('bb000000-0000-0000-0000-000000000004','aa000000-0000-0000-0000-000000000002','El Pacto Molotov-Ribbentrop','La alianza secreta que dividió Europa',1),
        ('bb000000-0000-0000-0000-000000000005','aa000000-0000-0000-0000-000000000002','El Desembarco de Normandía','El día que cambió la Segunda Guerra Mundial',2),
        ('bb000000-0000-0000-0000-000000000006','aa000000-0000-0000-0000-000000000003','La Mitosis','División celular sin cambio genético',1),
        ('bb000000-0000-0000-0000-000000000007','aa000000-0000-0000-0000-000000000003','El ADN y los Genes','El código de la vida',2),
        ('bb000000-0000-0000-0000-000000000008','aa000000-0000-0000-0000-000000000003','Las Mitocondrias','La central energética de la célula',3),
        ('bb000000-0000-0000-0000-000000000009','aa000000-0000-0000-0000-000000000004','La Selección Natural','El motor del cambio evolutivo',1),
        ('bb000000-0000-0000-0000-000000000010','aa000000-0000-0000-0000-000000000004','La Teoría de Darwin','El viaje que lo cambió todo',2),
        ('bb000000-0000-0000-0000-000000000011','aa000000-0000-0000-0000-000000000005','Los Ríos de Europa','Arterias del continente',1),
        ('bb000000-0000-0000-0000-000000000012','aa000000-0000-0000-0000-000000000005','Las Capitales Europeas','Ciudades que gobiernan naciones',2),
        ('bb000000-0000-0000-0000-000000000013','aa000000-0000-0000-0000-000000000006','Las Leyes de Newton','Los principios de la mecánica clásica',1),
        ('bb000000-0000-0000-0000-000000000014','aa000000-0000-0000-0000-000000000007','La Tabla Periódica','El orden de los elementos',1)
    """))

    # ------------------------------------------------------------------
    # EXERCISES  (base rows: 5 per subtopic × 14 subtopics = 70)
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises (id, subtopic_id, type, tag, question,
                               explanation_title, explanation_body, explanation_fact, lang) VALUES

        -- ===== S1: El Senado Romano =====
        ('e0000001-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000001','multiple-choice','senado-size',
         '¿Cuántos senadores tenía el Senado Romano en época clásica?',
         'El Senado en su apogeo',
         'El Senado llegó a tener 600 senadores tras las reformas de Sila en el siglo I a.C., aunque la cifra original era de 300.',
         'César amplió el Senado hasta 900 miembros, lo que fue muy impopular.','es'),

        ('e0000001-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000001','true-false','senado-war',
         'El Senado Romano tenía potestad para declarar la guerra.',
         'El poder del Senado',
         'El Senado romano controlaba el presupuesto militar y ratificaba las declaraciones de guerra.',
         'El Senado también aprobaba los tratados de paz y controlaba las provincias.','es'),

        ('e0000001-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000001','match','magistraturas',
         'Relaciona cada magistratura romana con su función principal.',
         'Las magistraturas de Roma',
         'Roma desarrolló un sistema de magistraturas electivas anuales para evitar la concentración de poder.',
         'El cargo de dictador era la única magistratura no electiva y con poderes absolutos.','es'),

        ('e0000001-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000001','chronological','rep-romana-crono',
         'Ordena estos hitos de la República Romana de más antiguo a más reciente.',
         'La cronología republicana',
         'La República Romana duró desde el 509 a.C. hasta el 27 a.C., cuando Augusto se convirtió en el primer emperador.',
         'Los romanos contaban los años desde la fundación de Roma (753 a.C.).','es'),

        ('e0000001-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000001','estimation','rep-romana-fundacion',
         '¿En qué año (a.C.) se fundó la República Romana?',
         'La fundación de la República',
         'Según la tradición, la República Romana se fundó en el 509 a.C. tras la expulsión del rey Tarquinio el Soberbio.',
         'El historiador Tito Livio relató en detalle la expulsión del último rey romano.','es'),

        -- ===== S2: Las Guerras Púnicas =====
        ('e0000002-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000002','multiple-choice','punicas-count',
         '¿Cuántas Guerras Púnicas hubo entre Roma y Cartago?',
         'Las tres Guerras Púnicas',
         'Hubo tres Guerras Púnicas (264-241, 218-201 y 149-146 a.C.), que terminaron con la destrucción total de Cartago.',
         'La frase "Cartago debe ser destruida" la popularizó el senador Catón el Viejo.','es'),

        ('e0000002-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000002','true-false','anibal-elefantes',
         'Aníbal Barca cruzó los Alpes con elefantes de guerra.',
         'El cruce de los Alpes',
         'En el 218 a.C. Aníbal cruzó los Alpes con unos 37 elefantes de guerra, aunque la mayoría murieron por el frío.',
         'Solo un elefante, llamado Surus, sobrevivió toda la campaña italiana.','es'),

        ('e0000002-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000002','odd-one-out','generales-punicos',
         '¿Cuál de estos generales NO era cartaginés?',
         'Escipión el Africano',
         'Publio Cornelio Escipión Africano fue el general romano que derrotó a Aníbal en la batalla de Zama (202 a.C.).',
         'Escipión aprendió las tácticas de Aníbal y las usó contra él.','es'),

        ('e0000002-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000002','chronological','punicas-batallas',
         'Ordena estas batallas de las Guerras Púnicas cronológicamente.',
         'Grandes batallas contra Cartago',
         'La batalla de Cannas (216 a.C.) fue una de las mayores derrotas de Roma: hasta 70.000 soldados muertos en un día.',
         'La táctica de doble envolvimiento de Aníbal en Cannas sigue estudiándose en academias militares.','es'),

        ('e0000002-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000002','estimation','anibal-ruta',
         '¿Cuántos kilómetros aproximados recorrió Aníbal desde Cartagena hasta el norte de Italia?',
         'La épica marcha de Aníbal',
         'Aníbal partió de Cartagena y marchó unos 2.500-3.000 km antes de cruzar los Alpes para invadir Italia.',
         'El ejército de Aníbal tardó varios meses en completar esta marcha épica.','es'),

        -- ===== S3: Julio César =====
        ('e0000003-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000003','multiple-choice','cesar-muerte',
         '¿En qué año fue asesinado Julio César?',
         'Los Idus de Marzo',
         'Julio César fue asesinado el 15 de marzo del 44 a.C. a manos de senadores liderados por Bruto y Casio.',
         'Shakespeare inmortalizó este momento con la frase "Et tu, Brute?"','es'),

        ('e0000003-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000003','true-false','cesar-emperador',
         'Julio César fue nombrado Emperador de Roma.',
         'Dictador, no Emperador',
         'César nunca fue emperador. Fue nombrado dictador perpetuo. El primer emperador fue su sobrino nieto Augusto.',
         'El título de César se convirtió en sinónimo de gobernante supremo en muchas lenguas.','es'),

        ('e0000003-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000003','match','cesar-hechos',
         'Relaciona cada hecho histórico con el año en que ocurrió.',
         'La vida de Julio César',
         'César reformó el calendario romano, creando el calendario Juliano con 365 días y un año bisiesto cada 4 años.',
         'El mes de julio lleva su nombre (Julius).','es'),

        ('e0000003-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000003','chronological','cesar-vida',
         'Ordena estos eventos de la vida de César cronológicamente.',
         'Cronología de Julio César',
         'César dijo "Veni, vidi, vici" tras una victoria relámpago en Asia Menor en el 47 a.C.',
         'Esta frase es uno de los ejemplos más famosos de brevedad en la retórica latina.','es'),

        ('e0000003-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000003','estimation','cesar-edad',
         '¿Cuántos años tenía Julio César cuando fue asesinado?',
         'La edad de César',
         'Julio César nació en el 100 a.C. y murió en el 44 a.C., por lo que tenía unos 55-56 años.',
         'La esperanza de vida media en Roma era de unos 35-40 años.','es'),

        -- ===== S4: El Pacto Molotov-Ribbentrop =====
        ('e0000004-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000004','multiple-choice','pacto-anio',
         '¿En qué año se firmó el Pacto Molotov-Ribbentrop?',
         'El pacto de 1939',
         'El Pacto Molotov-Ribbentrop se firmó el 23 de agosto de 1939, una semana antes de la invasión alemana de Polonia.',
         'Molotov era el ministro de Exteriores soviético y Ribbentrop el alemán.','es'),

        ('e0000004-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000004','true-false','pacto-protocolo',
         'El Pacto Molotov-Ribbentrop incluía un protocolo secreto que dividía Europa del Este.',
         'El protocolo secreto',
         'El protocolo secreto dividía Europa del Este en esferas de influencia alemana y soviética, facilitando la invasión de Polonia desde ambos lados.',
         'La existencia del protocolo secreto no fue reconocida oficialmente por la URSS hasta 1989.','es'),

        ('e0000004-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000004','odd-one-out','paises-no-pacto',
         '¿Cuál de estos países NO fue invadido u ocupado como consecuencia del pacto secreto?',
         'El reparto de Europa',
         'El protocolo secreto asignaba Polonia oriental, Finlandia, Estonia, Letonia y Lituania a la esfera soviética. Suiza mantuvo su neutralidad.',
         'Suiza no fue invadida en toda la Segunda Guerra Mundial gracias a su neutralidad y su terreno montañoso.','es'),

        ('e0000004-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000004','match','lideres-1939',
         'Relaciona cada país con su líder en 1939.',
         'Los líderes de 1939',
         'En 1939 el mundo estaba gobernado por figuras muy distintas: desde dictadores totalitarios hasta primeros ministros democráticos.',
         'Churchill aún no era primer ministro en 1939; lo sería en mayo de 1940.','es'),

        ('e0000004-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000004','estimation','polonia-dias',
         '¿Cuántos días duró la resistencia polaca ante la invasión combinada germano-soviética?',
         'La caída de Polonia',
         'Polonia resistió desde el 1 de septiembre hasta el 6 de octubre de 1939: unos 35-36 días.',
         'Polonia nunca capituló formalmente; el gobierno polaco continuó en el exilio en Londres.','es'),

        -- ===== S5: El Desembarco de Normandía =====
        ('e0000005-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000005','multiple-choice','normandia-operacion',
         '¿Cómo se llamó en código el plan del Desembarco de Normandía?',
         'Operación Overlord',
         'El Día D formaba parte de la Operación Overlord, el nombre en clave del desembarco aliado en Normandía el 6 de junio de 1944.',
         'El engaño aliado se llamó Operación Fortitude e hizo creer a los alemanes que el ataque sería en el Paso de Calais.','es'),

        ('e0000005-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000005','true-false','dia-d-fecha',
         'El Día D tuvo lugar el 6 de junio de 1944.',
         'La fecha del Día D',
         'El 6 de junio de 1944, el Día D, fue el mayor desembarco anfibio de la historia. Las tropas aliadas tomaron 5 playas en Normandía.',
         'El Día D fue precedido por el mayor lanzamiento aerotransportado nocturno de la historia.','es'),

        ('e0000005-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000005','odd-one-out','playas-normandia',
         '¿Cuál de estas NO fue una playa del Desembarco de Normandía?',
         'Las cinco playas',
         'Las cinco playas del Día D fueron Utah, Omaha, Gold, Juno y Sword. Dunkerque fue el escenario de la evacuación aliada en 1940.',
         'La playa de Omaha fue la más mortífera, con más de 2.000 bajas americanas en pocas horas.','es'),

        ('e0000005-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000005','chronological','normandia-crono',
         'Ordena estos eventos del Día D cronológicamente.',
         'La secuencia del Día D',
         'El Día D comenzó a medianoche con el lanzamiento de paracaidistas, horas antes de que las tropas de playa tocaran tierra al amanecer.',
         'Eisenhower retrasó el Día D un día por el mal tiempo; la pequeña ventana favorable fue clave.','es'),

        ('e0000005-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000005','estimation','normandia-soldados',
         '¿Cuántos miles de soldados aliados participaron en el Día D?',
         'La escala del Día D',
         'Unos 156.000 soldados aliados participaron el Día D, apoyados por casi 7.000 barcos y 11.000 aviones.',
         'Fue la mayor operación anfibia de la historia y requirió años de planificación.','es'),

        -- ===== S6: La Mitosis =====
        ('e0000006-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000006','multiple-choice','mitosis-celulas',
         '¿Cuántas células hija produce la mitosis?',
         'El resultado de la mitosis',
         'La mitosis produce exactamente 2 células hija genéticamente idénticas a la célula madre.',
         'Una persona adulta tiene unos 37 billones de células, casi todas originadas por mitosis.','es'),

        ('e0000006-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000006','true-false','mitosis-haploide',
         'La mitosis produce células haploides (con la mitad de cromosomas).',
         'Células diploides',
         'La mitosis produce células diploides (46 cromosomas en humanos). Son las células sexuales las que se producen por meiosis y son haploides.',
         'La confusión entre mitosis y meiosis es uno de los errores más comunes en biología.','es'),

        ('e0000006-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000006','chronological','fases-mitosis',
         'Ordena las fases de la mitosis en el orden correcto.',
         'Las fases de la mitosis',
         'La mitosis tiene 4 fases: Profase (cromosomas se condensan), Metafase (se alinean), Anafase (se separan) y Telofase (se forman dos núcleos).',
         'Truco para recordarlas: PMAT (Profase, Metafase, Anafase, Telofase).','es'),

        ('e0000006-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000006','match','mitosis-fases-desc',
         'Relaciona cada fase de la mitosis con lo que ocurre en ella.',
         'Descripción de cada fase',
         'Cada fase de la mitosis tiene un evento clave que la define y permite identificarla al microscopio.',
         'La citocinesis, que divide el citoplasma, ocurre al final de la telofase.','es'),

        ('e0000006-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000006','estimation','cromosomas-humanos',
         '¿Cuántos cromosomas tiene una célula humana normal?',
         'El número cromosómico humano',
         'Las células somáticas humanas tienen 46 cromosomas (23 pares). Este número se duplica antes de la mitosis.',
         'El síndrome de Down ocurre cuando hay un cromosoma 21 extra (trisomía 21).','es'),

        -- ===== S7: El ADN y los Genes =====
        ('e0000007-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000007','multiple-choice','adn-significado',
         '¿Qué significa el acrónimo ADN?',
         'La molécula de la herencia',
         'ADN significa Ácido Desoxirribonucleico. Almacena la información genética en todos los seres vivos excepto algunos virus.',
         'Si se estirara todo el ADN de una célula humana mediría aproximadamente 2 metros.','es'),

        ('e0000007-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000007','true-false','adn-helice',
         'El ADN tiene una estructura de doble hélice.',
         'La doble hélice',
         'Watson y Crick describieron la estructura de doble hélice del ADN en 1953, un hallazgo que les valió el Nobel.',
         'Rosalind Franklin hizo la fotografía de difracción de rayos X que fue clave para el descubrimiento.','es'),

        ('e0000007-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000007','odd-one-out','bases-adn',
         '¿Cuál de estas bases nitrogenadas NO se encuentra en el ADN?',
         'Las bases del ADN y el ARN',
         'El ADN contiene Adenina (A), Guanina (G), Citosina (C) y Timina (T). El Uracilo (U) solo se encuentra en el ARN.',
         'Las bases se emparejan: A con T y G con C.','es'),

        ('e0000007-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000007','match','bases-complementarias',
         'Relaciona cada base del ADN con su base complementaria.',
         'La complementariedad de bases',
         'La complementariedad de bases es fundamental para la replicación del ADN: cada hebra actúa como molde de la complementaria.',
         'Esta propiedad es la base de técnicas como la PCR y la secuenciación de ADN.','es'),

        ('e0000007-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000007','estimation','genoma-pares',
         '¿Cuántos miles de millones de pares de bases tiene el genoma humano aproximadamente?',
         'El tamaño del genoma humano',
         'El genoma humano contiene unos 3.200 millones de pares de bases. Solo el 1,5% codifica proteínas.',
         'El Proyecto Genoma Humano tardó 13 años y costó 3.000 millones de dólares.','es'),

        -- ===== S8: Las Mitocondrias =====
        ('e0000008-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000008','multiple-choice','mito-funcion',
         '¿Cuál es la función principal de las mitocondrias?',
         'La central energética celular',
         'Las mitocondrias producen ATP mediante la respiración celular. Por eso se las llama "la central energética de la célula".',
         'Una sola mitocondria puede producir hasta 38 moléculas de ATP por cada glucosa oxidada.','es'),

        ('e0000008-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000008','true-false','mito-adn',
         'Las mitocondrias tienen su propio ADN independiente del ADN del núcleo.',
         'El ADN mitocondrial',
         'Las mitocondrias contienen su propio ADN circular, lo que apoya la teoría endosimbiótica.',
         'El ADN mitocondrial se hereda exclusivamente por vía materna, sin recombinación.','es'),

        ('e0000008-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000008','odd-one-out','partes-mito',
         '¿Cuál de estos componentes NO pertenece a una mitocondria?',
         'La estructura mitocondrial',
         'Las mitocondrias tienen membrana externa, membrana interna con crestas, matriz y ribosomas de tipo 70S. Los 80S son del citoplasma.',
         'Los ribosomas mitocondriales son más parecidos a los de las bacterias que a los del citoplasma.','es'),

        ('e0000008-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000008','true-false','mito-endo',
         'La teoría endosimbiótica explica el origen evolutivo de las mitocondrias.',
         'La endosimbiosis',
         'La teoría endosimbiótica de Lynn Margulis (1967) propone que las mitocondrias son descendientes de bacterias que vivieron en simbiosis.',
         'Lynn Margulis fue rechazada 15 veces antes de que su teoría fuera publicada.','es'),

        ('e0000008-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000008','estimation','mito-cantidad',
         '¿Cuántas mitocondrias puede tener aproximadamente una célula hepática humana?',
         'La abundancia mitocondrial',
         'Las células hepáticas pueden tener entre 1.000 y 2.000 mitocondrias. Las cardíacas hasta 5.000.',
         'Los eritrocitos (glóbulos rojos) son las únicas células humanas sin mitocondrias.','es'),

        -- ===== S9: La Selección Natural =====
        ('e0000009-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000009','multiple-choice','sel-nat-def',
         '¿Cuál es la mejor definición de selección natural?',
         'El mecanismo evolutivo clave',
         'La selección natural es el proceso por el que individuos con características favorables tienen más probabilidad de reproducirse.',
         'La selección natural no actúa con un propósito; solo filtra lo que ya existe.','es'),

        ('e0000009-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000009','true-false','sel-nat-heredable',
         'La selección natural solo puede actuar sobre rasgos heredables genéticamente.',
         'Heredabilidad y selección',
         'La selección natural únicamente puede causar cambio evolutivo sobre rasgos que se transmiten genéticamente.',
         'Esta es la diferencia clave entre Darwin y Lamarck: Lamarck creía en la herencia de caracteres adquiridos.','es'),

        ('e0000009-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000009','odd-one-out','tipos-sel',
         '¿Cuál de estos NO es un tipo de selección natural reconocido en biología?',
         'Tipos de selección natural',
         'La selección puede ser direccional, estabilizadora o disruptiva. La selección "lamarckiana" no existe como tal.',
         'La selección sexual es un tipo especial de selección natural basada en el éxito reproductivo.','es'),

        ('e0000009-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000009','match','evolucion-conceptos',
         'Relaciona cada concepto evolutivo con su definición.',
         'Conceptos clave de la evolución',
         'Comprender la evolución requiere distinguir mutación (cambio en el ADN), deriva genética (azar) y selección natural (adaptación).',
         'El "cuello de botella" y el "efecto fundador" son casos especiales de deriva genética.','es'),

        ('e0000009-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000009','estimation','vida-millones',
         '¿Hace cuántos millones de años se estima que apareció la primera vida en la Tierra?',
         'El origen de la vida',
         'Los fósiles más antiguos son estromatolitos de ~3.700 millones de años. Evidencias moleculares apuntan a ~3.800 millones.',
         'La Tierra tiene ~4.500 millones de años, por lo que la vida apareció relativamente pronto.','es'),

        -- ===== S10: La Teoría de Darwin =====
        ('e0000010-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000010','multiple-choice','darwin-barco',
         '¿Cómo se llamó el barco en el que Darwin realizó su famoso viaje científico?',
         'El HMS Beagle',
         'Darwin viajó a bordo del HMS Beagle entre 1831 y 1836, recorriendo América del Sur, las Islas Galápagos y Australia.',
         'Darwin tenía solo 22 años cuando embarcó en el Beagle.','es'),

        ('e0000010-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000010','true-false','darwin-origen',
         'Darwin publicó "El origen de las especies" en 1859.',
         'La publicación más influyente de la biología',
         '"El origen de las especies" fue publicado el 24 de noviembre de 1859 y se agotó el mismo día.',
         'Alfred Russel Wallace llegó independientemente a las mismas conclusiones, lo que aceleró la publicación de Darwin.','es'),

        ('e0000010-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000010','chronological','darwin-vida',
         'Ordena estos eventos de la vida de Darwin cronológicamente.',
         'La vida de Charles Darwin',
         'Darwin pasó de ser estudiante de medicina a teólogo frustrado antes de convertirse en el naturalista más influyente.',
         'Darwin sufrió de una enfermedad crónica durante décadas; algunos creen que pudo ser la enfermedad de Chagas.','es'),

        ('e0000010-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000010','match','darwin-conceptos',
         'Relaciona cada término darwiniano con su significado.',
         'El vocabulario de Darwin',
         'Darwin introdujo conceptos que transformaron la biología y que la genética moderna ha enriquecido.',
         'La síntesis evolutiva moderna combina a Darwin con la genética de Mendel y la genética de poblaciones.','es'),

        ('e0000010-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000010','estimation','darwin-edad-pub',
         '¿Cuántos años tenía Darwin cuando publicó "El origen de las especies"?',
         'Darwin a los 50',
         'Darwin nació el 12 de febrero de 1809 y publicó su obra maestra el 24 de noviembre de 1859, cuando tenía 50 años.',
         'Darwin nació el mismo día que Abraham Lincoln, el 12 de febrero de 1809.','es'),

        -- ===== S11: Los Ríos de Europa =====
        ('e0000011-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000011','multiple-choice','rios-largo',
         '¿Cuál es el río más largo de Europa?',
         'El Volga, gigante europeo',
         'El Volga, con 3.531 km, es el río más largo de Europa. Fluye completamente dentro de Rusia y desemboca en el Mar Caspio.',
         'El Danubio, con 2.860 km, es el segundo más largo y el que atraviesa más países.','es'),

        ('e0000011-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000011','true-false','danubio-negro',
         'El río Danubio desemboca en el Mar Negro.',
         'El delta del Danubio',
         'El Danubio recorre 2.860 km atravesando 10 países (el río que pasa por más países del mundo) y desemboca en el Mar Negro.',
         'El Danubio es azul solo en el famoso vals de Strauss; en realidad suele ser verdoso o marrón.','es'),

        ('e0000011-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000011','match','rios-desembocaduras',
         'Relaciona cada río europeo con el mar en el que desemboca.',
         'Las desembocaduras europeas',
         'Los ríos europeos desembocan en distintos mares: Mediterráneo, Atlántico, Mar del Norte, Mar Negro y Mar Caspio.',
         'El Rin, uno de los más importantes de Europa occidental, nace en los Alpes suizos.','es'),

        ('e0000011-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000011','odd-one-out','rios-no-europeos',
         '¿Cuál de estos ríos NO está en Europa?',
         'El Nilo no es europeo',
         'El Nilo, con sus 6.650 km, es el río más largo del mundo, pero fluye por África. Los demás son ríos europeos.',
         'El Ródano nace en un glaciar de los Alpes suizos y fluye hacia el Mediterráneo francés.','es'),

        ('e0000011-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000011','estimation','volga-km',
         '¿Cuántos kilómetros mide el río Volga?',
         'La longitud del Volga',
         'El Volga tiene 3.531 km de longitud, lo que lo convierte en el río más largo de Europa.',
         'El Volga suministra el 80% del agua del Mar Caspio, el lago más grande del mundo.','es'),

        -- ===== S12: Las Capitales Europeas =====
        ('e0000012-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000012','multiple-choice','capital-austria',
         '¿Cuál es la capital de Austria?',
         'Viena, la ciudad imperial',
         'Viena es la capital de Austria y fue el centro del Imperio Habsburgo durante siglos.',
         'Viena fue durante siglos la mayor ciudad de habla alemana del mundo.','es'),

        ('e0000012-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000012','true-false','bruselas-ue',
         'Bruselas es considerada la capital de facto de la Unión Europea.',
         'Bruselas y la UE',
         'Bruselas alberga la Comisión Europea y el Consejo de la UE, siendo el centro administrativo de la institución.',
         'El Parlamento Europeo tiene sede oficial en Estrasburgo, aunque también funciona en Bruselas.','es'),

        ('e0000012-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000012','odd-one-out','no-capital-eu',
         '¿Cuál de estas ciudades NO es la capital de su país?',
         'Ginebra no es capital de Suiza',
         'Ginebra es la segunda ciudad de Suiza y sede de muchos organismos internacionales, pero la capital es Berna.',
         'Berna es la "ciudad federal" de Suiza pero no está reconocida constitucionalmente como capital.','es'),

        ('e0000012-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000012','match','paises-capitales',
         'Relaciona cada país europeo con su capital.',
         'Capitales de Europa',
         'Algunas capitales europeas sorprenden: la de Suiza es Berna (no Zúrich), y la de Países Bajos es Ámsterdam (no La Haya).',
         'La capital más pequeña de Europa es Vaduz, capital de Liechtenstein, con ~5.500 habitantes.','es'),

        ('e0000012-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000012','estimation','madrid-altitud',
         '¿A cuántos metros sobre el nivel del mar está Madrid?',
         'Madrid, la capital más alta de la UE',
         'Madrid, con 667 metros de altitud, es la capital de la Unión Europea situada a mayor altura.',
         'Felipe II estableció Madrid como capital en 1561 por su posición central en la Península Ibérica.','es'),

        -- ===== S13: Las Leyes de Newton =====
        ('e0000013-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000013','multiple-choice','newton-1a-ley',
         '¿Qué establece la Primera Ley de Newton (Ley de Inercia)?',
         'La inercia',
         'Un cuerpo permanece en reposo o en movimiento rectilíneo uniforme a menos que actúe una fuerza neta sobre él.',
         'En el espacio, sin fricción, un objeto lanzado seguiría moviéndose para siempre.','es'),

        ('e0000013-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000013','true-false','newton-2a-ley',
         'La Segunda Ley de Newton establece que la fuerza es igual a la masa por la aceleración (F = m·a).',
         'F = m·a',
         'La Segunda Ley establece que la fuerza neta sobre un objeto es igual al producto de su masa y su aceleración.',
         'Esta ecuación permite calcular desde el movimiento de un proyectil hasta la trayectoria de los planetas.','es'),

        ('e0000013-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000013','match','newton-leyes-match',
         'Relaciona cada Ley de Newton con su enunciado.',
         'Las tres leyes de Newton',
         'Las tres leyes de Newton forman la base de la mecánica clásica y funcionan bien para objetos cotidianos.',
         'A velocidades cercanas a la luz, la física newtoniana falla y es necesaria la relatividad de Einstein.','es'),

        ('e0000013-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000013','estimation','newton-principia',
         '¿En qué año publicó Newton sus Principia Mathematica?',
         'Los Principia de Newton',
         'Newton publicó sus "Philosophiæ Naturalis Principia Mathematica" en 1687, una de las obras científicas más influyentes.',
         'Se dice que Newton concibió la idea de la gravedad al ver caer una manzana, aunque probablemente sea una anécdota apócrifa.','es'),

        ('e0000013-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000013','chronological','newton-descub',
         'Ordena estos hitos científicos de Newton cronológicamente.',
         'La vida científica de Newton',
         'Newton realizó sus mayores descubrimientos en el "año milagroso" (1665-1666) cuando se retiró por la plaga.',
         'Newton dijo: "Me puse de pie sobre hombros de gigantes", refiriéndose a Kepler, Galileo y Copérnico.','es'),

        -- ===== S14: La Tabla Periódica =====
        ('e0000014-0000-0000-0000-000000000001','bb000000-0000-0000-0000-000000000014','multiple-choice','tabla-creador',
         '¿Quién organizó la tabla periódica moderna de los elementos?',
         'Mendeléiev y la tabla periódica',
         'Dmitri Mendeléiev publicó su tabla periódica en 1869, prediciendo la existencia de elementos aún no descubiertos.',
         'Mendeléiev dejó espacios vacíos para elementos no descubiertos, prediciendo sus propiedades con asombrosa precisión.','es'),

        ('e0000014-0000-0000-0000-000000000002','bb000000-0000-0000-0000-000000000014','true-false','tabla-numero-atomico',
         'Los elementos en la tabla periódica moderna están ordenados por número atómico.',
         'El orden de la tabla',
         'La tabla periódica moderna ordena los elementos por número atómico (número de protones), no por masa atómica.',
         'El número atómico del hidrógeno es 1 y el del oganesón (el último elemento) es 118.','es'),

        ('e0000014-0000-0000-0000-000000000003','bb000000-0000-0000-0000-000000000014','odd-one-out','gases-nobles',
         '¿Cuál de estos elementos NO es un gas noble?',
         'El nitrógeno no es gas noble',
         'Los gases nobles (grupo 18) son Helio, Neón, Argón, Kriptón, Xenón y Radón. El Nitrógeno pertenece al grupo 15.',
         'Los gases nobles se llaman así porque casi no reaccionan con otros elementos.','es'),

        ('e0000014-0000-0000-0000-000000000004','bb000000-0000-0000-0000-000000000014','estimation','tabla-elementos',
         '¿Cuántos elementos contiene la tabla periódica actualmente?',
         '118 elementos',
         'La tabla periódica actual contiene 118 elementos confirmados. Los últimos (113-118) fueron nombrados en 2016.',
         'El elemento 119 aún no ha sido sintetizado, pero ya hay laboratorios intentando crearlo.','es'),

        ('e0000014-0000-0000-0000-000000000005','bb000000-0000-0000-0000-000000000014','match','simbolos-elementos',
         'Relaciona cada símbolo químico con el nombre del elemento.',
         'Los símbolos de los elementos',
         'Muchos símbolos no coinciden con el nombre en español porque provienen del latín: Fe (ferrum), Au (aurum), Na (natrium).',
         'El símbolo del wolframio es W porque en alemán se llama "Wolfram".','es')
    """))

    # ------------------------------------------------------------------
    # MULTIPLE-CHOICE detail  (type: multiple-choice AND odd-one-out)
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises_multiple_choice (id, exercise_id, options, correct_index) VALUES
        -- S1 MC
        ('f1000001-0001-0000-0000-000000000001','e0000001-0000-0000-0000-000000000001',ARRAY['100','300','600','900'],2),
        -- S2 MC
        ('f1000002-0001-0000-0000-000000000001','e0000002-0000-0000-0000-000000000001',ARRAY['2','3','4','5'],1),
        -- S2 odd-one-out: generales cartagineses
        ('f1000002-0003-0000-0000-000000000001','e0000002-0000-0000-0000-000000000003',ARRAY['Aníbal','Asdrúbal','Magón','Escipión'],3),
        -- S3 MC
        ('f1000003-0001-0000-0000-000000000001','e0000003-0000-0000-0000-000000000001',ARRAY['42 a.C.','44 a.C.','46 a.C.','48 a.C.'],1),
        -- S4 MC
        ('f1000004-0001-0000-0000-000000000001','e0000004-0000-0000-0000-000000000001',ARRAY['1936','1937','1938','1939'],3),
        -- S4 odd-one-out: países no afectados
        ('f1000004-0003-0000-0000-000000000001','e0000004-0000-0000-0000-000000000003',ARRAY['Polonia','Finlandia','Suiza','Estonia'],2),
        -- S5 MC
        ('f1000005-0001-0000-0000-000000000001','e0000005-0000-0000-0000-000000000001',ARRAY['Operación Overlord','Operación Barbarroja','Operación Mercurio','Operación Sea Lion'],0),
        -- S5 odd-one-out: playas
        ('f1000005-0003-0000-0000-000000000001','e0000005-0000-0000-0000-000000000003',ARRAY['Utah','Omaha','Dunkerque','Gold'],2),
        -- S6 MC
        ('f1000006-0001-0000-0000-000000000001','e0000006-0000-0000-0000-000000000001',ARRAY['1','2','4','8'],1),
        -- S7 MC
        ('f1000007-0001-0000-0000-000000000001','e0000007-0000-0000-0000-000000000001',ARRAY['Ácido Desoxirribonucleico','Ácido Dextrornucleico','Acumulador De Nucleótidos','Ácido Diaminonucleico'],0),
        -- S7 odd-one-out: bases
        ('f1000007-0003-0000-0000-000000000001','e0000007-0000-0000-0000-000000000003',ARRAY['Adenina','Guanina','Uracilo','Citosina'],2),
        -- S8 MC
        ('f1000008-0001-0000-0000-000000000001','e0000008-0000-0000-0000-000000000001',ARRAY['Producir energía (ATP)','Sintetizar proteínas','Almacenar ADN','Digerir desechos celulares'],0),
        -- S8 odd-one-out: partes mitocondria
        ('f1000008-0003-0000-0000-000000000001','e0000008-0000-0000-0000-000000000003',ARRAY['Membrana interna','Matriz mitocondrial','Crestas','Ribosoma 80S'],3),
        -- S9 MC
        ('f1000009-0001-0000-0000-000000000001','e0000009-0000-0000-0000-000000000001',ARRAY['Supervivencia del más fuerte','Reproducción diferencial según adaptación','Mutación aleatoria de genes','Herencia de caracteres adquiridos'],1),
        -- S9 odd-one-out: tipos selección
        ('f1000009-0003-0000-0000-000000000001','e0000009-0000-0000-0000-000000000003',ARRAY['Selección direccional','Selección disruptiva','Selección estabilizadora','Selección lamarckiana'],3),
        -- S10 MC
        ('f1000010-0001-0000-0000-000000000001','e0000010-0000-0000-0000-000000000001',ARRAY['HMS Beagle','HMS Victory','Endeavour','Santa María'],0),
        -- S11 MC
        ('f1000011-0001-0000-0000-000000000001','e0000011-0000-0000-0000-000000000001',ARRAY['Volga','Danubio','Rin','Elba'],0),
        -- S11 odd-one-out: ríos no europeos
        ('f1000011-0004-0000-0000-000000000001','e0000011-0000-0000-0000-000000000004',ARRAY['Rin','Ródano','Nilo','Vístula'],2),
        -- S12 MC
        ('f1000012-0001-0000-0000-000000000001','e0000012-0000-0000-0000-000000000001',ARRAY['Berna','Viena','Bratislava','Budapest'],1),
        -- S12 odd-one-out: ciudad no capital
        ('f1000012-0003-0000-0000-000000000001','e0000012-0000-0000-0000-000000000003',ARRAY['Dublín','Ginebra','Oslo','Reikiavik'],1),
        -- S13 MC
        ('f1000013-0001-0000-0000-000000000001','e0000013-0000-0000-0000-000000000001',ARRAY['Todo cuerpo mantiene su estado si no actúa fuerza neta','F = m·a','Toda acción tiene reacción igual y opuesta','La gravedad es proporcional a la masa'],0),
        -- S14 MC
        ('f1000014-0001-0000-0000-000000000001','e0000014-0000-0000-0000-000000000001',ARRAY['Mendeléiev','Dalton','Bohr','Rutherford'],0),
        -- S14 odd-one-out: gases nobles
        ('f1000014-0003-0000-0000-000000000001','e0000014-0000-0000-0000-000000000003',ARRAY['Helio','Neón','Nitrógeno','Argón'],2)
    """))

    # ------------------------------------------------------------------
    # TRUE-FALSE detail
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises_true_false (id, exercise_id, correct) VALUES
        ('d1000001-0002-0000-0000-000000000001','e0000001-0000-0000-0000-000000000002',true),
        ('d1000002-0002-0000-0000-000000000001','e0000002-0000-0000-0000-000000000002',true),
        ('d1000003-0002-0000-0000-000000000001','e0000003-0000-0000-0000-000000000002',false),
        ('d1000004-0002-0000-0000-000000000001','e0000004-0000-0000-0000-000000000002',true),
        ('d1000005-0002-0000-0000-000000000001','e0000005-0000-0000-0000-000000000002',true),
        ('d1000006-0002-0000-0000-000000000001','e0000006-0000-0000-0000-000000000002',false),
        ('d1000007-0002-0000-0000-000000000001','e0000007-0000-0000-0000-000000000002',true),
        ('d1000008-0002-0000-0000-000000000001','e0000008-0000-0000-0000-000000000002',true),
        ('d1000008-0004-0000-0000-000000000001','e0000008-0000-0000-0000-000000000004',true),
        ('d1000009-0002-0000-0000-000000000001','e0000009-0000-0000-0000-000000000002',true),
        ('d1000010-0002-0000-0000-000000000001','e0000010-0000-0000-0000-000000000002',true),
        ('d1000011-0002-0000-0000-000000000001','e0000011-0000-0000-0000-000000000002',true),
        ('d1000012-0002-0000-0000-000000000001','e0000012-0000-0000-0000-000000000002',true),
        ('d1000013-0002-0000-0000-000000000001','e0000013-0000-0000-0000-000000000002',true),
        ('d1000014-0002-0000-0000-000000000001','e0000014-0000-0000-0000-000000000002',true)
    """))

    # ------------------------------------------------------------------
    # MATCH PAIRS detail
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises_match_pairs (id, exercise_id, position, left_text, right_text) VALUES
        -- S1: magistraturas romanas
        ('f3000001-0003-0000-0000-000000000001','e0000001-0000-0000-0000-000000000003',1,'Cónsul','Jefe supremo del ejército y del Estado'),
        ('f3000001-0003-0000-0000-000000000002','e0000001-0000-0000-0000-000000000003',2,'Pretor','Impartía justicia y gobernaba provincias'),
        ('f3000001-0003-0000-0000-000000000003','e0000001-0000-0000-0000-000000000003',3,'Censor','Realizaba el censo y vigilaba las costumbres'),
        ('f3000001-0003-0000-0000-000000000004','e0000001-0000-0000-0000-000000000003',4,'Cuestor','Administraba las finanzas del Estado'),
        -- S3: César hechos/años
        ('f3000003-0003-0000-0000-000000000001','e0000003-0000-0000-0000-000000000003',1,'49 a.C.','Cruce del Rubicón e inicio de la guerra civil'),
        ('f3000003-0003-0000-0000-000000000002','e0000003-0000-0000-0000-000000000003',2,'46 a.C.','Reforma del calendario juliano'),
        ('f3000003-0003-0000-0000-000000000003','e0000003-0000-0000-0000-000000000003',3,'44 a.C.','Nombramiento como dictador perpetuo y asesinato'),
        -- S4: líderes de 1939
        ('f3000004-0004-0000-0000-000000000001','e0000004-0000-0000-0000-000000000004',1,'Alemania','Adolf Hitler'),
        ('f3000004-0004-0000-0000-000000000002','e0000004-0000-0000-0000-000000000004',2,'URSS','Iósif Stalin'),
        ('f3000004-0004-0000-0000-000000000003','e0000004-0000-0000-0000-000000000004',3,'Reino Unido','Neville Chamberlain'),
        ('f3000004-0004-0000-0000-000000000004','e0000004-0000-0000-0000-000000000004',4,'Francia','Édouard Daladier'),
        -- S6: fases mitosis
        ('f3000006-0004-0000-0000-000000000001','e0000006-0000-0000-0000-000000000004',1,'Profase','Los cromosomas se condensan y la membrana nuclear desaparece'),
        ('f3000006-0004-0000-0000-000000000002','e0000006-0000-0000-0000-000000000004',2,'Metafase','Los cromosomas se alinean en el ecuador de la célula'),
        ('f3000006-0004-0000-0000-000000000003','e0000006-0000-0000-0000-000000000004',3,'Anafase','Las cromátidas hermanas se separan hacia los polos'),
        ('f3000006-0004-0000-0000-000000000004','e0000006-0000-0000-0000-000000000004',4,'Telofase','Se forman dos núcleos y la célula comienza a dividirse'),
        -- S7: bases complementarias del ADN
        ('f3000007-0004-0000-0000-000000000001','e0000007-0000-0000-0000-000000000004',1,'Adenina (A)','Timina (T)'),
        ('f3000007-0004-0000-0000-000000000002','e0000007-0000-0000-0000-000000000004',2,'Timina (T)','Adenina (A)'),
        ('f3000007-0004-0000-0000-000000000003','e0000007-0000-0000-0000-000000000004',3,'Guanina (G)','Citosina (C)'),
        ('f3000007-0004-0000-0000-000000000004','e0000007-0000-0000-0000-000000000004',4,'Citosina (C)','Guanina (G)'),
        -- S9: conceptos evolutivos
        ('f3000009-0004-0000-0000-000000000001','e0000009-0000-0000-0000-000000000004',1,'Mutación','Cambio aleatorio en la secuencia del ADN'),
        ('f3000009-0004-0000-0000-000000000002','e0000009-0000-0000-0000-000000000004',2,'Selección natural','Reproducción diferencial según adaptación'),
        ('f3000009-0004-0000-0000-000000000003','e0000009-0000-0000-0000-000000000004',3,'Deriva genética','Cambio evolutivo por azar en poblaciones pequeñas'),
        ('f3000009-0004-0000-0000-000000000004','e0000009-0000-0000-0000-000000000004',4,'Especiación','Formación de nuevas especies por aislamiento reproductivo'),
        -- S10: conceptos de Darwin
        ('f3000010-0004-0000-0000-000000000001','e0000010-0000-0000-0000-000000000004',1,'Variación','Diferencias hereditarias entre individuos de la misma especie'),
        ('f3000010-0004-0000-0000-000000000002','e0000010-0000-0000-0000-000000000004',2,'Lucha por la existencia','Competencia por recursos limitados en la naturaleza'),
        ('f3000010-0004-0000-0000-000000000003','e0000010-0000-0000-0000-000000000004',3,'Adaptación','Rasgo que mejora la supervivencia en un ambiente específico'),
        -- S11: ríos y sus desembocaduras
        ('f3000011-0003-0000-0000-000000000001','e0000011-0000-0000-0000-000000000003',1,'Volga','Mar Caspio'),
        ('f3000011-0003-0000-0000-000000000002','e0000011-0000-0000-0000-000000000003',2,'Danubio','Mar Negro'),
        ('f3000011-0003-0000-0000-000000000003','e0000011-0000-0000-0000-000000000003',3,'Rin','Mar del Norte'),
        ('f3000011-0003-0000-0000-000000000004','e0000011-0000-0000-0000-000000000003',4,'Ebro','Mar Mediterráneo'),
        -- S12: países y capitales
        ('f3000012-0004-0000-0000-000000000001','e0000012-0000-0000-0000-000000000004',1,'Países Bajos','Ámsterdam'),
        ('f3000012-0004-0000-0000-000000000002','e0000012-0000-0000-0000-000000000004',2,'Suiza','Berna'),
        ('f3000012-0004-0000-0000-000000000003','e0000012-0000-0000-0000-000000000004',3,'Bélgica','Bruselas'),
        ('f3000012-0004-0000-0000-000000000004','e0000012-0000-0000-0000-000000000004',4,'Polonia','Varsovia'),
        -- S13: leyes de Newton
        ('f3000013-0003-0000-0000-000000000001','e0000013-0000-0000-0000-000000000003',1,'Primera Ley','Todo cuerpo mantiene su estado si no hay fuerza neta'),
        ('f3000013-0003-0000-0000-000000000002','e0000013-0000-0000-0000-000000000003',2,'Segunda Ley','La fuerza neta es igual a masa por aceleración (F=ma)'),
        ('f3000013-0003-0000-0000-000000000003','e0000013-0000-0000-0000-000000000003',3,'Tercera Ley','Toda acción genera una reacción igual y opuesta'),
        -- S14: símbolos de elementos químicos
        ('f3000014-0005-0000-0000-000000000001','e0000014-0000-0000-0000-000000000005',1,'Fe','Hierro'),
        ('f3000014-0005-0000-0000-000000000002','e0000014-0000-0000-0000-000000000005',2,'Au','Oro'),
        ('f3000014-0005-0000-0000-000000000003','e0000014-0000-0000-0000-000000000005',3,'Na','Sodio'),
        ('f3000014-0005-0000-0000-000000000004','e0000014-0000-0000-0000-000000000005',4,'K','Potasio')
    """))

    # ------------------------------------------------------------------
    # CHRONOLOGICAL detail
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises_chrono_items (id, exercise_id, item_key, label, year, position) VALUES
        -- S1: hitos de la República Romana
        ('a2000001-0004-0000-0000-000000000001','e0000001-0000-0000-0000-000000000004','rep','Fundación de la República Romana',-509,1),
        ('a2000001-0004-0000-0000-000000000002','e0000001-0000-0000-0000-000000000004','leg12','Las Doce Tablas (primera ley escrita)',-450,2),
        ('a2000001-0004-0000-0000-000000000003','e0000001-0000-0000-0000-000000000004','pun1','Inicio de la Primera Guerra Púnica',-264,3),
        ('a2000001-0004-0000-0000-000000000004','e0000001-0000-0000-0000-000000000004','grac','Reformas de los hermanos Graco',-133,4),
        -- S2: batallas de las Guerras Púnicas
        ('a2000002-0004-0000-0000-000000000001','e0000002-0000-0000-0000-000000000004','mile','Batalla de Milas (primera victoria naval romana)',-260,1),
        ('a2000002-0004-0000-0000-000000000002','e0000002-0000-0000-0000-000000000004','treb','Batalla del Trebia (victoria de Aníbal)',-218,2),
        ('a2000002-0004-0000-0000-000000000003','e0000002-0000-0000-0000-000000000004','cann','Batalla de Cannas (mayor derrota de Roma)',-216,3),
        ('a2000002-0004-0000-0000-000000000004','e0000002-0000-0000-0000-000000000004','zama','Batalla de Zama (derrota final de Aníbal)',-202,4),
        -- S3: vida de Julio César
        ('a2000003-0004-0000-0000-000000000001','e0000003-0000-0000-0000-000000000004','nac','Nacimiento de Julio César',-100,1),
        ('a2000003-0004-0000-0000-000000000002','e0000003-0000-0000-0000-000000000004','gal','Conquista de la Galia',-58,2),
        ('a2000003-0004-0000-0000-000000000003','e0000003-0000-0000-0000-000000000004','rub','Cruce del Rubicón',-49,3),
        ('a2000003-0004-0000-0000-000000000004','e0000003-0000-0000-0000-000000000004','dic','Asesinato en los Idus de Marzo',-44,4),
        -- S5: secuencia del Día D
        ('a2000005-0004-0000-0000-000000000001','e0000005-0000-0000-0000-000000000004','para','Lanzamiento de paracaidistas (00:15h)',1944,1),
        ('a2000005-0004-0000-0000-000000000002','e0000005-0000-0000-0000-000000000004','bom','Bombardeo aéreo de las defensas alemanas',1944,2),
        ('a2000005-0004-0000-0000-000000000003','e0000005-0000-0000-0000-000000000004','des','Desembarco en las playas (06:30h)',1944,3),
        ('a2000005-0004-0000-0000-000000000004','e0000005-0000-0000-0000-000000000004','lib','Liberación de Cherbourg (25 días después)',1944,4),
        -- S6: fases de la mitosis
        ('a2000006-0003-0000-0000-000000000001','e0000006-0000-0000-0000-000000000003','pro','Profase',1,1),
        ('a2000006-0003-0000-0000-000000000002','e0000006-0000-0000-0000-000000000003','met','Metafase',2,2),
        ('a2000006-0003-0000-0000-000000000003','e0000006-0000-0000-0000-000000000003','ana','Anafase',3,3),
        ('a2000006-0003-0000-0000-000000000004','e0000006-0000-0000-0000-000000000003','tel','Telofase',4,4),
        -- S10: vida de Darwin
        ('a2000010-0003-0000-0000-000000000001','e0000010-0000-0000-0000-000000000003','nac','Nacimiento de Darwin en Shrewsbury',1809,1),
        ('a2000010-0003-0000-0000-000000000002','e0000010-0000-0000-0000-000000000003','bea','Inicio del viaje en el HMS Beagle',1831,2),
        ('a2000010-0003-0000-0000-000000000003','e0000010-0000-0000-0000-000000000003','ori','Publicación de El origen de las especies',1859,3),
        ('a2000010-0003-0000-0000-000000000004','e0000010-0000-0000-0000-000000000003','mue','Muerte de Darwin en Downe',1882,4),
        -- S13: hitos científicos de Newton (en orden cronológico correcto)
        ('a2000013-0005-0000-0000-000000000001','e0000013-0000-0000-0000-000000000005','cal','Invención del cálculo diferencial (año milagroso)',1666,1),
        ('a2000013-0005-0000-0000-000000000002','e0000013-0000-0000-0000-000000000005','pri','Publicación de los Principia Mathematica',1687,2),
        ('a2000013-0005-0000-0000-000000000003','e0000013-0000-0000-0000-000000000005','rsa','Presidente de la Royal Society',1703,3),
        ('a2000013-0005-0000-0000-000000000004','e0000013-0000-0000-0000-000000000005','opt','Publicación de Opticks',1704,4)
    """))

    # ------------------------------------------------------------------
    # ESTIMATION detail
    # ------------------------------------------------------------------
    op.execute(sa.text("""
        INSERT INTO exercises_estimation (id, exercise_id, unit, min_val, max_val, step, default_value, correct, tolerance) VALUES
        ('b2000001-0005-0000-0000-000000000001','e0000001-0000-0000-0000-000000000005','a.C.',400,700,10,550,509,20),
        ('b2000002-0005-0000-0000-000000000001','e0000002-0000-0000-0000-000000000005','km',500,6000,100,2500,3000,400),
        ('b2000003-0005-0000-0000-000000000001','e0000003-0000-0000-0000-000000000005','años',40,80,1,60,55,3),
        ('b2000004-0005-0000-0000-000000000001','e0000004-0000-0000-0000-000000000005','días',10,90,5,30,36,5),
        ('b2000005-0005-0000-0000-000000000001','e0000005-0000-0000-0000-000000000005','miles de soldados',30,300,10,100,156,20),
        ('b2000006-0005-0000-0000-000000000001','e0000006-0000-0000-0000-000000000005','cromosomas',20,100,2,46,46,0),
        ('b2000007-0005-0000-0000-000000000001','e0000007-0000-0000-0000-000000000005','miles de millones',1,8,0.5,3,3.2,0.5),
        ('b2000008-0005-0000-0000-000000000001','e0000008-0000-0000-0000-000000000005','mitocondrias',100,5000,100,1000,2000,500),
        ('b2000009-0005-0000-0000-000000000001','e0000009-0000-0000-0000-000000000005','millones de años',1000,5000,100,2500,3800,300),
        ('b2000010-0005-0000-0000-000000000001','e0000010-0000-0000-0000-000000000005','años',30,70,1,45,50,2),
        ('b2000011-0005-0000-0000-000000000001','e0000011-0000-0000-0000-000000000005','km',1000,5000,100,2500,3531,200),
        ('b2000012-0005-0000-0000-000000000001','e0000012-0000-0000-0000-000000000005','metros',200,1200,50,600,667,80),
        ('b2000013-0004-0000-0000-000000000001','e0000013-0000-0000-0000-000000000004','año',1650,1750,5,1700,1687,10),
        ('b2000014-0004-0000-0000-000000000001','e0000014-0000-0000-0000-000000000004','elementos',80,130,1,100,118,2)
    """))


def downgrade() -> None:
    exercise_ids = ",".join(
        f"'e{s:07d}-0000-0000-0000-{e:012d}'"
        for s in range(1, 15) for e in range(1, 6)
    )
    subtopic_ids = ",".join(
        f"'bb000000-0000-0000-0000-{i:012d}'" for i in range(1, 15)
    )
    op.execute(sa.text(f"DELETE FROM exercises_estimation    WHERE exercise_id IN ({exercise_ids})"))
    op.execute(sa.text(f"DELETE FROM exercises_chrono_items  WHERE exercise_id IN ({exercise_ids})"))
    op.execute(sa.text(f"DELETE FROM exercises_match_pairs   WHERE exercise_id IN ({exercise_ids})"))
    op.execute(sa.text(f"DELETE FROM exercises_true_false    WHERE exercise_id IN ({exercise_ids})"))
    op.execute(sa.text(f"DELETE FROM exercises_multiple_choice WHERE exercise_id IN ({exercise_ids})"))
    op.execute(sa.text(f"DELETE FROM exercises WHERE subtopic_id IN ({subtopic_ids})"))
    op.execute(sa.text(f"DELETE FROM subtopics WHERE id IN ({subtopic_ids})"))
    op.execute(sa.text("""
        DELETE FROM topics WHERE id IN (
            'aa000000-0000-0000-0000-000000000001','aa000000-0000-0000-0000-000000000002',
            'aa000000-0000-0000-0000-000000000003','aa000000-0000-0000-0000-000000000004',
            'aa000000-0000-0000-0000-000000000005','aa000000-0000-0000-0000-000000000006',
            'aa000000-0000-0000-0000-000000000007'
        )
    """))
    op.execute(sa.text("""
        DELETE FROM categories WHERE id IN (
            'c1000000-0000-0000-0000-000000000001','c1000000-0000-0000-0000-000000000002',
            'c1000000-0000-0000-0000-000000000003','c1000000-0000-0000-0000-000000000004'
        )
    """))
