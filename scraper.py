from bs4 import BeautifulSoup
import json
import sys
import time
import random
import requests
from requests.exceptions import RequestException


RETRIES = []  # a list of words that failed for any reason, to be re-fetched later
WORD_LIST = {}
def parse_word(word, lang):
    URL = "http://www.perseus.tufts.edu/hopper/morph?l=" + word + "&la=" + lang
    try:
        response = requests.get(URL)
    except requests.exceptions.RequestException as e:
        print (e)
        RETRIES.append(word)
        return

    if not response.status_code == 200:
        # print("Word '{}' failed.".format(word))
        RETRIES.append(word)
        return
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    lemmas = soup.find_all(class_="lemma")
    definition = soup.find_all(class_="lemma_definition")
    word_list = []
    index = 0
    for lemma in lemmas:
        word = {}
        try:
            # this was failing for me w/ beautifulsoup4 4.4.1 and lxml 3.6.0 (latest vers.)
            # @suheb you should make sure this works
            word['headword'] = lemma.find(class_="lemma_header").find(class_=lang).text.strip()
        except AttributeError:
            pass
        word['definition'] = lemma.find(class_="lemma_definition").text.strip()
        word['pos'] = lemma.find("table").find("tr").find_all("td")[1].text.strip()
        word_list.insert(index, word)
        index += 1

    return word_list

def add_word_to_list(word):

    # check if already in there
    if word in WORD_LIST:
        return

    WORD_LIST[word] = parse_word(word, lang)
    time.sleep(random.random() * 2) # wait for random time: 0-2 sec

    return



if __name__ == "__main__":
    infilename = sys.argv[1] # Take first argument as input file
    outfilename = sys.argv[2] # Take second argument as output file
    lang = sys.argv[3] # Take second argument as language code: la - latin, greek: greek

    with open(infilename) as infile:
        for i, line in enumerate(infile):
            # for testing
            #if i >= 10:
            #    break
            word_from_file = line.split()[0].strip('!').lower()

            add_word_to_list(word_from_file)
            # write every n iterations
            # write entire object again
            if i % 100 == 0:
                with open(outfilename, 'w') as outfile:
                    json.dump(WORD_LIST, outfile)
                with open("retries.json", 'w') as retriesfile:
                    json.dump(RETRIES, retriesfile)
   
    # save RETRIES to file to run later
    with open("retries.json", 'w') as retriesfile:
        json.dump(RETRIES, retriesfile)

    with open(outfilename, 'w') as outfile:
        json.dump(WORD_LIST, outfile)
