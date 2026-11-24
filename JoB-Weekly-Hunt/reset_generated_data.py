"""Explicit, verified backup and file-only cleanup of generated vacancy outputs."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ALLOWLIST = ('technopark', 'infopark', 'job_matching', 'matched_jobs')

def reset(root: Path):
    root = root.resolve()
    files = []
    for name in ALLOWLIST:
        directory = root / 'data' / name
        for path in directory.rglob('*'):
            if path.is_file():
                if not path.resolve().is_relative_to(directory.resolve()):
                    raise ValueError('Unsafe path')
                if path.suffix.lower() not in {'.json', '.csv', '.xlsx', '.log'}:
                    raise ValueError(f'Unreviewed file: {path}')
                files.append(path)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    archive = root.parent / '_archives' / f'JoB-Weekly-Hunt-pre-reset-2026-11-19-{stamp}.zip'
    archive.parent.mkdir(exist_ok=True)
    manifest = [{'path': p.relative_to(root).as_posix(), 'name': p.name, 'size': p.stat().st_size,
                 'modified_at': datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
                 'archive': str(archive), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    with ZipFile(archive, 'x', ZIP_DEFLATED) as z:
        for p, item in zip(files, manifest): z.write(p, item['path'])
        z.writestr('manifest.json', json.dumps(manifest, indent=2))
    with ZipFile(archive) as z:
        assert archive.stat().st_size > 0 and z.testzip() is None
        assert json.loads(z.read('manifest.json')) == manifest
        for item in manifest:
            assert hashlib.sha256(z.read(item['path'])).hexdigest() == item['sha256']
    # Only exact verified file paths, never recursive directory removal.
    for p, item in zip(files, manifest):
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256']
        p.unlink()
    receipt = {'archive': str(archive), 'files_archived': len(files), 'integrity_verified': True,
               'cleaned_allowlist': list(ALLOWLIST), 'restart_baseline': '2026-11-19'}
    (root / 'data' / 'run_metadata').mkdir(exist_ok=True)
    (root / 'data' / 'run_metadata' / 'reset_receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf8')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__': reset(Path(__file__).resolve().parent)
