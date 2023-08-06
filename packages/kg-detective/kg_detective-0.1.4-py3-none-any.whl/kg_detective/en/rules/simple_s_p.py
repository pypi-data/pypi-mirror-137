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
        "RIGHT_ID": "P",
        "RIGHT_ATTRS": {"POS": "VERB", "DEP": "ROOT"}
      },
      {
        "LEFT_ID": "P",
        "REL_OP": ">",
        "RIGHT_ID": "S",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
      },
    ],
  ]
  dep_matcher.add("simple_s_p", dep_patterns)
  matches = dep_matcher(doc)

  for _, (P, S) in matches:
    black = ['dative', 'dobj', 'attr', 'ccomp', 'oprd']
    is_valid = all([c.dep_ not in black for c in doc[P].children])
    if is_valid:
      subj_span = " ".join([e.text for e in doc[S].subtree])
      predicate_range = [l.i for l in doc[P].lefts if l.dep_=="aux"]
      predicate_range.append(P)
      predicate_span = doc[min(predicate_range): max(predicate_range)+1].text
      result.append({"subject": subj_span, "predicte": predicate_span})


  return result
   
