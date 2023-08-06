
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![PyPI](https://img.shields.io/pypi/v/Caribe) [![Transformer](https://img.shields.io/badge/Transformer-T5-blue.svg)](https://huggingface.co/docs/transformers/model_doc/t5) [![Pandas](https://img.shields.io/badge/Pandas-1.3.4-green.svg)](https://pandas.pydata.org/) [![AI](https://img.shields.io/badge/AI-Artifical_Intelligence-blue.svg)]() [![happytransformers](https://img.shields.io/badge/happytransformers-2.4.0-blue.svg)](https://happytransformer.com/) [![Python 3+](https://img.shields.io/badge/python-3+-blue.svg)]() [![NLP](https://img.shields.io/badge/nlp-natural_language_processing-blue.svg)]() [![T5-KES](https://img.shields.io/badge/T5-T5_KES-red.svg)](https://huggingface.co/KES/T5-KES)
# Caribe 


>This python library takes trinidadian dialect and converts it to standard english.
Future updates would include the conversion of other caribbean dialects to standard english and additional natural language processing methods.

____
## Installation
Use the below command to install package/library
```
pip install Caribe 

```
____
 ## Usage
 > Sample 1: Checks the dialect input against existing known phrases before decoding the sentence into a more standardized version of English language. A corrector is used to check and fix small grammatical errors.
```python
# Sample 1
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "Ah wah mi modda phone"
standard = cb.phrase_decode(sentence)
standard = cb.trinidad_decode(standard)
fixed = cb.caribe_corrector(standard)
print(fixed) #Output: I want my mother phone

```
>Sample 2: Checks the dialect input against existing known phrases
```python
# Sample 2 
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "Waz de scene"
standard = cb.phrase_decode(sentence)

print(standard) # Outputs: How are you

```
>Sample 3: Checks the sentence for any grammatical errors or incomplete words and corrects it.
```python
#Sample 3
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "I am playin fotball outsde"
standard = cb.caribe_corrector(sentence)

print(standard) # Outputs: I am playing football outside

```
>Sample 4: Makes parts of speech tagging on dialect words.
```python
#Sample 4
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "wat iz de time there"
analyse = cb.nlp()
output = analyse.caribe_pos(sentence)

print(output) # Outputs: ["('wat', 'PRON')", "('iz', 'VERB')", "('de', 'DET')", "('time', 'NOUN')", "('there', 'ADV')"]

```
>Sample 5: Remove punctuation marks.
```python
#Sample 5
import Caribe as cb
from Caribe import trinidad_decode, trinidad_decode_split, caribe_corrector

sentence = "My aunt, Shelly is a lawyer!"
analyse = cb.remove_signs(sentence)


print(analyse) # Outputs: My aunt Shelly is a lawyer

```

>Sample 6: Sentence Correction using T5-KES.
```python
#Sample 6 Using t5_kes_corrector
import Caribe as cb


sentence = "Wat you doin for d the christmas"
correction = cb.t5_kes_corrector(sentence)


print(correction) # Output: What are you doing for christmas?

```
>Sample 7: Sentence Correction using Decoder and T5-KES.
```python
#Sample 7 Using t5_kes_corrector and decoder
import Caribe as cb


sentence = "Ah want ah phone for d christmas"
decoded= cb.trinidad_decode(sentence)
correction = cb.t5_kes_corrector(decoded)


print(correction) # Output: I want a phone for christmas.

```

---
- ## Additional Information
    - `trinidad_decode()` : Decodes the sentence as a whole string.
    - `trinidad_decode_split()`: Decodes the sentence word by word.
    - `phrase_decode()`: Decodes the sentence against known dialect phrases.
    - `caribe_corrector()`: Corrects grammatical errors in a sentence using gingerit.
    - `t5_kes_corrector()`: Corrects grammatical errors in a sentence using a trained NLP model.
    - `trinidad_encode()`: Encodes a sentence to trinidadian dialect.
    - `caribe_pos()`: Generates parts of speech tagging on dialect.
    - `pos_report()`: Generates parts of speech tagging on english words.
    - `remove_signs()`: Takes any sentence and remove inefficient punctuation marks. 

---
- ## File Encodings on NLP datasets
Caribe introduces file encoding (Beta) in version 0.1.0. This allows a dataset or any supported filetype to be creolised in trinidad dialect.

- ### Usage of File Encodings:
```python
import Caribe as cb

convert = cb.file_encode("test.txt", "text")
# Generates a translated text file
convert = cb.file_encode("test.json", "json")
# Generates a translated json file
convert = cb.file_encode("test.csv", "csv")
# Generates a translated csv file

```
---
## Dictionary Data
The encoder and decoder utilises a dictionary data structure. The data for the dictionary was gathered from web-scapping social media sites among other websites and using Lise Winer Dictionary of the English Creole of Trinidad and Tobago among other scholarly resources.

---
## Transformer Models
State of the art NLP grammar correction T5-KES model was trained on a modified version of the JFLEG dataset and is currently being tested against existing models and benchmarks. The T5-KES model may be used as both of a grammar corrector and a parser for Trinidad dialect via training using custom datasets in a future update. 

---
## T5_KES_Corrector vs Caribe Corrector(Ginger Grammar Corrector)
Initial Tests were carried out with performance factors to measure the accuracy of the correction and the degree of sentence distortion from the correct sentence. Initial tests showed that the T5 corrector performed better in terms of accuracy with a lower sentence distortion.

---
- ## Contact 
For any concerns, issues with this library or want to become a collaborator to this project.

Email: keston.smith@my.uwi.edu 
___