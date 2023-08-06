def search_out(doc, nlp):
  """Search for relative pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """


  _result = [t for t in doc if t.tag_ in ["WP", "WP$", "WDT", "WRB"] and t.dep_ in ['nsubj', 'dobj']]
  result = [{"text": t.text} for t in _result]
  return result
   
