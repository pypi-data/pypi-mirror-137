from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions of time 

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
        "RIGHT_ATTRS": {"POS": "ADP", "LOWER": {"IN": ["in", "on", "between", "at", "for", "since"]}}
      },
      {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "time_obj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["pobj"]}, "POS": {"IN": ["NOUN", "PROPN", "NUM"]}}
      },
    ],
  ]
  dep_matcher.add("prep_time", dep_patterns)
  matches = dep_matcher(doc)

  for _, (prep, time_obj) in matches:
    if any([t.like_num or t.pos_=="NUM" for t in doc[time_obj].subtree]):
      span_text = doc[prep].text + " " + " ".join([t.text for t in doc[time_obj].subtree])
      result.append({"text": span_text})

  return result
   
