from spacy.matcher import Matcher, PhraseMatcher, DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for phrases with coordinating conjunctions 

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
        "RIGHT_ID": "conj",
        "RIGHT_ATTRS": {"POS": "CCONJ", "DEP": "cc"}
      },
      {
        "LEFT_ID": "conj",
        "REL_OP": "<",
        "RIGHT_ID": "A",
        "RIGHT_ATTRS": {}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "B",
        "RIGHT_ATTRS": {"DEP": "conj"}
      }
    ],
  ]

  dep_matcher.add("conj_coodinating", dep_patterns)
  matches = dep_matcher(doc)

  for _, (conj, A, B) in matches:
    A_children = [cs.i for cs in doc[A].rights if cs.dep_!="conj" and cs.dep_!="cc" and cs.pos_!="PUNCT"] + [cs.i for cs in doc[A].lefts if cs.dep_=="preconj"]
    B_children = [cs.i for cs in doc[B].rights]

    A_children.append(A)
    B_children.append(B)
    #print(A_children)
    #print(B_children)
    A_tree = doc[min(A_children):max(A_children)+1]
    B_tree = doc[min(B_children):max(B_children)+1]
    span_text = A_tree.text + " " + doc[conj].text + " " +B_tree.text
    result.append({"text": span_text})

  return result
   
