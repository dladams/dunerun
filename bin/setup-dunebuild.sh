source setup-dunesw.sh $@
if [ -z "$DUNE_BUILD_DIR" ]; then
  echo Please define DUNE_BUILD_DIR.
elif [ -z "$DUNE_INSTALL_DIR" ]; then
  echo Please define DUNE_INSTALL_DIR.
elif [ -z "$DUNESW_VERSION" ]; then
  echo It appears the setup of dunesw failed.
else
  export DUNE_BUILD_DIR=$(echo $DUNE_BUILD_DIR | sed "s/%VERSION%/$DUNESW_VERSION/g")
  export DUNE_INSTALL_DIR=$(echo $DUNE_INSTALL_DIR | sed "s/%VERSION%/$DUNESW_VERSION/g")
  setup cmake v3_22_0
  setup studio
fi
