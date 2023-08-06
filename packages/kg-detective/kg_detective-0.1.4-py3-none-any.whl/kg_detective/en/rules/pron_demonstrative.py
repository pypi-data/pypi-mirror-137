def search_out(doc, nlp):
  """Search for demonstrative pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """


  _result = [t for t in doc if t.text.lower() in ["this", "that", "those", "these"]]
  result = [{"text": t.text} for t in _result]
  return result
   
