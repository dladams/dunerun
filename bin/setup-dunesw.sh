# setup-dunesw.sh
#
# David Adams
# March 2022
#
# Script to set up dunesw under different scenarios depending on the value
# of the first positional argument _REL. If this argument contains '/', it
# is interpreted as a directory or file name. The action to take depends on
# _REL:
# -- If a file name ending '.sh', the file is sourced
# -- If a directory containing dunesetup.sh, then setup assuming build
#    with [dune-dev](https://github.com/dladams/dune-dev) is done.
# -- If a directory containing setup.sh, then that file is sourced.
# -- If no '/' is found then dunesw version VERS with qualifier QUAL is set
#    up from cvmfs. Those values are obrtained assuming that _REL is VERS:QUAL
#    or VERS:DEFQUAL with the latter defined below (and subject to change).

DEFQUAL=${DUNE_QUAL:-e20:prof}
_REL=$1
if [ -z "$_REL" ]; then
  _REL=$DUNE_VERSION
  if [ -n "$_REL" ]; then
    _REL=$_REL:$DUNE_QUAL
  fi
fi

DRELDIR=
RELDIR=
RELFIL=
if grep '/' <(echo $_REL) 2>&1 1>/dev/null; then
  if [ -d $_REL ]; then
    if [ -r $_REL/dunesetup.sh ]; then
      DRELDIR=$_REL
    elif [ -r $_REL/setup.sh ]; then
      RELFIL=$_REL/setup.sh
    else
      echo setup-dunesw.sh: ERROR: Not a build directory: $_REL >&2
    fi
  else
    if [ -r $_REL ]; then
      RELFIL=$_REL
    else
      echo setup-dunesw.sh: ERROR: Setup file not found: $_REL >&2
    fi
  fi
  _REL=
fi

if [ -n "$DRELDIR" ]; then
  echo setup-dunesw.sh: Setting up with dune-dev at $DRELDIR >&2
  source $DRELDIR/dunesetup.sh
  source $DRELDIR/run.sh
elif [ -n "$RELFIL" ]; then
  echo setup-dunesw.sh: Setting up with $DRELDIR >&2
  source $RELFIL
elif [ -n "$_REL" ]; then
  VERS=$(echo $_REL | sed 's/:.*//g')
  QUAL=${REL:$((${#VERS}+1))}
  if [ -z "$QUAL" ]; then
    QUAL=$DEFQUAL
  fi
  if [ -n "$VERS -a -n "$QUAL"" ]; then
    echo setup-dunesw.sh: Setting up dunesw $VERS $QUAL >&2
    source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh >/dev/null
    setup dunesw $VERS -q $QUAL >/dev/null
  else
    echo setup-dunesw.sh: ERROR: Invalid release:quailifier: $1 >&2
  fi
else
  echo setup-dunesw.sh: ERROR: Version not determined >&2
fi
