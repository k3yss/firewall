#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>
#include <linux/udp.h>
#include <linux/string.h>

/**
 * Macro to convert an IP address to its individual octets.
 * 
 * This macro takes an IP address as input and converts it to its individual octets.
 * It is used to extract the octets of an IP address for printing or manipulation purposes.
 * 
 * @param addr The IP address to convert.
 * @return The individual octets of the IP address.
 */
#define IPADDRESS(addr) \
  ((unsigned char *)&addr)[3], \
  ((unsigned char *)&addr)[2], \
  ((unsigned char *)&addr)[1], \
  ((unsigned char *)&addr)[0]


/**
 * @brief Pointer to the nf_hook_ops structure used to block ICMP packets.
 */
static char *ip_addr_rule = "127.0.0.1";

module_param(ip_addr_rule, charp, 0644);

MODULE_PARM_DESC(ip_addr_rule, "IP address to block");

static struct nf_hook_ops *nf_blockicmppkt_ops = NULL;
static struct nf_hook_ops *nf_blockipaddr_ops = NULL;

/**
 * nf_blockipaddr_handler - Function to handle blocking IP addresses
 * @priv: Pointer to private data
 * @skb: Pointer to the socket buffer
 * @state: Pointer to the netfilter hook state
 *
 * This function is responsible for handling the blocking of IP addresses.
 * It is called by the netfilter framework when a packet matches the configured rule.
 * The function takes a pointer to private data, a pointer to the socket buffer,
 * and a pointer to the netfilter hook state as parameters.
 *
 * Returns: Unsigned integer representing the netfilter verdict
 */
static unsigned int nf_blockipaddr_handler(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
	if (!skb) {
		return NF_ACCEPT;
	} else {
		char *str = (char *)kmalloc(16, GFP_KERNEL);
		u32 sip;
		struct sk_buff *sb = NULL;
		struct iphdr *iph;

		sb = skb;
		iph = ip_hdr(sb);
		sip = ntohl(iph->saddr);

		sprintf(str, "%u.%u.%u.%u", IPADDRESS(sip));

		if(!strcmp(str, ip_addr_rule)) {
			printk(KERN_ERR "[Firewall] Drop packet from %s\n", str);
			return NF_DROP;
		} else {
			return NF_ACCEPT;
		}
	}
}

/**
 * nf_blockicmppkt_handler - Function to handle ICMP packets in the firewall
 * @priv: Pointer to private data (not used in this function)
 * @skb: Pointer to the received packet
 * @state: Pointer to the firewall hook state
 *
 * This function is a callback function registered with the netfilter framework
 * to handle ICMP packets in the firewall. It is called whenever an ICMP packet
 * is received by the firewall. The function takes the received packet, along
 * with the firewall hook state, and performs the necessary actions to handle
 * the ICMP packet.
 *
 * Return: Unsigned integer representing the action to be taken on the packet
 */
static unsigned int nf_blockicmppkt_handler(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
  struct iphdr *iph;   // IP header
  struct udphdr *udph; // UDP header
  if (!skb)
    return NF_ACCEPT;
  iph = ip_hdr(skb); // retrieve the IP headers from the packet
  if (iph->protocol == IPPROTO_UDP)
  {
    udph = udp_hdr(skb);
    //  Port 53 is commonly used for DNS (Domain Name System) queries
    if (ntohs(udph->dest) == 53)
    {
      return NF_ACCEPT; // accept UDP packet
    }
  }
  else if (iph->protocol == IPPROTO_TCP)
  {
    return NF_ACCEPT; // accept TCP packet
  }
  else if (iph->protocol == IPPROTO_ICMP)
  {
    printk(KERN_ERR "[Firewall] Drop ICMP packet\n");
    return NF_DROP; // drop TCP packet
  }
  return NF_ACCEPT;
}

/**
 * Initializes the nf_minifirewall module.
 *
 * This function is called when the module is loaded into the kernel.
 * It performs the necessary initialization steps for the nf_minifirewall module.
 *
 * @return 0 on success, a negative error code on failure.
 */
static int __init nf_minifirewall_init(void) {
  printk(KERN_WARNING "[Firewall] Starting the firewall ...\n");
	nf_blockicmppkt_ops = (struct nf_hook_ops*)kcalloc(1,  sizeof(struct nf_hook_ops), GFP_KERNEL);
	if (nf_blockicmppkt_ops != NULL) {
		nf_blockicmppkt_ops->hook = (nf_hookfn*)nf_blockicmppkt_handler;
		/**
		 * Sets the hook number for blocking ICMP packets.
		 * 
		 * The hook number determines the position in the network stack where the
		 * Netfilter hook function will be called. By setting it to NF_INET_PRE_ROUTING,
		 * the hook function will be called before the routing decision is made.
		 * 
		 * @param nf_blockicmppkt_ops A pointer to the structure representing the Netfilter
		 *                            hook operation.
		 */
		nf_blockicmppkt_ops->hooknum = NF_INET_PRE_ROUTING;
		nf_blockicmppkt_ops->pf = NFPROTO_IPV4;
		nf_blockicmppkt_ops->priority = NF_IP_PRI_FIRST; // set the priority
		
		nf_register_net_hook(&init_net, nf_blockicmppkt_ops);
	}

  nf_blockipaddr_ops = (struct nf_hook_ops*)kcalloc(1, sizeof(struct nf_hook_ops), GFP_KERNEL);
	if (nf_blockipaddr_ops != NULL) {
		nf_blockipaddr_ops->hook = (nf_hookfn*)nf_blockipaddr_handler;
		nf_blockipaddr_ops->hooknum = NF_INET_PRE_ROUTING;  // register to the same hook
		nf_blockipaddr_ops->pf = NFPROTO_IPV4;
		nf_blockipaddr_ops->priority = NF_IP_PRI_FIRST + 1; // set a higher priority

		nf_register_net_hook(&init_net, nf_blockipaddr_ops);
	}

	return 0;
}

/**
 * @brief Function to exit the nf_minifirewall module.
 *
 * This function is called when the nf_minifirewall module is being unloaded from the kernel.
 * It performs any necessary cleanup operations before the module is removed.
 */
static void __exit nf_minifirewall_exit(void) {
	printk(KERN_WARNING "[Firewall] Exiting the firewall ...\n");
	if(nf_blockicmppkt_ops != NULL) {
		nf_unregister_net_hook(&init_net, nf_blockicmppkt_ops);
		kfree(nf_blockicmppkt_ops);
	}
	if (nf_blockipaddr_ops  != NULL) {
		nf_unregister_net_hook(&init_net, nf_blockipaddr_ops);
		kfree(nf_blockipaddr_ops);
	}
}


module_init(nf_minifirewall_init);
module_exit(nf_minifirewall_exit);
MODULE_LICENSE("GPL");
