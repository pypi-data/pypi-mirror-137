def search_out(doc, nlp):
  """Search for verbs with verb modal   

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed

  Returns:
    list: list of spacy.tokens.Span
  """

  result = []

  _result = [t for t in doc if t.tag_=="MD"]
  result = [{"text": t.text} for t in _result]
  return result
   
