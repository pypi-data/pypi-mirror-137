from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for verbs with present progressive tense 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)
  be_verb_ing = [
    {
      "RIGHT_ID": "core_verb",
      "RIGHT_ATTRS": {"POS": "VERB", "TAG": "VBG"}
    },
    {
      "LEFT_ID": "core_verb",
      "REL_OP": ">",
      "RIGHT_ID": "aux",
      "RIGHT_ATTRS": {"DEP": "aux", "POS": "AUX", "lemma": "be", "TAG": {"IN": ["VB", "VBP", "VBZ"]}}
    }
  ]

  dep_patterns = [be_verb_ing]
  dep_matcher.add("verb_present_progressive_tense", dep_patterns)
  matches = dep_matcher(doc)
  dep_ranges = [(token_ids[-1], token_ids[0]+1) for _, token_ids in matches]

  # merge ranges
  refined_matches = merge(dep_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    result.append({"text": span.text})

  return result
   
