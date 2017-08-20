# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 14:27:37 2017

@author: Sanju Menon
"""
import spacy
import re
from streetaddress import StreetAddressFormatter, StreetAddressParser
addr_parser = StreetAddressParser()



nlp = spacy.load('en')
place_list = ['Alexandra', 'Aljunied', 'Geylang', 'Ayer Rajah', 'Balestier', 'Bartley', 'Bishan', 'Marymount', 'Sin Ming', 'Bukit Timah', 'Buona Vista', 'Holland Village', 'one-north', 'Ghim Moh', 'Chinatown', 'Clarke Quay', 'Kreta Ayer', 'Telok Ayer', 'Kallang', 'Bendemeer', 'Geylang Bahru', 'Kallang Bahru', 'Kallang Basin', 'Kolam Ayer', 'Tanjong Rhu', 'Mountbatten', 'Old Airport', 'Lavender', 'Boon Keng', 'Kent Ridge', 'Kim Seng', 'Little India', 'Farrer Park', 'Jalan Besar', 'MacPherson', 'Marina Bay', 'Esplanade', 'Marina Bay Sands', 'Marina Centre', 'Marina East', 'Marina South', 'Mount Faber', 'Mount Vernon', 'Museum', 'Newton', 'Novena', 'Orchard Road', 'Dhoby Ghaut', 'Emerald Hill', 'Tanglin', 'Outram', 'Pasir Panjang', 'Paya Lebar', 'Eunos', 'Geylang East', 'Potong Pasir', 'Rochor-Kampong Glam', 'Bencoolen', 'Bras Basah', 'Bugis', 'Queenstown', 'Dover', 'Commonwealth', 'Raffles Place', 'River Valley', 'Singapore River', 'Southern Islands', 'Tanjong Pagar', 'Shenton Way', 'Telok Blangah', 'Bukit Chandu', 'Bukit Purmei', 'HarbourFront', 'Keppel', 'Radin Mas', 'Mount Faber', 'Tiong Bahru', 'Bukit Ho Swee', 'Bukit Merah', 'Toa Payoh', 'Bukit Brown', 'Caldecott Hill', 'Thomson', 'Whampoa', 'St. Michael\'s', 'Bedok','Bedok Reservoir', 'Chai Chee', 'Kaki Bukit', 'Tanah Merah', 'Changi', 'Changi Bay', 'Changi East', 'Changi Village', 'East Coast', 'Joo Chiat', 'Katong', 'Kembangan', 'Pasir Ris', 'Elias', 'Lorong Halus', 'Loyang', 'Marine Parade', 'Siglap', 'Tampines', 'Simei', 'Ubi', 'Central Catchment Nature Reserve', 'Kranji', 'Lentor', 'Lim Chu Kang', 'Neo Tiew', 'Sungei Gedong', 'Mandai', 'Sembawang', 'Canberra', 'Senoko', 'Simpang', 'Sungei Kadut', 'Woodlands', 'Admiralty', 'Innova', 'Marsiling', 'Woodgrove', 'Yishun', 'Chong Pang', 'Ang Mo Kio', 'Cheng San', 'Chong Boon', 'Kebun Baru', 'Teck Ghee', 'Yio Chu Kang', 'Bidadari', 'Hougang', 'Defu', 'Kovan', 'Lorong Chuan', 'North-Eastern Islands', 'Punggol', 'Punggol Point', 'Punggol New Town', 'Seletar', 'Sengkang', 'Serangoon', 'Serangoon Gardens', 'Serangoon North', 'Boon Lay', 'Tukang', 'Liu Fang', 'Samulun', 'Shipyard', 'Bukit Batok', 'Bukit Gombak', 'Hillview', 'Guilin', 'Bukit Panjang', 'Choa Chu Kang', 'Yew Tee', 'Clementi', 'Toh Tuck', 'West Coast', 'Pandan', 'Jurong East', 'Toh Guan', 'International Business Park', 'Teban Gardens', 'Penjuru', 'Yuhua', 'Jurong Regional Centre', 'Jurong West', 'Hong Kah', 'Taman Jurong', 'Boon Lay Place', 'Chin Bee', 'Yunnan', 'Central', 'Kian Teck', 'Safti', 'Wenya', 'Lim Chu Kang', 'Pioneer', 'Joo Koon', 'Gul Circle', 'Pioneer Sector', 'Tengah', 'Tuas', 'Wrexham', 'Promenade', 'Pioneer', 'Soon Lee', 'Tuas South', 'Western Islands Planning Area', 'Western Water Catchment', 'Murai', 'Sarimbun']



def check_if_place_mentioned(statement):
    doc1 = nlp(statement)
    found_from_list = 0
    is_place = 0
    place = []
    for ent in doc1.ents:
#        print(ent.label_, ent.text)
        if ent.label_ in ('GPE', 'LOC', 'ORG', 'FAC'):
            addr = addr_parser.parse(ent.text)
#            print(addr)
    
#    print(doc1.ents) 
    
    Address = dict()
    
    for x in place_list:
    
        if re.findall(r'%s' %x, str(statement).title()):
            found_from_list = 1
            print('Set location to ' + str(x))
    
    if found_from_list ==0:
            for np in doc1 :
                           
              
                if np.ent_type_ in ('GPE', 'LOC', 'ORG', 'FAC'):
#                  print(np.head.text)
                  
                  place.append(np.text)
                  is_place = 1
                elif np.pos_ == 'PROPN' and np.head.text in ( 'at', 'is') and np.dep_ != 'nsubj':
                  place.append(np.text)
                  
                  is_place = 1
            if is_place == 1:
                addr['street_full'] = str(" ".join((place))).title()
                try:
                    Address["Address"] = addr['street_full']
                    return Address
                except:
                    Address["Address"] = str(place).title() 
                    return Address
#                return str(place)
            else:
                print("no location in the input")
                return False
    return False

if __name__ == '__main__' :
    #inputQuery=  str(input("Type your request below: \n"))
    inputQuery = "Meeting is today at Blk 35 Mandalay Road # 13-37 Random Towers"
    print(check_if_place_mentioned(inputQuery))
    
