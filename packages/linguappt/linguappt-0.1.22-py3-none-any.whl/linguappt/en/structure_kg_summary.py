from linguappt.structure_kg_ppt import StructureKGPPT
import os
import json

class EnglishStructureKGPPT(StructureKGPPT):
  """Create StructureKG PPT for English study

  Attributes:
    content (list of dict): read from csv file
  """

  _template_dir = os.path.dirname(__file__)
  _templates = {
    "classic": os.path.join(_template_dir, 'templates/structure_kg_english_classic.pptx'),
  }
  lang = 'en'

  content_keys = ["sentence", "structure", "structure_rep", "kg"]

  def __init__(self, sourcefile, title="", genre="classic"):
    super().__init__(sourcefile, title, genre)

  def _create_structure(self, line):
    sentence_obj = line["sentence"]
    structure_str = line["structure_rep"]
    structure_obj = line["structure"]

    layout = self._prs.slide_layouts.get_by_name("Structure")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
  
    original_holder, translated_holder, structure_holder = holders[10], holders[11], holders[12]
    original_holder.text_frame.text = sentence_obj["text"]
    translated_holder.text_frame.text = sentence_obj["meaning"]
    structure_holder.text_frame.text = structure_str

    struct_analysis = ["{}    {}".format(p["text"], p["meaning"]) for p in structure_obj if p["explanation"]]
    struct_analysis_str = "\n".join(struct_analysis)
    struct_analysis_holder = holders[13]
    struct_analysis_holder.text_frame.text = struct_analysis_str 

  def _create_kg(self, line):
    sentence_obj = line["sentence"]
    kg_obj = line["kg"]

    layout = self._prs.slide_layouts.get_by_name("Detail")
    slide = self._prs.slides.add_slide(layout)
    holders = slide.shapes.placeholders
  
    original_holder, translated_holder = holders[10], holders[11]
    original_holder.text_frame.text = sentence_obj["text"]
    translated_holder.text_frame.text = sentence_obj["meaning"]

    kg = []
    for key, value in kg_obj.items():
      for v in value:
        kg.append("{}    {}".format(key, v["text"]))
    kg_str = "\n".join(kg)
    kg_holder = holders[12]
    kg_holder.text_frame.text = kg_str 


  def _create_structure_kg(self):
    """Create sturecture and kg by sentence
    """
    for line in self.content:
      self._create_structure(line)
      self._create_kg(line)


