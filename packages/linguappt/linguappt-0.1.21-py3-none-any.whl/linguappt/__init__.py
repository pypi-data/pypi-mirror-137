"""``linguappt`` Package

This module demostrates the usage of package `linguappt`.

.. topic:: Installation

  .. code:: shell

    $ pip3 install linguappt

.. topic:: Use as executable

  .. code:: shell

    $ lingua_vocabppt --sourcecsv [vocab csv file] --lang [language] --title [title shown in ppt] --destpptx [pptx file]

    $ lingua_phraseppt --sourcecsv [phrase csv file] --lang [language] --title [title shown in ppt] --destpptx [pptx file]

    $ lingua_pptx2pdf --sourcepptx [pptx file] --destdir [dest directory storing pdf and images]

.. topic:: Convert csv file containing vocabulary informatin into pptx file 

  .. code:: python

    from linguappt import SpanishVocabPPT, EnglishVocabPPT

    def vocabppt(sourcecsv, title, lang, destpptx):
      _PPTS = {
        "en": EnglishVocabPPT,
        "es": SpanishVocabPPT
      }

      _PPT = _PPTS[lang]

      vp = _PPT(sourcecsv, title)
      vp.convert_to_ppt(destpptx)

.. topic:: Convert csv file containing vocabulary informatin into pptx file 

  .. code:: python

    from linguappt import EnglishPhrasePPT, SpanishPhrasePPT

    def phraseppt(sourcecsv, title, lang, destpptx):
      _PPTS = {
        "en": EnglishPhrasePPT,
        "es": SpanishPhrasePPT
      }

      _PPT = _PPTS[lang]

      vp = _PPT(sourcecsv, title)
      vp.convert_to_ppt(destpptx)

"""

__version__ = '0.1.21'


from .es.vocab_summary import SpanishVocabPPT
from .en.vocab_summary import EnglishVocabPPT

from .en.phrase_summary import EnglishPhrasePPT
from .es.phrase_summary import SpanishPhrasePPT
from .de.phrase_summary import GermanPhrasePPT

from .en.structure_kg_summary import EnglishStructureKGPPT
from .es.structure_kg_summary import SpanishStructureKGPPT
from .de.structure_kg_summary import GermanStructureKGPPT
