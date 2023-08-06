from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "C",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT"}
      },
      {
        "LEFT_ID": "C",
        "REL_OP": ">",
        "RIGHT_ID": "S",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
      },
      {
        "LEFT_ID": "C",
        "REL_OP": ">",
        "RIGHT_ID": "P",
        "RIGHT_ATTRS": {"DEP": {"IN": ["attr", "oprd"]}}
      },
    ],
  ]
  dep_matcher.add("simple_s_c_p", dep_patterns)
  matches = dep_matcher(doc)

  for _, (C, S, P) in matches:
    black = ['dative', 'dobj']
    is_valid = all([c.dep_ not in black for c in doc[C].children])
    if is_valid:
      subj_span = " ".join([e.text for e in doc[S].subtree])
      copula_range = [l.i for l in doc[C].lefts if l.dep_=="aux"]
      copula_range.append(C)
      copula_span = doc[min(copula_range): max(copula_range)+1].text
      predicative_span = " ".join([e.text for e in doc[P].subtree])
      result.append({"subject": subj_span, "copula": copula_span, "predictive": predicative_span})

  return result
   
