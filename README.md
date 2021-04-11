# Python-NAT
Python based Static NAT Tool

Static NAT maps network traffic from a static external IP address to an internal IP address or network. It creates a static translation of real addresses to mapped addresses. To execute this utility you need to have Ubuntu box with two NICs. NAT translations are happens between these interfaces.

# Syntax
python3 <*Inside-Local-IP*> <*Inside-Global-IP*>
  

Inside-Local-IP = The IP address of the device in Inside Network.

Inside-Global-IP = The IP address of the outside interface.


Tested with Ubuntu 20.04 with Python 3.8.2

# Limitations
This utility only works with ICMP traffic because of I alter the TCP/UDP headers. Then TCP/UDP checksum validation fails. Also I hardcoded the ens33 and ens38 interfaces, change them to yours. 
