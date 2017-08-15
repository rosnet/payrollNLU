# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 09:58:40 2017

@author: Sanju Menon


Usage:
    
from TF_IDF_Intent import Intent



x = Intent('Example-Mesg.docx')
test = "meal allowance extended"   
x.get_best_match(test)




"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl, CT_Row, CT_TblGrid, CT_TblGridCol, CT_TblLayoutType, CT_TblPr, CT_TblWidth, CT_Tc, CT_TcPr, CT_VMerge
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from collections import OrderedDict


import math
from textblob import TextBlob as tb
from textblob import Word

from nltk.corpus import stopwords

import re

stops = set(stopwords.words("english"))



class ParseBlock():
        
        def __init__(self, path):
            self.document = Document(path)
            self.true_block= ""
            self.block_dict = OrderedDict()
            self.block_list = []
#            self.paras = self.get_true_block()
            self.filtered_para = ""
            self.documents = []
        
        def iter_block_items(self, parent):
            """
            Generate a reference to each paragraph and table child within *parent*,
            in document order. Each returned value is an instance of either Table or
            Paragraph. *parent* would most commonly be a reference to a main
            Document object, but also works for a _Cell object, which itself can
            contain paragraphs and tables.
            """
            
            self.parent = parent
            
            if isinstance(self.parent, _Document):
                self.parent_elm = self.parent.element.body
                # print(parent_elm.xml)
            elif isinstance(self.parent, _Cell):
                self.parent_elm = self.parent._tc
            else:
                raise ValueError("something's not right")
        
            for self.child in self.parent_elm.iterchildren():
                
                if isinstance(self.child, CT_P):
                    
                    yield Paragraph(self.child, self.parent)
                elif isinstance(self.child, CT_Tbl) or isinstance(self.child, CT_TblGrid) or isinstance(self.child, CT_TblGridCol) or isinstance(self.child, CT_TblLayoutType) or isinstance(self.child, CT_TblPr) or isinstance(self.child, CT_TblWidth) or isinstance(self.child, CT_Tc) or isinstance(self.child, CT_TcPr) or isinstance(self.child, CT_VMerge) : #CT_Tbl
                    yield Table(self.child, self.parent)
        
        
        
        
        
        def get_true_block(self):
                 
            
            for self.block in self.iter_block_items(self.document):
                if isinstance(self.block, Paragraph):
                    if not self.block.text.strip():
                        self.block_list.append(self.true_block)
                        self.true_block = ""
                    else:
                        self.true_block = self.true_block + "\n" + self.block.text
            
                elif isinstance(self.block, Table):
                    self.true_block = self.true_block + "\n" + "<table>"
                else:
                    print("unresolved type")
            print(len(self.block_list))      
            return self.block_list
        
        def filter_block(self):
            
            self.paras = self.get_true_block()
            
#            print("yay", len(self.paras[1]))
            
            count = len(self.paras)
            
            for i in range(0,count):                
                
                self.filtered_para = self.paras[i]
                self.filtered_para = "".join(self.filtered_para)                
                self.filtered_para = re.sub(r'[0-9]{1,}[A-Za-z]{1,}', '', self.filtered_para)                
                self.filtered_para = re.sub(r'[0-9]', '', self.filtered_para)                
                self.filtered_para = re.sub(r'[?|$|.|!|@|%|*|-|:|"|_|–|“|”|\b&\b|’|-|,|-|/|-]',r'',self.filtered_para)
                
            #    re.sub("[A-Z][a-zA-Z]*\s[A-Z][a-zA-Z]",'', filtered_para)
                self.pattern = re.compile('[A-Z]{4,}')                
                self.filtered_para = re.sub(self.pattern, '', self.filtered_para)
                self.filtered_para = self.filtered_para.lower()
                self.filtered_para.replace(",","")
                
            #    filtered_para = ''.join([i for i in filtered_para if not i.isdigit()])
                self.filtered_para = " ".join([self.w_ord for self.w_ord in self.filtered_para.split() if self.w_ord not in stops])
                print(self.filtered_para)
                
                self.lemmatized_para = Word(self.filtered_para).lemmatize()                
                self.documents.append(tb(self.lemmatized_para))
                
            
            return self.documents


        def get_bloblist(self):
          
            return self.filter_block()

class Intent():
    
    def __init__(self,file):
        
        bloblist = ParseBlock(file).get_bloblist()
        self.bloblist = bloblist
        
        self.tfidf_scores_sorted(self.bloblist)
        
        
#        for i, blob in enumerate(bloblist):
#            print("Top words in document {}".format(i + 1))
#            scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
#            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#            for word, score in sorted_words[:8]:
#                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

    
    def tf(self,word, blob):
        return blob.words.count(word) / len(blob.words)
    
    
    def n_containing(self, word):
        return sum(1 for blob in self.bloblist if word in blob.words)
    
    
    def idf(self, word):
        return math.log(len(self.bloblist) / (1 + self.n_containing(word)))
    
    
    def tfidf(self, word, blob):
        return self.tf(word, blob) * self.idf(word)
    
    
    def tfidf_scores_sorted(self, bloblist):
        for i, blob in enumerate(self.bloblist):
            print("Top words in document {}".format(i + 1))
            scores = {word: self.tfidf(word, blob) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for word, score in sorted_words[:6]:
                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    
    
    def get_best_match(self, to_check):
        highest = 0
        best_match =""
        check_string = tb(to_check)
    
        for i, blob_ in enumerate(self.bloblist):
            per_blob_score = 0
            
            if not len(blob_.words) == 0:
                for word_ in check_string.words:
                     
                    per_blob_score = per_blob_score + self.tfidf(word_, blob_) 
            
            if per_blob_score > highest:
                highest = per_blob_score
                best_match = "document {}".format(i+1)
        
        print("\nBest match document = {}".format(best_match))
        return best_match


if __name__ == '__main__':
    


    bloblist = ParseBlock('Example-Mesg.docx').get_bloblist()
            
    test = "meal allowance extended"
    x = Intent('Example-Mesg.docx')
    
    x.get_best_match(test)