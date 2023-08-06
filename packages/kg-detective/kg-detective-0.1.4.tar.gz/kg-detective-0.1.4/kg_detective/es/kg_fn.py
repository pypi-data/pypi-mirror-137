import sys

VOCAB_LABELS = ["NOUN", "ART", "VERB", "ADJ", "PREP", "PRON", "ADV", "NUM", "CONJ", "INTERJ"]

NOUN_RULES = ["noun_géneros", "noun_números", "noun_propios", "noun_comparativa"]

ART_RULES = ["art_indeterminado", "art_determinado", "art_omisión"]

VERB_RULES = ["verb_indicativo_presente", "verb_indicativo_pretérito", "verb_indicativo_pretérito_perfecto", "verb_indicativo_pretérito_imperfecto", "verb_indicativo_pretérito_pluscuamperfecto", "verb_indicativo_futuro", "verb_indicativo_futuro_perfecto", "verb_condicional_simple", "verb_condicional_compuesto", "verb_subjuntivo_presente", "verb_subjuntivo_pretérito_perfecto", "verb_subjuntivo_pretérito_imperfecto", "verb_subjuntivo_pretérito_pluscuamperfecto", "verb_imperativo_regulares", "verb_imperativo_irregulares", "verb_imperativo_con_pron", "verb_voz_pasiva", "verb_infinitivo", "verb_participio", "verb_gerundio", "verb_oraciones_impersonales", "verb_reflexivos"]

ADJ_RULES = ["adj_posesivos", "adj_demostrativos", "adj_indefinidos", "adj_género_y_número", "adj_comparativa", "adj_superlativa"]

PREP_RULES = ["prep_con_verbo", "prep_con_adjetivo"]

PRON_RULES = ["pron_personales_de_sujeto", "pron_ablativos", "pron_personales_de_objeto_directo", "pron_personales_de_objeto_indirecto", "pron_reflexivo", "pron_posesivo", "pron_demostrativo", "pron_indefinido", "pron_relativo", "pron_interrogativo"]

ADV_RULES = ["adv_lugar", "adv_tiempo", "adv_frecuencia", "adv_cantidad", "adv_modo", "adv_comparativa", "adv_afirmación_y_negación"]

NUM_RULES = ["num_cardinales", "num_ordinales", "num_múltiplos", "num_división_y_fracciones", "num_horas_y_fechas"]

CONJ_RULES = ["conj_conj"]

INTERJ_RULES = ["interj_interj"]

SEN_LABELS = ["COORDINALE", "SUBORDINADA"]
COORDINALE_RULES = ["coordinale"]
SUBORDINADA_RULES = ["subordinada_substantiva", "subordinada_adjetiva", "subordinada_temporal", "subordinada_locativa", "subordinada_modal", "subordinada_comparativa", "subordinada_causal", "subordinada_consecutiva", "subordinada_final", "subordinada_concesiva", "subordinada_condicional"]

LABELS = VOCAB_LABELS + SEN_LABELS

LABEL_RULES = {label: getattr(sys.modules[__name__], label+"_RULES") for label in LABELS}

