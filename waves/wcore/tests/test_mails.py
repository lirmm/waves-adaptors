from __future__ import unicode_literals

import logging

import waves.wcore.adaptors.const
from django.conf import settings
from django.core import mail
from django.test import override_settings
from django.utils import timezone
from waves.wcore.models import Job, JobInput, JobOutput, Service, Submission
from waves.wcore.settings import waves_settings as config
from waves.wcore.tests.base import WavesBaseTestCase

logger = logging.getLogger(__name__)


@override_settings(
    NOTIFY_RESULTS=True,
)
class JobMailTest(WavesBaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(JobMailTest, cls).setUpClass()
        logger.info('EMAIL_BACKEND: %s', settings.EMAIL_BACKEND)

    def test_mail_job(self):
        job = Job.objects.create(
            submission=Submission.objects.create(name='Default',
                                                 service=Service.objects.create(name='SubmissionSample Service')),
            email_to='marc@fake.com')
        job.job_inputs.add(JobInput.objects.create(name="param1", value="Value1", job=job))
        job.job_inputs.add(JobInput.objects.create(name="param2", value="Value2", job=job))
        job.job_inputs.add(JobInput.objects.create(name="param3", value="Value3", job=job))
        job.outputs.add(JobOutput.objects.create(_name="out1", value="out1", job=job))
        job.outputs.add(JobOutput.objects.create(_name="out2", value="out2", job=job))
        job.status_time = timezone.datetime.now()
        logger.debug("Job link: %s", job.link)
        logger.debug("Job notify: %s", job.notify)
        job.check_send_mail()
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[-1]
        self.assertTrue(job.service in sent_mail.subject)
        self.assertEqual(job.email_to, sent_mail.to[0])
        self.assertEqual(config.SERVICES_EMAIL, sent_mail.from_email)
        logger.debug('Mail subject: %s', sent_mail.subject)
        logger.debug('Mail from: %s', sent_mail.from_email)
        logger.debug('Mail content: \n%s', sent_mail.body)
        job.status = waves.wcore.adaptors.const.JOB_COMPLETED
        # job.save()
        job.check_send_mail()
        # no more mails
        self.assertEqual(len(mail.outbox), 1)

        job.status = waves.wcore.adaptors.const.JOB_TERMINATED
        # job.save()
        job.check_send_mail()
        self.assertEqual(len(mail.outbox), 2)
        sent_mail = mail.outbox[-1]
        logger.debug('Mail subject: %s', sent_mail.subject)
        logger.debug('Mail from: %s', sent_mail.from_email)
        logger.debug('Mail content: \n%s', sent_mail.body)
        job.status = waves.wcore.adaptors.const.JOB_ERROR
        # job.save()
        job.check_send_mail()
        # mail to user and mail to admin so +2
        self.assertEqual(len(mail.outbox), 4)
        sent_mail = mail.outbox[-1]
        logger.debug('Mail subject: %s', sent_mail.subject)
        logger.debug('Mail from: %s', sent_mail.from_email)
        logger.debug('Mail content: \n%s', sent_mail.body)
        job.status = waves.wcore.adaptors.const.JOB_CANCELLED
        # job.save()
        job.check_send_mail()
        self.assertEqual(len(mail.outbox), 5)
        sent_mail = mail.outbox[-1]
        logger.debug('Mail subject: %s', sent_mail.subject)
        logger.debug('Mail from: %s', sent_mail.from_email)
        logger.debug('Mail content: \n%s', sent_mail.body)