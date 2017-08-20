# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 11:06:38 2017

@author: Sanju Menon
"""

from TextAndTable import getTextAndTable

from TF_IDF_Intent import Intent

from payroll_entity_extraction import get_entity


from collections import OrderedDict
import json
import re

def get_intent_payload(alljson):
    
    response_for_alljson = []
    response_per_block = OrderedDict()
    
    blocklist = getTextAndTable(alljson)
    
    for block in blocklist:

        try:
            intent_name, confidence = Intent('Example-Mesg.docx').get_best_match(block)
            entities = get_entity(block)
            response_per_block["Intent"] = OrderedDict()
            response_per_block["Intent"]["Name"] = intent_name
            response_per_block["Intent"]["Confidence"] = confidence
            response_per_block["Entities"] = entities
        except:
            response_per_block["Table"] = block
        
                
        
        

            
        response_for_alljson.append(json.dumps(response_per_block, ensure_ascii = False))
        
    return response_for_alljson
        
        
    
    
        







if __name__ == '__main__':
    
    all_json = 'Meal Allowance Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F 2000.00 INR London TEXT TEXT \n\n Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F \n\n SOME SOME [{ "Employee":"1234","Salary":"1000"},{ "Employee":"2345","Salary":"2000"},{ "Employee":"3456","Salary":"3000"}] aftertext [{ "Employee":"1234","Salary":"1000"},{ "Employee":"2345","Salary":"2000"},{ "Employee":"3456","Salary":"5000000"}] some more aftertext'
    get_intent_payload(all_json)