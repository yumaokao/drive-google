#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
import os
import sys
import logging
import urllib2
import fnmatch
import colorama
import progressbar
import global_mod as gm
from apiclient import errors
from command_list import CommandList

lg = logging.getLogger("DRIVE.TRASH")
#lg.setLevel(logging.INFO)


class CommandTrash(CommandList):
    """ A Drive Command Class """

    def init_cmdparser(self):
        ## python2.7 lack of aliases of add_parser in sub command.
        self.cmdparser = self.subparser.add_parser('trash',
                                                   help='command trash help')
        self.cmdparser.add_argument('src', nargs='+',
                                    help='google drive files')

    def do_service_command(self):
        """trash files
        """

        #lg.debug(self.args)
        pulls = self.get_all_src_files(self.args.src, hidedir=False)

        if len(pulls) == 0:
            sys.exit("No files matched in drive")
        self.info(colorama.Fore.RED +
                  "Would you like to trash these files ?" +
                  colorama.Style.RESET_ALL)
        for pidx in range(len(pulls)):
            self.info("%d %s" % (pidx, pulls[pidx]['title']))
        self.info("[a]= all, [0-%d]: number: " % (len(pulls) - 1))
        inpstr = raw_input().strip()
        allidxs = self.parse_input_string(inpstr, len(pulls))
        for pidx in allidxs:
            self.trash_a_file(pulls[pidx])

## private methods ##
    def trash_a_file(self, pfile, pname=None):
        lg.debug("title %s id %s" % (pfile['title'], pfile['id']))
        try:
            self.service.files().trash(fileId=pfile['id']).execute()
        except errors.HttpError, error:
            lg.error('An error occured: %s' % error)
            return None
        self.info("file %s is trashed" % pfile['title'])
