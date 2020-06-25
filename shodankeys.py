#!/usr/bin/python3

import shodan
import sys
import argparse
import string
import random

#shodan api keys tester by waspy
#https://github.com/w4spy/shodan_keys_checker
#dogecoin:DBUgLF7hziKSjjEjz8cqayXWfFiwv8fNhY

free = []
paid = []
 
def test_key(key):
    test =shodan.Shodan(key)
    try:
        resault = test.info()
        resault = resault["plan"]
        if resault == "oss":
            return "Free"
        elif resault == "dev" or resault == "edu":
            return "Paid"
    except Exception:
        return "Invalid"

def generate():
    lettersAndDigits = string.ascii_letters + string.digits
    yield ''.join((random.choice(lettersAndDigits) for i in range(32)))

def register(value,key):
    if value == "Free":
        free.append(key)
        print(f"+\r {key} is free      ")
    elif value == "Paid":
        paid.append(key)
        print(f"+\r {key} is paid      ")
    else:
        sys.stdout.write(f"\r- {key} is invalid!")
        sys.stdout.flush()

def output():
    memory = ""
    if len(free)>0:
        memory += (f"\n--------found {len(free)} free keys--------")
        for i in free:
            memory += ("\n"+i)
        memory += ("\n---------------------------------\n")
    if len(paid)>0:
        memory += (f"\n--------Found {len(paid)} paid keys--------")
        for j in paid:
            memory += ("\n"+j)
        memory += ("\n---------------------------------\n")
    return memory

def save(save_to):
    with open(save_to, "w") as w:
        w.write(output())
    w.close

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate', type=int,dest="number_of_keys")
    parser.add_argument('-l', '--load', dest="file", help="load keys from a file")
    parser.add_argument('-o', '--output', dest="save_to_disk")
    args = parser.parse_args()

    if args.number_of_keys:
        print(f"+ testing {args.number_of_keys} random keys (u have a better chance to win the lottery than this)")
        for _ in range(args.number_of_keys):
            register(test_key(next(generate())),next(generate()))
    elif args.file:
        with open(args.file, "r") as f:
            for key in f.readlines():
                register(test_key(key.strip()),key.strip())
    else:
        parser.print_help()

    if args.save_to_disk:
        save(args.save_to_disk)
        
if __name__ == "__main__":
    main()
    print(output())