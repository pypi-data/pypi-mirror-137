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
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "num",
        "RIGHT_ATTRS": {"DEP": "nummod", "POS": "NUM"}
      },
    ],
  ]
  dep_matcher.add("num_cardinales", dep_patterns)
  matches = dep_matcher(doc)

  for _, (noun, num) in matches:
    num_tree = [e.i for e in doc[num].subtree]
    if num_tree[-1] + 1 == noun:
      num_tree.append(noun)
      span_text = " ".join([doc[i].text for i in num_tree]) 
      result.append({"text": span_text})


  return result
   
