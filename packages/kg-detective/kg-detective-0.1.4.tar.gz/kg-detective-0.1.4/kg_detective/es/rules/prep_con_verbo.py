from spacy.matcher import Matcher, PhraseMatcher, DependencyMatcher
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
        "RIGHT_ATTRS": {"POS": "VERB"}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "x",
        "RIGHT_ATTRS": {"DEP": "xcomp", "POS": "VERB"}
      },
      {
        "LEFT_ID": "x",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "mark", "POS": "ADP"}
      },
    ],
    [
      {
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "x",
        "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "PRON"]}, "DEP": "obj"}
      },
      {
        "LEFT_ID": "x",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "case", "POS": "ADP"}
      },
    ],
    [
      {
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
      },
      {
        "LEFT_ID": "verb",
        "REL_OP": ">",
        "RIGHT_ID": "x",
        "RIGHT_ATTRS": {"POS": {"IN": ["PROPN"]}, "DEP": "obl"}
      },
      {
        "LEFT_ID": "x",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "case", "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("prep_con_verb", dep_patterns)
  matches = dep_matcher(doc)

  for _, (verb, x, prep) in matches:
    if prep == verb + 1:
      verb_aux = [c.i for c in doc[verb].lefts if c.dep_ in ["aux", "iobj", "obj"]]
      verb_aux.append(verb)
      if max(verb_aux)-min(verb_aux) == len(verb_aux)-1:
        verb_span = doc[min(verb_aux):max(verb_aux)+1]
        span_text = verb_span.text + " " + doc[prep].text 
        result.append({"text": span_text})


  return result
   
