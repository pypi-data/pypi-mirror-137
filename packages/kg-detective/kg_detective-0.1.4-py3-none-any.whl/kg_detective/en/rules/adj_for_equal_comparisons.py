from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for adjective for equal comparisons 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  # pattern: as ... as ...
  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "A",
        "RIGHT_ATTRS": {"POS": "ADJ"}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "left_as",
        "RIGHT_ATTRS": {"DEP": "advmod", "LOWER": {"IN": ["as", "so"]}}
      },
      {
        "LEFT_ID": "A",
        "REL_OP": ">",
        "RIGHT_ID": "right_as",
        "RIGHT_ATTRS": {"DEP": "prep", "LOWER": "as"}
      },
      {
        "LEFT_ID": "right_as",
        "REL_OP": ">",
        "RIGHT_ID": "B",
        "RIGHT_ATTRS": {"DEP": "pobj"}
      },
    ],
    [
      {
        "RIGHT_ID": "same",
        "RIGHT_ATTRS": {"LOWER": "same"}
      },
      {
        "LEFT_ID": "same",
        "REL_OP": ";",
        "RIGHT_ID": "the",
        "RIGHT_ATTRS": {"LOWER": "the"}
      },
      {
        "LEFT_ID": "same",
        "REL_OP": ">",
        "RIGHT_ID": "right_as",
        "RIGHT_ATTRS": {"DEP": "prep", "LOWER": "as"}
      },
      {
        "LEFT_ID": "right_as",
        "REL_OP": ">",
        "RIGHT_ID": "B",
        "RIGHT_ATTRS": {"DEP": "pobj"}
      },
    ],
    [
      {
        "RIGHT_ID": "adj",
        "RIGHT_ATTRS": {"POS": "ADJ", "DEP": "amod"}
      },
      {
        "LEFT_ID": "adj",
        "REL_OP": ">",
        "RIGHT_ID": "left_as",
        "RIGHT_ATTRS": {"DEP": "advmod", "LOWER": "as"}
      },
      {
        "LEFT_ID": "adj",
        "REL_OP": "<",
        "RIGHT_ID": "noun",
        "RIGHT_ATTRS": {"POS": "NOUN"}
      },
      {
        "LEFT_ID": "noun",
        "REL_OP": ".",
        "RIGHT_ID": "right_as",
        "RIGHT_ATTRS": {"LOWER": "as", "POS": "ADP"}
      },
    ],
  ]
  dep_matcher.add("adj_equal_comprison", dep_patterns)
  matches = dep_matcher(doc)
  dep_ranges = [(token_ids[1], token_ids[-1]+1) for _, token_ids in matches]

  # merge ranges
  refined_matches = merge(dep_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})

  return result
   
