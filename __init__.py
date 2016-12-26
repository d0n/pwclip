from socket import getfqdn

hostname = getfqdn()

from system.stamp import stamp

from system.fileage import fileage

from system.path import absrelpath, realpaths, confpaths, confdats, jconfdats

from system.blockdevice import BlockDevice

from system.sysfs import SysFs

from system.bestlim import bestlim

from system.lineno import lineno

from system.which import which

from system.random import random

from system.string2bool import string2bool

from system.gpgagent import agentinfo

from system.user.whoami import whoami

from system.user.find import userfind

from system.clips import clips, copy, paste

from system.power import SystemPower

from system.uefi import UEFITool

from system.blkid import BlockDevices

from system.xlib import xinput, xnotify, xyesno, xmsgok
