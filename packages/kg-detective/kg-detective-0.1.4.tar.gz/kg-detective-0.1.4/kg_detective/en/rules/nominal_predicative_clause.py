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
        "RIGHT_ID": "copular",
        "RIGHT_ATTRS": {"POS": "AUX", "DEP": "ROOT", "LEMMA": "be"}
      },
      {
        "LEFT_ID": "copular",
        "REL_OP": ">",
        "RIGHT_ID": "predicative",
        "RIGHT_ATTRS": {"DEP": {"IN": ["ccomp", "advcl"]}}
      },
    ],
  ]
  dep_matcher.add("nominal_predicative_clause", dep_patterns)
  matches = dep_matcher(doc)

  for _, (copular, predicative) in matches:
    predicative_span = " ".join([e.text for e in doc[predicative].subtree])
    result.append(doc[copular].text)
    result.append(predicative_span)

  return result
   
