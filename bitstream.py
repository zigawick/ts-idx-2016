class BitstreamWriter:
    def __init__(self):
        self.nbits  = 0
        self.curbyte = 0
        self.vbytes = []

    """ add single bit """
    def add(self, x):
        self.curbyte |= x << (8-1 - (self.nbits % 8))
        self.nbits += 1

        if self.nbits % 8 == 0:
            self.vbytes.append(chr(self.curbyte))
            self.curbyte = 0

    """ get byte-aligned bits """
    def getbytes(self):
        if self.nbits & 7 == 0:
            return "".join(self.vbytes)

        return "".join(self.vbytes) + chr(self.curbyte)


class BitstreamReader:
    def __init__(self, blob):
        self.blob = blob
        self.pos  = 0

    """ extract next bit """
    def get(self):
        ibyte = self.pos / 8
        ibit  = self.pos & 7

        self.pos += 1
        return (ord(self.blob[ibyte]) & (1 << (7 - ibit))) >> (7 - ibit)

    def finished(self):
        return self.pos >= len(self.blob) * 8


"""
Input dl contains monotonically groving integers
"""


def compress_varbyte(dl):
    bs = BitstreamWriter()

    """ Write your code here """

    prev = 0
    for i in dl:
        j = 0;
        temp = i
        i -= prev
        prev = temp

        num = []
        bit = 1
        while i > 0:
            if bit == 8:
                num.append(1)
                bit = 1
            if i & 1:
                num.append(1)
            else:
                num.append(0)
            bit += 1
            i = i / 2
        while bit <= 8:
            bit += 1
            num.append(0)
        for val in num:
            bs.add(val)
    return bs.getbytes()


def decompress_varbyte(s):
    bs = BitstreamReader(s)
    dl = []

    """ Write your code here """
    summa = 0
    bit_num = 1
    while not bs.finished():
        bit = bs.get()
        if not bit_num % 8:
            if not bit:
                dl.append(summa)
                bit_num = 0
            else:
                bit_num += 1
                continue

        if bit:
            summa += 2 ** (bit_num - 1 - bit_num / 8)
        bit_num += 1

    return dl


def put(bs, ints, num):
    counter = 0
    num_c = num
    for k in range(4):
        if num_c & 1:
            bs.add(1)
        else:
            bs.add(0)
        num_c = num_c / 2
        counter += 1

    for i in ints:
        for k in range(28 / num):
            if i & 1:
                bs.add(1)
            else:
                bs.add(0)
            i = i / 2

            counter += 1
    while counter < 32:
        bs.add(0)
        counter += 1


def get(br, summa):
    num = 0
    count = 0
    for i in range(4):
        num += br.get() * 2 ** i
        count += 1
    ret = []
    for i in range(num):
        for k in range(28 / num):
            bit = br.get()
            summa += bit * 2 ** k
            count += 1
        ret.append(summa)
    for k in range(32 - count):
        br.get()
    return ret


def compress_simple9(dl):
    bs = BitstreamWriter()

    """ Write your code here """

    prev_max = 0
    prev = 0

    arr = []
    for i in dl:
        j = 0;
        temp = i
        i -= prev
        prev = temp

        if i > prev_max:
            prev_max = i

        if (len(arr) + 1) * prev_max.bit_length() > 28:
            put(bs, arr, len(arr))
            prev_max = i
            arr = [i]
            continue

        arr.append(i)
    if len(arr) > 0:
        put(bs, arr, len(arr))
    return bs.getbytes()


def decompress_simple9(s):
    bs = BitstreamReader(s)
    dl = []

    """ Write your code here """

    summa = 0
    while not bs.finished():
        if len(dl) > 0:
            summa = dl[-1]
        dl.extend(get(bs, summa))
    return dl