# Pi Hole Static DHCP Leases to Adguard Migration Script 

Simple Python script to migrate static DHCP leases from Pi-Hole to Adguard

## Usage:

```python3 pihole_migrate_dhcp.py inputFile```

This will take your **Pi-Hole** static DCHP leases file using DNS Masq syntax as input and output a ```leases.json``` in **AdGuard Home** format

If no inputFile is specified, the script will try to use default Pi-Hole DCHP leases file located in ```/etc/dnsmasq.d/04-pihole-static-dhcp.conf```

## Loading File into Adguard Home

Please follow these steps to load this file into your Adguard Home instance:

1. Stop your AdGuard home instance
2. Copy your ```leases.json``` file in the data subfolder of your work folder (Example: ```/opt/adguard/work/data```)
3. Start your AdGuard home instance
