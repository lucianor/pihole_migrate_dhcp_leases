import sys
import json
import os

# check if an input file was specificied, if not try to use the default location for pihole leases file
if (len(sys.argv) < 2):
    inputFile = "/etc/dnsmasq.d/04-pihole-static-dhcp.conf"
    print()
    print("WARNING: No input file specified. Please run 'python3 pihole_migrate_dhcp.py <inputFile>'")
    print()
    print("Trying default Pi-Hole file: /etc/dnsmasq.d/04-pihole-static-dhcp.conf")
    print()
else:
    inputFile= sys.argv[1]

# check if input file exists, otherwise exit
if (not os.path.isfile(inputFile)):
    print("ERROR: Input file {} does not exists".format(inputFile))
    print()
    exit()

# open pi-hole lease file
piHoleLeasesFile = open(inputFile, 'r')
piHoleLeaseLines = piHoleLeasesFile.readlines()

# create leases list of dict
leasesLists= []

# initiate lease counter
count = 0

# read line by line for pihole file
for line in piHoleLeaseLines:
    pihole_item=line.strip()
    pihole_item_trim = pihole_item[10:] # remove dhcp-host= from the beginning of the string
    pihole_data = pihole_item_trim.split(",")
    lease = {
        "mac": pihole_data[0],
        "ip": pihole_data[1],
        "hostname": (pihole_data[2] if (len(pihole_data)>2) else ""),
        "static": True,
    }
    leasesLists.append(lease)
    count += 1

# close pi-hole file
piHoleLeasesFile.close()

# create adguard lease json strucutre
adguardJson= {
    "version": 1,
    "leases": leasesLists
}

# create json file and dump list to it
adGuardLeasesFile = open('leases.json', 'w')
adGuardLeasesFile.writelines(json.dumps(adguardJson))
adGuardLeasesFile.close()

print()
print("SUCCESS: {} static leases imported".format(count))
print()

print("Please follow these steps to load this file into your Adguard Home instance:")
print()
print("Step 1: Stop your AdGuard home instance")
print("Step 2: Copy your leases.json file in the data subfolder of your work folder (Example: /opt/adguard/work/data)")
print("Step 3: Start your AdGuard home instance")
print()
