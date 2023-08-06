from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions of manner 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  # pattern: as ... as ...
  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"POS": "ADP", "LOWER": {"IN": ["by", "in", "with"]}}
      },
      {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "method_obj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["pobj", "pcomp"]}}
      },
    ],
  ]
  dep_matcher.add("prep_manner", dep_patterns)
  matches = dep_matcher(doc)

  for _, (prep, method_obj) in matches:
    span_text = doc[prep].text + " " + " ".join([t.text for t in doc[method_obj].subtree])
    result.append({"text": span_text})

  return result
   
