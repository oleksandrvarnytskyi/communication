class IllegalArgument(Exception):
    pass


class IPv4Address(object):
    def __init__(self, ip_address):
        self.ip_address_str = self.int2ip(ip_address) if isinstance(
            ip_address, (long, int)) else ip_address
        self.ip_address_int = self.ip2int(ip_address) if isinstance(
            ip_address, str) else ip_address

    @staticmethod
    def ip2int(address):
        try:
            parts = address.split('.')
            for key in range(4):
                if not 0 <= int(parts[key]) <= 255:
                    raise ValueError
            return int(parts[0]) << 24 | int(parts[1]) << 16 | \
                int(parts[2]) << 8 | int(parts[3])
        except (ValueError, TypeError):
            print 'Value or Type Error'

    @staticmethod
    def int2ip(address):
        for key in (24, 16, 8):
            if not 0 <= ((address >> key) & 255) <= 255:
                raise ValueError
        return '{0}.{1}.{2}.{3}'.format(str((address >> 24) & 255),
                                        str((address >> 16) & 255),
                                        str((address >> 8) & 255),
                                        str(address & 255))

    def __le__(self, ip_address):
        return int(self) < int(ip_address)

    def __gt__(self, ip_address):
        return int(self) > int(ip_address)

    def __eq__(self, ip_address):
        return int(self) == int(ip_address)

    def __ne__(self, ip_address):
        return int(self) != int(ip_address)

    def __int__(self):
        return self.ip_address_int

    def __str__(self):
        return self.ip_address_str


if __name__ == '__main__':
    ip = IPv4Address("127.12.45.22")
    print ip
    print int(ip)

    ip = IPv4Address(2131504406)
    print ip
    print int(ip)

    print ip == IPv4Address("127.12.45.22")
    print ip == IPv4Address(2131504406L)
    print ip == IPv4Address(0xF834AD02L)
    print ip == IPv4Address("189.11.23.211")
    print ip > IPv4Address("131.16.34.66")
    print ip < IPv4Address("131.16.34.66")
