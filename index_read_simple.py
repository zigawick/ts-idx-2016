import pickle
import re

import parser

import bitstream

if __name__ == '__main__':
    dictionary = open("dict.txt", "rb")
    term = pickle.load(dictionary)
    index_file = open("index.txt", "rb")
    url_file = open("url_file.txt", "rb")
    urls = pickle.load(url_file)

    while True:
        try:
            line = raw_input()

            result_ind = set()
            question = line.decode ('utf8')
            p = re.findall(parser.SPLIT_RGX, question)
            for i in range(len(p)):
                if not i % 2:
                    word = p[i].lower().encode('utf8')
                    found = []
                    if not term.has_key (word):
                        found = []
                    else:
                        place = term[word]
                        index_file.seek(place[0])
                        blob = index_file.read(place[1])
                        found = bitstream.decompress_simple9(blob)

                    if i == 0:
                        result_ind = set(found)
                    else:
                        result_ind = result_ind.intersection(set(found))

            print question.encode('utf8')
            print len(result_ind)
            for i in sorted (result_ind):
                print urls[i]

        except:
        #     print ''
            break
