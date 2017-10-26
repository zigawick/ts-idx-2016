import re

import bitstream
import mmhash
import dict_hash

SPLIT_RGX = re.compile(r'\w+|[\(\)&\|!]', re.U)


class QtreeTypeInfo:
    def __init__(self, value, op=False, bracket=False, term=False):
        self.value = value
        self.is_operator = op
        self.is_bracket = bracket
        self.is_term = term

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if isinstance(other, QtreeTypeInfo):
            return self.value == other.value
        return self.value == other


class QTreeTerm(QtreeTypeInfo):
    def __init__(self, term):
        QtreeTypeInfo.__init__(self, term, term=True)
        self.docid = 0  # alpha id

    def evaluate(self):
        if self.docid < 0:
            return self.docid

        return self.value[self.docid]

    def goto(self, urlid):
        if self.docid == -2:
            return
        if len(self.value) <= self.docid:
            self.docid = -2
            return

        while self.docid < len(self.value):
            if self.value[self.docid] >= urlid:
                return
            self.docid += 1
        self.docid = -2


class QTreeOperator(QtreeTypeInfo):
    def __init__(self, op):
        QtreeTypeInfo.__init__(self, op, op=True)
        self.priority = get_operator_prio(op)
        self.left = None
        self.right = None
        self.urlid = -1

    def evaluate(self):
        if self.value == '|':
            a = self.left.evaluate()
            b = self.right.evaluate()
            if a == -2:
                return b
            if b == -2:
                return a
            return min(a, b)

        if self.value == '&':
            a = self.left.evaluate()
            b = self.right.evaluate()

            while a != b:
                if a == -2 or b == -2:
                    return -2

                if a > b:
                    self.right.goto(a)
                    b = self.right.evaluate()
                else:
                    self.left.goto(b)
                    a = self.left.evaluate()
            return a

        if self.value == '!':
            if self.urlid < 0:
                return self.urlid

            curr = self.right.evaluate()
            if curr > self.urlid:
                return self.urlid

            while self.urlid == self.right.evaluate():
                self.urlid += 1
                self.right.goto(self.urlid)

            if self.right.evaluate() < 0:
                self.urlid = -2

            return self.urlid

    def goto(self, urlid):
        if self.value == '|':
            self.left.goto(urlid)
            self.right.goto(urlid)
            return

        if self.value == '&':
            self.left.goto(urlid)
            self.right.goto(urlid)
            return

        if self.value == '!':
            self.urlid = urlid
            self.right.goto(urlid)
            return


class QTreeBracket(QtreeTypeInfo):
    def __init__(self, bracket):
        QtreeTypeInfo.__init__(self, bracket, bracket=True)


def get_operator_prio(s):
    if s == '|':
        return 0
    if s == '&':
        return 1
    if s == '!':
        return 2

    return None


def is_operator(s):
    return get_operator_prio(s) is not None


def tokenize_query(q):
    tokens = []
    for t in map(lambda w: w.lower().encode('utf-8'), re.findall(SPLIT_RGX, q)):
        if t == '(' or t == ')':
            tokens.append(QTreeBracket(t))
        elif is_operator(t):
            tokens.append(QTreeOperator(t))
        else:
            tokens.append(QTreeTerm(t))

    return tokens


def build_query_tree(tokens):
    """ write your code here """
    if tokens[0].is_operator:  # !
        tokens[0].right = build_query_tree(tokens[1:])
        return tokens[0]
    if all(not t.is_operator for t in tokens):
        for t in tokens:
            if t.is_term:
                return t
        return None
    rightest = 0
    r_d = 999
    depth = 0
    offset = 0
    for t in tokens:
        if t == '(':
            depth += 1
        if t == ')':
            depth -= 1
        if is_operator(t):
            if is_operator(tokens[rightest]):
                if r_d >= depth:
                    if r_d > depth:
                        r_d = depth
                        rightest = offset
                    elif r_d == depth and get_operator_prio(tokens[rightest]) >= get_operator_prio(t):
                        r_d = depth
                        rightest = offset
            else:
                r_d = depth
                rightest = offset
        offset += 1
    tokens[rightest].left = build_query_tree(tokens[:rightest])
    tokens[rightest].right = build_query_tree(tokens[rightest + 1:])
    return tokens[rightest]


def parse_query(q):
    tokens = tokenize_query(q)
    return build_query_tree(tokens)


def term_to_list_simple(q, dict, index_file):
    if q.is_term:
        word = mmhash.get_unsigned_hash (q.value.lower())

        place = dict.find_term (word)
        if place[0] < 0:
            found = []
        else:
            index_file.seek(place[0])
            blob = index_file.read(place[1])
            found = bitstream.decompress_simple9(blob)
        q.value = found
    else:
        if q.left is not None:
            term_to_list_simple(q.left, dict, index_file)
        if q.right is not None:
            term_to_list_simple(q.right, dict, index_file)


def term_to_list_varbyte(q, dict, index_file):
    if q.is_term:
        word = mmhash.get_unsigned_hash (q.value.lower())

        place = dict.find_term (word)
        if place[0] < 0:
            found = []
        else:
            index_file.seek(place[0])
            blob = index_file.read(place[1])
            found = bitstream.decompress_varbyte(blob)
        q.value = found
    else:
        if q.left is not None:
            term_to_list_varbyte(q.left, dict, index_file)
        if q.right is not None:
            term_to_list_varbyte(q.right, dict, index_file)
