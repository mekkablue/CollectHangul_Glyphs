# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import traceback

LANGUAGES = {'Eng':0, 'Kor': 1}
defaultID = u'com.LineGap.CollectHangul'

class CollectHangul(GeneralPlugin):
	def settings(self):
		self.lang = LANGUAGES['Eng']
		if Glyphs.defaults['%s.language' % defaultID] in [0, 1]:
			self.lang = Glyphs.defaults['%s.language' % defaultID]

		self.menuName = ['_Collect Hangul', u'_한글 모으기'][self.lang]
		self.numWindows = [0]

	def start(self):
		try: 
			targetMenu = FILTER_MENU
			newMenuItem = NSMenuItem(self.menuName, self.showWindow)
			Glyphs.menu[targetMenu].insert(2, newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow, signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.menuName, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(11).submenu().insertItem_atIndex_(newMenuItem, 2)#addItem_(newMenuItem)
			print traceback.format_exc()

	def showWindow(self, sender):
		""" Do something like show a window"""
 		try:
 			if 0 == len(Glyphs.fonts):
 				strError = [u'❓ error ❓', u'❓ 오류 ❓'][self.lang]
 				strMessage = ['There is no opened font!', u'활성화된 폰트 창이 없습니다!'][self.lang]
				Message(strError, strMessage)
				return
 			if [0] != self.numWindows:
				strError = [u'❓ error ❓', u'❓ 오류 ❓'][self.lang]
 				strMessage = ['The plugin window already opened!', u'플러그인 창이 이미 열려 있습니다!'][self.lang]
 				return

 			Glyphs.clearLog()
 			import CollectHangulModule as CH

			import os
			fileName = '/Users/daekwonkim/Library/Application Support/Glyphs/Plugins/CollectHangul_update.glyphsPlugin/Contents/Resources/CollectHangulModule.pyc'
			if os.path.exists(fileName):
	 			os.remove(fileName)

			reload(CH)
 			CH.Run(self.numWindows, self.lang)

 		except:
 			print traceback.format_exc()

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
