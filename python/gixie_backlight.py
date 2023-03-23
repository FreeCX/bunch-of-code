import argparse
import asyncio
import json

import websockets


async def backlight_set(ip, value):
    assert not (value < 1 or value > 255)

    msg = {"cmdType": 1, "cmdNum": 14, "cmdCtx": {"value": value}}
    async with websockets.connect(f"ws://{ip}:81") as ws:
        await ws.send(json.dumps(msg))
        await ws.recv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gixie clock brightness")
    parser.add_argument("-i", dest="ip", type=str, default=None, help="gixie clock ip address")
    parser.add_argument("-b", dest="backlight", type=int, default=None, help="backlight value (1-255)")
    args = parser.parse_args()

    if args.backlight:
        asyncio.run(backlight_set(args.ip, args.backlight))
    else:
        parser.print_help()
