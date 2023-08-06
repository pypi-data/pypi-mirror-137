class SpanishVocabMeta:
  @classmethod
  def get_pos(cls, dict_pos):
    _pos = 'other'
    for pos, des in cls.pos_info.items():
      if dict_pos in des[2]:
        _pos = pos
        break
    return _pos 
  
  @classmethod
  def get_pos_name(cls, pos):
    return cls.pos_info[pos][1]

  @classmethod
  def get_pos_cn_name(cls, pos):
    return cls.pos_info[pos][0]

  pos_info = {
    'noun': ('名词', 'el nombre', ['noun.', 'f.', 'm.', 'f.m.', 'propn,', 'f.pl.', 'm.pl.']),
    'adj': ('形容词', 'el adjectivo', ['adj.']),
    'verb': ('动词', 'el verbo', ['verb.', 'vr.', 'vi.', 'vt.', 'aux.']),
    'adv': ('副词', 'el adverbio', ['adv.']),
    'pron': ('代词', 'los pronombres', ['pron.']),
    'prep': ('前置词', '', ['prep.', 'adp.']),
    'other': ('其他', 'los otros', [])
  }

  tense_info = {
    'imperativo_afirmativo': "命令式-肯定",
    'imperativo_negativo': "命令式-否定",
    'indicativo-pretérito': "陈述式-过去时",
    'indicativo-presente': "陈述式-现在时",
    'subjuntivo-presente': "虚拟式-现在时",
    'indicativo-futuro': "陈述式-将来时",
    'subjuntivo-futuro': "虚拟式-将来时",
    'indicativo-imperfecto': "陈述式-未完成时",
    'subjuntivo-imperfecto': "虚拟式-未完成时",
    'indicativo-condicional': "条件式",
    'participio': "过去分词",
    'gerundio': "现在分词"
  }

  article_variation = {
    "m.": ["un", "el", "unos", "los", "mpl"],
    "m.pl.": ["un", "el", "unos", "los", "m"],
    "f.": ["una", "la", "unas", "las", "fpl"],
    "f.pl.": ["una", "la", "unas", "las", "f"],
  }
