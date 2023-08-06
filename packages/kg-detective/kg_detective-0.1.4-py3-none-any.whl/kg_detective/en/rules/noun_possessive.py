from spacy.matcher import Matcher, DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for possessive nouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  # pattern: someone's
  token_matcher = Matcher(nlp.vocab)
  patterns = [
    [{"POS": "DET"}, {"POS": "ADV", "OP": "*"}, {"POS": "ADJ", "OP": "*"}, {"POS": "NOUN"}, {"TAG": "POS", "POS": "PART"}],
    [{"TAG": "PRP$"}, {"POS": "ADV", "OP": "*"}, {"POS": "ADJ", "OP": "*"}, {"POS": "NOUN"}, {"TAG": "POS", "POS": "PART"}],
    [{"POS": "NUM"}, {"POS": "NOUN"}, {"TAG": "POS", "POS": "PART"}],
    [{"POS": "PROPN"}, {"POS": "PART", "TAG": "POS"}],
    [{"POS": "PROPN"}, {"LOWER": "and"}, {"POS": "PROPN"}, {"POS": "PART", "TAG": "POS"}],
  ]
  token_matcher.add("noun_prime", patterns)

  matches = token_matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  # pattern: of someone / of someone's
  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "of",
        "RIGHT_ATTRS": {"ORTH": "of"}
      },
      {
        "LEFT_ID": "of",
        "REL_OP": ">",
        "RIGHT_ID": "of_possess",
        "RIGHT_ATTRS": {"DEP": "pobj", "TAG": "PRP"}
      },
    ],
    [
      {
        "RIGHT_ID": "of",
        "RIGHT_ATTRS": {"ORTH": "of"}
      },
      {
        "LEFT_ID": "of",
        "REL_OP": ">",
        "RIGHT_ID": "of_possess",
        "RIGHT_ATTRS": {"DEP": "pobj", "POS": "NOUN"}
      },
      {
        "LEFT_ID": "of_possess",
        "REL_OP": ".",
        "RIGHT_ID": "part",
        "RIGHT_ATTRS": {"POS": "PART", "TAG": "POS"}
      },
    ],
  ]
  dep_matcher.add("noun_of", dep_patterns)
  matches = dep_matcher(doc)
  dep_ranges = [(token_ids[0], token_ids[-1]+1) for _, token_ids in matches]

  # merge ranges
  refined_matches = merge(token_ranges+dep_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})
  return result
   
