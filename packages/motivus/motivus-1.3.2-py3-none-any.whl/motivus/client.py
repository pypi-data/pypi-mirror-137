#!/usr/bin/env python

from __future__ import annotations
import asyncio
import base64
import datetime
import json
import os
import sys
import uuid

import websockets
from websockets.client import WebSocketClientProtocol

default_uri = os.environ["WEBSOCKET_URI"] if "WEBSOCKET_URI" in os.environ else "ws://localhost:4000/client_socket/websocket"
default_token = os.environ["APPLICATION_TOKEN"] if "APPLICATION_TOKEN" in os.environ else "MWBatxipDHG4daX3hemGO4nXZEgAvOTbBPyWDj36AsWqbOJc="


class Client:
    """Handles connection to Motivus computing network and stores task execution data"""

    def __init__(self):
        self.uri = default_uri
        self.token = default_token
        self.tasks = {}
        self.loop = asyncio.get_event_loop()
        self.id = 0
        self.channel_id = ""
        self.user_uuid = ""
        self.websocket: WebSocketClientProtocol = WebSocketClientProtocol()
        self.result_files = {}

    @classmethod
    async def connect(cls) -> Client:
        """Sets up the client connection to the worker network. Must be called prior to task scheduling"""

        self = Client()
        self.websocket = await websockets.connect(f'{self.uri}?token={self.token}')
        await self.fetch_channel_id()
        await self.join_channel()

        asyncio.get_event_loop().create_task(self.heartbeat())
        asyncio.get_event_loop().create_task(self.message_listener())
        return self

    async def fetch_channel_id(self):
        """Ask for user_uuid of current associated token and generate a new channel id"""

        join_msg = dict(topic="room:client?", event="phx_join",
                        payload={}, ref="uuid")
        await self.websocket.send(json.dumps(join_msg))
        message = await self.websocket.recv()

        response = json.loads(message)
        if response["ref"] == "uuid" and "uuid" in response["payload"]["response"]:
            self.user_uuid = response["payload"]["response"]["uuid"]
            self.channel_id = f'{response["payload"]["response"]["uuid"]}:{str(uuid.uuid4())}'

            leave_msg = dict(topic="room:client?",
                             event="phx_leave", payload={}, ref=None)
            await self.websocket.send(json.dumps(leave_msg))
            await self.websocket.recv()

        else:
            sys.exit("Internal server error")

    async def join_channel(self):
        """Sets up channel communication"""

        join_msg = dict(topic="room:client:" + self.channel_id,
                        event="phx_join", payload={}, ref="join")
        await self.websocket.send(json.dumps(join_msg))
        message = await self.websocket.recv()

        response = json.loads(message)
        if response["ref"] == "join" and "status" in response["payload"] and response["payload"]["status"] == "error" and "reason" in response["payload"]["response"] and response["payload"]["response"]["reason"] == "unauthorized":
            sys.exit("Unauthorized connection. Check your APPLICATION_TOKEN")
        else:
            pass

    async def message_listener(self):
        """Listens for websocket messages and handles task responses"""
        async for message in self.websocket:
            response = json.loads(message)
            if response["event"] == "result":
                ref = response["payload"]["ref"]
                result = response["payload"]["body"]
                stderr = response["payload"]["stderr"]
                stdout = response["payload"]["stdout"]
                if ref in self.result_files:
                    self.write_logs(stdout, stderr, ref)
                    for file_name in self.result_files[ref]:
                        contents = result.get(file_name, None)
                        if contents == None:
                            print(
                                f'WARNING: {file_name} could not be retrieved, check the logs for more information. UUID: {ref}')
                        else:
                            output = self.result_files[ref].get(
                                file_name, None)
                            output_dir = os.path.dirname(output)
                            if not os.path.exists(output_dir):
                                os.makedirs(output_dir)
                            self.write_file(output, contents)
                if ref in self.tasks:
                    self.tasks[ref].set_result(result)
            else:
                # print(response)
                pass

    def write_logs(self, stdout, stderr, uuid):
        """Writes worker logs to log directory"""
        logs_path = '.motivus/logs/'
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        if stdout != "" or stderr != "":
            now = datetime.datetime.now()

            prefix = f'{now.strftime("%Y%m%d%H%M%S")}_{uuid}'
            self.write_file(f'{logs_path}{prefix}_stdout.log',
                            stdout) if stdout != None else None
            self.write_file(f'{logs_path}{prefix}_stderr.log',
                            stderr) if stderr != None else None

    async def heartbeat(self):
        """Keeps websocket connection alive"""
        data = dict(topic="phoenix", event="heartbeat", payload={}, ref=0)
        try:
            await self.websocket.send(json.dumps(data))

        except websockets.exceptions.ConnectionClosed:
            print('Connection with server closed')
        else:
            await asyncio.sleep(3)
            self.loop.create_task(self.heartbeat())

    def write_file(self, file_path, contents):
        """Puts content into file"""
        with open(file_path, 'wb') as binary_file:
            binary_file.write(base64.b64decode(contents))

    def read_file(self, file_path):
        """Decodes file content into ascii"""
        # Open a file: file
        file = open(file_path, mode='rb')
        # Read all lines at once
        all_of_it = file.read()
        # Encode
        encoded = base64.b64encode(all_of_it)
        all_of_it = encoded.decode('ascii')
        # close the file
        file.close()
        return all_of_it

    def empty_task(self):
        self.tasks = {}

    def call_async(self, metadata) -> str:
        """Creates a new task with payload provided and returns the task identifier"""
        ref = str(uuid.uuid4())
        loop = asyncio.get_running_loop()
        fut = loop.create_future()

        self.tasks[ref] = fut
        self.result_files[ref] = metadata.get('result_files', [])
        self.loop.create_task(self.call(metadata.copy(), ref))
        return ref

    def select_task(self, id) -> asyncio.Future:
        """Access the undelying task Future"""
        return self.tasks[id]

    def barrier(self, indexs=[]) -> asyncio.Future:
        """Waits for all task identifier supplied to finish execution"""
        buffer_task = [self.select_task(k) for k in indexs]
        task = asyncio.ensure_future(asyncio.gather(*buffer_task))
        return task

    async def reply_result(self, task_id, is_valid):
        """Set task result validation status"""
        payload = {"body": {"is_valid": is_valid}, "type": "validation",
                   "task_id": task_id, "client_id": self.user_uuid}
        msg = dict(
            topic="room:client:" + self.channel_id,
            payload=payload,
            event="set_validation",
            ref=None)
        msg = json.dumps(msg)
        await self.websocket.send(msg)
        return 1

    async def call(self, metadata, ref):
        """Send payload to available workers"""
        if (metadata['run_type'] == 'wasm'):
            payload = {"body": {
                "wasm": self.read_file(metadata['wasm_path']),
                "loader": self.read_file(metadata['loader_path']),
                "arguments": metadata.get('arguments', None),
                "run_type": metadata['run_type'],
                "processing_base_time": metadata['processing_base_time'],
                "flops": metadata['flops'],
                "flop": metadata['flop'],
                "data_link": metadata.get('data_link', None),
                "preload_files": metadata.get('preload_files', None),
                "result_files": metadata.get('result_files', None),
            },
                "type": "work",
                "ref": ref,
                "client_id": self.user_uuid
            }
        elif (metadata['run_type'] == 'js'):
            payload = {"body": {
                "loader": self.read_file(metadata['loader_path']),
                "arguments": metadata.get('arguments', None),
                "run_type": metadata['run_type']
            },
                "type": "work",
                "ref": ref,
                "client_id": self.user_uuid
            }

        msg = dict(
            topic="room:client:" + self.channel_id,
            payload=payload,
            event="task",
            ref=None)
        msg = json.dumps(msg)
        await self.websocket.send(msg)
