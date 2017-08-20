# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 11:02:01 2017

@author: Sanju Menon
"""
from AmbiguousTable import get_if_table
import json
from raspador import Parser, StringField
from CurrencyExtraction import get_money
from LocationExtraction import check_if_place_mentioned




class Parser(Parser):
#    begin = r'^Emp id:.*'
#    end = r'^PART.*'
    PAN_NO = StringField(r'\b([A-Z]{5}[0-9]{4}[A-Z])\b')
    EMPID = StringField(r'\b([0-9]{3})\b')
    TYPE = StringField(r'TYPE:([^\s]+) ')
    
def get_entity(out):
    
    if type(out) == list or out.startswith('[') and out.endswith(']'):
        return False
    
    
    if get_if_table(out):
        tableList = get_if_table(out)
        parseList = [" ".join(tableList[i]) for i in range(len(tableList))]
    else:
        parseList= [out]
        
    
#    print(parseList)
    
    a = Parser()
    
    res_list = []
    
    for i in range(len(parseList)):
        if a.parse(iter(parseList[i].splitlines())):
            res = a.parse(iter(parseList[i].splitlines()))
            res_list.extend(res)
        if get_money(parseList[i]):
             res2 = get_money(parseList[i])
             res_list.extend(res2)
    
    if check_if_place_mentioned(" ".join(parseList)):
        
        res3 =  check_if_place_mentioned(" ".join(parseList))
        res_list.extend(res3)

        

        
    out_as_json = json.dumps(res_list, indent=2, ensure_ascii=False)
    
#    print(out_as_json)
    
    return out_as_json


if __name__ == '__main__':
    out = "Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F INR 2000.00. Meeting is today at Mandalay Road Random Towers"
    get_entity(out)