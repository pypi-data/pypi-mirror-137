from linguappt.vocab_ppt import VocabPPT
from linguappt.en._vocab_meta import _EnglishVocabMeta
import os
import json

class EnglishVocabPPT(VocabPPT):
  """Create Vocabulary PPT for English study

  Attributes:
    content (list of dict): read from csv file
    word_distrubtion (dict): key is PoS, e.g, ``noun``, ``verb``, ``daj``, value is list of vocabularies
  """

  _template_dir = os.path.dirname(__file__)
  _templates = {
    "classic": os.path.join(_template_dir, 'templates/vocab_english_classic.pptx'),
  }
  lang = 'en'

  content_keys = ['word', 'meaning', 'dict_pos', 'from', 'extension', 'variations', 'examples']

  _metainfo = _EnglishVocabMeta

  ALLOWED_POSES = ['noun', 'adj', 'verb']

  def __init__(self, sourcefile, title="", genre="classic"):
    super().__init__(sourcefile, title, genre)

  def _create_noun_with_extension_B(self, v):
    layout = self._prs.slide_layouts.get_by_name("Noun with extension B")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, noun, meaning = holders[10], holders[11], holders[12]
    description = format_info["singular"]
    if v["variations"] != "":
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])

    pos.text_frame.text = " ".join([v["dict_pos"], description])
    noun.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]
    meaning.text_frame.text = "\n".join(ms) 

    extension = json.loads(v["extension"])
    single, plural = holders[13], holders[14]
    single.text_frame.text = extension["singular"]
    plural.text_frame.text = extension["plural"]

    examples = json.loads(v["examples"])
    if len(examples) == 2:
      original, translated = holders[15], holders[16]
      ex = examples[0]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]

      original, translated = holders[17], holders[18]
      ex = examples[1]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_noun_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Noun with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, noun, meaning = holders[10], holders[11], holders[12]
    description = format_info["singular"]
    if v["variations"] != "":
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])
    pos.text_frame.text = " ".join([v["dict_pos"], description])

    noun.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]
    meaning.text_frame.text = "\n".join(ms) 

    extension = json.loads(v["extension"])
    single, plural = holders[13], holders[14]
    single.text_frame.text = extension["singular"]
    plural.text_frame.text = extension["plural"]

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_noun(self, v):
    extension, variations, examples = v["extension"], v["variations"], v["examples"]
    if extension != "" and variations != "" and examples != "[]":
      self._create_noun_with_extension_B(v)
    elif extension != "" and examples == "[]":
      self._create_noun_with_extension_A(v)
    elif extension == "" and examples != "[]":
      self._create_default_word_with_examples(v)
    else:
      self._create_default_word(v)

  def _create_adj_with_extension_B(self, v):
    layout = self._prs.slide_layouts.get_by_name("Adj with extension B")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, adj, meaning = holders[10], holders[11], holders[12]
    description = ""
    if v["variations"] != "":
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])
    pos.text_frame.text = " ".join([v["dict_pos"], description])
    adj.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    much, more, most = holders[12], holders[13], holders[14]
    extension = json.loads(v["extension"])

    much.text_frame.text = extension['original'] 
    more.text_frame.text = extension['comparative']
    most.text_frame.text = extension['superlative']

    examples = json.loads(v["examples"])
    if len(examples) >= 1:
      original, translated = holders[15], holders[16]
      ex = examples[0]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]
    if len(examples) >= 2:
      original, translated = holders[17], holders[18]
      ex = examples[1]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]
 
    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]


  def _create_adj_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Adj with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, adj, meaning = holders[10], holders[11], holders[12]
    description = ""
    if v["variations"] != "":
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])
    pos.text_frame.text = " ".join([v["dict_pos"], description])
    adj.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    much, more, most = holders[13], holders[14], holders[15]
    extension = json.loads(v["extension"])

    much.text_frame.text = extension['original'] 
    more.text_frame.text = extension['comparative']
    most.text_frame.text = extension['superlative']

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]


  def _create_adj(self, v):
    extension, variations, examples = v["extension"], v["variations"], v["examples"]
    if extension != "" and variations != "" and examples != "[]":
      self._create_adj_with_extension_B(v)
    elif extension != "" and examples == "[]":
      self._create_adj_with_extension_A(v)
    elif extension == "" and examples != "[]":
      self._create_default_word_with_examples(v)
    else:
      self._create_default_word(v)

  def _create_verb_with_extension_B(self, v):
    layout = self._prs.slide_layouts.get_by_name("Verb with extension B")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, verb, meaning = holders[10], holders[11], holders[12]
    description = ""
    if v["variations"] != "":
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])
    pos.text_frame.text = " ".join([v["dict_pos"], description])
    verb.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    original, present_participle, past_tense, past_participle, third  = holders[13], holders[14], holders[15], holders[16], holders[17]
    extension = json.loads(v["extension"])

    original.text_frame.text = extension['original'] if 'original' in extension else " "
    past_tense.text_frame.text = extension['past_tense'] if 'past_tense' in extension else " "
    third.text_frame.text = extension['3'] if '3' in extension else " "
    present_participle.text_frame.text = extension['present_participle']  if 'present_participle' in extension else " "
    past_participle.text_frame.text = extension['past_participle'] if 'past_participle' in extension else " "

    examples = json.loads(v["examples"])
    if len(examples) >= 1:
      original, translated = holders[18], holders[19]
      ex = examples[0]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]
    if len(examples) >= 2:
      original, translated = holders[20], holders[21]
      ex = examples[1]
      original.text_frame.text = ex["original"]
      translated.text_frame.text = ex["translated"]
 
    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_verb_with_extension_A(self, v):
    layout = self._prs.slide_layouts.get_by_name("Verb with extension A")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders

    format_info = self.__class__._metainfo.format_info

    pos, verb, meaning = holders[10], holders[11], holders[12]
    description = ""
    if v["variations"]:
      variations = json.loads(v["variations"])
      description = " ".join([format_info[e] for e in variations["formats"]])
    pos.text_frame.text = " ".join([v["dict_pos"], description])
    verb.text_frame.text = v["word"]
    ms = v["meaning"].split(",")
    if len(ms) > 4:
      ms = ms[:4]

    meaning.text_frame.text = "\n".join(ms)

    original, past_tense, present_participle, past_participle, third = holders[13], holders[14], holders[15], holders[16], holders[17]
    extension = json.loads(v["extension"])

    original.text_frame.text = extension['original'] if 'original' in extension else " "
    past_tense.text_frame.text = extension['past_tense'] if 'past_tense' in extension else " "
    third.text_frame.text = extension['3'] if '3' in extension else " "
    present_participle.text_frame.text = extension['present_participle']  if 'present_participle' in extension else " "
    past_participle.text_frame.text = extension['past_participle'] if 'past_participle' in extension else " "

    note = slide.notes_slide
    note.notes_text_frame.text = v["word"]

  def _create_verb(self, v):
    extension, variations, examples = v["extension"], v["variations"], v["examples"]
    if extension != "" and variations != "" and examples != "[]":
      self._create_verb_with_extension_B(v)
    elif extension != "" and examples == "[]":
      self._create_verb_with_extension_A(v)
    elif extension == "" and examples != "[]":
      self._create_default_word_with_examples(v)
    else:
      self._create_default_word(v)


