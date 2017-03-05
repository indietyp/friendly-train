import json
import yaml
import re


class LanguageGenerator3000:
  def __init__(self):
    pass

  # def create(self, rules):
  #   pass

  def word(self, rules, target):
    return {'type': 'subject', 'word': 'oggle'}

  def wordlist(self, rules):
    return [{'type': 'subject', 'word': 'oggle'}, {'type': 'verb', 'word': 'uggle'}]

  def sentence(self, words, *args, **kwargs):
    return {'sentence': 'oggle wobble ding dong!', 'value': 7}

  def sentencelist(self, words, *args, **kwargs):
    return ['oggle gobble dingdong', 'oggle wobble dongdong', 'oggle diggle dunggung']

  def convert(self, raw):
    for k, rule in raw['rules'].items():
      converted = []

      for item in rule:
        item = re.findall(r'(.*) ?(\(\d*\.\d*\))?', item)
        item = list(item[0])
        new = {}
        new['probablity'] = -1 if item[1] == '' else float(item[1])
        new['letters'] = item[0]

        converted.append(new)

      raw[k] = converted
    converted = raw
    return converted

  def default(self, filepath="./config.yaml", sample_size=500):
    filetype = filepath.split('.')[-1]
    file = open(filepath, 'r').read()

    if type(file) == bytes:
      file = file.decode()

    if filetype == 'yaml':
      rules = yaml.load(file)
    elif filetype == 'json':
      rules = json.loads(file)

    print(rules)
    self.create(rules)


if __name__ == '__main__':
  LanguageGenerator3000().generate()
