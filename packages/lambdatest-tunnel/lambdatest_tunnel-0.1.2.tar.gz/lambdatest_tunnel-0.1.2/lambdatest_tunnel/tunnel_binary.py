import platform
import os
import subprocess
import sys
import stat
import requests
import zipfile
import io
import re
from lambdatest_tunnel.lt_errors import LambdaTestTunnelError


class LambdaTunnelBinary(object):

    LAMBDA_LOCAL_BINARY_NAME = 'LT'

    def __init__(self):
        self.local_binary_dir = self.get_download_directory()
        self.local_binary = self.get_local_binary_path()

    def download(self):
        # Check if binary already exists
        if not os.path.isfile(self.local_binary):
            response = requests.get(self.remote_binary_path())
            if not response.ok:
                raise LambdaTestTunnelError('Failed to download zipfile')
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall(self.local_binary_dir)
            if not os.path.isfile(self.local_binary):
                raise LambdaTestTunnelError('Failed to extract binary')
        st = os.stat(self.local_binary)
        os.chmod(self.local_binary, st.st_mode | stat.S_IXUSR)
        if not self.check_binary():
            raise LambdaTestTunnelError('File is corrupt?')
        return self.local_binary

    def get_download_directory(self):
        local_binary_path = os.path.join(os.path.expanduser('~'), '.lambdatest')
        os.makedirs(local_binary_path, exist_ok=True)
        return local_binary_path

    def get_local_binary_path(self):
        local_binary_name = self.LAMBDA_LOCAL_BINARY_NAME
        if platform.system() == 'Windows':
            local_binary_name += '.exe'
        return os.path.join(self.local_binary_dir, local_binary_name)

    def remote_binary_path(self):
        os_bits = '64bit' if sys.maxsize > 2 ** 32 else '32bit'
        platform_name = platform.system()
        if platform_name == 'Linux':
            return f'https://downloads.lambdatest.com/tunnel/v3/linux/{os_bits}/LT_Linux.zip'
        elif platform_name == 'Darwin':
            return f'https://downloads.lambdatest.com/tunnel/v3/mac/{os_bits}/LT_Mac.zip'
        elif platform_name == 'Windows':
            return f'https://downloads.lambdatest.com/tunnel/v3/windows/{os_bits}/LT_Windows.zip'
        else:
            raise LambdaTestTunnelError('OS not supported')

    def check_binary(self):
        try:
            r = subprocess.check_output([self.local_binary, "--version"]).decode("utf-8").strip()
            return bool(re.match("LT version \d+\.\d+\.\d+", r))  # noqa
        except:
            return False
