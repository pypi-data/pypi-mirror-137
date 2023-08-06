def search_out(doc, nlp):
  ARTS = ["the"]
  _result = [t for t in doc if t.text.lower() in ARTS]
  result = [{"text": t.text} for t in _result]
  return result
   
