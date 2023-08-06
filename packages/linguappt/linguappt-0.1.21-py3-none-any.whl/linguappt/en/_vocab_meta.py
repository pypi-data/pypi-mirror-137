class _EnglishVocabMeta:

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
    'noun': ('名词', 'noun', ['n.']),
    'adj': ('形容词', 'adjective', ['adj.']),
    'verb': ('动词', 'verb', ['v.', 'vt.vi.', 'v.vi.', 'v.vt.', 'v.aux.', 'vi.vt.']),
    'adv': ('副词', 'adverb', ['adv.']),
    'pron': ('代词', 'pronoun', ['pron.']),
    'prep': ('前置词', '', ['prep.']),
    'other': ('其他', 'others', [])
  }

  format_info = {
    'original': "原型",
    'present_participle': "现在分词",
    'past_participle': "过去分词",
    'past_tense': "过去式",
    '3': "三单",
    'comparative': "比较级",
    'superlative': "最高级",
    'singular': "单数",
    'plural': "复数"
  }


