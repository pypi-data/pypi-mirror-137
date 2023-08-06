def search_out(doc, nlp):
  _result = [t for t in doc if t.pos_=="INTJ"]
  result = [{"text": t.text} for t in _result]
  return result
   
