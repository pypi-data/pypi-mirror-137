from linguappt.vocab_ppt import VocabPPT
from linguappt.es.vocab_meta import SpanishVocabMeta
import os
import json

class SpanishVocabPPT(VocabPPT):
  """Create Vocabulary PPT for Spanish study

  Attributes:
    content (list of dict): read from csv file
    word_distrubtion (dict): key is PoS, e.g, ``noun``, ``verb``, ``daj``, value is list of vocabularies
  """

  _template_dir = os.path.dirname(__file__)
  _templates = {
    "classic": os.path.join(_template_dir, 'templates/vocab_spanish_classic.pptx'),
  }
  lang = 'es'

  content_keys = ['word', 'meaning', 'dict_pos', 'from', 'extension', 'variations', 'examples']

  _metainfo = SpanishVocabMeta

  ALLOWED_POSES = ['noun', 'adj', 'verb']

  def __init__(self, sourcefile, title="", genre="classic"):
    super().__init__(sourcefile, title, genre)

  def _create_noun_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Noun with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    pos = v["dict_pos"]

    pos_holder = holders[10]
    pos_holder.text_frame.text = pos 
    noun, meaning = holders[11], holders[12]
    noun.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]
    meaning.text_frame.text = "\n".join(ms) 


    s_def = holders[13]
    s_undef = holders[15]
    pl_def = holders[17]
    pl_undef = holders[19]

    arts = self.__class__._metainfo.article_variation[pos]

    s_def.text_frame.text = arts[0] 
    s_undef.text_frame.text = arts[1]
    pl_def.text_frame.text = arts[2]
    pl_undef.text_frame.text = arts[3]

    extension = json.loads(v["extension"])
    if "pl." in pos:
      s, pl = extension[arts[4]], v["word"]
    else:
      s, pl = v["word"], extension[arts[4]]     

    holders[14].text_frame.text = s
    holders[16].text_frame.text = s
    holders[18].text_frame.text = pl 
    holders[20].text_frame.text = pl 

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_noun(self, v):
    if v["extension"] != "":
      self._create_noun_with_extension_A(v)
    else:
      self._create_default_word(v)

  def _create_adj_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Adj with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    pos_holder = holders[10]
    adj, meaning = holders[11], holders[12]
    adj.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    s_m, s_f, pl_m, pl_f = holders[13], holders[14], holders[15], holders[16]

    extension = json.loads(v["extension"])

    s_m.text_frame.text = extension["m"]
    s_f.text_frame.text = extension["f"]
    pl_m.text_frame.text = extension["mpl"]
    pl_f.text_frame.text = extension["fpl"]

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_adj(self, v):
    if v["extension"] != "":
      self._create_adj_with_extension_A(v)
    else:
      self._create_default_word(v)

  def _create_verb_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Verb with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
    
    variations = json.loads(v["variations"])

    pos_holder = holders[10]
    pos_holder.text_frame.text = v["dict_pos"]

    original, word, meaning = holders[11], holders[12], holders[13]
    original.text_frame.text = variations["original"]
    word.text_frame.text = v["word"]

    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    sign = variations["formats"][0]
    tense = sign["tense"]
    person = sign["person"]

    extension = json.loads(v["extension"])[tense]

    holders[14].text_frame.text = extension["yo"] if extension["yo"] != "" else " "
    holders[15].text_frame.text = extension["tú"]
    holders[16].text_frame.text = extension["él/ella/Usted"]
    holders[17].text_frame.text = extension["nosotros"]
    holders[18].text_frame.text = extension["vosotros"]
    holders[19].text_frame.text = extension["ellos/ellas/Ustedes"]

    holders[20].text_frame.text = self.__class__._metainfo.tense_info[tense]
    holders[21].text_frame.text = " ".join(["人称", person, "的变位"])

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]


  def _create_verb_with_extension_B(self, v):
    layout = self._prs.slide_layouts.get_by_name("Verb with extension B")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
    
    variations = json.loads(v["variations"])

    pos_holder = holders[10]
    pos_holder.text_frame.text = v["dict_pos"]

    original, word, meaning = holders[11], holders[12], holders[13]
    original.text_frame.text = variations["original"]
    word.text_frame.text = v["word"]

    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)
 
    formats = variations["formats"]
    holders[14].text_frame.text = "\n".join([self.__class__._metainfo.tense_info[f["tense"]] if "tense" in f.keys() else self.__class__._metainfo.tense_info[f["format"]] for f in formats])
    holders[15].text_frame.text = "\n".join([" ".join([f["person"], "的变位"]) if "person" in f.keys() else "" for f in formats])

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_verb_with_extension_C(self, v):
    layout = self._prs.slide_layouts.get_by_name("Verb with extension C")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
    
    variations = json.loads(v["variations"])

    pos_holder = holders[10]
    pos_holder.text_frame.text = v["dict_pos"]
    original, word, meaning = holders[11], holders[12], holders[13]
    original.text_frame.text = variations["original"]
    word.text_frame.text = v["word"]

    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)
 
    sign = variations["formats"][0]

    holders[14].text_frame.text = self.__class__._metainfo.tense_info[sign["format"]]

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_verb(self, v):
    if v["variations"] == "":
      self._create_default_word(v)
    else:
      variations = json.loads(v["variations"])
      if "formats" in variations.keys():
        formats = variations["formats"]
        if len(formats) > 1:
          self._create_verb_with_extension_B(v)
        elif "tense" in formats[0].keys():
          self._create_verb_with_extension_A(v)
        elif "format" in formats[0].keys():
          self._create_verb_with_extension_C(v)
        else:
          self._create_default_word(v)
      else:
        self._create_default_word(v)

