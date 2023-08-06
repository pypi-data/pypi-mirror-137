# TEXTA MLP Python package

https://pypi.org/project/texta-mlp/

## Installation
### Requirements
`apt-get install python3-lxml`

##### From PyPI
`pip3 install texta-mlp`

##### From Git
`pip3 install git+https://git.texta.ee/texta/texta-mlp-python.git`

### Testing
`python3 -m pytest -v tests`

## Entities
MLP extracts several types of entities from text.

### Model-based Entities
MLP uses Stanza to extract:
* Persons (missing Estonian model)
* Organizations (missing Estonian model)
* Geopolitical entities (missing Estonian model)

### Regex-based Entities
MLP uses regular expressions to extract:
* Phone numbers (regex)
* Email addresses (regex)

### List-based Entitites
MLP also supports entity extraction using lists of predefined entities. These lists come with MLP:
* Companies (Estonian)
* Addresses (Estonian and Russian)
* Currencies (Estonian, Russian, and English)

### Custom List-based Entities
MLP also supports defining custom entity lists. Custom lists must be placed in the **entity_mapper** directory residing in **data** directory.
Entities are defined as JSON files:
```
{
  "MY_ENTITY": [
    "foo",
    "bar"
  ]
}
```

## Usage

### Load MLP
Supported languages: https://stanzanlp.github.io/stanzanlp/models.html
```
>>> from texta_mlp.mlp import MLP
>>> mlp = MLP(language_codes=["et","en","ru"])
```

### Process & Lemmatize Estonian
```
>>> mlp.process("Selle eestikeelse lausega võiks midagi ehk öelda.")
{'text': {'text': 'Selle eestikeelse lausega võiks midagi ehk öelda .', 'lang': 'et', 'lemmas': 'see eestikeelne lause võima miski ehk ütlema .', 'pos_tags': 'P A S V P J V Z'}, 'texta_facts': []}
>>>
>>> mlp.lemmatize("Selle eestikeelse lausega võiks midagi ehk öelda.")
'see eestikeelne lause võima miski ehk ütlema .'
```

You can use the "analyzers" argument to limit the amount of data you want to be analyzed and returned, thus speeding up the process.
Accepted options are: ["lemmas", "pos_tags", "transliteration", "ner", "contacts", "entity_mapper", "all"]
where "all" signifies that you want to use all analyzers (takes the most time). By the default, this value is "all".

```
>>> mlp.process("Selle eestikeelse lausega võiks midagi ehk öelda.", analyzers=["lemmas", "postags"])
```

### Process & Lemmatize Russian
```
>>> mlp.process("Лукашенко заявил о договоренности Москвы и Минска по нефти.")
{'text': {'text': 'Лукашенко заявил о договоренности Москвы и Минска по нефти .', 'lang': 'ru', 'lemmas': 'лукашенко заявить о договоренность москва и минск по нефть .', 'pos_tags': 'X X X X X X X X X X', 'transliteration': 'Lukašenko zajavil o dogovorennosti Moskvõ i Minska po nefti .'}, 'texta_facts': []}
>>>
>>> mlp.lemmatize("Лукашенко заявил о договоренности Москвы и Минска по нефти.")
'лукашенко заявить о договоренность москва и минск по нефть .
```

### Process & Lemmatize English
```
>>> mlp.process("Test sencences are rather difficult to come up with.")
{'text': {'text': 'Test sencences are rather difficult to come up with .', 'lang': 'en', 'lemmas': 'Test sencence be rather difficult to come up with .', 'pos_tags': 'NN NNS VBP RB JJ TO VB RB IN .'}, 'texta_facts': []}
>>>
>>> mlp.lemmatize("Test sencences are rather difficult to come up with.")
'Test sencence be rather difficult to come up with .'
```

### Make MLP Throw an Exception on Unknown Languages
By default, MLP will default to Estonian if language is unknown. To not do so, one must provide *use_default_language_code=False* when initializing MLP.
```
>>> mlp.process("المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.")
{'text': {'text': 'المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق . وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء .', 'lang': 'et', 'lemmas': 'lee 1 يولد جميع الناس leele leele في leele leele . وقد وهبوا عقلاً leele lee أن يعامل بعضهم بعضًا بروح lee .', 'pos_tags': 'S N S S S S S S S S Z S S S S S S S S Y Y Y Z'}, 'texta_facts': []}
>>>
>>> mlp = MLP(language_codes=["et","en","ru"], use_default_language_code=False)
>>> mlp.process("المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/rsirel/dev/texta-mlp-package/texta_mlp/mlp.py", line 150, in process
    document = self.generate_document(raw_text, loaded_analyzers)
  File "/home/rsirel/dev/texta-mlp-package/texta_mlp/mlp.py", line 96, in generate_document
    lang = self.detect_language(processed_text)
  File "/home/rsirel/dev/texta-mlp-package/texta_mlp/mlp.py", line 89, in detect_language
    raise LanguageNotSupported("Detected language is not supported: {}.".format(lang))
texta_mlp.exceptions.LanguageNotSupported: Detected language is not supported: ar.
```

### Change Default Language Code
Do use some other language as default, one must provide *default_language_code* when initializing MLP.
```
>>> mlp = MLP(language_codes=["et", "en", "ru"], default_language_code="en")
>>>
>>> mlp.process("المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.")
{'text': {'text': 'المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق . وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء .', 'lang': 'en', 'lemmas': 'المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق . وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء .', 'pos_tags': 'NN CD , NN NN NN NN IN NN NN . UH NN NN NN NN NN NN NN NN NN NN .'}, 'texta_facts': []}
```

### Process Arabic (for real this time)
```
>>> mlp = MLP(language_codes=["et","en","ru", "ar"])
>>> mlp.process("المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.")
{'text': {'text': 'المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق . وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضا بروح الإخاء .', 'lang': 'ar', 'lemmas': 'مَادَّة 1 وَلَّد جَمِيع إِنسَان حَرَر مُتَسَاوِي فِي كَرَامَة والحقوق . وَقَد وَ عَقَل وضميراً وعليهم أَنَّ يعامل بعضهم بَعض بروح إِخَاء .', 'pos_tags': 'N------S1D Q--------- VIIA-3MS-- N------S4R N------P2D N------P4I A-----MP4I P--------- N------S2D U--------- G--------- U--------- VP-A-3MP-- N------S4I A-----MS4I U--------- C--------- VISA-3MS-- U--------- N------S4I U--------- N------S2D G---------', 'transliteration': "AlmAdp 1 ywld jmyE AlnAs >HrArFA mtsAwyn fy AlkrAmp wAlHqwq . wqd whbwA EqlAF wDmyrFA wElyhm >n yEAml bEDhm bEDA brwH Al<xA' ."}, 'texta_facts': []}
>>>
>>> mlp.lemmatize("المادة 1 يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضا بروح الإخاء.")
'مَادَّة 1 وَلَّد جَمِيع إِنسَان حَرَر مُتَسَاوِي فِي كَرَامَة والحقوق . وَقَد وَ عَقَل وضميراً وعليهم أَنَّ يعامل بعضهم بَعض بروح إِخَاء .'
```

### Load MLP with Custom Resource Path
```
>>> mlp = MLP(language_codes=["et","en","ru"], resource_dir="/home/kalevipoeg/mlp_resources/")
```

### Different phone parsers

Texta MLP has three different phone parsers:

* 'phone_strict' - is used by default. It parses only those numbers that are verified by the [phonenumbers library](https://pypi.org/project/phonenumbers/). It verifies all correct numbers if they have an area code before it. Otherwise (without an area code) it verifies only Estonian ("EE") and Russian ("RU") phone numbers. This is because in this example "Maksekorraldusele märkida viitenumber 2800049900 ning selgitus ...", the "2800049900" is a valid number in Great Britain ("GB"), but not with "EE" or "RU".

* 'phone_high_precision' which output is mainly phonenumbers extracted by regex, but the regex excludes complicated versions. 

* 'phone_high_recall' was originally done for emails and it gets most of the phone numbers (includes complicated versions), but also outputs a lot of noisy data. This **parser is also used by default** in concatenating close entities (read below). This means that while concatenating, only "PHONE_high_recall" fact is considered and other parsers' results are not included in concatenating (avoids overlaping). The other parsers' results won't get lost and are still added in texta_facts. Just not under the fact "BOUNDED".

You can choose the parsers like so:
```
>>> mlp.process(analyzers=["lemmas", "phone_high_precision"], raw_text= "My phone number is 12 34 56 77.")
```
