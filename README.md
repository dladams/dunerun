# dunerun
David Adams  
March 2022  
  
Support for using DUNE software from the linux command line and python.

## Installation and set up
To install this package at MY-INSTALL-PATH:
<pre>
cd any-directory
git clone https://github.com/dladams/dunerun.git
./dunerun/build -i MY-INSTALL-PATH
</pre>
The option can be omitted if you have defined env variable DUNE_INSTALL_DIR.

To set up to use the package in this or any future session:
<pre>
source MY-INSTALL-PATH/setup.sh
</pre>

## Running from the linux command line
After the above setup, the command *dune-run* is available. To see the current options use the -h option:
<pre>
> dune-run -h
Usage: /home/dladams/proc/install/common/dunerun/bin/dune-run [-e ENV] [-r REL] [-d LEVEL] COM
Runs command COM in the environment defined by "source setup-ENV.sh REL"
  ENV - Environment name.
        Provided here:
          dune - Sets up dune w/o any packages.
          dunesw - Sets up dune w/ dunesw with argument REL
        If undefined or '.', the command is run without setup.
        Default is env variable DUNESW_SUPPORT_ENV or dunesw.
  REL - Release tag passed to the environment setup script.
        For dunesw, this can be
          -- VERS or VERS:QUAL where VERS is the version and QUAL is the
             qualifier (e.g. v09_42_03_00 or v09_42_03_00:c7:prof),
          -- the path to file that sets up a local build or installation
             of dunesw, or
          -- the path to a directory holding a local build made with
             dune-dev (See https://github.com/dladams/dune-dev)
        Default is env variable DUNESW_SUPPORT_RELEASE or a recent release.
  LEVEL - 0 - Command is executed with no output from this script or
              from the setup (default)
          1 - Command is executed with informational messages.
          2 - Command and infomational messages are displayed w/o execution.
Command 'shell' starts an interactive bash shell in the environment.
</pre>
The environment *dune* locates the DUNE/larsoft software without setting up any packages. This is useful for issuing the usual ups command to see what packages are available, e.g.
<pre>
> dune-run -e dune ups list -aK+ dunesw
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_41_00_02" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_00_01" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_02_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_03_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "c7:prof" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_03_01" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "debug:e20" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "e20:prof" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "c7:debug" "" 
"dunesw" "v09_42_04_00" "Linux64bit+3.10-2.17" "c7:prof" ""
</pre>

The environment *dunesw* sets up the specified version of that top-level DUNE package. For example, one can then ask for help:
<pre>
> dune-run -e dunesw -r v09_42_04_00:e20:prof duneHelp
Welcome to dunetpc 
Some available commands:
              duneHelp - Display information about the current setup of dunetpc.
                   lar - Run the art/larsoft event looop e.g. to process event data.
  product_sizes_dumper - Display the products and size in an event data file.
               fcldump - Display the resolved configuration for a fcl file.
               liblist - List available plugin libraries.
        pdChannelRange - Display protoDUNE channel grops and ranges.
           duneRunData - Display run data for a run.
           duneTestFcl - Test some high-level fcl configurations.
Use option "-h" with any of these for more information.
</pre>
Or run the fcl tests:
<pre>
> dune-run -e dunesw -r v09_42_04_00:c7:prof duneTestFcl
iceberg3_decode_reco.fcl is ok
iceberg4a_decode_reco.fcl is ok
iceberg4b_decode_reco.fcl is ok
iceberg5_decode_reco.fcl is ok
standard_reco_dune10kt_nu_1x2x6.fcl is ok
vdcoldbox_raw_dataprep.fcl is ok
vdcoldbox_raw_tdedataprep.fcl is ok
hdcoldbox_raw_dataprep.fcl is ok
protodune_dqm.fcl is ok
protodune_dqm2.fcl is ok
iceberg3_dqm1.fcl is ok
iceberg4_dqm1.fcl is ok
iceberg5cond_dqm1.fcl is ok
All 13 fcl files processed successfully.
</pre>

Significant time is required to set up up the *dunesw* environment when the each above commands are run. Use the special command 'shell' to start an interactive shell in the specified environment so this set up only has to be performed once. For example:
<pre>
> dune-run -e dunesw -r v09_42_04_00:c7:prof shell
dunesw-v09_42_04_00:c7:prof> duneHelp
Welcome to dunetpc 
Some available commands:
              duneHelp - Display information about the current setup of dunetpc.
                   lar - Run the art/larsoft event looop e.g. to process event data.
  product_sizes_dumper - Display the products and size in an event data file.
               fcldump - Display the resolved configuration for a fcl file.
               liblist - List available plugin libraries.
        pdChannelRange - Display protoDUNE channel grops and ranges.
           duneRunData - Display run data for a run.
           duneTestFcl - Test some high-level fcl configurations.
Use option "-h" with any of these for more information.
dunesw-v09_42_04_00:c7:prof> duneTestFcl
iceberg3_decode_reco.fcl is ok
iceberg4a_decode_reco.fcl is ok
iceberg4b_decode_reco.fcl is ok
iceberg5_decode_reco.fcl is ok
standard_reco_dune10kt_nu_1x2x6.fcl is ok
vdcoldbox_raw_dataprep.fcl is ok
vdcoldbox_raw_tdedataprep.fcl is ok
hdcoldbox_raw_dataprep.fcl is ok
protodune_dqm.fcl is ok
protodune_dqm2.fcl is ok
iceberg3_dqm1.fcl is ok
iceberg4_dqm1.fcl is ok
iceberg5cond_dqm1.fcl is ok
All 13 fcl files processed successfully.
dunesw-v09_42_04_00:c7:prof> exit
exit
>
</pre>

## Using a local build
It is possible to use the *dunesw* environment with a local build by specifying the release with the path to a setup file or to a build directory constructed with [dune-dev](https://github.com/dladams/dune-dev). Here is an example using my standard development area:
<pre>
dunerun> dune-run -e dunesw -r ~dladams/proc/build/dev01 shell
Setting up with dune-dev at /home/dladams/proc/build/dev01
dunesw-/home/dladams/proc/build/dev01> duneHelp
Welcome to dunetpc 
Some available commands:
              duneHelp - Display information about the current setup of dunetpc.
                   lar - Run the art/larsoft event looop e.g. to process event data.
  product_sizes_dumper - Display the products and size in an event data file.
               fcldump - Display the resolved configuration for a fcl file.
               liblist - List available plugin libraries.
        pdChannelRange - Display protoDUNE channel grops and ranges.
           duneRunData - Display run data for a run.
           duneTestFcl - Test some high-level fcl configurations.
Use option "-h" with any of these for more information.
dunesw-/home/dladams/proc/build/dev01> duneTestFcl
iceberg3_decode_reco.fcl is ok
iceberg4a_decode_reco.fcl is ok
iceberg4b_decode_reco.fcl is ok
iceberg5_decode_reco.fcl is ok
standard_reco_dune10kt_nu_1x2x6.fcl is ok
vdcoldbox_raw_dataprep.fcl is ok
vdcoldbox_raw_tdedataprep.fcl is ok
hdcoldbox_raw_dataprep.fcl is ok
protodune_dqm.fcl is ok
protodune_dqm2.fcl is ok
iceberg3_dqm1.fcl is ok
iceberg4_dqm1.fcl is ok
iceberg5cond_dqm1.fcl is ok
All 13 fcl files processed successfully.
dunesw-/home/dladams/proc/build/dev01> exit
exit
dunerun> 
</pre>

## Building analysis packages
Like this package, most of my analysis packages provide a script *build* that can be used to build and install that package. In most cases, the build is on top of DUNE software and requires setup of some development packages including *cmake*. The environment *dunebuild* sets up *dunesw* and those develpment packages. Here is an example session installing [duneproc](https://github.com/dladams/duneproc).
<pre>
[dladams@jupyter-dladams ~]$ source $HOME/proc/install/common/dunerun/setup.sh

[dladams@jupyter-dladams ~]$ cd $HOME/proc/pkgs

[dladams@jupyter-dladams pkgs]$ git clone https://github.com/dladams/duneproc.git
Cloning into 'duneproc'...
remote: Enumerating objects: 985, done.
remote: Counting objects: 100% (557/557), done.
remote: Compressing objects: 100% (376/376), done.
remote: Total 985 (delta 389), reused 303 (delta 179), pack-reused 428
Receiving objects: 100% (985/985), 180.69 KiB | 2.47 MiB/s, done.
Resolving deltas: 100% (628/628), done.

[dladams@jupyter-dladams pkgs]$ dune-run -e dunebuild -r v09_44_00_02 shell
Setting up dunesw v09_44_00_02 e20:prof

dunebuild-v09_44_00_02> duneproc/build


Source: /home/dladams/proc/pkgs/duneproc
Build: /home/dladams/tmp/build/v09_44_00_02/duneproc
Install: /home/dladams/proc/install/v09_44_00_02/duneproc

Running cmake in /home/dladams/proc/pkgs/duneproc...
      CMAKE_CXX_COMPILER: /cvmfs/larsoft.opensciencegrid.org/products/gcc/v9_3_0/Linux64bit+3.10-2.17/bin/c++
 CMAKE_CXX_COMPILE_FLAGS: 
         CMAKE_CXX_FLAGS: -std=c++17
Start building dictionaries
-- Configuring done
-- Generating done
-- Build files have been written to: /home/dladams/tmp/build/v09_44_00_02/duneproc

Building...
[  8%] Generating duneproc.cxx, duneprocDict.rootmap
.
.
.
-- Installing: /home/dladams/proc/install/v09_44_00_02/duneproc/doc/ibRunDates.txt

dunebuild-v09_44_00_02> source $DUNE_INSTALL_DIR/duneproc/setup.sh
Setting up duneproc

dunebuild-v09_44_00_02> duneprocHelp
/home/dladams/proc/install/v09_44_00_02/duneproc/bin/duneprocHelp OPT
  OPT = general for general commands
  OPT = pdsp for protoDUNE commands
  OPT = ib for Iceberg commands
  OPT = ibex fpr Iceberg examples
  OPT = ibex fpr Iceberg examples
</pre>
The build here is done in a *dunerun* shell instead of the *dunerun* command line. TYhis allows us to immediately setup *duneproc* and issue the help command to check the installation.

## Running from python
The python class *DuneRun* in module *dunerun* provides similar fuctionality from the python command line. For examples of use, see the [dunerun notebook](ipynb/dunerun.ipynb).

## Development plans

* Add options for timeout to deal with flaky filesystems like cvmfs.
* Add command dune-install-dir that returns DUNE_INSTALL_VERSION with %VERSION% replaced with DUNESW_VERSION. Better dune-find-product?
* Add setup of environment plus a list of ups packages. Update *dunebuild* to use this.
* Add setup of environment plus a list of analysis packages from DUNE_INSTALL_DIR.
* Other suggestions welcome.
