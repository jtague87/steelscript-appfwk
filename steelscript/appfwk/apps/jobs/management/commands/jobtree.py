# Copyright (c) 2014-2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


import logging
import optparse
from graphviz import Digraph

from django.core.management.base import BaseCommand
from steelscript.appfwk.apps.jobs.models import Job


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = None
    help = 'Work with already run jobs'

    def create_parser(self, prog_name, subcommand):
        """ Override super version to include special option grouping
        """
        parser = super(Command, self).create_parser(prog_name, subcommand)
        group = optparse.OptionGroup(parser, "Job Help",
                                     "Helper commands to manange jobs")
        group.add_option('--job',
                         default=None,
                         help='Restrict tree to this job')
        group.add_option('-o', '--outfile',
                         default='/tmp/job-graph.svg',
                         help='Restrict tree to this job')
        parser.add_option_group(group)

        return parser

    def handle(self, *args, **options):
        """ Main command handler. """

        dot = Digraph(name='Job Graph', comment='Job Graph', format='svg',
                      engine='twopi')

        def status_to_color(status):
            return {Job.NEW: 'lightgray',
                    Job.QUEUED: 'yellow',
                    Job.RUNNING: 'lightblue',
                    Job.COMPLETE: 'lightgreen',
                    Job.ERROR: 'red'}[status]

        for job in Job.objects.all():

            jobinfo = "%s&#10;Created: %s" % (str(job.table), job.created)

            dot.node('J-%d' % job.id,
                     style='filled', color=status_to_color(job.status),
                     tooltip=jobinfo)

            if job.parent:
                dot.edge('J-%d' % job.parent.id, 'J-%d' % job.id)

            if job.master:
                dot.edge('J-%d' % job.id, 'J-%d' % job.master.id,
                         style='dashed')

        outfile = options['outfile']
        if outfile.endswith('.svg'):
            outfile = outfile[:-4]
        dot.render(outfile)
        print "Rendered to %s.svg" % outfile
