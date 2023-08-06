def search_out(doc, nlp):
  IN_ARTS = ["a", "an"]
  _result = [t for t in doc if t.text.lower() in IN_ARTS]
  result = [{"text": t.text} for t in _result]
  return result
   
