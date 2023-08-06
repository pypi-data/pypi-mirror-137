from typing import Iterable
import requests

from zipr.core.remotezip import RemoteZip
from zipr.core.zip import EOCD, CDFileHeader

class Http(RemoteZip):
    def __init__(self, eocd: EOCD, records: Iterable[CDFileHeader]):
        super().__init__(eocd, records)

    @classmethod
    def from_url(cls, url: str, *args, **kwargs):
        eocd_response = requests.get(url=url, headers={'Range': 'bytes=-65556'}) # Max size of EOCD
        eocd = EOCD.from_bytes(eocd_response.content)
        cd_response = requests.get(url=url, headers={'Range': f"bytes={eocd.cd_offset}-{eocd.cd_offset+eocd.cd_size}"})
        return cls(
            eocd,
            (header for _, header in CDFileHeader.gen_from_bytes(cd_response.content)),
        )

    def open(self, filename: str) -> bytes:
        return b'cc'
