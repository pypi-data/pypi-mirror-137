from dataclasses import dataclass, fields
import inspect

@dataclass(frozen=True)
class EOCD:
    disk_index: int
    cd_start_disk: int
    cd_records_on_disk: int
    cd_records_total: int
    cd_size: int
    cd_offset: int
    comment_len: int=0
    comment: str=''

    @classmethod
    def from_bytes(cls, b: bytes):
        def e(start: int, end: int):
            return int.from_bytes(b[start:end], byteorder='little')

        # Find signature...start from smallest possible EOCD (no comment) to largest
        for i in range(65535, -1, -1):
            if b[i:i+4] == b'PK\x05\x06':
                comment_len = e(i+20,i+22)
                comment_last_byte = i+22+comment_len
                cd_meta = cls(
                    disk_index=e(i+4,i+6),
                    cd_start_disk=e(i+6,i+8),
                    cd_records_on_disk=e(i+8,i+10),
                    cd_records_total=e(i+10,i+12),
                    cd_size=e(i+12,i+16),
                    cd_offset=e(i+16,i+20),
                    comment_len=comment_len,
                    comment='' if len(b) < comment_last_byte else b[(i+22):comment_last_byte].decode(),
                )
                return cd_meta
        return None

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x05\x06' \
            + d(self.disk_index, 2) \
            + d(self.cd_start_disk, 2) \
            + d(self.cd_records_on_disk, 2) \
            + d(self.cd_records_total, 2) \
            + d(self.cd_size, 4) \
            + d(self.cd_offset, 4) \
            + d(self.comment_len, 2) \
            + self.comment.encode()

@dataclass(frozen=True)
class CDFileHeader:
    made_by_version: int
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_mod_time: int
    last_mod_date: int
    uncompressed_crc: bytes
    compressed_size: int
    uncompressed_size: int
    filename_len: int
    disk_of_file_start: int
    internal_file_attr: bytes
    external_file_attr: bytes
    file_header_offset: int
    filename: str
    extra_field_len: int=0
    file_comment_len: int=0
    extra_field: str=''
    comment: str=''

    @classmethod
    def from_bytes(cls, b: bytes):
        def e(start: int, end: int):
            return int.from_bytes(b[start:end], byteorder='little')

        # Find signature
        for i in range(0, len(b) - 4):
            if b[i:i+4] == b'PK\x01\x02':
                filename_len = e(i+28,i+30)
                extra_field_len = e(i+30,i+32)
                file_comment_len = e(i+32,i+34)
                filename_last_byte = i+46+filename_len
                extra_field_last_byte = filename_last_byte+extra_field_len
                comment_last_byte = extra_field_last_byte+file_comment_len
                cd_meta = cls(
                    made_by_version=e(i+4,i+6),
                    min_version_needed=e(i+6,i+8),
                    bit_flags=b[(i+8):(i+10)],
                    compression_method=e(i+10,i+12),
                    last_mod_time=e(i+12,i+14),
                    last_mod_date=e(i+14,i+16),
                    uncompressed_crc=b[(i+16):(i+20)],
                    compressed_size=e(i+20,i+24),
                    uncompressed_size=e(i+24,i+28),
                    filename_len=filename_len,
                    extra_field_len=extra_field_len,
                    file_comment_len=file_comment_len,
                    disk_of_file_start=e(i+34,i+36),
                    internal_file_attr=b[(i+36):(i+38)],
                    external_file_attr=b[(i+38):(i+42)],
                    file_header_offset=e(i+42,i+46),
                    filename='' if len(b) < filename_last_byte else b[(i+46):filename_last_byte].decode(),
                    extra_field='' if len(b) < extra_field_last_byte else b[filename_last_byte:extra_field_last_byte].decode(),
                    comment='' if len(b) < comment_last_byte else b[extra_field_last_byte:comment_last_byte].decode()
                )
                return cd_meta
        return None

    @classmethod
    def gen_from_bytes(cls, b: bytes):
        start_byte = 0
        while start_byte < len(b):
            cd_meta = cls.from_bytes(b[start_byte:])
            if not cd_meta:
                break
            yield start_byte, cd_meta
            start_byte += 46+cd_meta.filename_len+cd_meta.file_comment_len

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x01\x02' \
            + d(self.made_by_version, 2) \
            + d(self.min_version_needed, 2) \
            + self.bit_flags \
            + d(self.compression_method, 2) \
            + d(self.last_mod_time, 2) \
            + d(self.last_mod_date, 2) \
            + self.uncompressed_crc \
            + d(self.compressed_size, 4) \
            + d(self.uncompressed_size, 4) \
            + d(self.filename_len, 2) \
            + d(self.extra_field_len, 2) \
            + d(self.file_comment_len, 2) \
            + d(self.disk_of_file_start, 2) \
            + self.internal_file_attr \
            + self.external_file_attr \
            + d(self.file_header_offset, 4) \
            + self.filename.encode() \
            + self.extra_field.encode() \
            + self.comment.encode()

@dataclass(frozen=True)
class FileHeader:
    min_version_needed: int
    bit_flags: bytes
    compression_method: int
    last_mod_time: int
    last_mod_date: int
    uncompressed_crc: bytes
    compressed_size: int
    uncompressed_size: int
    filename_len: int
    filename: str
    extra_field_len: int=0
    extra_field: str=''

    @classmethod
    def from_bytes(cls, b: bytes):
        def e(start: int, end: int):
            return int.from_bytes(b[start:end], byteorder='little')

        # Find signature
        for i in range(0, len(b) - 4):
            if b[i:i+4] == b'PK\x03\x04':
                filename_len = e(i+26,i+28)
                extra_field_len = e(i+28,i+30)
                filename_last_byte = i+30+filename_len
                extra_field_last_byte = filename_last_byte+extra_field_len
                cd_meta = cls(
                    min_version_needed=e(i+4,i+6),
                    bit_flags=b[(i+6):(i+8)],
                    compression_method=e(i+8,i+10),
                    last_mod_time=e(i+10,i+12),
                    last_mod_date=e(i+12,i+14),
                    uncompressed_crc=b[(i+14):(i+18)],
                    compressed_size=e(i+18,i+22),
                    uncompressed_size=e(i+22,i+26),
                    filename_len=filename_len,
                    extra_field_len=extra_field_len,
                    filename='' if len(b) < filename_last_byte else b[(i+30):filename_last_byte].decode(),
                    extra_field='' if len(b) < extra_field_last_byte else b[filename_last_byte:extra_field_last_byte].decode(),
                )
                return cd_meta
        return None

    @classmethod
    def from_central_directory(cls, cd_meta: CDFileHeader):
        return cls(**{
            i: cd_meta.__getattribute__(i) for i in map(lambda field: field.name, fields(cd_meta))
            if i in inspect.signature(cls).parameters
        })

    def to_bytes(self) -> bytes:
        def d(value: int, size: int) -> bytes:
            return int.to_bytes(value, length=size, byteorder='little')

        return b'PK\x03\x04' \
            + d(self.min_version_needed, 2) \
            + self.bit_flags \
            + d(self.compression_method, 2) \
            + d(self.last_mod_time, 2) \
            + d(self.last_mod_date, 2) \
            + self.uncompressed_crc \
            + d(self.compressed_size, 4) \
            + d(self.uncompressed_size, 4) \
            + d(self.filename_len, 2) \
            + d(self.extra_field_len, 2) \
            + self.filename.encode() \
            + self.extra_field.encode()
