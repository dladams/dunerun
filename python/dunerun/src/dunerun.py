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
    
def version():
    """Return package version string"""
    scom = findup(__file__, os.path.join('bin', 'dunerunVersion'))
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
    def __init__(self, senv='', sopt='', shell=False, dbg=0, lev=2):
        """
        Ctor for class that runs dune commands.
        senv = '' - Run in bash (no dune set up).
               'dune' - Set up dune env but no products.
               'dunesw' - Set up dunesw.
        sopt = string passed to setup, e.g. 'e20:prof' for dunesw.
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
        self.scoms = []
        myname = 'DuneRun'
        if len(senv):
            sfil = findup(__file__, os.path.join('bin', 'setup-'+senv+".sh"))
            if os.path.exists(sfil):
                if self.dbg>0: print(f"{myname}: Using setup file {sfil}")
                scom = sfil
                if len(sopt):
                    scom = scom + ' ' + sopt
                self.scoms.append(scom)
            else:
                print(f"{myname}: ERROR: Unable to find setup file {sfil}")
        if self._shell:
             signal.signal(signal.SIGUSR1, handler)

    def run(self, com, a_lev=None):
        myname ='DuneRun::run'
        lev = self.lev if a_lev is None else a_lev
        if self._shell:
            if self._popen is None:
                stderr = None if lev > 0 else subprocess.DEVNULL
                stdout = None if lev > 1 else subprocess.DEVNULL
                self._popen = subprocess.Popen(['/bin/bash'], stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True)
                for scom in self.scoms:
                    self.run(f"source {scom}")
            sigcom = f"kill -{signal.SIGUSR1} {os.getpid()}"
            if self.dbg: print(f"{myname}: Executing command {com}")
            self._popen.stdin.write(com + '\n')
            self._popen.stdin.write(sigcom + '\n')
            self._popen.stdin.flush()
            while True:
                if len(sigrecs):
                    sig = sigrecs.pop()
                    #if self.dbg: print(f"{myname}: Received signal {sig}")
                    if sig == signal.SIGUSR1: break
                else:
                    #if self.dbg: print(f"{myname}: Sleeping")
                    time.sleep(1)
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
        myname = 'DuneRun::dtor'
        if self._popen is not None and self._popen.poll() is None:
            if self.dbg: print(f"{myname}: Terminating process {self._popen.pid}")
            self._popen.terminate()
            if self._popen.poll() is None:
                if self.dbg: print(f"{myname}: Killing process {self._popen.pid}")
                self._popen.kill()
