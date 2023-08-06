from linguappt import SpanishVocabPPT, EnglishVocabPPT
from linguappt import EnglishPhrasePPT, SpanishPhrasePPT, GermanPhrasePPT
from linguappt import EnglishStructureKGPPT, SpanishStructureKGPPT, GermanStructureKGPPT
from linguappt.lib import pptx2pdf, pdf2images 
from linguappt import __version__
import click
import json
import os
 
def _print_version(ctx, param, value):
  if not value or ctx.resilient_parsing:
      return
  click.echo(__version__)
  ctx.exit()
 
@click.command()
@click.option("--sourcecsv", prompt="source csv file path", help="Specify the source csv file path")
@click.option("--title", prompt="title of the pptx", help="Specify the title of the pptx")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--destpptx", default="test.pptx", prompt="destination pptx file", help="Specify the destination pptx file name")
def vocabppt(sourcecsv, title, lang, destpptx):
  _PPTS = {
    "en": EnglishVocabPPT,
    "es": SpanishVocabPPT
  }

  _PPT = _PPTS[lang]

  phase = {"step": 1, "msg": "Start ppt generation"}
  print(json.dumps(phase))

  vp = _PPT(sourcecsv, title)
  vp.convert_to_ppt(destpptx)

  phase = {"step": 2, "msg": "Finish ppt generation"}
  print(json.dumps(phase))


@click.command()
@click.option("--sourcecsv", prompt="source csv file path", help="Specify the source csv file path")
@click.option("--title", prompt="title of the pptx", help="Specify the title of the pptx")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--destpptx", default="test.pptx", prompt="destination pptx file", help="Specify the destination pptx file name")
def phraseppt(sourcecsv, title, lang, destpptx):
  _PPTS = {
    "en": EnglishPhrasePPT,
    "es": SpanishPhrasePPT,
    "de": GermanPhrasePPT
  }

  _PPT = _PPTS[lang]

  phase = {"step": 1, "msg": "Start ppt generation"}
  print(json.dumps(phase))

  vp = _PPT(sourcecsv, title)
  vp.convert_to_ppt(destpptx)

  phase = {"step": 2, "msg": "Finish ppt generation"}
  print(json.dumps(phase))

@click.command()
@click.option("--sourcejson", prompt="source json file path", help="Specify the source json file path")
@click.option("--title", prompt="title of the pptx", help="Specify the title of the pptx")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--destpptx", default="test.pptx", prompt="destination pptx file", help="Specify the destination pptx file name")
def structurekgppt(sourcejson, title, lang, destpptx):
  _PPTS = {
    "en": EnglishStructureKGPPT,
    "es": SpanishStructureKGPPT,
    "de": GermanStructureKGPPT
  }

  _PPT = _PPTS[lang]

  phase = {"step": 1, "msg": "Start ppt generation"}
  print(json.dumps(phase))

  vp = _PPT(sourcejson, title)
  vp.convert_to_ppt(destpptx)

  phase = {"step": 2, "msg": "Finish ppt generation"}
  print(json.dumps(phase))




@click.command()
@click.option("--sourcepptx", prompt="source pptx file path", help="Sepcify the source pptx file path")
@click.option("--destdir", prompt="dest pdf and pictures directory", help="Sepcify the pdf and picture destionation directory")
def pptx2pdf2images(sourcepptx, destdir):
  phase = {"step": 1, "msg": "Start pdf generation"}
  print(json.dumps(phase))

  pdf = pptx2pdf(sourcepptx, destdir)

  phase = {"step": 2, "msg": "Finish pdf generation"}
  print(json.dumps(phase))

  phase = {"step": 3, "msg": "Start images generation"}
  print(json.dumps(phase))

  images_len = pdf2images(pdf, destdir)
   
  phase = {"step": 4, "msg": "Finish images generation", "images_len": images_len}
  print(json.dumps(phase))


@click.command()
@click.option('--version', is_flag=True, callback=_print_version, expose_value=False, is_eager=True)
@click.option('--ptype', prompt="parser type[VOCAB | PHRASE | SKG]", help="Specify the parse type, VOCAB or PHRASE or SKG")
@click.option("--sourcemeta", prompt="source meta file path", help="Specify the source meta file path")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--name", default="test", prompt="output file name", help="Specify the file name")
@click.option("--pptxdir", prompt="dest pptx directory", help="Specify the pptx destination directory")
@click.option("--pdfdir", prompt="dest pdf directory", help="Sepcify the pdf destionation directory")
@click.option("--imgdir", prompt="dest image directory", help="Sepcify the preview image destionation directory")
def meta2media(ptype, sourcemeta, lang, name, pptxdir, pdfdir, imgdir):
  _PPTS = {
    "en_VOCAB": EnglishVocabPPT,
    "es_VOCAB": SpanishVocabPPT,
    "en_PHRASE": EnglishPhrasePPT,
    "es_PHRASE": SpanishPhrasePPT,
    "de_PHRASE": GermanPhrasePPT,
    "en_SKG": EnglishStructureKGPPT,
    "es_SKG": SpanishStructureKGPPT,
    "de_SKG": GermanStructureKGPPT,
  }

  _PPT = _PPTS[lang+"_"+ptype]
  phase = {"step": 1, "msg": "Start ppt generation"}
  print(json.dumps(phase), flush=True)

  if not os.path.isdir(pptxdir):
    os.mkdir(pptxdir) 

  vp = _PPT(sourcemeta, "歧舌AI备课助教")
  pptx = pptxdir + "/" + name +'.pptx'
  vp.convert_to_ppt(pptx)

  phase = {"step": 2, "msg": "Finish ppt generation, start pdf generation"}
  print(json.dumps(phase), flush=True)

  if not os.path.isdir(pdfdir):
    os.mkdir(pdfdir) 

  pdf = pptx2pdf(pptx, pdfdir)

  phase = {"step": 3, "msg": "Finish pdf generation, start images generation"}
  print(json.dumps(phase), flush=True)

  images_len = pdf2images(pdf, imgdir, 0, 6)
   
  phase = {"step": 4, "msg": "Finish images generation", "images_len": images_len}
  print(json.dumps(phase), flush=True)

