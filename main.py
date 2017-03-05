import json
import yaml
import re
import string
import random
from copy import deepcopy


class LanguageGenerator3000:
  def __init__(self):
    pass

  def generate_single_word(self, rules, target):
    return {'type': 'subject', 'word': 'oggle'}

  def generate_word_list(self, rules):
    return [{'type': 'subject', 'word': 'oggle'}, {'type': 'verb', 'word': 'uggle'}]

  def generate_single_sentence(self, words, *args, **kwargs):
    return {'sentence': 'oggle wobble ding dong!', 'value': 7}

  def generate_sentence_list(self, words, *args, **kwargs):
    return [{'sentence': 'oggle gobble dingdong!', 'raw': {'text': 'oggle gobble dingdong', 'punctuation': '!'}},
            {'sentence': 'oggle wobble dongdong?', 'raw': {'text': 'oggle wobble dongdong', 'punctuation': '?'}},
            {'sentence': 'oggle diggle dunggung.', 'raw': {'text': 'oggle diggle dunggung', 'punctuation': '.'}}]

  def convert(self, raw):
    converted = self.__convert(raw)
    # print(converted)
    # TODO: rules change keys
    # TODO: alphbet conversion vowel, consonant

    end_vowels = ''
    end_consonant = ''

    used = 0
    no_probablity = []
    for charlist in converted['vowels']['charlist']:
      if 'INHERIT' in charlist['letters']:
          # if alphabet['probablity'] != -1:
          #   no_probablity.append(alphabet[])

        for alphabet in converted['alphabet']:
          vowels = ''
          if string.ascii_lowercase in ''.join(alphabet['letters']):
            vowels = 'aeiou'
          else:
            length = len(alphabet['letters']) / 10

            vowels = ''
            for i in range(int(length)):
              vowels += random.choice(alphabet['letters'])

            vowels = ''.join(set(vowels))

          consonant = re.findall(r'([^{}])'.format(','.join(list(vowels))), ''.join(alphabet['letters']))
          consonant = ''.join(consonant)

          if alphabet['probablity'] == -1:
            no_probablity.append(vowels)
          else:
            used += alphabet['probablity']
            end_vowels += vowels * int(alphabet['probablity'] * 100)
            end_consonant += consonant * int(alphabet['probablity'] * 100)

      else:
        end_vowels += ''.join(charlist['letters'] * int(charlist['probablity'] * 100))
        used += charlist['probablity']

    if used < 1 and used > 0:
      for vowels in no_probablity:
        end_vowels += vowels * int(((1 - used) / len(no_probablity)) * 100)
        end_consonant += consonant * int(alphabet['probablity'] * 100)

    vowels = end_vowels
    consonant = end_consonant

    if consonant == '':
      letters = []
      no_probablity = []
      used = 0
      for alphabet in converted['alphabet']:
        print(alphabet)
        if alphabet['probablity'] == -1:
          no_probablity.append(alphabet['letters'])
        else:
          used += alphabet['probablity']
          letters += alphabet['letters'] * int(alphabet['probablity'] * 100)

      if used < 1:
        for tmp in no_probablity:
          vowels += ''.join(tmp * int(((1 - used) / len(no_probablity)) * 100))

      consonant = re.findall(r'([^{}])'.format(','.join(list(set(vowels)))), ''.join(letters))
      consonant = ''.join(consonant)

    converted['rules'] = self.__vowel_consonant_replacer(converted['rules'], list(set(vowels)), list(set(consonant)))

    self.consonant = consonant
    self.vowels = vowels

    return converted, consonant, vowels

  def __vowel_consonant_replacer(self, values, vowels, consonants):
    cont = False

    converted = deepcopy(values)
    for k, rule in values.items():
      old = deepcopy(k)

      count = k.count('VOWEL')
      if count > 0:
        if count > 1:
          cont = True

        for vowel in vowels:
          converted[k.replace('VOWEL', vowel, 1)] = rule

        del converted[old]

      count = k.count('CONSONANT')
      if count > 0:
        if count > 2:
          cont = True

        for consonant in consonants:
          converted[k.replace('CONSONANT', consonant, 1)] = rule

        del converted[old]

    if cont:
      return self.__vowel_consonant_replacer(converted, vowels, consonants)
    else:
      return converted

  def __convert(self, raw):
    for k, rule in raw.items():
      if isinstance(rule, dict):
        raw[k] = self.__convert(rule)
      elif isinstance(rule, str) or isinstance(rule, list):
        converted = []

        if isinstance(rule, str):
          rule = [rule]

        for item in rule:
          if not isinstance(item, str):
            continue

          search = re.findall(r'(.*) (\(\d*\.\d*\))?', item)
          if len(search) < 1:
            search = [[item]]

          item = list(search[0])
          new = {}
          new['probablity'] = -1 if len(item) < 2 else float(item[1][1:-1])
          if item[0] in ['GERMAN', 'ENGLISH', 'LATIN']:
            mode = item[0]
            item[0] = string.ascii_lowercase

            if mode == 'GERMAN':
              item[0] += 'öäü'

          item[0] = re.split(r'(VOWEL|CONSONANT|INHERIT)', item[0])
          pointer = 0
          tmp = []
          for pointer in range(len(item[0])):
            if item[0][pointer] not in ['VOWEL', 'CONSONANT', 'INHERIT']:
              item[0][pointer] = list(item[0][pointer])
            else:
              item[0][pointer] = [item[0][pointer]]

            tmp.extend(item[0][pointer])
          item[0] = tmp

          # item
          new['letters'] = item[0]

          converted.append(new)

        raw[k] = converted
    converted = raw
    return converted

  def generate(self, filepath="./config.yaml", sample_size=500):
    print('started')
    filetype = filepath.split('.')[-1]
    file = open(filepath, 'r').read()

    if type(file) == bytes:
      file = file.decode()

    if filetype == 'yaml':
      rules = yaml.load(file)
    elif filetype == 'json':
      rules = json.loads(file)

    converted, _, _ = self.convert(rules)


if __name__ == '__main__':
  LanguageGenerator3000().generate()
