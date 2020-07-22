from KnitCrypter import knitpattern,handlemethod,equals,notequals
from random import choice,randint
from datetime import datetime
from sys import stdout,stdin
from math import floor,ceil
import time,string

@handlemethod('debug')
def powerof(x,b):
    return x**b

iters = int(input("number of iterations: "))

base_options = [x for x in range(2,11)] + [hex,int,oct]
func_options = [equals,notequals,powerof]

#strings
l = string.ascii_lowercase
u = string.ascii_uppercase
p = string.punctuation
s = ' '

braid = s+l+u+p

run_animation = [
    '[/]',
    '[-]',
    '[\\]',
    '[|]'
]

time_options = [
    "LIGHTSPEED",
    "seconds",
    "minutes",
    "hours"
]

def performance_case():
    base = choice(base_options)
    func = choice(func_options)
    arg = randint(1,10)

    start = time.time()
    knitpattern(braid,base,func,arg)
    return time.time() - start

def performance_status(current_inter,stop_inter):
    status = round((current_inter / stop_inter) * 100,2)
    frame = run_animation[floor(status) % 4]
    stdout.write(f"\r{frame} {status}% complete. {current_inter}/{stop_inter} ")
    stdout.flush()

def performance_test():
    performance_tests = []
    for i in range(iters):
        performance_status(i,iters)
        performance_tests.append(performance_case())
    stdout.write(f"\rPerfomance test complete                                 ")

    return sum(performance_tests) / iters

def completion_time(start_time):
    time_stack = []
    seconds_top = ceil(time.time() - start_time)
    seconds_bot = floor((seconds_top - round(time.time() - start_time,2)) * 100)

    while seconds_top > 0:
        next_count = seconds_top % 60
        if next_count < 10:
            time_stack.insert(0,f"0{next_count}")
        else:
            time_stack.insert(0,f"{next_count}")
        seconds_top //= 60
    
    top_time = ":".join(time_stack)
    return f"{top_time}.{seconds_bot} {time_options[len(time_stack)]}"

def main():
    performance_start = time.time()
    results = performance_test()

    performance_comp = completion_time(performance_start)
    print(f"\n{iters} iterations returned on average of {results} second(s)")
    print(f"Completed in {performance_comp}")

    return 0

if __name__ == "__main__":
    main()