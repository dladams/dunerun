XRDIR_TOM=/dune/app/users/trj/xrootd542/install/lib64
XRDIR_LOC=$HOME/lib/xrootd542/lib64

if [ -r $XRDIR_TOM ]; then
  XRDIR=$XRDIR_TOM
elif [ -r $XRDIR_LOC ]; then
  XRDIR=$XRDIR_LOC
else
  #TARFIL=xrootd542.tar.gzdd
  #SRC=dunegpvm01.fnal.gov:$TARFIL
  TARFIL=xrd542.tgz
  SRC=dunegpvm01.fnal.gov:/dune/app/users/trj/xrootd542/$TARFIL
  DST=$(dirname $XRDIR_LOC)
  echo Copying $SRC to $DST
  mkdir -p $DST
  scp $SRC $DST
  SAVEPWD=$(pwd)
  cd $DST
  echo Untarring
  tar -zxf $TARFIL
  mv install/* .
  rmdir install
  cd $SAVEPWD
  if [ -r $XRDIR_LOC ]; then
    XRDIR=$XRDIR_LOC
  else
    echo Copy failed.
    exit 1
  fi
fi

export LD_LIBRARY_PATH=$XRDIR:${LD_LIBRARY_PATH}
export LD_PRELOAD=$XRDIR/libXrdPosixPreload.so:${LD_PRELOAD}
echo WARNING: xrd542 is obsolete. Please switch to xrdhdf5.
