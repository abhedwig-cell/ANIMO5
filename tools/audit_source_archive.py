#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, io, zipfile
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoding_of(data: bytes) -> str:
    try:
        data.decode('ascii')
        return 'ascii'
    except UnicodeDecodeError:
        try:
            data.decode('utf-8')
            return 'utf-8'
        except UnicodeDecodeError:
            return 'cp1252'


def build_manifest(archive: Path) -> str:
    out = io.StringIO(newline='')
    w = csv.writer(out, lineterminator='\n')
    w.writerow(['path','size_bytes','crc32','sha256','zip_timestamp','encoding','crlf_count'])
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            data = z.read(info.filename)
            ts = '%04d-%02d-%02dT%02d:%02d:%02d' % info.date_time
            w.writerow([
                info.filename,
                len(data),
                f'{info.CRC:08x}',
                sha256_bytes(data),
                ts,
                encoding_of(data),
                data.count(b'\r\n'),
            ])
    return out.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('archive', type=Path)
    ap.add_argument('--manifest', type=Path)
    ns = ap.parse_args()
    data = ns.archive.read_bytes()
    print(f'archive_sha256={sha256_bytes(data)}')
    manifest = build_manifest(ns.archive)
    if ns.manifest:
        ns.manifest.write_text(manifest, encoding='utf-8', newline='')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
