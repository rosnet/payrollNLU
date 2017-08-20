# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 18:48:17 2017

@author: Sanju Menon
"""

import spacy
from collections import OrderedDict
from string import punctuation
import re
import json
from forex_python.converter import CurrencyCodes


#def get_symbol(price):
#        
#        pattern =  r'(\D*)\d*\.?\d*(\D*)'
#            g = re.match(pattern,price).groups()
#        return g[0] or g[1]
#    
nlp = spacy.load('en')
punctuation = punctuation.replace('$','')

def get_money(text):
    
    if type(text) == list:
        text = " ".join(text)

            
    
    for i,word in enumerate(text.split()):
        if CurrencyCodes().get_symbol(word): #and not word.isdigit()
#            print(word, "This",CurrencyCodes().get_symbol(word) )
            text = text.replace(word, CurrencyCodes().get_symbol(word))
            if i == len(text.split())- 1:
                text = text + " SOMEPADDING"
#    print(text) 
    doc = nlp(text) 
#    for i in range(len(doc)):
#        print(doc[i].text, doc[i].lemma_, doc[i].tag_, doc[i].pos_)

          
    
       
    money_in_text= []
    
    money = OrderedDict()
    
    for i in range(len(doc)-2):

        if doc[i].pos_ == 'NUM' and doc[i].tag_ == 'CD':
            
            if doc[i+1].pos_ == 'ADP' and doc[i+2].pos_ in ('NOUN') :
                money["Amount"] = doc[i].text
                money["Unit"] = doc[i+2].text
        
            elif doc[i+1].pos_ in ('SYM', 'NOUN') and i < (len(doc)-2) and doc[i+2].pos_ == 'ADP' and doc[i+3].pos_ in ('NOUN'):
                if doc[i+2].pos_ == 'ADP' and doc[i+3].pos_ in ('NOUN'):
                    money["Amount"] = doc[i].text
                    money["Unit"] = doc[i+3].text
                else:
                    money["Amount"]= doc[i].text
            elif not len(doc[i].text) == 1:
                money["Amount"] = doc[i].text
            
            if doc[i+1].pos_ in ('SYM', 'NOUN', 'NUM') and  not doc[i+1].text in punctuation: money["Currency"] = str(doc[i+1].text)
            elif doc[i-1].pos_ in ('SYM', 'NOUN') and not doc[i+1].text in punctuation: money["Currency"] = str(doc[i-1].text)
            
            if money:
                pattern = re.compile(r'([0][0-9]{2})')
                if pattern.match(money["Amount"]):
                    pass
                else:
                    money_in_text.append(json.dumps(money, ensure_ascii=False))
        money.clear()
            
    return money_in_text if money_in_text else False

        

            
if __name__ == '__main__':

    input = "25000.00 INR Rent Details – 8000.00$ per month"
    input = "Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F 2000.00 INR"
    print(get_money(input))      
        
    

