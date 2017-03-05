import json
import yaml
import os
import re
import uuid
import string
import random
from copy import deepcopy


class LanguageGenerator3000:
  def __init__(self):
    pass

  def generate_single_sentence(self, *args, **kwargs):
    return {'sentence': 'oggle gobble dingdong!',
            'raw': {
                'text': [
                    {'type': 'subject', 'word': 'oggle'},
                    {'type': 'subject', 'word': 'gobble'},
                    {'type': 'object', 'word': 'dingdong'},
                ],
                'punctuation': '!'
            }
            }

  def generate_sentence_list(self, sample_size=3, *args, **kwargs):
    return [{'sentence': 'oggle gobble dingdong!',
            'raw': {
                'text': [
                    {'type': 'subject', 'word': 'oggle'},
                    {'type': 'subject', 'word': 'gobble'},
                    {'type': 'object', 'word': 'dingdong'},
                ],
                'punctuation': '!'
            }
    },
    ]

  def generate_single_word(self, word_type):
    rules = deepcopy(self.rules)

    if isinstance(rules['words'][word_type], dict) and 'extends' in rules['words'][word_type]:
      rules['words'][word_type]['extends']['rules'] = self.__vowel_consonant_replacer(rules['words'][word_type]['extends']['rules'], self.vowels, self.consonants)
      for key, items in rules['words'][word_type]['extends'].items():
        if key == rules:
          items.keys()

        rules[key].update(items)

    limit = rules['char limit']
    vconfig = rules['vowels']
    vowels = deepcopy(self.vowels)

    length = random.randint(limit['min'], limit['max'])
    vlimit = random.randint(vconfig['min'], vconfig['max'])

    word = ''
    letters = ''
    vlength = 0

    while len(word) <= length:
      apply_rule = False
      applied_rule = []
      if letters in rules['rules'].keys():
        apply_rule = True
        applied_rule = [rules['rules'][letters]]

      else:
        for letter in list(letters):
          if letter in rules['rules']:
            apply_rule = True
            applied_rule.append(rules['rules'][letter])

      if not apply_rule:
        if len(vowels) > 0:
          stuff = [self.consonants, vowels]
        letters = random.choice(random.choice(stuff))
      else:
        letters = ''
        print(applied_rule[0])
        applied_rule = applied_rule[0]

        selector = ''
        no_probablity = []
        used = 0
        for pointer in range(0, len(applied_rule)):
          if applied_rule[pointer]['probablity'] == -1:
            no_probablity.append(pointer)

          used += applied_rule[pointer]['probablity']
          selector += str(pointer) * int(applied_rule[pointer]['probablity'] * 100)

        if used < 1:
          for pointer in no_probablity:
            selector += '{}'.format(pointer) * int(((1 - used) / len(no_probablity)) * 100)

        selected = int(random.choice(selector))

        for letter in applied_rule[selected]['letters']:
          if letter == 'CONSONANT' or (letter == 'VOWEL' and vowels == 0):
            letter = list(self.consonants)
          elif letter == 'VOWEL':
            letter = list(vowels)

          letters += random.choice(letter)

      if vlength <= vlimit:
        vlength = len(re.findall(r'([^{}])'.format(','.join(list(set(vowels)))), ''.join(letters))[1:-1])
        vlimit += vlength

        if vlength >= vlimit:
          vowels = ''

      word += letters

    return {'type': word_type, 'word': word}

  def generate_word_list(self, sample_size=50, sort=False):
    rules = deepcopy(self.rules)

    if os.path.isfile('wordlist.json'):
      with open('wordlist.json', 'r') as out:
        wordlist = json.loads(out.read())
        if sort:
          wordlist = sorted(wordlist, key=lambda x: x['word'])
        self.wordlist = wordlist
        return wordlist

    else:
      wordlist = []
      no_limit = []
      generated = 0

      for key, item in rules['words'].items():
        if isinstance(item, dict) and 'limit' in item:
          generated += item['limit']
          for _ in range(item['limit']):
            wordlist.append(self.generate_single_word(key))
        else:
          no_limit.append(key)

      if generated < sample_size:
        for key in no_limit:
          for _ in range(int((sample_size - generated) / len(no_limit))):
            wordlist.append(self.generate_single_word(key))

      with open('wordlist.json', 'w') as out:
        out.write(json.dumps(wordlist))

      if sort:
        wordlist = sorted(wordlist, key=lambda x: x['word'])

      self.wordlist = wordlist
      return wordlist

  def wordcount(self):
    return len(self.generate_word_list())

  def get_word_str(self, word):
    return word['word']

  def get_correlated_word_str(self, word, word_type):
    if isinstance(word, str):
      wordstr = word
    else:
      wordstr = word['word']
    correlated_words_dict = self.__weights[word_type][wordstr]
    random_number = random.random()
    for correlated_word in correlated_words_dict:
      random_number -= correlated_words_dict[correlated_word]
      if random_number <= 0:
        return correlated_word

  def generate_probabilities(self, randomness=0.2):
    # generate giant sentence list
    sentence_basis = self.generate_sentence_list(count=(1 / randomness) * self.wordcount(), weighted=False)
    occurances_by_word_type = {}
    # count occurances
    for single_sentence in sentence_basis:
      for single_word in single_sentence['raw']['text']:
        word_type = single_word['type']
        if word_type not in occurances_by_word_type:
          occurances_by_word_type[word_type] = {}
        if self.get_word_str(single_word) not in occurances_by_word_type[word_type]:
          occurances_by_word_type[word_type][self.get_word_str(single_word)] = {}

        for correlated_word in single_sentence['raw']['text']:
          if self.get_word_str(correlated_word) not in occurances_by_word_type[word_type][self.get_word_str(single_word)]:
            occurances_by_word_type[word_type][self.get_word_str(single_word)][self.get_word_str(correlated_word)] = {}
          if self.get_word_str(correlated_word) not in occurances_by_word_type[word_type][self.get_word_str(single_word)][self.get_word_str(correlated_word)]:
            occurances_by_word_type[word_type][self.get_word_str(single_word)][self.get_word_str(correlated_word)] = 0

          occurances_by_word_type[word_type][self.get_word_str(single_word)][self.get_word_str(correlated_word)] += 1

    # build word list by word type
    all_words_by_type = {}

    # add randomness
    for word_type in occurances_by_word_type:
      all_words_by_type[word_type] = []
      for single_word in occurances_by_word_type[word_type]:
        sum_of_occurances = 0
        all_words_by_type[word_type].append(single_word)

        for correlated_word in occurances_by_word_type[word_type][single_word]:
          sum_of_occurances += occurances_by_word_type[word_type][single_word][correlated_word]
        # calculate default
        occurances_of_randomness_total = sum_of_occurances * randomness
        occurances_of_randomness_per_word = occurances_of_randomness_total / self.wordcount()
        # add default
        for correlated_word in occurances_by_word_type[word_type][single_word]:
          occurances_by_word_type[word_type][single_word][correlated_word] += occurances_of_randomness_per_word

    # zipfify
    # 1. randomize order
    all_weights_by_type = {}
    all_weights_by_word = {}
    for word_type in all_words_by_type:
      random.shuffle(all_words_by_type[word_type])
      all_weights_by_type[word_type] = {}
      index = 1
      # 2. generate weights
      for single_word in all_words_by_type[word_type]:
        index += 1
        all_weights_by_type[word_type][single_word] = index / (index - 1)
        all_weights_by_word[single_word] = all_weights_by_type[word_type][single_word]

    # 3. zipfify occurances
    for word_type in occurances_by_word_type:
      for single_word in occurances_by_word_type[word_type]:
        for correlated_word in occurances_by_word_type[word_type][single_word]:
          occurances_by_word_type[word_type][single_word][correlated_word] *= all_weights_by_word[correlated_word]

    # normalize (sum of probabilities to 1)
    for word_type in occurances_by_word_type:
      for single_word in occurances_by_word_type[word_type]:
        sum_of_occurances = 0
        # 1. count occurances
        for correlated_word in occurances_by_word_type[word_type][single_word]:
          sum_of_occurances += occurances_by_word_type[word_type][single_word][correlated_word]
        # 2. normalize
        for correlated_word in occurances_by_word_type[word_type][single_word]:
          occurances_by_word_type[word_type][single_word][correlated_word] /= sum_of_occurances

    # save result
    self.__weights = occurances_by_word_type

  def convert(self, raw):
    converted = self.__convert(raw)
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

    self.consonants = consonant
    self.vowels = vowels
    self.rules = converted

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

  def get_weights(self):
    return self.__weights

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
    print(self.generate_word_list(500, sort=True))
    self.generate_probabilities()

    print('Generating probabilities...')


if __name__ == '__main__':
  LanguageGenerator3000().generate()
