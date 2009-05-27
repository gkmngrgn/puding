#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3

import os
import gettext

app_launch_name = 'puic'

if os.path.exists('locale'):
    localedir = 'locale'

else:
    localedir = '/usr/share/locale'

t = gettext.translation(app_launch_name, localedir, fallback = True)
_ = t.ugettext

