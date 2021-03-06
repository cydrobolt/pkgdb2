#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
Script to run to branch packages from the `devel` collection into the new,
specified collection.
'''

import argparse
import os

from sqlalchemy.exc import SQLAlchemyError


if 'PKGDB2_CONFIG' not in os.environ \
        and os.path.exists('/etc/pkgdb2/pkgdb2.cfg'):
    print 'Using configuration file `/etc/pkgdb2/pkgdb2.cfg`'
    os.environ['PKGDB2_CONFIG'] = '/etc/pkgdb2/pkgdb2.cfg'


try:
    import pkgdb2
except ImportError:
    import sys
    sys.path.insert(
        0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    import pkgdb2

import pkgdb2.lib


class FakeFasUser(object):
    ''' Fake FAS user sent to pkgdb2 to behave as if we had logged in
    normally.
    We can do that since we are running directly from the host and thus
    calling directly the internal method.
    '''

    def __init__(self, username, groups=[]):
        ''' Instanciate a FakeFasUser object.

        :arg username: the username of the user in FAS.
        :type username: str
        :kwarg groups: the FAS groups in which the user is.
        :type groups: list

        '''

        self.username = username
        self.groups = []
        if groups:
            self.groups = groups
        self.cla_done = True


def get_arguments():
    ''' Set the command line parser and retrieve the arguments provided
    by the command line.
    '''
    parser = argparse.ArgumentParser(
        description='pkgdb2_branch')
    parser.add_argument(
        'new_branch',
        help='Name of the new collection in which to branch `master`')
    parser.add_argument(
        '--user', dest='user', nargs='+',
        help='FAS username of the user performing the action')
    parser.add_argument(
        '--groups', dest='groups', action='append',
        help='FAS groups in which the user performing the action is')

    return parser.parse_args()


def main():
    ''' Retrieve all the package associated to the collection `devel` and
    branch them into the specified collection.

    :arg collection_name: the name of the collection in which to branch the
        ACL of the packages present in `master`.

    '''
    # Retrieve arguments
    args = get_arguments()

    user = FakeFasUser(username=args.user, groups=args.groups)

    try:
        pkgdlist = pkgdb2.lib.add_branch(
            pkgdb2.SESSION,
            clt_from='master',
            clt_to=args.new_branch,
            user=user,
        )
    except pkgdb2.lib.PkgdbException, err:
        print err
        return 1

    try:
        pkgdb2.SESSION.commit()
    except SQLAlchemyError. err:
        print err
        return 1

    return 0


if __name__ == '__main__':
    main()
