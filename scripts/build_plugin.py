"""Build the OpenAI plugin from its manifest and the canonical research skill."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build(output_dir):
    source = ROOT / 'plugins/podcast-search-openai'
    manifest = json.loads((source / 'plugin.json').read_text())
    name, version = manifest['name'], manifest['version']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid plugin name or version.')
    files = {source / 'plugin.json': 'plugin.json', source / 'mcp.json': 'mcp.json', ROOT / 'LICENSE': 'LICENSE'}
    for directory, prefix in ((source / 'assets', 'assets'), (ROOT / 'skills/podcast-mcp', 'skills/podcast-mcp')):
        for path in directory.rglob('*'):
            if path.is_symlink():
                raise ValueError('Plugin files must not be symbolic links.')
            if path.is_file() and not any(part.startswith('.') or part == '__pycache__' for part in path.relative_to(directory).parts):
                files[path] = prefix + '/' + path.relative_to(directory).as_posix()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f'{name}-{version}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for path, destination in sorted(files.items(), key=lambda item: item[1]):
            # Stable contents and timestamps make a reviewed build reproducible.
            info = zipfile.ZipInfo(name + '/' + destination, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        required = {name + '/' + value for value in ('plugin.json', 'mcp.json', 'skills/podcast-mcp/SKILL.md',
                                                     'assets/logo.png', 'assets/logo-dark.png')}
        if not required <= names or any('.app.json' in value or 'node_modules/' in value for value in names):
            raise ValueError('The built plugin inventory is invalid.')
        if bundle.read(name + '/skills/podcast-mcp/SKILL.md') != (ROOT / 'skills/podcast-mcp/SKILL.md').read_bytes():
            raise ValueError('The bundled skill differs from its canonical source.')
    print(archive)
    print('SHA256 ' + hashlib.sha256(archive.read_bytes()).hexdigest())
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    build(args.output_dir)
