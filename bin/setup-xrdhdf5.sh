# setup-xrdhdf5.sh
#
# Set up the test version of xrootd that has hdf5 streaming enabled.
# We require the use have already set up xrootd and prepend streaming
# libs the same version and flavor to LD_LIBRARYPATH and LD_PRELOAD.

LIBNAM=libXrdPosixPreload.so
if [ -n "$XROOTD_LIB" ]; then
  if [ ! -r $XROOTD_LIB ]; then
    echo setup-xrdhdf5: ERROR: Directory not found: $XROOTD_LIB >&2
  elif [ ! -r $XROOTD_LIB/$LIBNAM ]; then
    echo setup-xrdhdf5: ERROR: Library not found: $XROOTD_LIB/$LIBNAM >&2
  else
    export LD_PRELOAD=$XROOTD_LIB/$LIBNAM:${LD_PRELOAD}
  fi
else
  echo setup-xrfhdf5: ERROR: Please first set up xrootd, e.g. from dunesw. >&2
fi

