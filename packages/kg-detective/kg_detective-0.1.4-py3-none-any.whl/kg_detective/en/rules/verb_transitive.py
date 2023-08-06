from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for transitive verbs   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)

  verb_phrase = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "dobj",
      "RIGHT_ATTRS": {"DEP": {"IN": ["dobj", "nsubjpass"]}}
    },
  ]

  dep_patterns = [verb_phrase]
  dep_matcher.add("verb_transitive", dep_patterns)
  matches = dep_matcher(doc)

  for _, (verb, obj) in matches:
    span_text = doc[verb].text + " " + " ".join([e.text for e in doc[obj].subtree])
    result.append({"text": span_text})

  return result
   
