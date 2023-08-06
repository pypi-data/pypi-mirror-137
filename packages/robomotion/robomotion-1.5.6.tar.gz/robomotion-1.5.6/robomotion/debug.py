from enum import Enum
import grpc
from json import dumps, loads
import os
from robomotion.utils import File
from robomotion import plugin_pb2
from robomotion import plugin_pb2_grpc


class AttachConfig:
    def __init__(self, protocol: str, addr: str, pid: int, namespace: str):
        self.protocol = protocol
        self.addr = addr
        self.pid = pid
        self.namespace = namespace


class EProtocol(Enum):
    ProtocolInvalid = ''
    ProtocolNetRPC = 'netrpc'
    ProtocolGRPC = 'grpc'


class Debug:
    @staticmethod
    def attach(g_addr: str, ns: str):
        cfg = AttachConfig(str(EProtocol.ProtocolGRPC.value),
                           g_addr, os.getpid(), ns)
        cfg_data = dumps(cfg.__dict__)
        if 'ATTACH_TO' not in os.environ:
            print('Please specify ATTACH_TO environment variable to attach')
            exit(0)

        addr = os.environ['ATTACH_TO']
        channel = grpc.insecure_channel(addr)
        client = plugin_pb2_grpc.DebugStub(channel)

        request = plugin_pb2.AttachRequest(config=cfg_data.encode())
        client.Attach(request)
        channel.close()

    @staticmethod
    def detach(ns: str):
        if 'ATTACH_TO' not in os.environ:
            print('ATTACH_TO environment variable is None')
            exit(0)

        addr = os.environ['ATTACH_TO']
        channel = grpc.insecure_channel(addr)
        client = plugin_pb2_grpc.DebugStub(channel)

        request = plugin_pb2.DetachRequest(namespace=ns)
        client.Detach(request)
        channel.close()
