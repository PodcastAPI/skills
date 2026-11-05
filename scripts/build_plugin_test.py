from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock
import zipfile

import build_plugin


class PluginBuildTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / 'skills/podcast-mcp'
        self.source = self.root / 'plugins/podcast-search-openai'
        self.bundled = self.source / 'skills/podcast-mcp'
        self.write(self.skill / 'SKILL.md', 'Research skill\n')
        self.write(self.skill / 'references/connection.md', 'OAuth connection instructions\n')
        self.write(self.source / 'plugin.json', json.dumps({'name': 'podcast-search', 'version': '1.0.4'}))
        self.write(self.source / 'mcp.json', json.dumps({
            'mcpServers': {'listen_notes': {'type': 'streamable-http', 'url': 'https://mcp.listennotes.com/mcp/'}},
        }))
        self.write(self.source / 'assets/logo.png', 'light logo fixture')
        self.write(self.source / 'assets/logo-dark.png', 'dark logo fixture')
        self.write(self.root / 'LICENSE', 'License fixture')
        patcher = mock.patch.object(build_plugin, 'ROOT', self.root)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def test_sync_replaces_changed_content_and_removes_deleted_references(self):
        build_plugin.sync_skill(self.source)
        self.write(self.skill / 'SKILL.md', 'Updated research skill\n')
        (self.skill / 'references/connection.md').unlink()
        self.write(self.skill / 'references/authorization.md', 'Renamed connection reference\n')
        build_plugin.sync_skill(self.source)
        self.assertEqual((self.bundled / 'SKILL.md').read_text(), 'Updated research skill\n')
        self.assertFalse((self.bundled / 'references/connection.md').exists())
        self.assertTrue((self.bundled / 'references/authorization.md').is_file())

    def test_missing_canonical_skill_does_not_destroy_previous_bundle(self):
        build_plugin.sync_skill(self.source)
        previous = build_plugin.skill_files(self.bundled)
        (self.skill / 'SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, 'canonical podcast-mcp skill is missing'):
            build_plugin.sync_skill(self.source)
        self.assertEqual(build_plugin.skill_files(self.bundled), previous)

    def test_symlinks_cannot_read_or_overwrite_files_outside_the_plugin(self):
        outside = self.root / 'outside.txt'
        self.write(outside, 'Do not change')
        for directory in (self.skill, self.bundled):
            with self.subTest(directory=directory):
                directory.mkdir(parents=True, exist_ok=True)
                link = directory / 'linked.txt'
                link.symlink_to(outside)
                with self.assertRaisesRegex(ValueError, 'symbolic links'):
                    build_plugin.sync_skill(self.source)
                link.unlink()
                self.assertEqual(outside.read_text(), 'Do not change')
        (self.source / 'skills').rename(self.source / 'old-skills')
        (self.source / 'skills').symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symbolic links'):
            build_plugin.sync_skill(self.source)

    def test_zip_is_reproducible_and_contains_only_the_research_skill(self):
        self.write(self.root / 'skills/podcast-api/SKILL.md', 'API development skill')
        self.write(self.skill / '__pycache__/unwanted.pyc', 'Not a package resource')
        self.write(self.skill / '.hidden', 'Not a package resource')
        output = self.root / 'dist'
        with redirect_stdout(io.StringIO()):
            archive = build_plugin.build(output)
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            archive = build_plugin.build(output)
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), digest)
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(bundle.read('podcast-search/skills/podcast-mcp/references/connection.md'),
                             (self.skill / 'references/connection.md').read_bytes())
            self.assertEqual(bundle.read('podcast-search/mcp.json'), (self.source / 'mcp.json').read_bytes())
            self.assertFalse(any('podcast-api' in name or '__pycache__' in name or '.hidden' in name
                                 for name in bundle.namelist()))

    def claude_source(self):
        source = self.root / 'plugins/podcast-search-claude'
        self.write(source / '.claude-plugin/plugin.json', json.dumps({
            'name': 'listennotes-podcast-search', 'version': '1.0.0',
        }))
        self.write(source / '.mcp.json', json.dumps({
            'mcpServers': {'listen_notes': {'type': 'http', 'url': 'https://mcp.listennotes.com/mcp/'}},
        }))
        self.write(source / 'README.md', 'Public installation and usage instructions')
        self.write(source / 'LICENSE', 'License fixture')
        self.write(source / 'assets/logo.png', 'light logo fixture')
        self.write(source / 'assets/logo-dark.png', 'dark logo fixture')
        return source

    def test_claude_archive_preserves_native_manifests_and_leaves_openai_unchanged(self):
        source = self.claude_source()
        output = self.root / 'dist'
        with redirect_stdout(io.StringIO()):
            openai = build_plugin.build(output)
            previous_archive = openai.read_bytes()
            previous_source = build_plugin.skill_files(self.source)
            archive = build_plugin.build(output, 'claude')
            previous_claude = archive.read_bytes()
            build_plugin.build(output, 'claude')
        self.assertEqual(archive.name, 'listennotes-podcast-search-1.0.0.zip')
        self.assertEqual(archive.read_bytes(), previous_claude)
        self.assertEqual(openai.read_bytes(), previous_archive)
        self.assertEqual(build_plugin.skill_files(self.source), previous_source)
        with zipfile.ZipFile(archive) as bundle:
            prefix = 'listennotes-podcast-search/'
            self.assertEqual(bundle.read(prefix + '.claude-plugin/plugin.json'),
                             (source / '.claude-plugin/plugin.json').read_bytes())
            self.assertEqual(bundle.read(prefix + '.mcp.json'), (source / '.mcp.json').read_bytes())
            self.assertEqual(bundle.read(prefix + 'README.md'), (source / 'README.md').read_bytes())
            self.assertEqual(bundle.read(prefix + 'LICENSE'), (source / 'LICENSE').read_bytes())
            self.assertEqual(bundle.read(prefix + 'skills/podcast-mcp/SKILL.md'), self.skill.joinpath('SKILL.md').read_bytes())
            self.assertFalse(any(name == prefix + 'plugin.json' or name == prefix + 'mcp.json' or 'podcast-api/' in name
                                 for name in bundle.namelist()))

    def test_claude_required_paths_cannot_escape_through_symlinks(self):
        source = self.claude_source()
        for relative in ('README.md', '.mcp.json', '.claude-plugin'):
            with self.subTest(relative=relative):
                path = source / relative
                backup = source / ('backup-' + path.name)
                path.rename(backup)
                path.symlink_to(backup, target_is_directory=backup.is_dir())
                with self.assertRaisesRegex(ValueError, 'symbolic links'):
                    build_plugin.build(self.root / 'dist', 'claude')
                path.unlink()
                backup.rename(path)


if __name__ == '__main__':
    unittest.main()
