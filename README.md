# dunerun

David Adams  
May 2022  
Version 1.16.0  
  
This package provides upport for using different versions of DUNE software from the linux command line and python.
It also facilitates the building and use of user packages that follw the [dunerun build convention](./build_convention.md).
In particular, it provides support to run short jobs processing DUNE data from a terminal or notebook in an jupyter server
which can then be used to immediatesly view generated image files in the same browser session.
It is regularly tested used the [FNAL analysis server](https://analytics-hub.fnal.gov).

## Installation
To install this package at \<install-path>:
<pre>
cd &lt;any-directory>
git clone https://github.com/dladams/dunerun.git
./dunerun/build -i &lt;install-path> -b &lt;build-path> -v &lt;dune-version> -q &lt;dune-qualifier>
</pre>
The command-line options may be omitted if the corresponding DUNE build env variables
specified in the [dunerun build convention](./build_convention.md) are defined.
The flag "-p false" may be added to indicate files are to be installed in shared
(rather than the default package-specific) directories.

The setup file generated by the installation exports the definitions used here for the DUNE
build env variables.
Thus sourcing this setup before building subsequent (dune-run-conformant) packages ensures those
packages will be built and installed in a consistent manner.

If the install and build path include the special fields %VERSION% and/or %QUAL%, these are
respectively replaced with rectified versions of \<dune-version> and \<dune-qualifier>.
Rectified means that colons are replaced with underscores.
The substituted values are exported in the generated setup.
The build directory is not presently used here but is specified so that it can be echoed in
the setup file and used in the build of other packages.

If the install or build paths include fields matching the rectified environment values of the version or qualifier,
then those values are also respectively replaced with \<dune-version> and \<dune-qualifier>.
Thus, setting up dunerun for one version ensures the same conventions are followed for
unspecified fields in the builds of other versions or qualifiers.
In particular, constently-named but different install and build directories are used if their names
incoporate ther DUNE version and qualifier.
To avoid this version and qualify carryover, unset DUNE_VERSION and DUNE_QUALIFIER before the build command.

## Setting up

After installation, set up to use the package in this or any future session:
<pre>
source &lt;install-path>/dunerun/setup.sh
</pre>
This assumes package-specific installation.
see the [dunerun build convention](./build_convention.md) to locate the setup file
for shared-directory installation.
In addition to adding this package's bash and python utilities to the the
caller's paths, the setup defines the DUNE build env variables as discussed above.

## Running from the linux command line
After the above setup, the dunerun commands are available. For information about dunerun:
<pre>
[dladams@jupyter-dladams console]$ dunerunHelp
This is dunerun version 1.16.0

It provides the following commands:
  dunerunHelp: This message.
  dunerunVersion: Show package version number.
  dunerunRelease: Show the DUNE version and qualifier.
  dune-run: Run a command in dune environments.
  dune-timeout: Run command with a timeout.
  dunerun-check-proxy: Check and, if needed, get VOMS proxy.
  dunerun-check-cvmfs: Check if cvmfs dirs are mounted.
  dunerun-test-all: Test dune installation and environment.
Use option -h for help with any of these.

The following classes are provided in python module dunerun:
  dunerun.DuneRun: Run a command in dune environments.
  dunerun.DuneProxy: Manage VOMS proxy.
</pre>
To learn more about the command *dune-run*, use the -h option:
<pre>
duneproc> dune-run -h
Usage: /home/dladams/proc/install/v09_46_00_00/dunerun/bin/dune-run [-e ENV] [-r REL] [-d LEVEL] COM
Runs command COM in the environment defined by "source setup-ENV.sh REL"
  ENV - Environment name is any of
          dune - Sets up dune w/o any packages.
          dunesw - Sets up dune w/ dunesw with argument REL.
          dunebuild - Sets up dunesw with argument REL plus packages
                      needed to build other DUNE packages (cmake, studio).
          pkgname - Name of any package installed alngside dunerun.
          dunex,pkg1,pkg2... - Where dunex is any of dune, dunesw, dunebuild
                               or omitted and pkgi is any of pkgname.
        If undefined or '.', the command is run without setup.
        Default is dunesw.
  REL - Release tag passed to the environment setup script.
        For dunesw, this can be
          -- VERS or VERS:QUAL where VERS is the version and QUAL is the
             qualifier (e.g. v09_42_03_00 or v09_42_03_00:c7:prof),
          -- the path to file that sets up a local build or installation
             of dunesw, or
          -- the path to a directory holding a local build made with
             dune-dev (See https://github.com/dladams/dune-dev)
        Default is v09_46_00_00:e20:prof
  LEVEL - 0 - Command is executed with no output from this script or
              from the setup (default)
          1 - Command is executed with informational messages.
          2 - Command and infomational messages are displayed w/o execution.
Command 'shell' starts an interactive bash shell in the environment.
duneproc> 
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

If the release (-r) is omitted, then it is constructed from the DUNE version and qualifiers specified when *dunerun* was installed.

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
Like this package, most of my analysis packages provide a script *build* that can be used to build and install that package. In most cases, the build is on top of DUNE software and requires setup of some development packages including *cmake*. The environment *dunebuild* sets up *dunesw* and those development packages. Here is an example session installing [duneproc](https://github.com/dladams/duneproc).
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
The build here is done in a *dunerun* shell instead of the *dunerun* command line. This allows us to immediately setup *duneproc* and issue the help command to check the installation.

## Using analysis packages
The environment specified on the *dune-run* command line may include multiple packages specified in a comma-separated list.
For example, to set up *dunesw* and *duneproc* and then check the version for the latter:
<pre>
dunerun> dune-run -e dunesw,duneproc shell
setup-dunesw.sh: Setting up dunesw v09_46_00_00 e20:prof
duneproc> duneprocVersion
2.0.0
</pre>
This is a convenient way to set up one or more analysis packages that depend on *dunesw*. 

## Setting up to run without *dune-run*
The setup files provided by *dunerun* may be used directly to set up the *dunesw* or *dunesw* build envirnonment for a particular release. E.g. after installing *dunerun*:
<pre>
setup $DUNERUN_DIR/bin/setup-dunesw.sh v09_45_00_00
</pre>
sets up *dunesw* with the indicated version. Replace "dunesw" with "dunebuild" to set up the build environment and replace "v09_45_00_00" with any *dunerun* release specifier (REL in the *dune-run* help message).

## Running from python
The python class *DuneRun* in module *dunerun* provides similar fuctionality from the python command line. For examples of use, see the notebooks:
* [dunerun](ipynb/dunerun.ipynb) - Introduction to using *DuneRun*
* [dunedata](ipynb/dunedata.ipynb) - Demonstrates how to find and access DUNE event data

## Package test
A script is provided to test this package and the current environment. It carries out most of what is described above. To test the current *dunerun* after set up:
<pre>
dunerun> dunerun-test-all
</pre>
To install and test in a new directory \<testdir>:
<pre>
cd &lt;any-directory>
git clone https://github.com/dladams/dunerun.git
dunerun/bin/dunerun-test-alll &lt;testdir>
</pre>
  
## Development plans

* Add package sequence set up to *DuneRun*.
* Other suggestions are welcome.
