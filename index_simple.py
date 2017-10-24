import docreader
from docreader import DocumentStreamReader
import index_creation
import bitstream
import pickle


if __name__ == '__main__':
    reader = DocumentStreamReader(docreader.parse_command_line().files)
    index = index_creation.Url_Index()
    for doc in reader:
        index.scan_text(doc)
    blob = []
    term = dict()
    for k, v in index.terms.iteritems():
        prev_len = len(blob)
        compr = bitstream.compress_simple9(v)
        blob.extend(compr)
        term[k.encode('utf8')] = [prev_len, len(compr)]

    index_file = open("index.txt", "wb")
    index_file.write(bytearray(blob))

    url_file = open("url_file.txt", "wb")
    pickle.dump(index.url, url_file)

    dictionary = open("dict.txt", "wb")
    pickle.dump(term, dictionary)