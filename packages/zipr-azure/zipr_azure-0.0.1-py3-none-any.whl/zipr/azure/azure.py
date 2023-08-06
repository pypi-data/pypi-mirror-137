from io import BytesIO
from typing import Iterable
import zlib

from azure.storage.blob import BlobClient

from zipr.core.remotezip import RemoteZip
from zipr.core.zip import EOCD, CDFileHeader

class Azure(RemoteZip):
    def __init__(self, eocd: EOCD, records: Iterable[CDFileHeader]):
        super().__init__(eocd, records)
    
    @classmethod
    def from_blob(cls, *, conn_str, container_name, blob_name, **kwargs):
        client = BlobClient.from_connection_string(
            conn_str=conn_str,
            container_name=container_name,
            blob_name=blob_name,
        )
        eocd_bytes = BytesIO()
        client.download_blob(offset=client.get_blob_properties().size - 65556, length=65556).readinto(eocd_bytes)
        eocd_bytes.seek(0)
        eocd = EOCD.from_bytes(eocd_bytes.read())
        cd_bytes = BytesIO()
        client.download_blob(offset=eocd.cd_offset, length=eocd.cd_size).readinto(cd_bytes)
        cd_bytes.seek(0)
        return AzureBlob(
            eocd,
            (header for _, header in CDFileHeader.gen_from_bytes(cd_bytes.read())),
            client,
        )

class AzureBlob(Azure):
    def __init__(self, eocd: EOCD, records: Iterable[CDFileHeader], client: BlobClient):
        super().__init__(eocd, records)
        self.client = client
    
    def open(self, file: CDFileHeader) -> bytes:
        data_start = file.file_header_offset+30+file.filename_len+file.extra_field_len
        data = BytesIO()
        self.client.download_blob(offset=data_start, length=file.compressed_size).readinto(data)
        data.seek(0)
        return zlib.decompress(data.read(), wbits=-zlib.MAX_WBITS)
