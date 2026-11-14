"""Variable-length subnetting (VLSM) of 192.168.10.0/24 for a college campus."""
import math
import ipaddress


def to_int(ip):
    a, b, c, d = map(int, ip.split("."))
    return (a << 24) | (b << 16) | (c << 8) | d


def to_ip(n):
    return ".".join(str((n >> s) & 255) for s in (24, 16, 8, 0))


def vlsm(base, needs, largest_first=True):
    addr = to_int(base)
    for name, hosts in sorted(needs, key=lambda x: -x[1] if largest_first else x[1]):
        # smallest power-of-two block that holds hosts + 2 addresses
        block = 1
        while block < hosts + 2:
            block *= 2
        prefix = 32 - int(math.log2(block))
        first, last, bcast = addr + 1, addr + block - 2, addr + block - 1
        print(f"{name} {to_ip(addr)}/{prefix} hosts {to_ip(first)} - {to_ip(last)} "
              f"bcast {to_ip(bcast)}")
        # check that the block really starts on its own boundary
        try:
            ipaddress.ip_network(f"{to_ip(addr)}/{prefix}")
        except ValueError:
            print("   -> MISALIGNED: not a valid network address for /%d" % prefix)
        addr += block
    return to_ip(addr)


if __name__ == "__main__":
    needs = [("Labs", 100), ("Staff", 50), ("Library", 25), ("WAN link", 2)]
    print("next free address:", vlsm("192.168.10.0", needs))
    print()
    print("--- with the hostel (60 hosts) added ---")
    print("next free address:", vlsm("192.168.10.0", needs + [("Hostel", 60)]))
    print()
    print("--- smallest-first (wrong order) ---")
    print("next free address:", vlsm("192.168.10.0", needs, largest_first=False))
