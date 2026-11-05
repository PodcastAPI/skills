"""Build OpenAI or Claude plugin archives from the canonical research skill."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    'openai': ('podcast-search-openai', 'plugin.json', 'mcp.json'),
    'claude': ('podcast-search-claude', '.claude-plugin/plugin.json', '.mcp.json'),
}


def package_path(source, relative):
    """Reject symlinks and escapes before reading or synchronizing a package."""
    if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Plugin files must not be symbolic links or escape the repository.')
    path = source
    for part in Path(relative).parts:
        if part == '..':
            raise ValueError('Plugin paths must stay inside the plugin.')
        path /= part
        if path.is_symlink():
            raise ValueError('Plugin files must not be symbolic links.')
    if not path.resolve().is_relative_to(source.resolve()):
        raise ValueError('Plugin paths must stay inside the plugin.')
    return path


def skill_files(directory):
    files = {}
    if directory.is_symlink():
        raise ValueError('Plugin files must not be symbolic links.')
    for path in directory.rglob('*'):
        if path.is_symlink():
            raise ValueError('Plugin files must not be symbolic links.')
        relative = path.relative_to(directory)
        if path.is_file() and not any(part.startswith('.') or part == '__pycache__' for part in relative.parts):
            files[relative] = path.read_bytes()
    return files


def sync_skill(source):
    """Keep the Git-importable plugin's skill identical to its canonical source."""
    files = skill_files(ROOT / 'skills/podcast-mcp')
    if Path('SKILL.md') not in files:
        raise ValueError('The canonical podcast-mcp skill is missing.')
    directory = package_path(source, 'skills/podcast-mcp')
    bundled = skill_files(directory)
    for stale in bundled.keys() - files.keys():
        (directory / stale).unlink()
    for relative, content in files.items():
        if bundled.get(relative) != content:
            path = directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)


def build(output_dir, target='openai'):
    if target not in TARGETS:
        raise ValueError('Unknown plugin target.')
    directory_name, manifest_name, mcp_name = TARGETS[target]
    source = ROOT / 'plugins' / directory_name
    manifest_path = package_path(source, manifest_name)
    manifest = json.loads(manifest_path.read_text())
    name, version = manifest['name'], manifest['version']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid plugin name or version.')
    files = {manifest_path: manifest_name, package_path(source, mcp_name): mcp_name}
    if target == 'claude':
        files.update({package_path(source, name): name for name in ('README.md', 'LICENSE')})
    else:
        files[ROOT / 'LICENSE'] = 'LICENSE'
    # Check required inputs before changing the synchronized skill directory.
    if any(not path.is_file() for path in files):
        raise ValueError('A required plugin file is missing.')
    sync_skill(source)
    for directory, prefix in ((source / 'assets', 'assets'), (source / 'skills/podcast-mcp', 'skills/podcast-mcp')):
        for relative in skill_files(package_path(source, prefix)):
            files[directory / relative] = prefix + '/' + relative.as_posix()
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
        required = {name + '/' + value for value in (manifest_name, mcp_name, 'LICENSE',
                    'skills/podcast-mcp/SKILL.md', 'assets/logo.png', 'assets/logo-dark.png')}
        if target == 'claude':
            required.add(name + '/README.md')
        if not required <= names or any('.app.json' in value or 'node_modules/' in value for value in names):
            raise ValueError('The built plugin inventory is invalid.')
        if bundle.read(name + '/skills/podcast-mcp/SKILL.md') != (ROOT / 'skills/podcast-mcp/SKILL.md').read_bytes():
            raise ValueError('The bundled skill differs from its canonical source.')
    print(archive)
    print('SHA256 ' + hashlib.sha256(archive.read_bytes()).hexdigest())
    return archive


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=TARGETS, default='openai')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    build(args.output_dir, args.target)
