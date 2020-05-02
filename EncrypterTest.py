from encrypter import encrypter
import random,time,string
from math import floor

class Knots:

    @staticmethod
    def fBraid(charObj):
        strings = charObj.getCharacters()
        max_length = 0

        braided_string = ""

        for i in strings:
            if len(i) > max_length:
                max_length = len(i)

        step = 0
        while step < max_length:
            for i in strings:
                try:
                    braided_string += i[step]
                except IndexError:
                    pass
            step += 1

        charObj.CHARACTERS["fBRAIDED"] = braided_string

class Interpreter:

    def __init__(self,key,baseObj):
        self.key = key
        self.baseObj = baseObj
    
    def encoder(self,string):

        def encode(char):
            if self.key.__contains__(char):
                return self.key[char]

        encoded_string = [encode(c) for c in string]
        for i in encoded_string:
            if i == None:
                index = encoded_string.index(i)
                encoded_string.pop(index)
                encoded_string.insert(index,'\n')

        return "".join(encoded_string)

    def decoder(self,string,aglet=False):
        length = self.baseObj.getMaxLength()        

        def decode(string,step):
            sub = string[step:step+length]
            for char in self.key:
                if self.key[char] == sub:
                    return char

        decoded_string = []
        step = 0
        while (step + length) - 1 < len(string):
            decoded_string.append(decode(string,step))
            step += length
        
        if aglet == False:
            decoded_string.append("\n")
        
        return "".join(decoded_string)
    
    def fileCoder(self,path,file_mode='e'):
        test_length = self.baseObj.getMaxLength()
        file_lines = []
        match_percent = 0

        with open(file=path,mode='r') as file:
            file_lines = file.readlines()
            test_line_0 = file_lines[0]
            matches = 0
            total_count = 0

            step = 0
            while step < len(test_line_0):
                next_char = test_line_0[step:step+test_length]
                for char in self.key:
                    if next_char == self.key[char]:
                        matches += 1
                total_count += 1
                step += test_length
            try:
                match_percent = floor((matches / total_count) * 100)
                print(f"{match_percent}% match to the encryption key")
            except ZeroDivisionError:
                pass

        with open(path,mode='w') as file:
            for line in file_lines:
                if file_mode == 'e' and match_percent == 0:
                    file.write(self.encoder(line))
                elif file_mode == 'd' and match_percent in range(90,100):
                    if line != file_lines[-1]:
                        file.write(self.decoder(line))
                        continue
                    file.write(self.decoder(line,aglet=True))
                else:
                    file.write(line)

class EncrypterTest:
    base_test = encrypter.BaseConverter(8)
    char_test = encrypter.CharGenerator()
    Knots().fBraid(char_test)

    @classmethod
    def setup(cls):
        cls.char_test.setStitch("EQUALS","fBRAIDED",STEP=4,
                                OFFSET=3,ROTATION=15)
        cls.char_test.strand("fBRAIDED")
        cls.braid = cls.char_test.getStrandedDict("fBRAIDED")

    @classmethod
    def makeKey(cls):
        for char in cls.braid:
            next_char = cls.braid[char]
            next_value = cls.base_test.convert(next_char,fill_char='|',
                                                neg_char='&')
            cls.braid[char] = next_value
    
        test_length = cls.base_test.getMaxLength()
        for char in cls.braid:
            next_char = cls.braid[char]
            next_value = [c for c in next_char]
            next_value = cls.base_test.testLength(next_value,test_length,'?',
                                            inserts=True)
            cls.braid[char] = "".join(next_value) 

def main():
    file_path = 'test files/test.txt'
    
    EncrypterTest()
    EncrypterTest.setup()
    EncrypterTest.makeKey()

    Interpreter(EncrypterTest.braid,
                EncrypterTest.base_test).fileCoder(file_path,file_mode='e')

if __name__ == "__main__":
    start = time.time()

    main()

    finish = time.time()

    t_time = round(finish - start,4)
    print(f"Finished script in {t_time} seconds")