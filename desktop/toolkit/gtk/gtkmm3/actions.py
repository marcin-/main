#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

def setup():
    autotools.configure("--disable-static")

    pisitools.dosed("libtool", " -shared ", " -Wl,-O1,--as-needed -shared ")

    pisitools.dosed("libtool", "^(hardcode_libdir_flag_spec=).*", '\\1""')
    pisitools.dosed("libtool", "^(runpath_var=)LD_RUN_PATH", "\\1DIE_RPATH_DIE")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.dodoc("ChangeLog","COPYING", "NEWS", "README")
