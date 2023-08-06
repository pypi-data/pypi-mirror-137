from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for verbs with passive voice  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  complex_passive = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB", "TAG": "VBN"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "aux_2",
      "RIGHT_ATTRS": {"DEP": "auxpass", "POS": "AUX", "lemma": "be", "TAG": {"IN": ["VBN", "VBG"]}}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "aux_1",
      "RIGHT_ATTRS": {"DEP": "aux", "POS": "AUX"}
    }
  ]
  simple_passive = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB", "TAG": "VBN"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "aux",
      "RIGHT_ATTRS": {"DEP": "auxpass", "POS": "AUX", "lemma": "be", "TAG": {"NOT_IN": ["VBN", "VBG"]}}
    }
  ]

  dep_patterns = [simple_passive, complex_passive]
  dep_matcher.add("verb_passive_voice", dep_patterns)
  matches = dep_matcher(doc)
  dep_ranges = [(token_ids[-1], token_ids[0]+1) for _, token_ids in matches]

  # merge ranges
  refined_matches = merge(dep_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})

  return result
   
