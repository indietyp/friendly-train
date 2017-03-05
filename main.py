import json
import yaml
import re


class LanguageGenerator3000:
  def __init__(self):
    pass

  # def create(self, rules):
  #   pass

  def word(self, rules):
    pass

  def wordlist(self, rules):
    pass

  def sentence(self, words, *args, **kwargs):
    pass

  def sentencelist(self, words, *args, **kwargs):
    pass

  def convert(self, raw):
    for k, rule in raw['rules'].items():
      converted = []

      for item in rule:
        item = re.findall(r'(.*) (\(\d*\.\d*\))', item)
        new = {}
        new['probablity'] = item[]
        converted.append()

      raw[k] = converted

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
