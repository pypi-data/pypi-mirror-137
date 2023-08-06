from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions with noun 

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
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "prep", "POS": "ADP"}
      },
      {
        "LEFT_ID": "prep",
        "REL_OP": ">",
        "RIGHT_ID": "prep_obj",
        "RIGHT_ATTRS": {"DEP": "pobj"}
      },
    ],
  ]
  dep_matcher.add("prep_with_noun", dep_patterns)
  matches = dep_matcher(doc)

  for _, (noun, _, _) in matches:
    noun_tree = " ".join([e.text for e in doc[noun].subtree])
    span_text = noun_tree
    result.append({"text": span_text})

  return result
   
