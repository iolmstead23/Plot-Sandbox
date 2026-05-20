[[Domain Names]] are human-readable addresses that simplify navigation on the internet. Instead of remembering numerical IP addresses, users can use domain names like “www.google.com” to access websites. The **Domain Name System (DNS)** acts as a bridge between human-friendly domain names and machine-friendly IP addresses, translating them into the numeric addresses necessary for computers to locate and communicate with each other over the internet.

### How DNS Works:
When you type a domain name into your browser, a DNS server is consulted to find the corresponding IP address. This process involves several steps:
1. **DNS Query**: Your browser sends a DNS query to a DNS resolver (usually provided by your ISP) to ask for the IP address of the domain.
2. **Recursive Search**: If the resolver doesn't have the address cached, it contacts other DNS servers in a hierarchical fashion:
   - **Root DNS Server**: Directs the resolver to the correct **Top-Level Domain (TLD)** server, based on the extension (like .com, .org).
   - **TLD Server**: Points the resolver to the authoritative DNS server for the domain.
   - **Authoritative DNS Server**: Provides the exact IP address of the domain.
3. **Returning IP Address**: The resolver returns the IP address to your browser, which can then establish a connection to the website’s server.

This DNS lookup process usually happens within milliseconds.

### History of DNS and Domain Names:
The need for a system like DNS arose in the early days of the internet (ARPANET), where a centralized file (hosts.txt) was used to map domain names to IP addresses. As the internet grew, this method became impractical. In 1983, **Paul Mockapetris** proposed the DNS system, which created a distributed, hierarchical naming system, making it easier to scale as the internet expanded.

### IP Addresses and DNS:
- **IPv4**: Initially, the internet used a 32-bit address system (IPv4), providing approximately 4.3 billion unique IP addresses. As internet usage exploded, the pool of available IPv4 addresses diminished.
- **IPv6**: To address the exhaustion of IPv4 addresses, **IPv6** was introduced, which uses a 128-bit address system, vastly increasing the number of possible addresses.

The **[[Icann Internet Corporation For Assigned Names And Numbers]]** manages the allocation of IP address blocks to ISPs, who then assign individual IP addresses to devices. DNS servers, maintained by various organizations and ISPs, ensure that when a user enters a domain name, it gets translated into the right IP address quickly and efficiently.