import os
def search_out(doc, nlp):
  """Search for reflexive pronouns 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Token
  """

  pkg_path = os.path.dirname(__file__)
  REFLEXIVE = open(pkg_path + '/pron_reflexive.txt', 'r').read().splitlines() 


  _result = [t for t in doc if t.text.lower() in REFLEXIVE]
  result = [{"text": t.text} for t in _result]
  return result
   
