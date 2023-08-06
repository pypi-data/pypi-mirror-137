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
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT"}
      },
      {
        "LEFT_ID": "P",
        "REL_OP": ">",
        "RIGHT_ID": "S",
        "RIGHT_ATTRS": {"DEP": "nsubj"}
      },
      {
        "LEFT_ID": "P",
        "REL_OP": ">",
        "RIGHT_ID": "IO",
        "RIGHT_ATTRS": {"DEP": {"IN": ["dative"]}}
      },
      {
        "LEFT_ID": "P",
        "REL_OP": ">",
        "RIGHT_ID": "O",
        "RIGHT_ATTRS": {"DEP": {"IN": ["dobj"]}}
      },
    ],
  ]
  dep_matcher.add("simple_s_p_io_o", dep_patterns)
  matches = dep_matcher(doc)

  for _, (P, S, IO, O) in matches:
    black = ['attr', 'ccomp', 'oprd']
    is_valid = all([c.dep_ not in black for c in doc[P].children])
    if is_valid:
      subj_span = " ".join([e.text for e in doc[S].subtree])
      obj_span = " ".join([e.text for e in doc[O].subtree])
      iobj_span = " ".join([e.text for e in doc[IO].subtree])
      result.append({"subject": subj_span, "predicate": doc[P].text, "indirect object": iobj_span, "direct object": obj_span})

  return result
   
