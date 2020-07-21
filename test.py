from KnitCrypter import knitpattern,handlemethod,equals,notequals
from random import choice,randint
from sys import stdout
from math import floor
import time,string

@handlemethod('debug')
def powerof(x,b):
    return x**b

iters = 10000

base_options = [x for x in range(2,11)] + [hex,int,oct]
func_options = [equals,notequals,powerof]

#strings
l = string.ascii_lowercase
u = string.ascii_uppercase
p = string.punctuation
s = ' '

braid = s+l+u+p

def performance_test():
    base = choice(base_options)
    func = choice(func_options)
    arg = randint(1,10)

    start = time.time()
    knitpattern(braid,base,func,arg)
    return time.time() - start

def performance_status(current_interval,stop_interval):
    status = floor((current_interval / stop_interval) * 100)
    stdout.write(f"\r{status}% complete")

def main(*args):
    performance_tests = []
    for i in range(iters):
        performance_status(i,iters)
        performance_tests.append(performance_test())
    stdout.write(f"\rperfomance test complete")
    
    perf_avg = sum(performance_tests) / iters
    print(f"\n{iters} iterations returned on average of {perf_avg} second(s)")

if __name__ == "__main__":
    main()