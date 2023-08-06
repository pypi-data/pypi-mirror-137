import datetime
import os
import sys

import codefast as cf
import oss2
from cryptography.fernet import Fernet

from dofast.config import FERNET_KEY_UNSAFE
from dofast.pipe import author
from dofast.utils import download as idm
from dofast.utils import shell


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class Tor:
    def __init__(self) -> None:
        self.fernet = Fernet(FERNET_KEY_UNSAFE)

    def encrypt(self, file_name: str) -> str:
        '''Encrypt file contents, write it down, and return the encrypted filename.'''
        with open(file_name, 'rb') as f:
            encrypted_data = self.fernet.encrypt(f.read())
            basename, _, suffix = file_name.rpartition('.')
            file_new = ''.join((basename, '_encrypted.', suffix))
            with open(file_new, 'wb') as fn:
                fn.write(encrypted_data)
                return file_new

    def decrypt(self, file_name: str) -> str:
        '''decrypt file and write the contents down to local.'''
        with open(file_name, 'rb') as f:
            decrypted_data = self.fernet.decrypt(f.read())
            basename, _, suffix = file_name.rpartition('.')
            file_new = ''.join((basename, '_decrypted', '.', suffix))
            cf.info('Decrypt file and export to {}'.format(file_new))
            with open(file_new, 'wb') as fn:
                fn.write(decrypted_data)
                return file_new


class Bucket:
    def __init__(self):
        self._bucket = None
        self._url_prefix = None
        self._tor = None

    @property
    def tor(self) -> Tor:
        if not self._tor:
            self._tor = Tor()
        return self._tor

    @property
    def bucket(self) -> oss2.Bucket:
        _id = author.get("ALIYUN_ACCESS_KEY_ID")
        _secret = author.get("ALIYUN_ACCESS_KEY_SECRET")
        _bucket = author.get("ALIYUN_BUCKET")
        _region = author.get("ALIYUN_REGION")
        _auth = oss2.Auth(_id, _secret)
        self._bucket = oss2.Bucket(_auth, _region, _bucket)
        return self._bucket

    @property
    def url_prefix(self) -> str:
        _bucket = author.get("ALIYUN_BUCKET")
        _region = author.get("ALIYUN_REGION")
        _http_region = _region.lstrip('http://')
        self._url_prefix = f"https://{_bucket}.{_http_region}/"
        return self._url_prefix

    def upload(self, local_file: str, remote_dir: str = 'transfer') -> None:
        """Upload a file to remote_dir"""
        object_name = os.path.join(remote_dir, cf.io.basename(local_file))
        cf.info("uploading {} to {}".format(object_name, remote_dir))

        sys.stdout.write("[%s 🍄" % (" " * 100))
        sys.stdout.flush()
        sys.stdout.write("\b" * (101))     # return to start of line, after '['

        def progress_bar(*args):
            acc = args[0]

            def ratio(n):
                return n * 100 // args[1]

            if ratio(acc + 8192) > ratio(acc):
                sys.stdout.write(str(ratio(acc) // 10))
                sys.stdout.flush()

        file_new = self.tor.encrypt(local_file)
        self.bucket.put_object_from_file(object_name,
                                         file_new,
                                         progress_callback=progress_bar)
        sys.stdout.write("]\n")     # this ends the progress bar
        cf.info("{} uploaded to {}".format(object_name, remote_dir))
        cf.io.rm(file_new)

    def _download(self, file_name: str, export_to: str = None) -> None:
        """Download a file from transfer/"""
        f = export_to if export_to else cf.io.basename(file_name)
        self.bucket.get_object_to_file(f"transfer/{file_name}", f)
        cf.logger.info(f"{file_name} Downloaded.")

    def download(self, remote_path: str, local_file_name: str) -> None:
        """Download a file from oss
        Args:
            remote_path(str): the path of the file in oss, e.g., work/docs/1111.xlsx
            local_file_name: the name of the file to be saved locally, e.g., 1111.xlsx
        """
        url = cf.urljoin(self.url_prefix, remote_path)
        idm(url, referer=self.url_prefix, name=local_file_name)
        file_new = self.tor.decrypt(local_file_name)
        cf.io.rename(file_new, local_file_name)

    def delete(self, file_name: str) -> None:
        """Delete a file from transfer/"""
        self.bucket.delete_object(f"transfer/{file_name}")
        cf.logger.info(f"{file_name} deleted from transfer/")

    def _get_files(self, prefix="transfer/") -> list:
        res = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
            res.append((obj.key, obj.last_modified, obj.size))
        return res

    def list_files(self, prefix="transfer/") -> None:
        files = self._get_files(prefix)
        files.sort(key=lambda e: e[1])
        for tp in files:
            print("{:<25} {:<10} {:<20}".format(
                str(datetime.datetime.fromtimestamp(tp[1])), sizeof_fmt(tp[2]),
                tp[0]))

    def list_files_by_size(self, prefix="transfer/") -> None:
        files = self._get_files(prefix)
        files.sort(key=lambda e: e[2])
        for tp in files:
            print("{:<25} {:<10} {:<20}".format(
                str(datetime.datetime.fromtimestamp(tp[1])), sizeof_fmt(tp[2]),
                tp[0]))

    def __repr__(self) -> str:
        return '\n'.join('{:<20} {:<10}'.format(str(k), str(v))
                         for k, v in vars(self).items())


class Message(Bucket):
    def __init__(self):
        super(Message, self).__init__()
        self._tmp = '/tmp/msgbuffer.json'
        self.bucket.get_object_to_file('transfer/msgbuffer.json', self._tmp)
        __ = self.tor.decrypt(self._tmp)
        cf.io.rename(__, self._tmp)
        self.conversations = cf.js.read(self._tmp)

    def read(self, top: int = 10) -> dict:
        for conv in self.conversations['msg'][-top:]:
            name, content = conv['name'], conv['content']
            sign = "🔥" if name == shell('whoami').strip() else "❄️ "
            print('{} {}'.format(sign, content))

    def write(self, content: str) -> None:
        name = shell('whoami').strip()
        self.conversations['msg'].append({'name': name, 'content': content})
        cf.js.write(self.conversations, self._tmp)
        self.upload(self._tmp)
