# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 11:57:24 2017

@author: Sanju Menon
"""

import json 
import re
from AmbiguousTable import get_if_table

def getTextAndTable(inputstring):

      
    
    
    paragraphs = re.split('\n{2,}',inputstring)
    
    textAndTables = []
    paragraphs = [[i] for i in paragraphs]
    print(paragraphs, '\n\n\n')
    
    for para in paragraphs:
        textAndTablesInPara = re.split(r'\[(.*?)\]', " ".join(para))
        textAndTables.extend(textAndTablesInPara)
       
    
    for i in range(len(textAndTables)):
        try:
            json.loads("["+ textAndTables[i]+"]")
            textAndTables[i] = "["+ textAndTables[i]+"]"
            
               
        except:
            if '\n\t' in textAndTables[i]:
                textAndTables[i] = get_if_table(textAndTables[i])
            else:
                pass
            
    
    textAndTables = [x for x in textAndTables if x]
    
    print(textAndTables)
    
    return textAndTables


if __name__ == '__main__':
    inputstring = 'TEXT TEXT \n\n Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F \n\n SOME SOME [{ "Employee":"1234","Salary":"1000"},{ "Employee":"2345","Salary":"2000"},{ "Employee":"3456","Salary":"3000"}] aftertext [{ "Employee":"1234","Salary":"1000"},{ "Employee":"2345","Salary":"2000"},{ "Employee":"3456","Salary":"5000000"}] some more aftertext'
    getTextAndTable(inputstring)