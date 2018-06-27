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
    MAX_LIST_SIZE = 1000


    def __init__(self, key, last_seed):
        '''
        Constructor
        '''
        self.key_list = []
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
            while index < size:
                test_byte = seed & 0xff
                self.real_key.append(test_byte)
                if size != len(key) or test_byte != key[index]:
                    self.locked = True
                seed = (self.SLOPE * seed + self.OFFSET) % self.MODULO
                index = index + 1
        else:
            self.locked = True
            self.last_seed = seed
        self.key_list.append(self.real_key)

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

    def check_another_key(self, key):
        '''
        Checks a key to see if it could be for this lock - given
        the seed, the corrects bytes must follow and the key must
        not be a member of recently used keys.
        '''
        if len(key) < 5:
            #This can not be a key, set the lock to locked and return
            print("key is too short")
            print(key)
            self.locked = True
            return False

        candidate_key = bytearray()
        candidate_key.append(key[0])
        candidate_key.append(key[1])
        candidate_key.append(key[2])
        candidate_key.append(key[3])
        self.locked = False
        seed = int((key[0] << 24) + ((key[1] << 16) & 0xff0000) +
                   ((key[2] << 8) & 0xff00) + (key[3] & 0xff))
        #important to limit initial seed
        seed = seed % self.MODULO

        if self.not_in_list(key):
            self.last_seed = seed
            size = seed % 7 + 5
            index = 4
            seed = (self.SLOPE * seed + self.OFFSET) % self.MODULO
            while index < size:
                test_byte = seed & 0xff
                candidate_key.append(test_byte)
                if size != len(key) or test_byte != key[index]:
                    self.locked = True
                seed = (self.SLOPE * seed + self.OFFSET) % self.MODULO
                index = index + 1
            self.key_list.append(candidate_key)
            if len(self.key_list) > self.MAX_LIST_SIZE:
                self.key_list.pop(0)
            self.real_key = candidate_key
            return True
        else:
            self.locked = True
            self.last_seed = seed
            return False

    def not_in_list(self, key):
        '''
        Check the key with prior keys, report if found
        '''
        for old_key in self.key_list:
            if len(old_key) == len(key):
                index = 0
                for old_key_byte in old_key:
                    if old_key_byte != key[index]:
                        break
                    else:
                        index = index + 1
                if index == len(key):
                    print("key is in the list of previously seen keys")
                    return False
        print("key is not in the list of previously seen keys")
        return True
