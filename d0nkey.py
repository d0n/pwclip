#!/usr/bin/env python3
"""
d0nkey - yubikey module
"""
import sys

from os import environ

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from yubico import \
    find_yubikey, yubikey, \
    yubico_exception

from yubico.yubikey_usb_hid import YubiKeyHIDDevice

from yubico.yubikey_neo_usb_hid import YubiKeyNEO_USBHID

from yubico.yubikey_4_usb_hid import YubiKey4_USBHID

from binascii import hexlify

def _yubikeys(ykser=None, dbg=None):
	"""
	return a list of yubikeys objects
	"""
	keys = {}
	for i in range(0, 255):
		try:
			key = find_yubikey(debug=dbg, skip=i)
		except yubikey.YubiKeyError:
			break
		if ykser and int(ykser) != int(key.serial()):
			continue
		keys[key.serial()] = key
	return keys

def _slotchalres(yk, chal, slot):
	try:
		return hexlify(yk.challenge_response(
            chal.ljust(64, '\0').encode(), slot=slot)).decode()
	except yubico_exception.YubicoError as err:
		pass

def chalres(chal, slot=2, ykser=None):
	keys = _yubikeys(ykser)
	for (ser, key) in keys.items():
		return _slotchalres(key, chal, slot)
	"""
	if not slot:
		return [_slotchalres(k, chal, s) for k in _yubikeys(ykser=ykser) for s in (2, 1)]
	res = [_slotchalres(k, chal, slot) for k in _yubikeys(ykser=ykser)]
	return res if len(res) > 1 else res[0]
	"""

def cpchalres(chal=None, slot=2, ykser=None):
	if not ykser:
		ykser = '' if 'YKSERIAL' not in environ.keys() else environ['YKSERIAL']
	if not chal:
		chal = input('enter challenge: ')
	__res = chalres(chal, slot, ykser)
	copyclip(__res)

class PasswordDialog(Gtk.MessageDialog):
	pwd = ''
	def __init__(self, parent):
		Gtk.Dialog.__init__(self, "password", parent, 0)
		self.set_border_width(50)
		box = self.get_content_area()
		entry = Gtk.Entry()
		entry.set_visibility(False)
		entry.set_invisible_char("*")
		entry.connect("key-press-event", self.okonenter)
		box.add(entry) #, False, False, 0)
		self.show_all()

	@staticmethod
	def clipswitch():
		p = Popen(['xsel', '-x'])
		p.communicate()

	@staticmethod
	def setpric(text):
		p = Popen(['xsel', '-i', '-p'], stdin=PIPE)
		p.communicate(input=text.encode('utf-'))

	@staticmethod
	def setclip(text):
		cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		cb.set_text(text, -1)
		cb.store()

	def okonenter(self, widget, ev, data=None):
		if ev.keyval == Gdk.KEY_Return:
			try:
				__hash = chalres(widget.get_text())
				self.clipswitch()
				self.setpric(__hash)
			finally:
				self.destroy()

class PassWin(Gtk.Window):
	checkpacks()
	def __init__(self):
		Gtk.Window.__init__(self, title="clipper")
		self.hide()

	def askpass(self): #, widget, ev, data=None):
		dialog = PasswordDialog(self)
		res = dialog.run()
		self.destroy()


