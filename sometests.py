# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 18:39:51 2017

@author: Sanju Menon

***      hug -f sometests.py --manual_reload     ***
***  
TF_IDF_Intent
AmbiguousTable
Table
payroll_entity_extraction
LocationExtraction

example-mesg.docx
payroll_intent_example



"""

from IntentWithPayload import get_intent_payload



import hug

    
@hug.cli()
@hug.get()
@hug.local()
def test(text: str):
    
    response = get_intent_payload(text)
    print(response)
    return {'response': response}   


if __name__ == '__main__':
    text = 'Meal Allowance \n\n Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F'
    test(text)






    