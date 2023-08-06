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
        "RIGHT_ID": "A",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT"}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "conj",
        "RIGHT_ATTRS": {"DEP": "cc"}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "B",
        "RIGHT_ATTRS": {"DEP": "conj"}
      },
    ],
  ]
  dep_matcher.add("compound", dep_patterns)
  matches = dep_matcher(doc)

  for _, (A, conj, B) in matches:
    is_valid = any([e.dep_=="nsubj" for e in doc[B].children])
    if is_valid:
      A_subtrees = [t.subtree for t in doc[A].children if t.dep_ not in ["cc", "conj"]]
      A_range = sum([[e.i for e in st] for st in A_subtrees], [])
      A_range.append(A)

      A_span = doc[min(A_range):max(A_range)+1].text
      B_span = " ".join([e.text for e in doc[B].subtree])
      conj_span = doc[conj].text
      result.append({"sen A": A_span, "conj": conj_span, "sen B": B_span})

  return result
   
