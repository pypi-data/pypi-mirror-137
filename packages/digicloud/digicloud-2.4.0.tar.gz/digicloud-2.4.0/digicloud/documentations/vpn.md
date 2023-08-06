VPN is a virtual private network is like bridge between your network in DigiCloud and outside network.

You can extend your DigiCloud private network across internet.
VPN is an encrypted connection over the Internet from a device to a network.
The encrypted connection helps ensure that sensitive data is safely transmitted.
It prevents unauthorized people from eavesdropping on the traffic and allows the user to conduct work remotely.

## Examples:

1. **Create VPN**
    
    One can simply create a vpn with bellow command:

        $ digicloud vpn external create  \
            --description "some description"  \
            --local-endpoint-group "4e01f3ec-2548-4b53-8f38-74345e4ba9e0"  \
            --peer-id 1.1.1.1  \
            --peer-address 1.1.1.1  \
            --peer-endpoint-group "10.10.0.0/24"  \
            --psk "some secret here"  \
            --vpn-router-id "c06a72d2-b25a-4b21-b7af-93e4a0f392a9"  \
            --mtu=68  \
            "my-vpn-connection"
        
        Required arguments:
   
            --local-endpoint-group:
           
                List of local subnet names or ids. E.g: subnet_1 subnet_2
           
            --peer-id:
                
                The peer router identity for authentication.
                A valid value is an IPv4 address, IPv6 address or FQDN.
                Typically, this value matches the --peer-address.
           
            --peer-address:
           
                The peer gateway public IPv4 or IPv6 address or FQDN.
           
            --peer-endpoint-group:
           
                list of peer networks in CIDR format. E.g: cidr_1 cidr_2
           
            --psk:
           
                Pre-shared shared key for the VPN connection.
           
            --vpn-router-id:
           
                The id of the router to be used with the VPN
           
            --mtu:
           
                The maximum transmission unit (MTU) value to address fragmentation.
                Minimum value is 68 for IPv4, and 1280 for IPv6.
        
        Optinal arguments:
            
            --initiator:
                
                Indicates whether this VPN can only respond to connections or both respond to and initiate connections. 
                A valid value is 'response-only' or 'bi-directional'. Default is 'bi-directional'.
            
            --admin-state-down:
                
                Sets the administrative state of the resource to 'down',
                Including this switch means 'down' state. Omitting this switch means 'up' state

            --ike-auth-algorithm:
   
                The IKE authentication hash algorithm. Valid values are 'sha1', 'sha256', 'sha384', 'sha512'.
                The default is 'sha1'.
   
            --ike-encryption-algorithm:
   
                The IKE encryption algorithm. A valid value is '3des', 'aes-128', 'aes-192', 'aes-256'. 
                Default is 'aes-128'.
   
            --ike-pfs:
            
                Perfect forward secrecy (PFS). A valid value is 'group2', 'group5', 'group14'. Default is 'group5'.
   
            --ike-lifetime:
   
                IKE lifetime in seconds. Default is 3600.
   
            --ike-version:
            
                The IKE version. A valid value is 'v1' or 'v2'. Default is 'v1'.
   
            --vpn-router-id:
                
                The id of the router to be used with the VPN
   
            --ipsec-auth-algorithm:
            
                The IpSec authentication hash algorithm. Valid values are 'sha1', 'sha256', 'sha384', 'sha512'. 
                The default is 'sha1'. 
   
            --ipsec-encapsulation-mode:
    
                The IpSec encapsulation mode. A valid value is 'tunnel' or 'transport'. Default is 'tunnel'.
   
            --ipsec-encryption-algorithm:
   
                The IpSec encryption algorithm. A valid value is '3des', 'aes-128', 'aes-192', 'aes-256'.
                Default is 'aes-128'.
   
            --ipsec-pfs:
   
                The IpSec perfect forward secrecy (PFS). A valid value is 'group2', 'group5', 'group14',
                Default is 'group5'.
   
            --ipsec-transform-protocol:
   
                The IpSec transform protocol. A valid value is 'esp', 'ah', or 'ah-esp'. Default is 'esp'.

            --ipsec-lifetime:
   
                The IpSec lifetime in seconds. Default is 3600.
   

2. **List VPNs**
    
       $ digicloud vpn external list

3. **VPN details**

       $ digicloud vpn external show my-vpn-connection

4. **VPN update**

       $ digicloud vpn external show my-vpn-connection  \
            --name my-vpn-new-name  \
            --desription "my new description"  \
            --admin-state-down or --admin-state-up

5. **Delete VPN**

      $ digicloud vpn external delete my-vpn-connection
