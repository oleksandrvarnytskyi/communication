from ipv4address import IPv4Address


class InvalidMaskLength(Exception):
    pass


class Network(object):
    def __init__(self, ip_addr, mask_length):
        self.mask_length = mask_length
        self.quantity_of_ip = 1 << 32 >> self.mask_length
        self.mask = (1 << 32) - self.quantity_of_ip
        self.network_address = IPv4Address((int(ip_addr) & self.mask))
        if 0 <= mask_length < 31:
            self.total_hosts = self.quantity_of_ip - 2
            self.first_usable_address = IPv4Address(
                int(self.network_address) + 1)
            self.last_usable_address = IPv4Address(
                int(self.network_address) + self.total_hosts)
            self.broadcast_address = IPv4Address(
                int(self.network_address) + self.total_hosts + 1)
        elif mask_length == 31:
            self.total_hosts = 0
            self.first_usable_address = None
            self.last_usable_address = None
            self.broadcast_address = IPv4Address(
                int(self.network_address) + self.total_hosts + 1)
        elif mask_length == 32:
            self.total_hosts = 0
            self.first_usable_address = None
            self.last_usable_address = None
            self.broadcast_address = self.network_address
        else:
            raise InvalidMaskLength

    def __contains__(self, ip):
        return int(self.network_address) <= int(ip) <= \
                int(self.broadcast_address)

    @property
    def is_public(self):
        flag = True
        for item in PRIVATE_NETWORKS:
            if self.network_address in item:
                flag = False
        return flag

    @property
    def get_mask_str(self):
        return IPv4Address.int2ip(self.mask)

    @property
    def subnets(self):
        sub_mask_length = self.mask_length + 1
        if self.mask_length > 31:
            return []
        else:
            subnet1 = Network(self.network_address, sub_mask_length)
            subnet2 = Network(self.broadcast_address, sub_mask_length)
            return [subnet1, subnet2]

    def __str__(self):
        return '{0}/{1}'.format(self.network_address, self.mask_length)


PRIVATE_NETWORKS = [Network(IPv4Address('10.0.0.0'), 8),
                    Network(IPv4Address('172.16.0.0'), 12),
                    Network(IPv4Address('192.168.0.0'), 16)]

if __name__ == '__main__':
    address = IPv4Address("192.168.0.1")
    net = Network(address, 8)
    print net
    print address
    print net.get_mask_str
    print 'network_address:     ', net.network_address
    print 'first_usable_address:', net.first_usable_address
    print 'last_usable_address: ', net.last_usable_address
    print 'broadcast_address:   ', net.broadcast_address
    print IPv4Address("10.0.23.4") in net
    print IPv4Address("192.168.0.25") in net
    print net.is_public

    subnets = net.subnets
    print '-'*33
    try:
        print subnets[0]
        print subnets[0].network_address
        print subnets[0].first_usable_address
        print subnets[0].last_usable_address
        print subnets[0].broadcast_address
        print subnets[0].mask_length
        print subnets[0].total_hosts

        print '-'*33
        print subnets[1]
        print subnets[1].network_address
        print subnets[1].first_usable_address
        print subnets[1].last_usable_address
        print subnets[1].broadcast_address
        print subnets[1].mask_length
        print subnets[1].total_hosts
    except IndexError:
        print 'IndexError'
