#!/usr/bin/python

# 5-line fuzzer below is from Charlie Miller's
# "Babysitting an Army of Monkeys":
# Part 1 - http://www.youtube.com/watch?v=Xnwodi2CBws
# Part 2 - http://www.youtube.com/watch?v=lK5fgCvS2N

import math
import random
import string
import subprocess
import time
import os

content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Phasellus sollicitudin condimentum libero,
sit amet ultrices lacus faucibus nec.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Cum sociis natoque penatibus et magnis dis parturient montes,
nascetur ridiculus mus. Cras nulla nisi, accumsan gravida commodo et,
venenatis dignissim quam. Mauris rutrum ullamcorper consectetur.
Nunc luctus dui eu libero fringilla tempor. Integer vitae libero purus.
Fusce est dui, suscipit mollis pellentesque vel, cursus sed sapien.
Duis quam nibh, dictum ut dictum eget, ultrices in tortor.
In hac habitasse platea dictumst. Morbi et leo enim.
Aenean ipsum ipsum, laoreet vel cursus a, tincidunt ultrices augue.
Aliquam ac erat eget nunc lacinia imperdiet vel id nulla."""


# defined app
app = [
    "\Program Files\Microsoft Office\Office14\WINWORD.EXE"
    ]

fuzz_output = "fuzz.txt"

FuzzFactor = 244
num_tests = 10000

########### end configuration ##########


crashes = {}

for i in range(num_tests):

    buf = bytearray(content)
	
	# start Charlie Miller code
    numwrites=random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)
    #end Charlie Miller code

    with open(fuzz_output, "w") as f:
        f.write(buf)
	
    print "Opening file with app '%s', %d bytes changed" % (app, numwrites)
    p = subprocess.Popen([app, fuzz_output])
    time.sleep(3)
 
    crashed = p.poll()
    if not crashed:
        p.terminate()
    else:
        crashes[app] += 1
 
 
print "Test summary"
print "=" * 40
for app, count in crashes.items():
    print "App '%s' crashed %d times." % (app, count)