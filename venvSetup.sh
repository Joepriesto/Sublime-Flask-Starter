#!/bin/bash 

$ command -v python >/dev/null 2>&1 || { echo "I require python but it's not installed.  Aborting." >&2; exit 1; }
$ command -v flump >/dev/null 2>&1 || { echo "I require flump but it's not installed.  Aborting." >&2; exit 1; }

$ command -v pip >/dev/null 2>&1 || { echo "I require pip but it's not installed.  Aborting." >&2 ; exit 1; }

echo "It worked!!!!"