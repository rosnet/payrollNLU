# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 22:56:54 2017

@author: Sanju Menon
"""

from raspador import Parser, StringField

#out = "Emp id: 067 – LIC Premium – 25000.00\n\tRent Details – 8000.00 per month"




out = "Emp id: 052 – BTBPM1234X \n\t060 - GLXPS8254F"

import asciitable  as t
import json
import re
DEBUG = True

def skip_bad_lines(self, str_vals, ncols):
  """Simply ignore every line with the wrong number of columns."""
  if DEBUG:
    print ( 'Skipping line:', ' '.join(str_vals))
  return None



def fix_bad_lines(self, str_vals, ncols):
  """Pad with zeros at the end (not enough columns) or truncate
  (too many columns)"""
  if DEBUG:
    print ('Fixing line:', ' '.join(str_vals))
  n_str_vals = len(str_vals)
  
  if n_str_vals == ncols:
      first = str_vals[0]
      second = str_vals[1]

  if n_str_vals < ncols:
    return ['first', 'second'] + str_vals
    


def read_rdb_table(_table):
    reader = t.Basic()
#    reader = t.NoHeader()
    
    reader.header.splitter.delimiter = '\t'
    reader.data.splitter.delimiter = '\t'
    reader.header.splitter.process_line = None
    reader.data.splitter.process_line = None
    reader.data.start_line = 0
    t.BaseReader.inconsistent_handler = fix_bad_lines
 

    return reader.read(_table)

def get_row(out):
 
    if re.split('\n\t{1,2}',out):
        possibleTable = re.split('\n\t{1,2}',out)
        possibleTable = [[i] for i in possibleTable]
        return possibleTable
    elif read_rdb_table(out):
        possibleTable = read_rdb_table(out)
        return possibleTable
    
    else:
        return False



def get_if_table(out): 
       
    if not get_row(out) == False:
        indentedTable = get_row(out)
    else:
        return False
    
    fullTable = []
    
    for i in range(len(indentedTable)):
        
        to_append = re.split('\s{1,}|–|:|-{1,}',indentedTable[i][0])
        
        fullTable.append(to_append)
        fullTable[i] = [j for j in fullTable[i] if j]
    
    
    
    full_column_len, full_column_row = sorted([(len(fullTable[i]),i) for i in range(len(fullTable))], reverse = True)[0]
    
    completeTable = []
    
    for count, row in enumerate(fullTable):
        new_row = []
    
        if len(row) < full_column_len:
            for i in range(full_column_len - len(row)):
                new_row.append(fullTable[full_column_row][i])
            new_row.extend(row)
            completeTable.append(new_row)
        else:
            completeTable.append(row)
    
    
    return completeTable
"""
tableList = get_if_table(out)

tableString = [" ".join(tableList[i]) for i in range(len(tableList))]

print(tableString)

class LogParser(Parser):
#    begin = r'^Emp id:.*'
#    end = r'^PART.*'
    PAN_NO = StringField(r'\b([A-Z]{5}[0-9]{4}[A-Z])\b')
    EMPID = StringField(r'\b([0-9]{3})\b')
    TYPE = StringField(r'TYPE:([^\s]+) ')
    

a = LogParser()

#res = a.parse(iter)
for i in range(len(tableString)):
    res = a.parse(iter(tableString[i].splitlines()))
    out_as_json = json.dumps(list(res), indent=2)
    print (out_as_json)

"""

if __name__ == '__main__':
    print(get_if_table(out))
