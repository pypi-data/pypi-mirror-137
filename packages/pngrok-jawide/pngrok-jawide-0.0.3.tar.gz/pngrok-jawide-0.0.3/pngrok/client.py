import pngrok
import logging
import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("connect_server_addr", help="Server address for server, example: 101.1.1.1:4000")
    parser.add_argument("connect_bob_addr", help="Server address for bob, example: 127.0.0.1:80")
    parser.add_argument("--buffer_size", help="buffer size, default 2048", default=2048, type=int)
    parser.add_argument("--log_level", help="DEBUG、INFO、WARN、ERROR、FATAL", type=lambda s:s in ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"])
    args = parser.parse_args()

    host_pattern = "(.*)"
    port_pattern = "([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])"
    server_group = re.match(f"^{host_pattern}:{port_pattern}$", args.connect_server_addr)
    bob_group = re.match(f"^{host_pattern}:{port_pattern}$", args.connect_bob_addr)

    server_host = server_group.groups()[0]
    server_port = int(server_group.groups()[1])
    bob_host = bob_group.groups()[0]
    bob_port = int(bob_group.groups()[1])

    if args.log_level:
        logging.basicConfig(level=args.log_level, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    client_connecter = pngrok.ClientConnecter((server_host, server_port), (bob_host, bob_port), buffer_size=args.buffer_size)
    client_connecter.setDaemon(True)
    client_connecter.start()
    try:
        while True:
            pass
    except Exception:
        pass
