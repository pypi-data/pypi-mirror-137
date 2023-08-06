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
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ">",
        "RIGHT_ID": "clause",
        "RIGHT_ATTRS": {"DEP": "relcl"}
      },
    ],
  ]
  dep_matcher.add("relative_restrictive_clause", dep_patterns)
  matches = dep_matcher(doc)

  for _, (noun, clause) in matches:
    clause_ordered_tree = [e.i for e in doc[clause].subtree]
    clause_ordered_tree.sort()
    clause_span = " ".join([doc[i].text for i in clause_ordered_tree])
    result.append(doc[noun].text)
    result.append(clause_span)

  return result
   
