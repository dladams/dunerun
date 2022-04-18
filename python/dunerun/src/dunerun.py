import os
import sys
import subprocess
import signal
import time

def findup(startpath, fnam):
    """Search up the path of a file for another file"""
    insdir = startpath
    while len(insdir) > 1:
        insdir = os.path.dirname(insdir)
        path = os.path.join(insdir, fnam)
        if os.path.exists(path): return path
    return None

def dunerun_find_setup(pkgname='dunerun', special=False, dironly=False):
    """
    Return expected path for a package setup file.
    If special is True, returns setup_<pkgname>.sh in dunerun bin area
    Otherwise at the dunerun-compliant location
    Raises an exception if DUNE_INSTALL_DIR does not point to a directory.
    if dironly is true, returns directory where the setup file resides.
    Does not check if the setup directory or file exists.
    """
    myname = 'dunerun_find_setup'
    if special:
        supdir = dunerun_find_setup(dironly=True) + '/bin'
        if dironly: return supdir
        supfil = supdir + '/setup-' + pkgname + '.sh'
        return supfil
    insbas = os.getenv('DUNE_INSTALL_DIR')
    if len(insbas) == 0:
        raise Exception(f"{myname}: ERROR: Env variable DUNE_INSTALL_DIR must de befined.")
    bypkg = os.getenv('DUNE_INSTALL_BYPKG')
    if bypkg == 'false':
        supdir = insbas + '/bin'
        supfil = supdir + '/setup_' + pkgname + '.sh'
    else:
        supdir = insbas + '/' + pkgname
        supfil = supdir + '/setup.sh'
    if dironly: return supdir
    return supfil
    
def version():
    """Return package version string"""
    scom = os.path.join(os.getenv('DUNERUN_DIR'), 'bin', 'dunerunVersion')
    errsuf = f"-from-{__file__}"
    if scom is not None:
        cpr = subprocess.run(scom, capture_output=True)
        if cpr.returncode == 0: return cpr.stdout.decode().strip()
        errsuf = f"-at-{scom}"
    return f"Unable-to-find-version{errsuf}"

sigrecs = []
def handler(signum, frame):
    """ Signal handler that appends the signal to the global list sigrecs. """
    #print('Signal handler called with signal', signum)
    sigrecs.append(signum)

class DuneRun:
    def __init__(self, senv='', sopt='', shell=False, dbg=0, lev=2, precoms=[]):
        """
        Ctor for class that runs dune commands.
        senv = '' - Run in bash (no dune set up).
               'dune' - Set up dune env but no products.
               'dunesw' - Set up dunesw.
               Other string - try to set up as dunerun-compliant package.
               Sequence of string - Set up any of the above in turn.
        sopt = string passed to setup, e.g. 'e20:prof' for dunesw.
        precoms = Commands run before environment setup.
        shell = If true, all calls to run use the same shell.
        lev = Output level for the executed commands:
              0 - All output is discarded
              1 - stderr only
              2 - stdout and stderr [default]
        dbg = Output level (in addition to stdout, stderr) for run commands:
              0 - Command is executed with no extra messages. [default]
              1 - Command is executed with informational messages."
              2 - Command and infomational messages are displayed. No command execution."
        """
        self._shell = shell
        self._popen = None
        self.dbg = dbg
        self.lev = lev
        self.pcoms = precoms
        self.scoms = []
        myname = f"{os.getpid()}: DuneRun:ctor"
        # This package may have been set up in python and not the supporting shell
        # so we add a setup of this package.
        if False:
            sfil = findup(__file__, 'setup.sh')
            if os.path.exists(sfil):
                if self.dbg>0: print(f"{myname}: Using package setup file {sfil}")
                self.scoms.append(sfil)
            else:
                print(f"{myname}: ERROR: Unable to find setup file {sfil}")
        # Add the environment setup files.
        if len(senv):
            if type(senv) == str:
                pkgs = senv.split(',')
            else:
                pkgs = senv
            for pkg in pkgs:
                sfils = []
                sfil = dunerun_find_setup(pkg, special=True)
                if os.path.exists(sfil):
                    scom = sfil
                    if len(sopt):
                        scom = scom + ' ' + sopt
                    self.scoms.append(scom)
                else:
                    sfils.append(sfil)
                    sfil = dunerun_find_setup(pkg)
                    if os.path.exists(sfil):
                        self.scoms.append(sfil)
                    else:
                        sfils.append(sfil)
                        print(f"{myname}: Unable to find any of these setup files:")
                        for sfil in sfils:
                            print(f"{myname}:   {sfil}")
                        continue
                if self.dbg: print(f"{myname}: Added set up: {scom}")
        #else:
            #if self.dbg: print(f"{myname}: No environment specified.")
        if self._shell:
            signal.signal(signal.SIGUSR1, handler)

    def run(self, com, a_lev=None):
        myname =f"{os.getpid()}: DuneRun::run"
        lev = self.lev if a_lev is None else a_lev
        if self._shell:
            if self._popen is None:
                stderr = None if lev > 0 else subprocess.DEVNULL
                stdout = None if lev > 1 else subprocess.DEVNULL
                if self.dbg: print(f"{myname}: Starting subprocess.")
                self._popen = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True)
                for pcom in self.pcoms:
                    if self.dbg: print(f"{myname}: Sourcing {pcom}")
                    self.run(pcom)
                for scom in self.scoms:
                    if self.dbg: print(f"{myname}: Sourcing {scom}")
                    self.run(f"source {scom}")
            sigcom = f"kill -{signal.SIGUSR1} {os.getpid()}"
            if self.dbg: print(f"{myname}: Executing command {com}")
            self._popen.stdin.write(com + '\n')
            self._popen.stdin.write(sigcom + '\n')
            self._popen.stdin.flush()
            nsleep = 0
            while True:
                if len(sigrecs):
                    sig = sigrecs.pop()
                    if sig == signal.SIGUSR1: break
                else:
                    if self.dbg and nsleep: print(f"{myname}: Sleeping...")
                    time.sleep(1)
                    nsleep = nsleep + 1
            sys.stdout.flush()
        else:
            line = ''
            for scom in self.scoms:
                line += 'source ' + scom
                line += '; '
            line += com
            if self.dbg: print(f"{myname}: Running command {line}")
            #os.system(line)         # This uses sh instead of bash and can't parse setup-dunesw.sh
            stderr = None if lev > 0 else subprocess.DEVNULL
            stdout = None if lev > 1 else subprocess.DEVNULL
            subprocess.run(['bash', '-c', line], stdout=stdout, stderr=stderr)

    def __del__(self):
        myname = f"{os.getpid()}: DuneRun::dtor"
        if self._popen is not None and self._popen.poll() is None:
            if self.dbg: print(f"{myname}: Terminating process {self._popen.pid}")
            self._popen.terminate()
            if self._popen.poll() is None:
                if self.dbg: print(f"{myname}: Killing process {self._popen.pid}")
                self._popen.kill()
