import pngrok
import logging
import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("listen_alice_addr", help="Server address for alice, example: 0.0.0.0:40000")
    parser.add_argument("listen_client_addr", help="Server address for client, example: 0.0.0.0:4000")
    parser.add_argument("--buffer_size", help="buffer size, default 2048", default=2048, type=int)
    parser.add_argument("--log_level", help="DEBUG、INFO、WARN、ERROR、FATAL", type=lambda s:s in ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"])
    args = parser.parse_args()

    host_pattern = "(.*)"
    port_pattern = "([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])"
    alice_group = re.match(f"^{host_pattern}:{port_pattern}$", args.listen_alice_addr)
    client_group = re.match(f"^{host_pattern}:{port_pattern}$", args.listen_client_addr)
    
    alice_host = alice_group.groups()[0]
    alice_port = int(alice_group.groups()[1])
    client_host = client_group.groups()[0]
    client_port = int(client_group.groups()[1])

    if args.log_level:
        logging.basicConfig(level=args.log_level, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    alice_listener = pngrok.AliceListener((alice_host, alice_port), (client_host, client_port), buffer_size=args.buffer_size)
    alice_listener.setDaemon(True)
    alice_listener.start()
    try:
        while True:
            pass
    except Exception:
        pass