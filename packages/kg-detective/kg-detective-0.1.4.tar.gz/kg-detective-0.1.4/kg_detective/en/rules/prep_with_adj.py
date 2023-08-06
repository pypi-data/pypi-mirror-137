from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions with adj 

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
        "RIGHT_ID": "aux",
        "RIGHT_ATTRS": {"POS": {"IN": ["AUX", "VERB"]}, "LEMMA": "be"}
      },
      {
        "LEFT_ID": "aux",
        "REL_OP": ">",
        "RIGHT_ID": "adj",
        "RIGHT_ATTRS": {"DEP": "acomp", "POS": {"IN": ["ADJ", "VERB"]}}
      },
      {
        "LEFT_ID": "adj",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "prep", "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("prep_with_adj", dep_patterns)
  matches = dep_matcher(doc)

  for _, (aux, adj, prep) in matches:
    span_text = " ".join([doc[i].text for i in [aux, adj, prep]])
    result.append({"text": span_text})

  return result
   
