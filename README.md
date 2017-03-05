# friendly-train
friendly-train is a project to generate an artificial language from a bunch of rules.

Using a network of probabilities between words, full texts can be generated.

The name has been provided by github. Thanks, github!

# Rule Definition
//todo
see the example yaml file

# API

## Get The Config Dictionary
All functions are initialized with the config-dictionary. This dictionary can be generated from a file and a string:

```python
config_dic_by_file ( file_name ) 
```
`file_name` is a string to a file name and can be a `.json` or a `.yaml` file.

```python
config_dic_by_str ( config_str ) 
```
`config_str` is a string in the json or yaml format.

Both functions return a config dictionary for further use.

## Generate Words, Sentences

### Generate Words

```python
generate_single_word ( config_dic, word_type )
```
`word_type` being string containing a word type according to the given config dictionary (config file).  
This function returns a string that is a word of the given word type.

```python
generate_word_list ( config_dic, word_type, count )
```
`word_type` being string containing a word type according to the given config dictionary (config file).  
`count` being an integer containing the length of the word list.  
This function returns a list of strings that are words of the given word type.

### Generate Sentences

```python
generate_single_sentence ( config_dic )
```
This function returns a string that is a sentence.

```python
generate_sentence_list ( config_dic, count )
```
`count` being an integer containing the length of the sentence list.  
This function returns a list of strings that are sentences.

## Generate Sentences About A Certain Topic
In the language, groups of word make up topics. For example, `programming` and `python` are words of the same topic. A cointaining the word `programming` therefore would contain the word `python` with a higher likelyhood than a random text.


```python
generate_single_topic_sentence ( config_dic, topic )
```
`topic` being a string that is a valid word according to the given config.  
This function returns a string that is a sentence about a certain topic.

```python
generate_topic_sentence_list ( config_dic, topic, count )
```
`topic` being a string that is a valid word according to the given config.  
`count` being an integer containing the length of the sentence list.  
This function returns a list of strings that are sentences about the given word.

# Grammar
Grammar is not currently supported.