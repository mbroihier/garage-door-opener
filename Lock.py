class Lock(object):
    def __init__(self, key):
        print(key)
        self.M = 214326
        self.A = 1807
        self.C = 45289
        self.locked = False
        sign_extend = ~ 0xff
        test_byte = key[0]
        if test_byte & 0x80 == 0x80:
            test_byte = test_byte | sign_extend
        print(test_byte)
        test_byte = key[1]
        if test_byte & 0x80 == 0x80:
            test_byte = test_byte | sign_extend
        print(test_byte)
        test_byte = key[2]
        if test_byte & 0x80 == 0x80:
            test_byte = test_byte | sign_extend
        print(test_byte)
        test_byte = key[3]
        if test_byte & 0x80 == 0x80:
           test_byte = test_byte | sign_extend
        print(test_byte)
        seed = int((key[0] << 24) + ((key[1] << 16) & 0xff0000) + ((key[2] << 8) & 0xff00) + (key[3] & 0xff))
        seed = seed % self.M
        print("original seed")
        print(seed)
        index = 4;
        seed = (self.A * seed + self.C) % self.M
        print("New seed")
        print(seed)
        size = len(key)
        while index < size:
            print(seed >> 24 & 0xff)
            print(seed >> 16 & 0xff)
            print(seed >> 8 & 0xff)
            print(seed & 0xff)
            test_byte = seed & 0xff
            #if test_byte & 0x80 == 0x80:
            #    test_byte = test_byte | sign_extend
            #test_byte = (((test_byte) << 24) >> 24)
            print("Index: " + str(index))
            if test_byte != key[index]:
                self.locked = True
            seed = (self.A * seed + self.C) % self.M
            print(test_byte)
            print(key[index])
            print("New Seed")
            print(seed)
            index = index + 1

    def isLocked(self):
        return self.locked

    
