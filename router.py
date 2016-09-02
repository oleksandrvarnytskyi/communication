from ipv4address import IPv4Address
from network import Network


class Route(object):
    def __init__(self, network, gateway, interface_name, metric):
        self.network = network
        self.gateway = gateway
        self.interface_name = interface_name
        self.metric = metric

    def __str__(self):
        if self.gateway:
            return 'net: {0}, gateway: {1}, interface: {2}, metric: {3}\n'.\
                format(self.network, str(self.gateway), self.interface_name,
                       self.metric)
        return 'net: {0}, interface: {1}, metric: {2}\n'. \
            format(self.network, self.interface_name, self.metric)


class Router:
    def __init__(self, exist_routes):
        self.routes = exist_routes

    def add_route(self, other_route):
        self.routes.append(other_route)

    def remove_route(self, exist_route):
        self.routes.remove(exist_route)

    def get_route_for_address(self, other_address):
        pref_route = None
        for item in self.routes:
            if other_address in item.network:
                if not pref_route:
                    pref_route = item

                if item.network.mask_length > pref_route.network.mask_length:
                    pref_route = item

                if item.network.mask_length == pref_route.network.mask_length \
                        and item.metric > pref_route.metric:
                    pref_route = item

        return pref_route

    def __str__(self):
        return ''.join(str(item) for item in self.routes)


if __name__ == '__main__':
    address = IPv4Address("10.123.0.0")
    net = Network(address, 24)
    route = Route(net, address, "en1", 10)
    print route
    print '-'*70
    routes = [(Route(Network(IPv4Address("0.0.0.0"), 0),
                     "192.168.0.1", "en0", 10)),
              (Route(Network(IPv4Address("192.168.0.0"), 24),
                     None, "en0", 10)),
              (Route(Network(IPv4Address("10.0.0.0"), 8),
                     "10.123.0.1", "en1", 10)),
              (Route(Network(IPv4Address("10.123.0.0"), 20),
                     None, "en1", 8))]
    router = Router(routes)
    print router
    router.remove_route(routes[0])
    router.add_route(route)
    print router

    print '-'*70
    route1 = router.get_route_for_address(IPv4Address("192.168.0.176"))
    print route1

    print '-'*70
    route2 = router.get_route_for_address(IPv4Address("10.123.1.1"))
    print route2
