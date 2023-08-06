def search_out(doc, nlp):
  """Search for adjective with -ed as its ending

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """
  _result = [t for t in doc if t.pos_=="ADJ" and t.tag_=="JJ" and len(t.text)>3 and t.text[-2:]=="ed"]
  
  result = [{"text": t.text} for t in _result]
  return result
   
