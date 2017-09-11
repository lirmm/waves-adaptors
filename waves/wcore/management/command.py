""" Daemonized WAVES system commands """
from __future__ import unicode_literals

import logging
import os
import sys
import tempfile
import time
from itertools import chain

import datetime
from django.core.management.base import BaseCommand, CommandError

import waves.wcore.adaptors.const
import waves.wcore.exceptions
from waves.wcore.adaptors.exceptions import AdaptorException
from waves.wcore.management.runner import DaemonRunner
from waves.wcore.models import Job, Submission
from waves.wcore.settings import waves_settings
from waves.wcore.settings import waves_settings as config

logger = logging.getLogger('waves.daemon')


class DaemonCommand(BaseCommand):
    """
    Run a management command as a daemon.

    Subclass this and override the `loop_callback` method with the code the 
    daemon process should run. Optionally, override `exit_callback` with 
    code to run when the process is stopped.

    Alternatively, if your code has more complex setup/shutdown requirements,
    override `handle_noargs` along the lines of the basic version here. 
    
    Pass one of --start, --stop, --restart or --status to work as a daemon.
    Otherwise, the command will run as a standard application.
    """

    # Django command params
    requires_model_validation = True
    # parameters python-daemon app
    stdin_path = '/dev/null'
    stdout_path = '/dev/stdout'
    stderr_path = '/dev/stderr'
    work_dir = waves_settings.DATA_ROOT
    # pid configuration
    pidfile_path = '/tmp/daemon_command.pid'
    pidfile_timeout = 5
    # logs parameters defaults
    log_backup_count = 5
    log_max_bytes = 5 * 1024 * 1024
    log_file = '/tmp/daemon_command.log'

    def add_arguments(self, parser):
        """
        Add options to daemon command, compatible for Django version >= 1.8
        :param parser: current Command parser
        :return: Nothing
        """
        parser.add_argument('action', choices=('start', 'stop', 'restart', 'status'), action="store",
                            help="Queue action")
        parser.add_argument('--workdir', action='store', dest='work_dir', help='Setup daemon working dir',
                            default=self.work_dir)
        parser.add_argument('--pidfile', action='store', dest='pidfile_path', default=self.pidfile_path,
                            help='PID absolute filename.')
        parser.add_argument('--logfile', action='store', dest='log_file', default=self.log_file,
                            help='Path to log file')
        parser.add_argument('--stdout', action='store', dest='stdout', default=self.stdout,
                            help='Destination to redirect standard out')
        parser.add_argument('--stderr', action='store', dest='stderr', default=self.stderr,
                            help='Destination to redirect standard error')
        parser.add_argument('--verbose', action='store', dest='verbose', default=True, type=bool,
                            help='Verbose, or not')

    def loop_callback(self):
        """ Main loop executed by daemon """
        raise NotImplementedError('You must implement loop_callback method to define a daemon')

    def exit_callback(self, signal_number, stack_frame):
        """
        Exit callback, called whenever process is manually stopped, or killed elsewhere.
        .. WARNING:
            If you plan to override this function, remember to always call parent method in order to terminate process
        """
        exception = SystemExit(
            "Terminating on signal {signal_number!r}".format(
                signal_number=signal_number))
        raise exception

    def preloop_callback(self):
        """
        Override this method if you want to do initialization before actual daemon process infinite loop
        """
        pass

    def run(self):
        """
        Method called upon 'start' command from daemon manager, must be overriden in actual job daemon subclass
        """
        logger.debug("Starting Daemon...")
        try:
            self.preloop_callback()
            logger.debug("Starting loopback...")
            while True:
                self.loop_callback()
        except (SystemExit, KeyboardInterrupt):
            # Normal exit getting a signal from the parent process
            pass
        except Exception as exc:
            # Something unexpected happened?
            logger.exception("Unexpected Exception %s", exc.message)

    def handle(self, **options):
        """
        Handle commands for a daemon (--start|--stop|--restart|--status)
        :param options: list of possible django command options
        :return: Nothing
        """
        try:
            # refactor sys.argv in order to remove the django command and setup action from Django command option
            sys.argv.pop(0)
            sys.argv[1] = options.pop('action')
            run = DaemonRunner(self, **options)
            run.do_action()
        except KeyError:
            raise CommandError('You must specify an action with this command')


class JobQueueCommand(DaemonCommand):
    """
    Dedicated command to summarize current WAVES specific settings
    """
    help = 'Managing WAVES job queue states'
    SLEEP_TIME = 2
    pidfile_path = os.path.join(tempfile.gettempdir(), 'waves_queue.pid')
    pidfile_timeout = 5

    def loop_callback(self):
        """
        Very very simple daemon to monitor jobs queue.

        - Retrieve all current non terminated job, and process according to current status.
        - Jobs are run on a stateless process

        .. todo::
            Implement this as separated forked processes for each jobs, inspired by Galaxy queue treatment.

        :return: Nothing
        """
        print Submission.objects.all()
        jobs = Job.objects.prefetch_related('job_inputs'). \
            prefetch_related('outputs').filter(_status__lt=waves.wcore.adaptors.const.JOB_TERMINATED)
        if jobs.count() > 0:
            logger.info("Starting queue process with %i(s) unfinished jobs", jobs.count())
        for job in jobs:
            runner = job.adaptor
            if runner and logger.isEnabledFor(logging.DEBUG):
                logger.debug('[Runner]-------\n%s\n----------------', runner.dump_config())
            try:
                job.check_send_mail()
                logger.debug("Launching Job %s (adaptor:%s)", job, runner)
                if job.status == waves.wcore.adaptors.const.JOB_CREATED:
                    job.run_prepare()
                    logger.debug("[PrepareJob] %s (adaptor:%s)", job, runner)
                elif job.status == waves.wcore.adaptors.const.JOB_PREPARED:
                    logger.debug("[LaunchJob] %s (adaptor:%s)", job, runner)
                    job.run_launch()
                elif job.status == waves.wcore.adaptors.const.JOB_COMPLETED:
                    job.run_results()
                    logger.debug("[JobExecutionEnded] %s (adaptor:%s)", job.get_status_display(), runner)
                else:
                    job.run_status()
            except (waves.wcore.exceptions.WavesException, AdaptorException) as e:
                logger.error("Error Job %s (adaptor:%s-state:%s): %s", job, runner, job.get_status_display(),
                             e.message)
            finally:
                logger.info("Queue job terminated at: %s", datetime.datetime.now().strftime('%A, %d %B %Y %H:%M:%I'))
                job.check_send_mail()
                if runner is not None:
                    runner.disconnect()
        # logger.debug('Go to sleep for %i seconds' % self.SLEEP_TIME)
        time.sleep(self.SLEEP_TIME)


class PurgeDaemonCommand(DaemonCommand):
    help = 'Clean up old jobs '
    SLEEP_TIME = 86400
    pidfile_path = os.path.join(waves_settings.DATA_ROOT, 'waves_clean.pid')

    def loop_callback(self):
        logger.info("Purge job launched at: %s", datetime.datetime.now().strftime('%A, %d %B %Y %H:%M:%I'))
        date_anonymous = datetime.date.today() - datetime.timedelta(config.KEEP_ANONYMOUS_JOBS)
        date_registered = datetime.date.today() - datetime.timedelta(config.KEEP_REGISTERED_JOBS)
        anonymous = Job.objects.filter(client__isnull=True, updated__lt=date_anonymous)
        registered = Job.objects.filter(client__isnull=False, updated__lt=date_registered)
        for job in list(chain(*[anonymous, registered])):
            logger.info('Deleting job %s created on %s', job.slug, job.created)
            job.delete()
        logger.info("Purge job terminated at: %s", datetime.datetime.now().strftime('%A, %d %B %Y %H:%M:%I'))
