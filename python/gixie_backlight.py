import argparse
import asyncio
import json

import websockets


async def backlight_set(ip, value):
    assert not (value < 1 or value > 255)

    # set
    msg = {"cmdType": 1, "cmdNum": 14, "cmdCtx": {"value": value}}
    # get
    # msg = {"cmdType": 0, "cmdNum": 14}
    async with websockets.connect(f"ws://{ip}:81") as ws:
        # recv Connected
        await ws.recv()
        # send data
        await ws.send(json.dumps(msg))
        # recv Response
        print(await ws.recv())


def main():
    parser = argparse.ArgumentParser(description="Gixie clock brightness")
    parser.add_argument("-i", dest="ip", type=str, default=None, help="gixie clock ip address")
    parser.add_argument("-b", dest="backlight", type=int, default=None, help="backlight value (1-255)")
    args = parser.parse_args()

    if args.backlight:
        asyncio.run(backlight_set(args.ip, args.backlight))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
