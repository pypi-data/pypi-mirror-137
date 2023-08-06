from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for prepositions with verb 

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
        "RIGHT_ATTRS": {"POS": "VERB"}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": {"IN": ["prep", "prt"]}, "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("prep_with_verb", dep_patterns)
  matches = dep_matcher(doc)

  for _, (verb, prep) in matches:
    if prep > verb:
      verb_tree = [e.subtree for e in doc[verb].rights if e.pos_!="PUNCT" and e.dep_ not in ["dep", "cc", "conj"]]
      span_text = doc[verb].text + " " + " ".join([" ".join([e.text for e in st]) for st in verb_tree])
      result.append({"text": span_text})

  return result
   
