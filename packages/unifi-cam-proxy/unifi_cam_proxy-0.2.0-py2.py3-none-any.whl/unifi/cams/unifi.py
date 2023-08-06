import argparse
import asyncio
import http.server
import json
import logging
import ssl

import websockets
from aiohttp import web

from unifi.cams.base import SmartDetectObjectType, UnifiCamBase


class UnifiCam(UnifiCamBase):
    def __init__(self, args: argparse.Namespace, logger: logging.Logger) -> None:
        super().__init__(args, logger)
        self.cert = args.cert

    @classmethod
    def add_parser(cls, parser: argparse.ArgumentParser) -> None:
        # parser.add_argument(
        #     "--username",
        #     "-u",
        #     required=True,
        #     help="Camera username",
        # )
        # parser.add_argument(
        #     "--password",
        #     "-p",
        #     required=True,
        #     help="Camera password",
        # )
        pass

    def get_snapshot(self):
        raise FileNotFoundError()

    def enable_passthrough(self):
        return True

    async def pipe(self, reader, writer):
        try:
            while not reader.at_eof():
                writer.write(await reader.read(2048))
        finally:
            writer.close()

    def stream_proxy_handler(self, port):
        async def inner(local_reader, local_writer):
            self.logger.info(f"Handling proxy stream for port {port}")
            try:
                remote_reader, remote_writer = await asyncio.open_connection(
                    self.args.host, port
                )
                pipe1 = self.pipe(local_reader, remote_writer)
                pipe2 = self.pipe(remote_reader, local_writer)
                await asyncio.gather(pipe1, pipe2)
            finally:
                local_writer.close()

        return inner

    async def ws_proxy(self, websocket, path):
        """
        Handles messages received from the camera and forwards them
        to the server
        """
        self._client_ws = websocket
        async for message in websocket:
            self.logger.debug(message)
            msg = json.loads(message)
            if type(msg) == dict:
                if msg["functionName"] == "ubnt_avclient_hello":
                    msg["payload"]["ip"] = self.args.ip
                self.latest_ts = msg["messageId"]
            await self.send(msg)

    async def run(self) -> None:

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.ssl_context.load_cert_chain(self.cert, self.cert)

        self.logger.info("Enabling HTTP API on port 8080")
        coro1 = asyncio.start_server(self.stream_proxy_handler(7550), "0.0.0.0", 7550)
        coro2 = asyncio.start_server(
            self.stream_proxy_handler(7444),
            "0.0.0.0",
            7444,
            ssl=self.ssl_context,
        )
        asyncio.get_event_loop().create_task(coro1)
        asyncio.get_event_loop().create_task(coro2)

        # server_address = ('localhost', 4443)
        # httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
        # httpd.socket = ssl.wrap_socket(httpd.socket,
        #                             server_side=True,
        #                             certfile='localhost.pem',
        #                             ssl_version=ssl.PROTOCOL_TLS)
        # httpd.serve_forever()

        app = web.Application()

        async def start_motion(request):
            self.logger.debug("Starting motion")
            await self.trigger_motion_start(SmartDetectObjectType.PERSON)
            return web.Response(text="ok")

        async def stop_motion(request):
            self.logger.debug("Stopping motion")
            await self.trigger_motion_stop(SmartDetectObjectType.PERSON)
            return web.Response(text="ok")

        app.add_routes([web.get("/start_motion", start_motion)])
        app.add_routes([web.get("/stop_motion", stop_motion)])

        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, port=8080)
        await site.start()

        async with websockets.serve(
            self.ws_proxy, "0.0.0.0", 7442, ssl=self.ssl_context
        ):
            self.logger.info("Started websocket server")
            await asyncio.Future()  # run forever

    async def passthrough(self, msg) -> None:
        if self._client_ws:
            await self._client_ws.send(msg)
