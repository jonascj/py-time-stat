#!/usr/bin/env python 
import argparse
import subprocess
import os
import tempfile
from numpy import std, mean
from math import sqrt

# Arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-c", "--command", type=str, required=True,
        help="Command to time. Remember to think about relative and absolute paths.")

parser.add_argument("-n", "--runs", type=int, required=True, 
        help="Number of timing runs to base the average and variance on.")

parser.add_argument("-o", "--stdout", action="store_true",
        help="Print stdout from each command invocation.")

parser.add_argument("-e", "--stderr", action="store_true",
        help="Print stdout from each command invocation.")

args = parser.parse_args()

# Temp file setup
fi, fpath = tempfile.mkstemp(suffix='.out', prefix='py-time-stat-', dir='/tmp')

# Command to run
# %realtime;%usercpu;%kernelcpu
# http://man7.org/linux/man-pages/man1/time.1.html
cmd = '/usr/bin/time -f "%e;%U;%S" -a -o {} {}'.format(fpath, args.command)

# stdout and stderr
devnull = open(os.devnull, 'wb')

if args.stdout:
    _stdout = stdout=subprocess.PIPE
else:
    _stdout = devnull

if args.stderr:
    _stderr = subprocess.PIPE
else:
    _stderr = devnull


# Loop and time execution    
for i in range(1,args.runs+1):
    
    print "Run #{}".format(i)

    p = subprocess.Popen(cmd, shell=True, stdout=_stdout, stderr=_stderr)
    p.wait()
    if args.stdout:
        print "STDOUT:\n{}".format(p.stdout.read())

    if args.stderr:
        print "STDERR:\n{}".format(p.stderr.read())

devnull.close()

# Parse the file outputted by /usr/bin/time
with open(fpath) as f:
    lines = f.readlines()

treal = []
tuser = []
tkernel = []

for l in lines:
    tr, tu, tk = [float(x) for x in l.split(';')]
    treal.append(tr)
    tuser.append(tu)
    tkernel.append(tk)

os.remove(fpath)

# Output statistics
print "Real:\t{:.4E} +/- {:.4E} s".format(mean(treal), std(treal)/sqrt(len(treal)))
print "User:\t{:.4E} +/- {:.4E} s".format(mean(tuser), std(tuser)/sqrt(len(tuser)))
print "Kernel:\t{:.4E} +/- {:.4E} s".format(mean(tkernel), std(tkernel)/sqrt(len(tkernel)))



