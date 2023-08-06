def search_out(doc, nlp):
  """Search for intransitive verbs

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []
  black_children_deps = ["dobj", "nsubjpass", "ccomp"]
  black_deps = ["acl"]
  verbs = [t for t in doc if t.pos_=="VERB" and t.dep_ not in black_deps]
  for t in verbs:
    deps = [c.dep_ for c in t.children]
    if len(set(deps).intersection(black_children_deps))==0:
      result.append({"text": t.text})
  return result
   
