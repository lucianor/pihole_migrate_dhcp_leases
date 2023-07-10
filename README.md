# Pi Hole Static DHCP Leases to AdGuard Migration Script 

Simple Python script to migrate static DHCP leases from Pi-Hole to AdGuard

## Usage:

```python3 pihole_migrate_dhcp.py inputFile```

This will take your **Pi-Hole** static DCHP leases file using DNS Masq syntax as input and output a ```leases.json``` in **AdGuard Home** format

If no inputFile is specified, the script will try to use default Pi-Hole DCHP leases file located in ```/etc/dnsmasq.d/04-pihole-static-dhcp.conf```

## Loading File into AdGuard Home

Please follow these steps to load this file into your AdGuard Home instance:

1. Stop your AdGuard home instance
2. Copy your ```leases.json``` file in the data subfolder of your work folder (Example: ```/opt/adguard/work/data```)
3. Start your AdGuard home instance



## EXAMPLE: Replacing Pi-Hole with AdGuard Home on an Ubuntu Server

Commands to get an AdGuard Home with your DHCP static leases from Pi-Hole running in less than 2 minutes.

Step 1: Become a root user and download this script - optionally, you can prefix all other commands with ```sudo``` if you prefer
```
sudo -s
cd ~
git clone https://github.com/lucianor/pihole_migrate_dhcp_leases.git
cd pihole_migrate_dhcp_leases/
python3 pihole_migrate_dhcp.py
```

Step 2: Prepare AdGuard Home Installation folder
```
mkdir -p /opt/adguard
mkdir -p /opt/adguard/conf
mkdir -p /opt/adguard/work
```

Step 3: Say goodbye to Pi-Hole. **Warning**: I chose not to remove system packages 
```
pihole uninstall
rm -rf /etc/.pihole /etc/pihole /opt/pihole /usr/bin/pihole-FTL /usr/local/bin/pihole /var/www/html/admin
```

Step 4: Disable Ubuntu ```systemd-resolved``` following [AdGuard Home FAQ](https://github.com/AdguardTeam/AdGuardHome/wiki/FAQ#bindinuse)
```
mkdir -p /etc/systemd/resolved.conf.d
nano /etc/systemd/resolved.conf.d/adguardhome.conf
```
4.1 Paste contents below and save
```
[Resolve]
DNS=127.0.0.1
DNSStubListener=no
```
4.2 Reload systemd-resolved DNS stub
```
mv /etc/resolv.conf /etc/resolv.conf.backup
ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
systemctl reload-or-restart systemd-resolved
```

Step 5 (OPTIONAL): I have other Web services running on lightttpd, so I stop it first for the initial install of AdGuard Home
```
service lighttpd stop
```

Step 6: Start AdGuard Home docker container using the folders created on step 2, and with ```--net-host``` option since I'm planning to use it as a DHCP Server, following instructions [here](https://hub.docker.com/r/adguard/adguardhome#dhcp)
```
docker run --name adguardhome --restart unless-stopped -v /opt/adguard/work:/opt/adguardhome/work -v /opt/adguard/conf:/opt/adguardhome/conf --net=host -d adguard/adguardhome
```

Step 7: Access your server IP on port 80 and configure it. OPTIONAL: Configure to use port 3000 for management instead of port 80

Step 8: Stop your AdGuard Home installation and load the imported DHCP static leases file from Pi-Hole from step 1
```
docker stop adguardhome
cd ~
cp leases.json /opt/adguard/work/data
```

Step 9: Start your AdGuard Home container and enable your DHCP server. Repeat step 8 if leases are not listed on the page
```
docker start adguardhome
```

