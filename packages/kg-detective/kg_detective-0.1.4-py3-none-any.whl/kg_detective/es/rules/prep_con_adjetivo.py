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
        "RIGHT_ID": "adj",
        "RIGHT_ATTRS": {"POS": "ADJ"}
      },
      {
        "LEFT_ID": "adj",
        "REL_OP": ">",
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"DEP": "nmod", "POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "prep",
        "RIGHT_ATTRS": {"DEP": "case", "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("prep_con_adj", dep_patterns)
  matches = dep_matcher(doc)

  for _, (adj, noun, prep) in matches:
    if prep == adj + 1:
      noun_tree = " ".join([e.text for e in doc[noun].subtree])
      span_text = doc[adj].text + " " + noun_tree 
      result.append({"text": span_text})


  return result
   
