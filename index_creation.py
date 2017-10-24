import doc2words
from collections import defaultdict


class Url_Index:
    def __init__(self):
        self.terms = defaultdict(list)
        self.ind = 0
        self.url = []

    def scan_text(self, doc):
        for word in set(doc2words.extract_words(doc.text)):
            # print word
            # word = unicode (word, "utf-8")
            self.terms[word].append(self.ind)
        self.ind += 1
        self.url.append(doc.url)
