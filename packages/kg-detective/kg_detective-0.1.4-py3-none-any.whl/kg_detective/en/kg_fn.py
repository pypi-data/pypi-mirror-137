import sys

VOCAB_LABELS = ["NOUN", "ADJ", "ADV", "PREP", "VERB", "PRON", "DETERMINER", "CONJ", "INTERJ"]


NOUN_RULES = ["noun_proper", "noun_countability", "noun_with_indefinite_art", "noun_with_definite_art", "noun_possessive"]

ADJ_RULES = ["adj_ending_in_ed", "adj_ending_in_ing", "adj_order", "adj_for_equal_comparisons", "adj_comparative", "adj_superlative"]

ADV_RULES = ["adv_of_frequency", "adv_of_manner", "adv_of_time", "adv_of_place", "adv_of_degree", "adv_for_equal_comparisons", "adv_comparative", "adv_superlative"]

PREP_RULES = ["prep_of_time", "prep_of_movement", "prep_of_manner", "prep_with_verb", "prep_with_adj", "prep_with_noun"]

VERB_RULES = ["verb_passive_voice", "verb_simple_present_tense", "verb_simple_past_tense", "verb_simple_future_tense", "verb_present_progressive_tense", "verb_past_progressive_tense", "verb_present_perfect_tense", "verb_past_perfect_tense", "verb_copular", "verb_non_finite", "verb_modal", "verb_auxiliary", "verb_transitive", "verb_intransitive"]

PRON_RULES = ["pron_personal", "pron_possessive", "pron_reflexive", "pron_demonstrative", "pron_indefinite", "pron_relative", "pron_interrogative"]

DETERMINER_RULES = ["det_cardinal_num", "det_ordinal_num", "det_indefinite_art", "det_definite_art"]

CONJ_RULES = ["conj_subordinating", "conj_coordinating"]

INTERJ_RULES = ["interj_interj"]


SEN_LABELS = ["SIMPLE_SEN", "COMPOUND_SEN", "NOMINAL_CLAUSE", "RELATIVE_CLAUSE", "ADVERBIAL_CLAUSE", "SUBJUNCTIVE_MOOD"]

SIMPLE_SEN_RULES= ["simple_s_p", "simple_s_c_p", "simple_s_p_o", "simple_s_p_io_o", "simple_s_p_o_c"]

COMPOUND_SEN_RULES = ["compound_sen"]

NOMINAL_CLAUSE_RULES = ["nominal_subject_clause", "nominal_object_clause", "nominal_predicative_clause", "nominal_appositive_clause"]

RELATIVE_CLAUSE_RULES = ["relative_restrictive_clause", "relative_non_restrictive_clause"]

ADVERBIAL_CLAUSE_RULES = ["adverbial_clause_of_time", "adverbial_clause_of_reason", "adverbial_clause_of_comparison", "adverbial_clause_of_condition", "adverbial_clause_of_concession", "adverbial_clause_of_purpose", "adverbial_clause_of_result"]

SUBJUNCTIVE_MOOD_RULES = ["subjunctive_present", "subjunctive_past", "subjunctive_future", "subjunctive_inversion_in_mood"]

LABELS = VOCAB_LABELS# + SEN_LABELS

LABEL_RULES = {label: getattr(sys.modules[__name__], label+"_RULES") for label in LABELS}


