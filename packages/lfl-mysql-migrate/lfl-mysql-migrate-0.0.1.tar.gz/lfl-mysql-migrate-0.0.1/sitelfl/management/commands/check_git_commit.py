import logging
import subprocess

from django.core.management import BaseCommand

from isc_common.string import BytesToStr

logger = logging.getLogger(__name__)


class GitCommand(BaseCommand):
    def print_std_out( self , stdout , stderr ) :
        res_str = [ ]
        for st in BytesToStr( stdout ).split( '\n' ) :
            res_str.append( st )

        if len( res_str ) > 0 :
            for s in res_str :
                print( s )
            return True
        return False

    def _handle(self, *args, **options):
        cwd=options.get('cwd')
        if cwd is None:
            cwd='C:\lflru'
        logger.info(self.help)

        print('git add .')
        out = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
        stdout, stderr = out.communicate()
        self.print_std_out(stdout=stdout, stderr=stderr)

        print('git status -s')
        out = subprocess.Popen(['git', 'status', '-s'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

        stdout, stderr = out.communicate()
        need_commit = self.print_std_out(stdout=stdout, stderr=stderr)

        if need_commit is True:
            print('git commit -am"."')
            out = subprocess.Popen(['git', 'commit', '-am"."'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
            stdout, stderr = out.communicate()
            self.print_std_out(stdout=stdout, stderr=stderr)

            print('git push')
            out = subprocess.Popen(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
            stdout, stderr = out.communicate()

            print('git push --tags')
            out = subprocess.Popen(['git', 'push', '--tags'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
            stdout, stderr = out.communicate()

            self.print_std_out(stdout=stdout, stderr=stderr)

        print('Done.')


class Command(GitCommand):
    def handle(self, *args, **options):
        self._handle(*args, **options)
