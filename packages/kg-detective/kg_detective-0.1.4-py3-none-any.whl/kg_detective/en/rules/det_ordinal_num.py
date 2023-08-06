def search_out(doc, nlp):
  _result = [t for t in doc if t.like_num and t.pos_=="ADJ"]
  result = [{"text": t.text} for t in _result]
  return result
   
