def search_out(doc, nlp):
  """Search for personal pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """


  _result = [t for t in doc if t.tag_ == "PRP"]
  result = [{"text": t.text} for t in _result]
  return result
   
