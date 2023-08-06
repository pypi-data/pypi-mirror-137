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
        "RIGHT_ID": "root",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "ROOT"},
      },
      {
        "LEFT_ID": "root",
        "REL_OP": ">",
        "RIGHT_ID": "subject_verb",
        "RIGHT_ATTRS": {"POS": {"IN": ["VERB", "AUX"]}, "DEP": "csubj"}
      },
      {
        "LEFT_ID": "subject_verb",
        "REL_OP": ">",
        "RIGHT_ID": "subj",
        "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}, "TAG": {"IN": ["WDT", "WP", "WP$", "WRB"]}}
      },
    ],
  ]
  dep_matcher.add("nominal_subject_clause", dep_patterns)
  matches = dep_matcher(doc)

  for _, (root, verb, _) in matches:
    subj_span = " ".join([e.text for e in doc[verb].subtree])
    object_span = doc[root+1:].text
    result.append({"subject": subj_span, "predicate": doc[root], "object": object_span})

  return result
   
