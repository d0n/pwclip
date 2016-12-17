# to only import all necessarry modules/libs define the calling executable
from net.rfkill import rfklocks, rfklist
from net.ping import ping
from net.eth import ETHConfig
from net.ldap import LDAPSearch
from net.vpn import VPNConfig
from net.wlan import WLANConfig
from net.wwan import WWANConfig

from net.network import addrmask, netips, ifaces, mac, macs, ifaddrs, isip, \
    anyifconfd, isconfd, haslink, isup, gateway, askdns, vpninfo, iftype, \
    netcat, raflookup, iternet, currentnets

from net.wakeonlan import wol

from net.telnet import telnet

from net.dhcp import DHCPDiscover

from net.ssh import SecureSHell
