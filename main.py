import json
import yaml
import re
import random


class LanguageGenerator3000:
  def __init__(self):
    pass

  # def create(self, rules):
  #   pass

  def word(self, rules, target):
    return {'type': 'subject', 'word': 'oggle'}

  def wordlist(self, rules=''):
    return [{'type': 'subject', 'word': 'oggle'}, {'type': 'verb', 'word': 'uggle'}]

  def wordcount(self):
    return len(self.wordlist())

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
    sentence_basis = self.sentencelist(count=(1 / randomness) * self.wordcount())
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

  def sentence(self, *args, **kwargs):
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

  def sentencelist(self, count=3, *args, **kwargs):
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

  def generate(self):
    print('Generate executed.')
    self.generate_probabilities()


if __name__ == '__main__':
  LanguageGenerator3000().generate()
