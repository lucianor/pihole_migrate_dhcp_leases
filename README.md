# Pi Hole Static DHCP Leases to Adguard Migration Script 
Simple Python script to migrate static DHCP leases from Pi-Hole to Adguard

Usage:

_python3 pihole_migrate_dhcp.py <inputFile>_

If no inputFile is specified, the script will try to use default Pi-Hole DCHP leases file located in /etc/dnsmasq.d/04-pihole-static-dhcp.conf
