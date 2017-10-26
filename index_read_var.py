import cPickle
import re
import dict_hash
import parser

import bitstream

if __name__ == '__main__':
    index_file = open("index.txt", "rb")
    url_file = open("url_file.txt", "rb")
    urls = cPickle.load(url_file)

    dict = dict_hash.dict_hash()

    while True:
        try:
            line = raw_input()

            result_ind = set()
            question = line.decode('utf8')

            q = parser.parse_query(question)
            parser.term_to_list_varbyte(q, dict, index_file)

            curr = 0
            res = []
            while curr >= 0:
                q.goto(curr)
                curr = q.evaluate()
                if curr != -2:
                    res.append(curr)
                curr += 1

            print question.encode('utf8')
            print len(res)
            for i in sorted(res):
                print urls[i]

        except:
            break
