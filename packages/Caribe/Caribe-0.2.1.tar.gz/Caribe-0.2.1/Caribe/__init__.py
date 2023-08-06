# Author: Keston Smith
# Library: Caribe 
# Contact: keston.smith@my.uwi.edu
#Copyright: MIT 2021
from gingerit.gingerit import GingerIt
import re
import nltk
from nltk import *
import pandas as pd
from happytransformer import HappyTextToText, TTSettings



caribedict = {
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "My g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up",
  "O dawg":"What's up",
  "ah wah": "I want",
  "waz de scene": "How are you",
  "waz d scn":"How are you",
  "waz de scn":"How are you",
  "waz d scene":"How are you",
  "waz di scene":"How are you",
  "waz di scn":"How are you",
  "waiz d scn": "How are you",
  "waiz de scene": "How are you",
  "waiz d scene": "How are you",
  "waiz d scn":"How are you",
  "come nah boi": "I am being serious",
  "wais d scn": "How are you",
  "wais de scn":"How are you",
  "wais de scene": "How are you",
  "wais d scene": "How are you",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "wais":"what is",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "presha": "pressure",
  "ahse": "ass",
  "wajang":"roudy",
  "tief":"thief",
  "hush": "quiet",
  "wat":"what",
  "oi": "Hello",
   "d" : "the",
  "whey":"where",
  "whey yuh say": "can you repeat?",
  "you an all":  "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "wifey":"wife",
  "dey":"there",
  "Yo": "Hi",
  "Yoo": "Hi",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
   "waiz" : "what is",
   "moda":"mother",
   "modda" : "mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  "Ah" : "I",
  "doh": "do not",
  "eh" : "not",
  "cah": "cannot",
  "fuh":"for",
  "dat": "that",
  "waz": "what is",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "scene":"weather",
  "rel": "very",
  "mi": "my",
  "ah": "I",
  "yh":"yes",
  "dias":"that is",
  "waiz":"what",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "Oooo": "Hi",
  "Oo":"Hi",
  "cud":"could",
  "g":"friend",
  "dat": "that",
  "dawg":"friend",
  "iz":"is",
  "weh":"where",
  "y":"why",
  "shud":"should",
  "shudda": "should of",
  "cudda": "could of",
  "cuda": "could of",
  "boi":"boy",
  "bai":"boy",
  "aye":"hey",
  "nah":"no",
  "wais":"what is",
  "waiz":"what is",
  "orhor":"alright",
  "wen":"when",
  "di": "the",
  "alyuh":"everyone",
  "gyal":"girl",
  "bout":"about",
  "mins":"minutes",
  "hrs":"hours",
  "hr":"hour",
  "dem":"them",
  "gud":"good",
  "yunno":"you know",
  "tho":"though",
  "Ik":"I know",
  "ik":"I know",
  "doh":"don't",
  "doe":"don't",
  "gosh":"god",
  "hardlucks":"sorry",
  "daz":"that is",
  "issa":"is a",
  "jusso":"just so",
  "ite":"alright",
  "aite":"alright",
  "rn":"right now",
  "smallie":"girl",
  "lova":"lover",
  "later":"laterz",
  "buh":"but",
  "lawd":"lord",
  "gawd":"god",
  "fren":"friend",
  "oh gosh":"oh my god",
  "lol":"haha",
  "Idk":"I don't know",
  "n":"and",
  "prolly":"probably",
  "tryna":"try to",
  "sis":"sister",
  "sista":"sister",
  "sistas":"sisters",
  "cuz":"cause",
  "inno":"you know",
  "enno":"you know",
  "da":"that",
  "inna": "in a",
  "sen":"send",
  "cyah":"can't",
  "bcuz":"because",
  "bcus":"because",
  "cus":"cause",
  "cuz":"cause",
  "baigan":"eggplant",
  "manicou":"opossum",
  "hoss":"friend",
  "weys":"wow",
  "bess":"sexy",
  "ah lime": "a get together",
  "ey":"hey",
  "di":"the",
  "wam":"what happen",


}
splitdict = {
  "waz":"what is",
  "dawg": "friend",
  "topdawg": "friend",
  "d":"the",
  "y":"why",
  "Tabanca": "still holding feelings",
  "allyuh":"Everybody",
  "chupid": "stupid",
  "dotish": "stupid",
  "chupidee": "stupid",
  "fone":"phone",
  "tick":"thick",
  "crapo": "Frog",
  "trinbago": "Trinidad and Tobago",
  "dias":"that is",
  "lix" : "beating",
  "ent": "Is that not so?",
  "fed up": "tired",
  "preshah": "pressure",
  "presha": "pressure",
  "ahse": "ass",
  "wajang":"roudy",
  "tief":"thief",
  "oi": "Hello",
   "d" : "the",
  "hush": "quiet",
  "whey":"where",
  "boldface": "ignorant",
  "bolface": "ignorant",
  "bacchanal":"confusion", 
  "liming": "hanging out",
  "hambug":"pester",
  "ting":"thing",
  "tanty":"aunty",
  "tantie":"aunty",
  "gyul": "girl",
  "gyal": "girl",
  "horn":"cheat",
  "Yo": "Hi",
  "Yoo": "Hi",
  "iz":"is",
  "Yooo": "Hi",
  "dis":"this",
  "wah": "want",
  "meh": "me",
  "waiz" : "what is",
  "wais": "what is",
  "modda" : "mother",
  "fadda" : "father",
  "fada" : "father",
  "faddah": "father",
  "brodda": "brother",
  "broda": "brother",
  "dougla": "mixed race person",
  "backchat":"talks",
  "boi" : "boy",
  "yuh": "you",
  "tho":"though",
  "dey" : "there",
  "Ah" : "I",
  "doh": "do not",
  "eh" : "not",
  "cah": "cannot",
  "fuh":"for",
  "dat": "that",
  "waz": "what is",
  "dah": "that",
  "nah": "no",
  "de": "the",
  "scene":"weather",
  "rel": "very",
  "waiz":"what is",
  "mi": "my",
  "ah": "I",
  "Eyyy":"Hey",
  "Eyy":"Hey",
  "Ey": "Hey",
  "Yo":"Hi",
  "Yoo": "Hi",
  "g":"friend",
  "iz":"is",
  "Oooo": "Hi",
  "cud":"could",
  "wais":"what is",
  "dat": "that",
  "meh":"my",
  "cud":"could",
  "weh":"where",
  "y":"why",
  "wat":"what",
  "wa":"what",
  "wen":"when",
  "di": "the",
  "shud":"should",
  "cudda": "could of",
  "cuda": "could of",
  "boi":"boy",
  "bai":"boy",
  "aye":"hey",
  "nah":"no",
  "wais":"what is",
  "waiz":"what is",
  "orhor":"alright",
  "alyuh":"everyone",
  "gyal":"girl",
  "bout":"about",
  "mins":"minutes",
  "hrs":"hours",
  "hr":"hour",
  "dem":"them",
  "gud":"good",
  "yunno":"you know",
  "tho":"though",
  "Ik":"I know",
  "ik":"I know",
  "doh":"don't",
  "doe":"don't",
  "gosh":"god",
  "hardlucks":"sorry",
  "daz":"that is",
  "issa":"is a",
  "jusso":"just so",
  "ite":"alright",
  "aite":"alright",
  "rn":"right now",
  "smallie":"girl",
  "lova":"lover",
  "later":"laterz",
  "buh":"but",
  "lawd":"lord",
  "gawd":"god",
  "fren":"friend",
  "oh gosh":"oh my god",
  "lol":"haha",
  "Idk":"I don't know",
  "n":"and",
  "prolly":"probably",
  "tryna":"try to",
  "sis":"sister",
  "sista":"sister",
  "sistas":"sisters",
  "cuz":"cause",
  "inno":"you know",
  "enno":"you know",
  "da":"that",
  "inna": "in a",
  "sen":"send",
  "cyah":"can't",
  "bcuz":"because",
  "bcus":"because",
  "cus":"cause",
  "cuz":"cause",
  "baigan":"eggplant",
  "manicou":"opossum",
  "hoss":"friend",
  "weys":"wow",
  "bess":"sexy",
  "ah lime": "a get together",
  "ey":"hey",
  "di":"the",
  "wam":"what happen",
  
  
  

}


phrasedict = {
  "whey yuh say": "can you repeat?",
  "you an all":  "You too?",
  "you so": "people like you",
  "yuh makin joke":  "you can't be serious",
  "yuh look fuh dat": "it is your fault",
  "ah wah": "I want",
  "waz de scene": "How are you",
  "come nah boi": "I am being serious",
  "Father lawd": "Jesus help me", 
  "Skinnin yuh teet":"grinning",
  "Skinnin yuh teeth":"grinning",
  "Tabanca": "still holding feelings",
  "Wah foolishness is this" : "that was foolish",
  "Know how long meen see you" : "I have not seen you in a long time",
  "Oo monsta" : "What's up",
  "Eyyy, look who" : "long time no see friend" ,
  "My g":"my friend",
  "Wais d word dawg":"what's up bro",
  "wam dawg": "how are you?",
  "everyting cool" : "how is everything",
  "wais d order": "What's up",
  "wais d order": "What's up",  
  "ah wah": "I want",
  "waz de scene": "How are you",
  "waz d scn":"How are you",
  "waz de scn":"How are you",
  "waiz d scn": "How are you",
  "waiz de scene": "How are you",
  "waiz d scene": "How are you",
  "come nah boi": "I am being serious",
  "wais d scn": "How are you",
  "wais de scene": "How are you",
  "wais d scene": "How are you"

}



class Parser:
    texts:str
    def __init__(self, sentence:str):
        self.sentence = sentence
        self.sentence = nltk.pos_tag(nltk.word_tokenize(self.sentence), lang="eng")
        
    def pos_report(self):
        return(self.sentence)

class nlp:
    def __init__(self):
        pass
    def caribe_pos(self, text:str):
     
        x = []
        full =[]
        
        status:int = 0
        
        for word in text.split():
            for items in splitdict:
                if word not in x:
                    if re.findall(r'\b%s\b' %word, items):
                        holder=nltk.pos_tag(caribe_word_tokenize(splitdict[items]), lang="eng")  
                        s1 ="".join(map(str, holder))
                        s1= s1.replace(splitdict[items], word)
                        x.append(eval(s1))
                        holder.clear()
                        break
                    
                    elif splitdict.get(word) is None:
                        holder=nltk.pos_tag(caribe_word_tokenize(word), lang="eng")  
                        s1 ="".join(map(str, holder))
                        x.append(eval(s1))
                        holder.clear()
                        break
                        
        return x 

class dict_generate:
    _dialect = []
    _standard = []

    def __init__(self):
        for words in splitdict:
            xar = words
            yar = splitdict[words]
            if xar not in self._dialect:
                self._dialect.append(xar)

            self._standard.append(yar)
        

    def generate_dictionary(self):
        df = pd.DataFrame({'Dialects':self._dialect,'Standard':self._standard})
        df.to_csv("Dictionary.csv", index=False, encoding='utf-8')

class file_encode:
    _data = []
    _out = []
    def __init__(self, filename:str, encode_filetype:str):
        self.filename = filename
        self.filetype = encode_filetype
        __mode = "r+"
        self.file = open(self.filename, __mode, encoding='utf-8') 

        for _ in self.file:
            self._data.append(_)
        for __ in self._data:
            encode = trinidad_encode(__)
            self._out.append(encode)
        self.file.close()
    
        if (self.filetype == "text" or self.filetype == "txt"):
            if (self.filename.endswith(".txt")):
                self.output = open("Translated.txt", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
            else:
                raise TypeError("filename type  and encode filetype mismatch")

        elif (self.filetype == "json"):
            if (self.filename.endswith(".json")):
                self.output = open("Translated.json", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
            else:
                raise TypeError("filename type  and encode filetype mismatch")

        elif(self.filetype == "csv"): 
            if (self.filename.endswith(".csv")):
                self.output = open("Translated.csv", "w")
                for x in self._out:
                    self.output.write(x)
                self.output.close()
                
            else:
                raise TypeError("filename type  and encode filetype mismatch")

        else: 
            raise TypeError("filetype options only include 'text', 'json' or 'csv'")

def trinidad_decode(sentence:str):
    sentence=sentence.lower()
    sentence = " " + sentence 

    for x in caribedict:
        if sentence.find(x):
            sentence = re.sub(r'\b%s\b' %x, caribedict[x], sentence)
    return sentence.strip()


def phrase_decode(sentence:str):
    sentence=sentence.lower()
    sentence = " " + sentence
    for x in phrasedict:
        if sentence.find(x):
            sentence=sentence.replace(x, phrasedict[x])
    return sentence.strip()


def trinidad_decode_split(sentence:str):
    sentence= sentence.lower()

    for subs in sentence.split():
        if subs in splitdict: 	
            sentence = sentence.replace(subs, str(splitdict[subs.lower()]))
    return sentence

def t5_kes_corrector(sentence:str):
    model = HappyTextToText("T5", "KES/T5-KES")
    arguments = TTSettings(num_beams=4, min_length=1)
    input=str(sentence)
    correction = model.generate_text("grammar: "+input, args=arguments)
    if(correction.text.find(" .")):
        correction.text=correction.text.replace(" .", ".")
    return correction.text

def caribe_corrector(sentence:str):
    parser = GingerIt()
    sentence = parser.parse(sentence)
    sentence = sentence['result']
    return str (sentence)

def remove_signs(sentence:str)->str:
    stop_signs = ['!', ".", "%", '"', "'", "`", "*", "&", ",", "-", "+", "/", "'\'", "?", ";", ":", "$", "%", "#", "@", "=", "-", "~", "(", ")", "[", "]" ]
    for signs in stop_signs:
        sentence = sentence.replace(signs, "")
    return sentence

def caribe_word_tokenize(sentence:str):
    sentence = remove_signs(sentence)
    sentence = re.split("\s", sentence)
    return sentence


def trinidad_encode(sentence:str):
    sentence=sentence.lower()
    sentence = " " + sentence 
    for words in caribedict:
        if caribedict[words].lower() in sentence:
            sentence = re.sub(r'\b%s\b' %caribedict[words], words, sentence)
    return sentence


