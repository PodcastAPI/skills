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


if __name__ == '__main__':
    unittest.main()
