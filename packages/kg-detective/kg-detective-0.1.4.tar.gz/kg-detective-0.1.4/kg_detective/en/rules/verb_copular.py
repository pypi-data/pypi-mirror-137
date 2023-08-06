from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for copular verbs   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  attr_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB", "LEMMA": "become"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "attr",
      "RIGHT_ATTRS": {"DEP": "attr"}
    },
  ]
  acomp_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "LEMMA": {"IN": ["come", "look", "sound", "taste", "be", "smell", "go", "get", "feel"]}}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "acomp",
      "RIGHT_ATTRS": {"DEP": {"IN": ["acomp", "advcl"]}}
    }
  ]

  oprd_dep = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": {"IN": ["VERB"]}, "LEMMA": {"IN": ["appear"]}}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "oprd",
      "RIGHT_ATTRS": {"DEP": "oprd"}
    }
  ]


  dep_patterns = [attr_dep, acomp_dep, oprd_dep]
  dep_matcher.add("verb_copular", dep_patterns)
  matches = dep_matcher(doc)

  for _, (copular, copular_obj) in matches:
    if copular < copular_obj:
      span_text = doc[copular].text + " " + " ".join([e.text for e in doc[copular_obj].subtree])
      result.append({"text": span_text})

  return result
   
