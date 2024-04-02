# Kernel Module Firewall for Linux Based Systems
Implementation of software based firewall for linux based systems.

**Features**:
- *ICMP blocking*: commands like `ping` use ICMP protocol but modern browsers use the TCP/IP protocol, which is beyond the scope of this project
- *IP blocking*: we can specify the IP address we want to block

### Quickstart

**Prerequisites**

Install the linux kernel headers
```
$ sudo apt install linux-headers
```
**Build and run**
```shell
$ git clone https://github.com/k3ys/firewall && cd firewall
$ make
$ sudo insmod firewall.ko ip_addr_rule=<desired-ip>
```

## Notes:
**Why are we using a kernel module?**

Don't want to recompile the kernel everytime, it is easier this way and also the standard practice.

## Future plans

Making the firewall more robust and incorporate more hooks: `NP_INET_FORWARD`, `NP_INET_POST_ROUTING`, `NP_INET_LOCAL_IN`, `NP_INET_LOCAL_OUT`.

## References
1. [Simple Kernel Module in C (video)](https://www.youtube.com/watch?v=SOo1rbnryeo)
2. [Linux firewall from scratch based on Netfilter (blog)](https://levelup.gitconnected.com/write-a-linux-firewall-from-scratch-based-on-netfilter-462013202686)
3. [Linux Kernel Module Programming Guide (documentation)](https://sysprog21.github.io/lkmpg/)
4. [Linux Kernel Source Tree](https://github.com/torvalds/linux)
5. [Linux Kernel Networking Documenation](https://www.kernel.org/doc/html/latest/networking/index.html)