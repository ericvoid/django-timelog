from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from timelog.lib import generate_table_from, generate_csv_from, analyze_log_file, PATTERN


class Command(BaseCommand):

    generate_output_functions = {
        'table': generate_table_from,
        'csv':   generate_csv_from,
    }

    option_list = BaseCommand.option_list + (
        make_option('--file',
            dest='file',
            default=settings.TIMELOG_LOG,
            help='Specify file to use'),
        make_option('--output',
            dest='output',
            default='table',
            help='Specify output format - valid choices are {0}'.format(generate_output_functions.keys())),
        make_option('--noreverse',
            dest='reverse',
            action='store_false',
            default=True,
            help='Show paths instead of views'),
        make_option('--noprogress',
            dest='progress',
            action='store_false',
            default=True,
            help='Suppress displaying progress bar'),
        )

    def handle(self, *args, **options):

        if options.get('output') not in self.generate_output_functions:
            print "Invalid output format, valid choices are {0}".format(generate_output_functions.keys())

        LOGFILE = options.get('file')

        try:
            data = analyze_log_file(LOGFILE, PATTERN, reverse_paths=options.get('reverse'), progress=options.get('progress'))
        except IOError:
            print "File not found"
            exit(2)

        generate_output_fn = self.generate_output_functions[options.get('output')]
        print generate_table_from(generate_output_fn(data))