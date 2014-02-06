# Country ISO codes: http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
# 2013-10-17/18
# Based on a project by Ralph Straumann, ralphstraumann.ch

import urllib, urllib2
import json
import time
import codecs
import os
from nltk.corpus import stopwords


dir = os.path.split(os.path.dirname(__file__))

in_file = os.path.join(dir[0],'data_sources/nationality_list.txt')

sep = ','
iso_field = 'iso_a3'
name_field = 'admin'
plural_field = 'plural'
definite_field = 'definite'
nationality_field='nationalities'

out_file = os.path.join(dir[0], 'data_sources/country_stereotypes_results.txt')

# API endpoint
google_endpoint = 'http://google.com/complete/search?output=firefox&q='


def find_index(fieldname, in_file):
    ''' Given a field (column) name, this function finds the index of a field
    in a CSV file '''

    with open(in_file, 'r') as f:
        header = f.readline().rstrip().split(sep)
        i = 0
        for i in range(0, len(header)):
            if header[i] == fieldname:
                return i
                break
        else:
            return -1


def build_phrase(name, plural, definite):
    ''' Given a country name and <plural>, <definite> flag, this function 
    assembles the search query '''

    if plural == '1':
        phrase = u'why are'
    else:
        phrase = u'why is'
    
    if definite == '1':
        phrase = u'%s the' % phrase

    return u'%s %s so ' % (phrase, name)

def build_nationality_phrase(nationality):
    ''' Given a country name and <plural>, <definite> flag, this function 
    assembles the search query '''

    phrase = 'why are'
    print u'%s %s so ' % (phrase, nationality)
    return u'%s %s so ' % (phrase, nationality)


def query_google(phrase):
    ''' Query using the Google endpoint '''

    url = '%s%s' % (google_endpoint, urllib.quote_plus(phrase))
    data = urllib2.urlopen(url)
    data = json.load(data)
    results = [result.replace(phrase.lower(), '') for result in data[1]]
    return results



iso_idx = find_index(iso_field, in_file)
name_idx = find_index(name_field, in_file)
plural_idx = find_index(plural_field, in_file)
definite_idx = find_index(definite_field, in_file)
nationality_idx = find_index(nationality_field,in_file)

with codecs.open(in_file, 'r', 'utf-8') as f:

    with codecs.open(out_file, 'w', 'utf-8') as f_out:
        f_out.write('iso\tname\tterm\n')
        
        data = f.readlines()
        for record in data[1:]:
            time.sleep(0.3)
            
            record = record.rstrip()
            items = record.split(sep)
            iso = items[iso_idx]
            name = items[name_idx]
            plural = items[plural_idx]
            definite = items[definite_idx]
            nationality=items[nationality_idx]
            print stopwords.words('english')
                        
            phrase = build_nationality_phrase(nationality)
            try:
                results = query_google(phrase)
                
                
                if len(results) > 0:
                    for result in results:
                        filtered_words = [w for w in result if not w in stopwords.words('english')]
                        
                        f_out.write('%s\t%s\t%s\n' % (iso, nationality, result))
                else:
                    f_out.write('%s\t%s\t\n' % (iso, nationality))
            except:
                f_out.write('%s\t%s\t\n' % (iso, nationality))

