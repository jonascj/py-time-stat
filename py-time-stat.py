import argparse
import subprocess
import os
import tempfile

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
