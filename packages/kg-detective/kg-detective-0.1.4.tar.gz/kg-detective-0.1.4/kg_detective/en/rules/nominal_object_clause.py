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
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": {"IN": ["ROOT", "xcomp"], "LEMMA": {"NOT_IN": ["be"]}}}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "obj",
        "RIGHT_ATTRS": {"DEP": "ccomp"}
      },
    ],
  ]
  dep_matcher.add("nominal_object_clause", dep_patterns)
  matches = dep_matcher(doc)

  for _, (verb, obj) in matches:
    obj_span = " ".join([e.text for e in doc[obj].subtree])
    result.append(doc[verb].text)
    result.append(obj_span)

  return result
   
