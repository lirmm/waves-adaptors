# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-29 15:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import swapper
import django.db.models.manager
import uuid
import waves.wcore.compat
import waves.wcore.models.base
import waves.wcore.utils.storage
import waves.wcore.utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        swapper.dependency('wcore', 'Service'),
        swapper.dependency('wcore', 'Submission')
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('description', waves.wcore.compat.RichTextField(blank=True, help_text='Description (HTML)', null=True, verbose_name='Description')),
                ('short_description', models.TextField(blank=True, help_text='Short description (Text)', null=True, verbose_name='Short Description')),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('name', models.CharField(help_text='Service displayed name', max_length=255, verbose_name='Service name')),
                ('authors', models.CharField(help_text='Tools authors', max_length=255, null=True, verbose_name='Authors')),
                ('citations', models.CharField(help_text='Citation link (Bibtex format)', max_length=500, null=True, verbose_name='Citation link')),
                ('version', models.CharField(blank=True, default='1.0', help_text='Service displayed version', max_length=10, null=True, verbose_name='Current version')),
                ('status', models.IntegerField(choices=[[0, 'Draft (only creator)'], [1, 'Staff (Team members)'], [4, 'Registered'], [2, 'Restricted'], [3, 'Public']], default=0, help_text='Service online status')),
                ('email_on', models.BooleanField(default=True, help_text='This service sends notification email', verbose_name='Notify results')),
                ('partial', models.BooleanField(default=False, help_text='Set whether some service outputs are dynamic (not known in advance)', verbose_name='Dynamic outputs')),
                ('remote_service_id', models.CharField(editable=False, max_length=255, null=True, verbose_name='Remote service tool ID')),
                ('edam_topics', models.TextField(blank=True, help_text='Comma separated list of Edam ontology topics', null=True, verbose_name='Edam topics')),
                ('edam_operations', models.TextField(blank=True, help_text='Comma separated list of Edam ontology operations', null=True, verbose_name='Edam operations')),
            ],
            options={
                'ordering': ['name'],
                'swappable': swapper.swappable_setting('wcore', 'Service'),
                'verbose_name_plural': 'Online Services',
                'verbose_name': 'Online Service',
            },
            bases=(waves.wcore.models.base.ExportAbleMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('order', models.PositiveIntegerField(default=0)),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('availability', models.IntegerField(choices=[(0, 'Disabled API'), (1, 'Enabled API')], default=1, verbose_name='Availability')),
                ('name', models.CharField(max_length=255, verbose_name='Label')),
            ],
            options={
                'ordering': ('order',),
                'swappable': swapper.swappable_setting('wcore', 'Submission'),
                'verbose_name': 'Submission method',
                'verbose_name_plural': 'Submission methods',
            },
        ),
        migrations.CreateModel(
            name='AdaptorInitParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Param name', max_length=100, null=True, verbose_name='Name')),
                ('value', models.CharField(blank=True, help_text='Default value', max_length=500, null=True, verbose_name='Value')),
                ('crypt', models.BooleanField(default=False, editable=False, verbose_name='Encrypted')),
                ('prevent_override', models.BooleanField(default=False, help_text='Prevent override', verbose_name='Prevent override')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Initial param',
                'verbose_name_plural': 'Init params',
            },
        ),
        migrations.CreateModel(
            name='AParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('label', models.CharField(help_text='Input displayed label', max_length=100, verbose_name='Label')),
                ('name', models.CharField(help_text="Input runner's job param command line name", max_length=50, verbose_name='Parameter name')),
                ('multiple', models.BooleanField(default=False, help_text='Can hold multiple values', verbose_name='Multiple')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='Help Text')),
                ('required', models.NullBooleanField(choices=[(True, 'Required'), (None, 'Not submitted by user'), (False, 'Optional')], default=True, help_text='Submitted and/or Required', verbose_name='Required')),
                ('default', models.CharField(blank=True, max_length=50, null=True, verbose_name='Default value')),
                ('cmd_format', models.IntegerField(choices=[(0, '-- Not used in job command line--'), (6, 'Assigned named parameter: [name]=value'), (2, 'Named short parameter: -[name] value'), (1, 'Named assigned long parameter: --[name]=value'), (3, 'Named short option: -[name]'), (5, 'Named long option: --[name]'), (4, 'Positional parameter: value')], default=2, help_text='Command line pattern', verbose_name='Command line format')),
                ('edam_formats', models.CharField(blank=True, help_text='comma separated list of supported edam format', max_length=255, null=True, verbose_name='Edam format(s)')),
                ('edam_datas', models.CharField(blank=True, help_text='comma separated list of supported edam data param_type', max_length=255, null=True, verbose_name='Edam data(s)')),
                ('when_value', models.CharField(blank=True, help_text='Input is treated only for this parent value', max_length=255, null=True, verbose_name='When value')),
                ('regexp', models.CharField(blank=True, max_length=255, null=True, verbose_name='Validation Regexp')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Input',
                'verbose_name_plural': 'Inputs',
                'base_manager_name': 'base_objects',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='FileInputSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, null=True, verbose_name='Input Label')),
                ('help_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Help text')),
                ('file', models.FileField(storage=waves.wcore.utils.storage.WavesStorage(), upload_to=waves.wcore.utils.storage.file_sample_directory, verbose_name='Sample file')),
            ],
            options={
                'verbose_name': 'Input sample',
                'verbose_name_plural': 'Input samples',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Job title')),
                ('_status', models.IntegerField(choices=[(-1, 'Undefined'), (0, 'Created'), (1, 'Prepared'), (2, 'Queued'), (3, 'Running'), (4, 'Suspended'), (5, 'Run completed, pending data retrieval'), (6, 'Results data retrieved'), (7, 'Cancelled'), (8, 'Warnings'), (9, 'Error')], default=0, verbose_name='Job status')),
                ('status_mail', models.IntegerField(default=9999, editable=False)),
                ('email_to', models.EmailField(blank=True, help_text='Notify results to this email', max_length=254, null=True, verbose_name='Email results')),
                ('exit_code', models.IntegerField(default=0, help_text='Job exit code on relative adaptor', verbose_name='Job system exit code')),
                ('results_available', models.BooleanField(default=False, editable=False, verbose_name='Results are available')),
                ('nb_retry', models.IntegerField(default=0, editable=False, verbose_name='Nb Retry')),
                ('remote_job_id', models.CharField(editable=False, max_length=255, null=True, verbose_name='Remote job ID')),
                ('remote_history_id', models.CharField(editable=False, max_length=255, null=True, verbose_name='Remote history ID')),
                ('_command_line', models.CharField(editable=False, max_length=255, null=True, verbose_name='Final generated command line')),
                ('_adaptor', models.TextField(editable=False, null=True, verbose_name='Adaptor classed used for this Job')),
                ('service', models.CharField(default='', editable=False, max_length=255, null=True, verbose_name='Service name')),
                ('notify', models.BooleanField(default=False, editable=False, verbose_name='Notify this result')),
                ('client', models.ForeignKey(blank=True, help_text='Associated registered user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients_job', to=settings.AUTH_USER_MODEL)),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_jobs', to=swapper.get_model_name('wcore', 'Submission'))),
            ],
            options={
                'ordering': ['-updated', '-created'],
                'abstract': False,
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
            bases=(models.Model, waves.wcore.models.base.UrlMixin),
        ),
        migrations.CreateModel(
            name='JobHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='History timestamp', verbose_name='Date time')),
                ('status', models.IntegerField(choices=[(-1, 'Undefined'), (0, 'Created'), (1, 'Prepared'), (2, 'Queued'), (3, 'Running'), (4, 'Suspended'), (5, 'Run completed, pending data retrieval'), (6, 'Results data retrieved'), (7, 'Cancelled'), (8, 'Warnings'), (9, 'Error')], help_text='History job status', null=True, verbose_name='Job Status')),
                ('message', models.TextField(blank=True, help_text='History log', null=True, verbose_name='History log')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin Message')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_history', to='wcore.Job')),
            ],
            options={
                'ordering': ['-timestamp', '-status'],
            },
        ),
        migrations.CreateModel(
            name='JobInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('value', models.CharField(blank=True, help_text='Input value (filename, boolean value, int value etc.)', max_length=255, null=True, verbose_name='Input content')),
                ('remote_input_id', models.CharField(editable=False, max_length=255, null=True, verbose_name='Remote input ID (on adaptor)')),
                ('param_type', models.CharField(choices=[('file', 'Input file'), ('list', 'List of values'), ('boolean', 'Boolean'), ('decimal', 'Decimal'), ('int', 'Integer'), ('text', 'Text')], editable=False, max_length=50, null=True, verbose_name='Param param_type')),
                ('name', models.CharField(editable=False, max_length=50, null=True, verbose_name='Param name')),
                ('cmd_format', models.IntegerField(choices=[(0, '-- Not used in job command line--'), (6, 'Assigned named parameter: [name]=value'), (2, 'Named short parameter: -[name] value'), (1, 'Named assigned long parameter: --[name]=value'), (3, 'Named short option: -[name]'), (5, 'Named long option: --[name]'), (4, 'Positional parameter: value')], default=4, editable=False, null=True, verbose_name='Parameter Type')),
                ('label', models.CharField(editable=False, max_length=100, null=True, verbose_name='Label')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_inputs', to='wcore.Job')),
            ],
        ),
        migrations.CreateModel(
            name='JobOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('value', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Output value')),
                ('remote_output_id', models.CharField(editable=False, max_length=255, null=True, verbose_name='Remote output ID (on adaptor)')),
                ('_name', models.CharField(help_text='Output displayed name', max_length=50, verbose_name='Name')),
                ('extension', models.CharField(default='', max_length=5, verbose_name='File extension')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='wcore.Job')),
            ],
            bases=(waves.wcore.models.base.UrlMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RepeatedGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=50, verbose_name='Group name')),
                ('title', models.CharField(max_length=200, verbose_name='Group title')),
                ('max_repeat', models.IntegerField(blank=True, null=True, verbose_name='Max repeat')),
                ('min_repeat', models.IntegerField(default=0, verbose_name='Min repeat')),
                ('default', models.IntegerField(default=0, verbose_name='Default repeat')),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission_groups', to=swapper.get_model_name('wcore', 'Submission'))),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', waves.wcore.compat.RichTextField(blank=True, help_text='Description (HTML)', null=True, verbose_name='Description')),
                ('short_description', models.TextField(blank=True, help_text='Short description (Text)', null=True, verbose_name='Short Description')),
                ('clazz', models.CharField(help_text='This is the concrete class used to perform job execution', max_length=100, verbose_name='Adaptor object')),
                ('name', models.CharField(help_text='Displayed name', max_length=50, verbose_name='Label')),
                ('enabled', models.BooleanField(default=True, help_text='Runner is enable for job runs', verbose_name='Enabled')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Computing infrastructure',
                'verbose_name_plural': 'Computing infrastructures',
            },
            bases=(waves.wcore.models.base.ExportAbleMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SampleDepParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_default', models.CharField(max_length=200, verbose_name='Set value to ')),
            ],
            options={
                'verbose_name': 'Sample dependency',
                'verbose_name_plural': 'Sample dependencies',
            },
        ),
        migrations.CreateModel(
            name='ServiceBinaryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('slug', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True)),
                ('label', models.CharField(max_length=255, verbose_name='Binary file label')),
                ('binary', models.FileField(storage=waves.wcore.utils.storage.BinaryStorage(), upload_to=waves.wcore.utils.storage.binary_directory, verbose_name='Binary file')),
            ],
            options={
                'verbose_name': 'Binary file',
                'verbose_name_plural': 'Binaries files',
            },
        ),
        migrations.CreateModel(
            name='SubmissionExitCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exit_code', models.IntegerField(default=0, verbose_name='Exit code value')),
                ('message', models.CharField(max_length=255, verbose_name='Exit code message')),
                ('is_error', models.BooleanField(default=False, verbose_name='Is an Error')),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exit_codes', to=swapper.get_model_name('wcore', 'Submission'))),
            ],
            options={
                'verbose_name': 'Exit Code',
            },
        ),
        migrations.CreateModel(
            name='SubmissionOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created on')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Last update timestamp', verbose_name='Last Update')),
                ('api_name', models.CharField(blank=True, help_text='App short code, used in url, leave blank for automatic setup', max_length=100, null=True, verbose_name='App short code')),
                ('label', models.CharField(help_text='Label', max_length=255, null=True, verbose_name='Label')),
                ('name', models.CharField(blank=True, help_text='Output name', max_length=255, null=True, verbose_name='Name')),
                ('file_pattern', models.CharField(help_text='Pattern is used to match input value (%s to retrieve value from input)', max_length=100, verbose_name='File name or name pattern')),
                ('edam_format', models.CharField(blank=True, help_text='Edam ontology output format', max_length=255, null=True, verbose_name='Edam format')),
                ('edam_data', models.CharField(blank=True, help_text='Edam ontology output data', max_length=255, null=True, verbose_name='Edam data')),
                ('help_text', models.TextField(blank=True, null=True, verbose_name='Help Text')),
                ('extension', models.CharField(blank=True, default='', help_text='Leave blank accept all, or set in file pattern', max_length=5, verbose_name='File extension')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Expected output',
                'verbose_name_plural': 'Expected outputs',
            },
        ),
        migrations.CreateModel(
            name='BooleanParam',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('true_value', models.CharField(default='True', max_length=50, verbose_name='True value')),
                ('false_value', models.CharField(default='False', max_length=50, verbose_name='False value')),
            ],
            options={
                'verbose_name': 'Boolean choice',
                'verbose_name_plural': 'Boolean choices',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='DecimalParam',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('min_val', models.DecimalField(blank=True, decimal_places=3, default=None, help_text='Leave blank if no min', max_digits=50, null=True, verbose_name='Min value')),
                ('max_val', models.DecimalField(blank=True, decimal_places=3, default=None, help_text='Leave blank if no max', max_digits=50, null=True, verbose_name='Max value')),
                ('step', models.DecimalField(blank=True, decimal_places=3, default=0.5, max_digits=50, verbose_name='Step')),
            ],
            options={
                'verbose_name': 'Decimal',
                'verbose_name_plural': 'Decimal',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='FileInput',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('max_size', models.BigIntegerField(default=20480, help_text='in Ko', verbose_name='Allowed file size ')),
                ('allowed_extensions', models.CharField(default='*', help_text='Comma separated list, * means no filter', max_length=255, validators=[waves.wcore.utils.validators.validate_list_comma], verbose_name='Filter by extensions')),
                ('allow_copy_paste', models.BooleanField(default=False, help_text='Set whether file input field should add a copy/paste text field', verbose_name='Allow copy paste in forms')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'File input',
                'verbose_name_plural': 'Files inputs',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='IntegerParam',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('min_val', models.IntegerField(blank=True, default=0, help_text='Leave blank if no min', null=True, verbose_name='Min value')),
                ('max_val', models.IntegerField(blank=True, default=None, help_text='Leave blank if no max', null=True, verbose_name='Max value')),
                ('step', models.IntegerField(blank=True, default=1, help_text='Step to increment/decrement values', verbose_name='Step')),
            ],
            options={
                'verbose_name': 'Integer',
                'verbose_name_plural': 'Integer',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ListParam',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('list_mode', models.CharField(choices=[('select', 'Select List'), ('radio', 'Radio buttons'), ('checkbox', 'Check box')], default='select', max_length=100, verbose_name='List display mode')),
                ('list_elements', models.TextField(help_text='One Element per line label|value', validators=[waves.wcore.utils.validators.validate_list_param], verbose_name='Elements')),
            ],
            options={
                'verbose_name': 'List',
                'verbose_name_plural': 'Lists',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='TextParam',
            fields=[
                ('aparam_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wcore.AParam')),
                ('max_length', models.CharField(default=255, max_length=255, verbose_name='Max length (<255)')),
            ],
            options={
                'verbose_name': 'Text Input',
                'verbose_name_plural': 'Text Input',
            },
            bases=('wcore.aparam',),
            managers=[
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='submissionoutput',
            name='from_input',
            field=models.ForeignKey(blank=True, default=None, help_text='Is valuated from an input', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_outputs', to='wcore.AParam'),
        ),
        migrations.AddField(
            model_name='submissionoutput',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to=swapper.get_model_name('wcore', 'Submission')),
        ),
        migrations.AddField(
            model_name='sampledepparam',
            name='related_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_samples', to='wcore.AParam'),
        ),
        migrations.AddField(
            model_name='sampledepparam',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependent_inputs', to='wcore.FileInputSample'),
        ),
        migrations.AddField(
            model_name='runner',
            name='binary_file',
            field=models.ForeignKey(blank=True, help_text="If set, 'Execution parameter' param line:'command' will be ignored", null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcore.ServiceBinaryFile'),
        ),
        migrations.AddField(
            model_name='fileinputsample',
            name='dependent_params',
            field=models.ManyToManyField(blank=True, through='wcore.SampleDepParam', to='wcore.AParam'),
        ),
        migrations.AddField(
            model_name='aparam',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Input is associated to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dependents_inputs', to='wcore.AParam'),
        ),
        migrations.AddField(
            model_name='aparam',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_wcore.aparam_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='aparam',
            name='repeat_group',
            field=models.ForeignKey(blank=True, help_text='Group and repeat items', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcore.RepeatedGroup'),
        ),
        migrations.AddField(
            model_name='aparam',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to=swapper.get_model_name('wcore', 'Submission')),
        ),
        migrations.AddField(
            model_name='submission',
            name='binary_file',
            field=models.ForeignKey(blank=True, help_text="If set, 'Execution parameter' param line:'command' will be ignored", null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcore.ServiceBinaryFile'),
        ),
        migrations.AddField(
            model_name='submission',
            name='runner',
            field=models.ForeignKey(help_text='Service job runs configuration', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wcore_submission_runs', to='wcore.Runner', verbose_name='Computing infrastructure'),
        ),
        migrations.AddField(
            model_name='submission',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=swapper.get_model_name('wcore', 'Service')),
        ),
        migrations.AddField(
            model_name='service',
            name='binary_file',
            field=models.ForeignKey(blank=True, help_text="If set, 'Execution parameter' param line:'command' will be ignored", null=True, on_delete=django.db.models.deletion.SET_NULL, to='wcore.ServiceBinaryFile'),
        ),
        migrations.AddField(
            model_name='service',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='restricted_client',
            field=models.ManyToManyField(blank=True, help_text="Public access is granted to everyone, If status is 'Restricted' you may restrict access to specific users here.", related_name='wcore_service_restricted_services', to=settings.AUTH_USER_MODEL, verbose_name='Restricted clients'),
        ),
        migrations.AddField(
            model_name='service',
            name='runner',
            field=models.ForeignKey(help_text='Service job runs configuration', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wcore_service_runs', to='wcore.Runner', verbose_name='Computing infrastructure'),
        ),
        migrations.CreateModel(
            name='JobAdminHistory',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('wcore.jobhistory',),
        ),
        migrations.CreateModel(
            name='ServiceRunParam',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('wcore.adaptorinitparam',),
        ),
        migrations.CreateModel(
            name='SubmissionRunParam',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('wcore.adaptorinitparam',),
        ),
        migrations.AlterUniqueTogether(
            name='submissionexitcode',
            unique_together=set([('exit_code', 'submission')]),
        ),
        migrations.AddField(
            model_name='sampledepparam',
            name='file_input',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sample_dependencies', to='wcore.FileInput'),
        ),
        migrations.AlterUniqueTogether(
            name='joboutput',
            unique_together=set([('api_name', 'job')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobinput',
            unique_together=set([('name', 'value', 'job')]),
        ),
        migrations.AlterUniqueTogether(
            name='jobhistory',
            unique_together=set([('job', 'timestamp', 'status', 'is_admin')]),
        ),
        migrations.AddField(
            model_name='fileinputsample',
            name='file_input',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_samples', to='wcore.FileInput'),
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together=set([('api_name', 'version', 'status')]),
        ),
    ]
