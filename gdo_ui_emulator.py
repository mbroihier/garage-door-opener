'''
Created on Jun 16, 2018

@author: broihier
'''
import random
import sys
import Lock

def check_bytes(b1, b2):
    '''
    Check byte arrays for equality
    '''
    if len(b1) != len(b2):
        return False
    index = 0
    for b1_byte in b1:
        if b1_byte != b2[index]:
            return False
        else:
            index = index + 1
    return True

class GDOEmulator(object):
    '''
    GDOEmulator class - creates a GDO user interface emulator for creating
    test cases for the GDO controller
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.save_patterns = []


    def string_to_byte_stream(self, data):
        '''
        Convert a string of hex digits to a byte stream
        '''
        data_bytes = bytearray()
        ascii_bytes = data.strip().split(" ")
        for ascii_byte in ascii_bytes:
            data_bytes.append(bytes.fromhex(ascii_byte)[0])
        return data_bytes

    def byte_stream_to_string(self, data):
        '''
        Covert a byte stream into ASCII hex string
        '''
        ascii_bytes = ""
        for a_byte in data:
            ascii_byte = "{:2x} ".format(a_byte)
            if a_byte < 0x10:
                ascii_byte = "0" + ascii_byte.strip() + " "
            ascii_bytes = ascii_bytes + ascii_byte
        return ascii_bytes

    def data_based_on_control_type(self, control_type, data):
        '''
        Process the data based on the control type
        '''
        if control_type == "free form":
            return data
        if control_type == "valid":
            byte_stream = self.string_to_byte_stream(data)
            lock = Lock.Lock(byte_stream, 1)
            byte_stream_string = self.byte_stream_to_string(lock.get_real_key())
            self.save_patterns.append(byte_stream_string)
            return byte_stream_string
        if control_type == "valid but extra":
            byte_stream = self.string_to_byte_stream(data)
            lock = Lock.Lock(byte_stream, 1)
            key = lock.get_real_key()
            key.append(random.randrange(0, 255))
            byte_stream_string = self.byte_stream_to_string(key)
            return byte_stream_string
        if control_type == "valid but short":
            byte_stream = self.string_to_byte_stream(data)
            lock = Lock.Lock(byte_stream, 1)
            key = lock.get_real_key()
            del key[-1]
            byte_stream_string = self.byte_stream_to_string(key)
            return byte_stream_string
        if control_type == "random":
            length = random.randrange(1, 1000) + 1024
            byte_stream = bytearray()
            for index in range(length):
                byte_stream.append(random.randrange(0, 255))
            byte_stream_string = self.byte_stream_to_string(byte_stream)
            return byte_stream_string
        print("control file error - unknow control type: " + control_type)
        exit(-1)

    def gdo_ui_emulator(self, control_path):
        '''
        Run the GDO user interface emulator
        '''
        file_object = open(control_path, "r")
        line = file_object.readline().strip()
        if line != "":
            test_category_title = line
        else:
            print("file open error: " + control_path)
            exit(-1)
        identification = open(test_category_title + ".testDbID", "w")
        objective = open(test_category_title + ".testDbObjective", "w")
        pre = open(test_category_title + ".testDbPre", "w")
        post = open(test_category_title + ".testDbPost", "w")
        procedures = open(test_category_title + ".testDbProcedures", "w")
        expected_results = open(test_category_title + ".testDbExpectedResults", "w")
        results = open(test_category_title + ".testDbResults", "w")
        driver = open(test_category_title + ".driver", "w")
        driver.write(test_category_title + "\n")
        long_title = file_object.readline().strip()
        description = file_object.readline().strip()
        category_information = open(test_category_title + ".testDbCategoryTitle", "w")
        category_information.write(long_title)
        category_information.close()
        category_information = open(test_category_title + ".testDbCategoryDescription", "w")
        category_information.write(description)
        category_information.close()

        test_case_number = 10
        line = file_object.readline() # read test case title
        while line != "":
            ascii_test_case_number = str(test_case_number).zfill(4)
            test_case_id = "{:s}-{:s}\n".format(test_category_title, ascii_test_case_number)
            identification.write(test_case_id)
            identification.write(line)

            line = file_object.readline() # read objective line
            requirements, text = line.split(":")
            objective_test_case_id = "{:s}-{:s}: {:s}\n".format(test_category_title, ascii_test_case_number, requirements)
            objective.write(objective_test_case_id)
            objective.write(text)
            line = file_object.readline() # read control line
            driver.write(test_case_id)
            test_type, data = line.split(":")
            data = self.data_based_on_control_type(test_type, data)
            driver.write(data.strip() + "\n")
            line = file_object.readline() # read expected results line
            expected_results.write(test_case_id)
            expected_results.write(line)
            results.write(test_case_id)
            results.write("UNTESTED\n")
            pre.write(test_case_id)
            pre.write(data.strip() + "\n")
            post.write(test_case_id)
            post.write("\n")
            procedures.write(test_case_id)
            procedures.write("/step This test case will be executed using the GDO driver via the " + test_category_title + ".driver file.  The byte stream shown in the setup section will be sent by the driver and should produce the expected results shown in the expected results section.\step\n")


            line = file_object.readline() # read next test case title

            test_case_number = test_case_number + 10

if __name__ == "__main__":
    GDO = GDOEmulator()
    GDO.gdo_ui_emulator(sys.argv[1])
