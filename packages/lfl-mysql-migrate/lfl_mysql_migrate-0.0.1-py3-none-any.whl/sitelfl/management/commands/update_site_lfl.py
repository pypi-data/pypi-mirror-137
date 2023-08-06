import logging
import subprocess
from shutil import copy

from sitelfl.management.commands.check_git_commit import GitCommand

logger = logging.getLogger(__name__)


class Command(GitCommand):
    help = "Обновление сайта"

    # def runAsAdmin(cmdLine=None, wait=True):
    #
    #     if os.name != 'nt':
    #         raise RuntimeError("This function is only implemented on Windows.")
    #
    #     python_exe = sys.executable
    #
    #     if cmdLine is None:
    #         cmdLine = [python_exe] + sys.argv
    #
    #     elif type(cmdLine) not in (types.TupleType, types.ListType):
    #         raise ValueError("cmdLine is not a sequence.")
    #     cmd = '"%s"' % (cmdLine[0],)
    #     # XXX TODO: isn't there a function or something we can call to massage command line params?
    #     params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    #
    #     showCmd = win32con.SW_SHOWNORMAL
    #
    #     lpVerb = 'runas'  # causes UAC elevation prompt.
    #
    #     procInfo = ShellExecuteEx(nShow=showCmd,
    #                               fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
    #                               lpVerb=lpVerb,
    #                               lpFile=cmd,
    #                               lpParameters=params)
    #
    #     if wait:
    #         procHandle = procInfo['hProcess']
    #         obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
    #         rc = win32process.GetExitCodeProcess(procHandle)
    #
    #     else:
    #         rc = None
    #
    #     return rc

    def handle(self, *args, **options):
        # disc = 'd:/lflru'
        disc = '/home/uandtrew/Job/GIT-HUB/LFL/lflru-old/'
        logger.info(self.help)

        print('git checkout develop')
        out = subprocess.Popen(['git', 'checkout', 'develop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=disc)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        print('git pull')
        out = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=disc)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        print('git checkout master')
        out = subprocess.Popen(['git', 'checkout', 'master'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=disc)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        print('git pull')
        out = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=disc)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        print('git merge develop')
        out = subprocess.Popen(['git', 'merge', 'develop'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=disc)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        copy(src=f'{disc}lflru/web.config.prod', dst=f'{disc}lflru//web.config')

        options=dict(cwd=disc)
        self._handle(*args, **options)
