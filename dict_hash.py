import struct


def store_dict(term):
    num = len(term)
    num_boxes = num / 50

    box_size = [0] * num_boxes
    boxes = [bytearray() for i in range(num_boxes)]

    for k, v in term.iteritems():
        box_num = k % num_boxes
        box_size[box_num] += 1
        boxes[box_num].extend(struct.pack('Q', k))
        for x in v:
            boxes[box_num].extend(struct.pack('I', x))


    blob = bytearray (struct.pack('I', num_boxes))

    summ = 0
    for x in box_size:
        blob.extend(struct.pack('I', summ))
        summ += x

    blob.extend(struct.pack('I', summ))

    for x in boxes:
        blob.extend (x)

    dict_hash_file = open("dict_hash.txt", "wb")
    dict_hash_file.write(blob)


class dict_hash:
    def __init__(self):
        self.file = open("dict_hash.txt", "rb")
        res = self.file.read(4)
        self.num = struct.unpack('I', res[0: 4])[0]
        self.sizes = []
        res = self.file.read(4 * (self.num + 1))
        for i in range(self.num + 1):
            self.sizes.append(struct.unpack('I', res[4 * i: 4 * i + 4])[0])

    def find_term(self, term):
        box = term % self.num
        offset = self.sizes[box] * 16
        self.file.seek(offset + 4 * (self.num + 1) + 4)
        res = self.file.read((self.sizes[box + 1] - self.sizes[box]) * 16)
        for x in range((self.sizes[box + 1] - self.sizes[box])):
             if term == struct.unpack('Q', res[16 * x: 16 * x + 8])[0]:
                off = struct.unpack('I', res[16 * x + 8: 16 * x + 12])[0]
                size = struct.unpack('I', res[16 * x + 12: 16 * x + 16])[0]
                return [off, size]
        return [-1, -1]
