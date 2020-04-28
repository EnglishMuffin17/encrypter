from encrypter import encrypter
import random
import time

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

        charObj.CHARACTERS["BRAIDED"] = braided_string

class Encoder:

    def __init__(self,key,baseObj):
        self.key = key
        self.baseObj = baseObj
    
    def encoder(self,string):

        def encode(char):
            if self.key.__contains__(char):
                return self.key[char]

        encoded_string = [encode(c) for c in string]
        return "".join(encoded_string)

    def decoder(self,string):
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
        
        return "".join(decoded_string)

def main():
    char_test = encrypter.CharGenerator()
    base_test = encrypter.BaseConverter(9)

    #Create a new strand and add it to the CharGenerator object
    Knots.fBraid(char_test)
    char_test.setStitch("NOTEQUALS","BRAIDED",STEP=3,OFFSET=2,ROTATION=-45)
    char_test.strand("BRAIDED")

    #Grab the strand to assign new values
    braids = char_test.getStrandedDict("BRAIDED")

    #Create a mask using random.choice, convert strand values to a base count
    fill_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?&%#!@-'
    neg_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?&%#!@-'
    for key in braids:
        fill_char = random.choice(fill_chars)
        neg_char = random.choice(neg_chars)

        value = base_test.baseConverter(braids[key],fill_char=fill_char,neg_char=neg_char)
        value = [x for x in value]
        braids[key] = value
    
    #Ensure all values are the same length using mask
    length = base_test.getMaxLength()
    for key in braids:
        fill_char = random.choice(fill_chars)
        value = base_test.testLength(braids[key],length,char=fill_char,inserts=True)
        braids[key] = value

    #Use strand as a key for an Encoder object
    control = Encoder(braids,base_test)
    mystring = "Banana Boats"

    mystring_encoded = control.encoder(mystring)
    mystring_decoded = control.decoder(mystring_encoded)
    
    print(f"mystring: {mystring} [length: {len(mystring)}]")
    print(f"Encoded: {mystring_encoded}")
    print(f"Decoded: {mystring_decoded} [length: {len(mystring_decoded)}]")

if __name__ == "__main__":
    start = time.time()
    main()
    finish = time.time()
    t_time = round(finish - start,4)
    print(f"Finished script in {t_time} seconds")