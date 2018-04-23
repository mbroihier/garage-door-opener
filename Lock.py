'''
Created on Apr 16, 2018

@author: broihier
'''

class Lock(object):
    '''
    Creates and uses a lock object
    '''
    MODULO = 214326
    SLOPE = 1807
    OFFSET = 45289


    def __init__(self, key, last_seed):
        '''
        Constructor
        '''
        self.real_key = bytearray()
        self.real_key.append(key[0])
        self.real_key.append(key[1])
        self.real_key.append(key[2])
        self.real_key.append(key[3])
        self.locked = False
        seed = int((key[0] << 24) + ((key[1] << 16) & 0xff0000) +
                   ((key[2] << 8) & 0xff00) + (key[3] & 0xff))
        #important to limit initial seed
        seed = seed % self.MODULO
        if seed > last_seed and last_seed != 0:
            self.last_seed = seed
            size = seed % 7 + 5
            index = 4
            seed = (self.SLOPE * seed + self.OFFSET) % self.MODULO
            while index < size and size == len(key):
                test_byte = seed & 0xff
                self.real_key.append(test_byte)
                if test_byte != key[index]:
                    self.locked = True
                seed = (self.SLOPE * seed + self.OFFSET) % self.MODULO
                index = index + 1
        else:
            self.locked = True
            self.last_seed = seed

    def is_locked(self):
        '''
        Returns True if the lock is locked
        '''
        return self.locked

    def get_real_key(self):
        '''
        Returns what the key should be given the initial seed
        '''
        return self.real_key

    def get_last_seed(self):
        '''
        Returns the seed that was used to generate the key
        '''
        return self.last_seed
