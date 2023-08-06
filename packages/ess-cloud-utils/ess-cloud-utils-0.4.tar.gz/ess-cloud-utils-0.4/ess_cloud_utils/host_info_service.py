#!/usr/bin/env python3
import requests
import socket


class AwsHostInfoService(object):
    @staticmethod
    def get_ip():
        r = requests.get("http://169.254.169.254/latest/meta-data/local-ipv4")
        return r.text


class LocalHostInfoService(object):
    @staticmethod
    def get_ip():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip


class DockerHostInfoService(object):
    @staticmethod
    def get_ip():
        return "host.docker.internal"


class LoopBackHostInfoService(object):
    @staticmethod
    def get_ip():
        return "127.0.0.1"


print(LocalHostInfoService.get_ip())
