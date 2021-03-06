#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
general functions for FritzCall plugin

$Id: __init__.py 1454 2017-06-11 13:24:13Z michael $
$Author: michael $
$Revision: 1454 $
$Date: 2017-06-11 15:24:13 +0200 (Sun, 11 Jun 2017) $
'''

from Components.config import config #@UnresolvedImport
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS #@UnresolvedImport
import gettext, os
from enigma import eBackgroundFileEraser
from logging import NOTSET

lang = language.getLanguage()
os.environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("FritzCall", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/FritzCall/locale/"))

def _(txt): # pylint: disable=C0103
	td = gettext.dgettext("FritzCall", txt)
	if td == txt:
		td = gettext.gettext(txt)
	return td

# scramble text
def __(text, front=True):
	#===========================================================================
	# if len(text) > 5:
	#	if front:
	#		return '.....' + text[5:]
	#	else:
	#		return text[:-5] + '.....'
	# else:
	#	return '.....' 
	#===========================================================================
	out =""
	for i in range(len(text)/2):
		out = out + text[i*2] + '.'
	return out

import re
def normalizePhoneNumber(intNo):
	
	found = re.match(r'^\+' + config.plugins.FritzCall.country.value.replace('00','') + '(.*)', intNo)
	if found:
		intNo = '0' + found.group(1)
	found = re.match(r'^\+(.*)', intNo)
	if found:
		intNo = '00' + found.group(1)
	intNo = intNo.replace('(', '').replace(')', '').replace(' ', '').replace('/', '').replace('-', '')
	found = re.match('^49(.*)', intNo) # this is most probably an error
	if found:
		intNo = '0' + found.group(1)
	found = re.match('.*?([0-9]+)', intNo)
	if found:
		return found.group(1)
	else:
		return '0'
