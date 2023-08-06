DNS

What is a DNS? The Domain Name System (DNS) is the phonebook of the Internet.
Humans access information online through domain names, like digicloud.com or digikala.com.
Web browsers interact through Internet Protocol (IP) addresses.
DNS translates domain names to IP addresses so browsers can load Internet resources.

Domain

What is a domain? A domain name is the identity of one or more IP addresses.
Domain names are invented as it is easy to remember a name rather than a long string of numbers.

Digicloud present you DNS service. You can add your domain and records.
Notice that these operations are related to your digicloud namespace.

## Examples:
    
1 **Create a Domain**

    $ digicloud dns domain create digicloud.com

2 **List Domains**

    $ digicloud dns domain list


Record

What is a record? DNS records are instructions that live in authoritative DNS servers and 
provide information about a domain including what IP address is associated with that domain
and how to handle requests for that domain.

All DNS records have a TTL, which stands for time-to-live, and indicates how often a DNS server will refresh that record.

Supported types of DNS record in DigiCloud:

* A Record:

    The record that holds the IP address of a domain.

* TXT Record:

    Lets an admin store text notes in the record.

* CNAME Record:

    Forwards one domain or subdomain to another domain, does NOT provide an IP address.

* MX Record:

    Directs mail to an email server.

* SRV Record:

    Specifies a port for specific services.

TTL choices:

    2m, 10m, 30m, 1h, 3h, 10h

Record type choices:

    A, TXT, CNAME, MX, SRV

SRV record proto choices:

    _tcp, _udp, _tls

## Examples:

1 **Create a Record type A**

    $ digicloud dns record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type A
      --ip-address 10.10.10.10

2 **Create a Record type TXT**

    $ digicloud dns record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type TXT
      --content "my content"

3 **Create a Record type CNAME**

    $ digicloud dns record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type CNAME
      --target digikala.com

4 **Create a Record type MX**

    $ digicloud dns record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type MX
      --mail-server mail.com
      --priority 100

5 **Create a Record type SRV**

    $ digicloud dns record create
      --domain your-domain-name-or-id
      --name my-record
      --ttl 2m
      --type SRV
      --port 8000
      --weight 100
      --proto _tcp
      --service _servicename
      --target digicloud.com
      --priority 100

6 **List Records of a domain**

    $ digicloud dns record list --domain your-domain-name-or-id

9 **Get a Record details**

    $ digicloud dns record show record-id --domain your-domain-name-or-id

8 **Update a Record**

Note record type can not be changed.

    $ digicloud dns record update record-id --name new_name --domain your-domain-name-or-id

9 **Delete a Record**

    $ digicloud dns record delete record-id --domain your-domain-name-or-id
