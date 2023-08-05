import os
import requests
import subprocess
from time import sleep
from lambdatest_tunnel.tunnel_binary import LambdaTunnelBinary
from lambdatest_tunnel.lt_errors import LambdaTestTunnelError


class LambdaTunnel:

    def __init__(self, options={}):
        self.local_binary_name = None
        self.tunnel_process = None
        self.options = {**{'--infoAPIPort': '8005', '--logFile': os.path.join(os.getcwd(), 'local.log')}, **options}

    def start(self):
        if not self.tunnel_running():
            self.local_binary_name = LambdaTunnelBinary().download()
            self.tunnel_process = subprocess.Popen(self.create_tunnel_cmdline(), stdout=subprocess.DEVNULL,
                                                   stderr=subprocess.DEVNULL)
        self.wait_tunnel_ready()

    def stop(self):
        r = requests.delete(f'http://127.0.0.1:{self.options["--infoAPIPort"]}/api/v1.0/stop', timeout=5)
        self.tunnel_process.communicate()
        return r.ok

    def tunnel_running(self):
        try:
            r = requests.get(f'http://127.0.0.1:{self.options["--infoAPIPort"]}/api/v1.0/info', timeout=2)
            return r.ok
        except:
            return False

    def wait_tunnel_ready(self):
        for count in range(0, 10):
            if self.tunnel_running():
                return True
            sleep(1)
        raise LambdaTestTunnelError('Failed to start tunnel')

    def create_tunnel_cmdline(self):
        cmd = [self.local_binary_name]
        for flag, value in self.options.items():
            cmd.append(flag)
            if value:
                cmd.append(str(value))
        return cmd

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
