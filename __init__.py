# to only import all necessarry modules/libs define the calling executable
from net.addr import \
	addrmask, netips, \
	iternet, gateway, isip

from net.dns import \
	fqdn, askdns, raflookup

from net.iface import \
	haslink, isup, \
	ifaces, ifaddrs, \
	anyifconfd, isconfd, \
	iftype, currentnets, iftrough

from net.mac import mac, macs
from net.ssh import SecureSHell
from net.ldap import LDAPSearch

# interface
from net.interface.eth import ETHConfig
from net.interface.vpn import VPNConfig
from net.interface.wlan import WLANConfig
from net.interface.wwan import WWANConfig

# util
from net.util.dhcp import DHCPDiscover
from net.util.ifdrougs import \
	dhclient, ifup, ifdown, ifconfup, ifconfdown, ping
from net.util.mailing import sendmail
from net.util.netcat import netcat
from net.util.ping import ping
from net.util.rfkill import rfklocks, rfklist
from net.util.wakeonlan import wol
