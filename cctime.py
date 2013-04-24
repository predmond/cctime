#!/usr/bin/env python
import argparse
import fcntl
import os
import subprocess
import sys
import time

def compile(cc, opts, args):
  cmd = '%s %s %s %s' % (cc,
                         '' if opts.c is None else '-c %s' % opts.c,
                         '' if opts.o is None else '-o %s' % opts.o,
                         ' '.join(args))
  status = subprocess.call(cmd, shell=True)
  if status:
    sys.exit(status)

def time_compile(n, cc, opts, args):
  timings = []
  for i in range(n):
    t = time.time()
    compile(cc, opts, args)
    timings.append(time.time() - t)
  return timings

def time_compiler(n, cc, opts, args):
  syntax_timings = time_compile(n, cc, opts, args + ['-fsyntax-only'])
  timings = time_compile(n, cc, opts, args)
  return syntax_timings, timings

def main():
  # Parse the args as "cc ..."
  parser = argparse.ArgumentParser()
  parser.add_argument('-n', type=int, default=1,
                      help='number of times to compile')
  parser.add_argument('--ref', type=str, default=None,
                      help='path to reference compiler executable')
  parser.add_argument('csv',
                      help='path to output csv file (will be appended)')
  parser.add_argument('cc', 
                      help='path to compiler executable')
  parser.add_argument('cc_args', nargs=argparse.REMAINDER,
                      help='compilation arguments passed to cc')
  (opts, args) = parser.parse_known_args()

  # Parse the remainder args
  parser = argparse.ArgumentParser()
  parser.add_argument('-c')
  parser.add_argument('-o')
  (cc_opts, cc_args) = parser.parse_known_args(opts.cc_args)

  # re-escape strings in the cc arguments
  cc_args = [x.replace('"', '\\"') for x in cc_args]

  if cc_opts.c is None:
    # no -c to determine the file so just skip this and compile only.
    compile(opts.cc, cc_opts, cc_args)
  else:
    # time the reference compiler if requested
    if opts.ref is not None:
      syntax_ref, total_ref = time_compiler(opts.n, opts.ref, cc_opts, cc_args)
    # time the target compiler
    syntax, total = time_compiler(opts.n, opts.cc, cc_opts, cc_args)

    # open the output csv file and write the results. The file is locked
    # so it will work with make -jN.
    with open(opts.csv, 'a') as out:
      fcntl.flock(out, fcntl.LOCK_EX)
      out.write('%s' % cc_opts.c)
      def write_run(r):
        out.write(', %d, %s' % (len(r), ', '.join(str(x) for x in r)))
      write_run(syntax)
      write_run(total)
      if opts.ref is not None:
        write_run(syntax_ref)
        write_run(total_ref)
      out.write('\n')
      fcntl.flock(out, fcntl.LOCK_UN)
  
  sys.exit(0)

if __name__ == '__main__':
  main()
