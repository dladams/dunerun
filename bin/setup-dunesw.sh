# setup-dunesw.sh
#
# David Adams
# March 2022
#
# Script to set up dunesw under different scenarios depending on the value
# of the first positional argument REL. If this argument contains '/', it
# is interpreted as a directory or file name. The action to take depends on
# REL:
# -- If a file name ending '.sh', the file is sourced
# -- If a directory containing dunesetup.sh, then setup assuming build
#    with [dune-dev](https://github.com/dladams/dune-dev) is done.
# -- If a directory containing setup.sh, then that file is sourced.
# -- If no '/' is found then dunesw version VERS with qualifier QUAL is set
#    up from cvmfs. Those values are obrtained assuming that REL is VERS:QUAL
#    or VERS:DEFQUAL with the latter defined below (and subject to change).

DEFQUAL=e20:prof
REL=$1

DRELDIR=
RELDIR=
RELFIL=
if grep '/' <(echo $REL) 2>&1 1>/dev/null; then
  if [ -d $REL ]; then
    if [ -r $REL/dunesetup.sh ]; then
      DRELDIR=$REL
    elif [ -r $REL/setup.sh ]; then
      RELFIL=$REL/setup.sh
    else
      echo setup-dunesw.sh: ERROR: Not a build directory: $REL >&2
    fi
  else
    if [ -r $REL ]; then
      RELFIL=$REL
    else
      echo setup-dunesw.sh: ERROR: Setup file not found: $REL >&2
    fi
  fi
  REL=
fi

if [ -n "$DRELDIR" ]; then
  echo Setting up with dune-dev at $DRELDIR >&2
  source $DRELDIR/dunesetup.sh
  source $DRELDIR/run.sh
elif [ -n "$RELFIL" ]; then
  echo Setting up with $DRELDIR >&2
  source $RELFIL
elif [ -n "$REL" ]; then
  VERS=$(echo $1 | sed 's/:.*//g')
  QUAL=${1:$((${#VERS}+1))}
  if [ -z "$QUAL" ]; then
    QUAL=$DEFQUAL
  fi
  if [ -n "$VERS -a -n "$QUAL"" ]; then
    echo Setting up dunesw $VERS $QUAL >&2
    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh >/dev/null
    setup dunesw $VERS -q $QUAL >/dev/null
  else
    echo setup-dunesw.sh: ERROR: Invalid release:quailifier: $1 >&2
  fi
fi
