import re

SPLIT_RGX = re.compile(r'\w+|[\(\)&\|!]', re.U)


# class QtreeTypeInfo:
#     def __init__(self, value, op=False, bracket=False, term=False):
#         self.value = value
#         self.is_operator = op
#         self.is_bracket = bracket
#         self.is_term = term
#
#     def __repr__(self):
#         return repr(self.value)
#
#     def __eq__(self, other):
#         if isinstance(other, QtreeTypeInfo):
#             return self.value == other.value
#         return self.value == other
#
#
# class QTreeTerm(QtreeTypeInfo):
#     def __init__(self, term):
#         QtreeTypeInfo.__init__(self, term, term=True)
#
#
# class QTreeOperator(QtreeTypeInfo):
#     def __init__(self, op):
#         QtreeTypeInfo.__init__(self, op, op=True)
#         self.priority = get_operator_prio(op)
#         self.left = None
#         self.right = None
#
#
# class QTreeBracket(QtreeTypeInfo):
#     def __init__(self, bracket):
#         QtreeTypeInfo.__init__(self, bracket, bracket=True)
#
#
# def get_operator_prio(s):
#     if s == '|':
#         return 0
#     if s == '&':
#         return 1
#     if s == '!':
#         return 2
#
#     return None
#
#
# def is_operator(s):
#     return get_operator_prio(s) is not None
#
#
# def tokenize_query(q):
#     tokens = []
#     for t in map(lambda w: w.encode('utf-8'), re.findall(SPLIT_RGX, q)):
#         if t == '(' or t == ')':
#             tokens.append(QTreeBracket(t))
#         elif is_operator(t):
#             tokens.append(QTreeOperator(t))
#         else:
#             tokens.append(QTreeTerm(t))
#
#     return tokens
#
#
# def build_query_tree(tokens):
#     """ write your code here """
#     if tokens[0].is_operator:
#         tokens[0].right = build_query_tree(tokens[1:])
#         return tokens[0]
#     if len(tokens) <= 2:
#         if tokens[0].is_term:
#             return tokens[0]
#         elif tokens[0].is_operator:
#             print tokens[0]
#             tokens[1].right = tokens[0]
#             return tokens[1]
#         return tokens[1]
#     rightest = 0
#     r_d = 999
#     depth = 0
#     offset = 0
#     for t in tokens:
#         if t == '(':
#             depth += 1
#         if t == ')':
#             depth -= 1
#         if is_operator(t):
#             if is_operator(tokens[rightest]):
#                 if get_operator_prio(tokens[rightest]) >= get_operator_prio(t) and r_d >= depth:
#                     r_d = depth
#                     rightest = offset
#             else:
#                 r_d = depth
#                 rightest = offset
#         offset += 1
#     tokens[rightest].left = build_query_tree(tokens[:rightest])
#     tokens[rightest].right = build_query_tree(tokens[rightest + 1:])
#     return tokens[rightest]
#
#
# def parse_query(q):
#     tokens = tokenize_query(q)
#     return build_query_tree(tokens)
#
#
# class tree:
#     def __init__(self, value, op=False):
#         self.value = value
#         self.is_operator = is_operator
#
#     def evaluate (self):
#         return -1
#
#     def goto (self, docid):
#         pass
#
#
# class term_node(tree):
#     def __init__(self, value):
#         tree.__init__(self, value)
#         self.docid = 0
#
#     def evaluate(self):
#         if self.docid == -2:
#             return -2
#
#         return self.value[self.docid]
#
#     def goto(self, docid):
#         while self.value[self.docid] < docid:
#             if self.docid == len(self.value) - 1:
#                 self.docid = -2
#                 break
#             self.docid += 1
#
#
# class op_node(tree):
#     def __init__(self, value, l, r):
#         tree.__init__(self, value, op=True)
#         self.right = r
#         self.left = l
#
#     def evaluate(self):
#         if self.value == '|':
#             a = self.left.evaluate()
#             b = self.right.evaluate()
#             if a == -2:
#                 return b
#             if b == -2:
#                 return a
#             return min(a, b)
#
#         if self.value == '&':
#             a = self.left.evaluate()
#             b = self.right.evaluate()
#
#             while a != b:
#                 if a == -2 or b == -2:
#                     return -2
#
#                 if a < b:
#                     self.right.goto(a)
#                     b = self.right.evaluate()
#                 else:
#                     self.left.goto(b)
#                     a = self.left.evaluate()
#             return a
#         if self.value == '!':
#             if self.right.evaluate () != -1:
#                 prev = self.right.evaluate ()
#                 while self.right.evaluate
#
#
#
# def from_query_to_apply(q):
#     return q
