# SPDX-License-Identifier: GPL-3.0-only
# Part of LEM. See the accompanying LICENSE for license terms and warranty disclaimer.

"""Read-only local-link checker regressions. Run with unittest discovery."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'check_docs.py'
SPEC = importlib.util.spec_from_file_location('check_docs', SOURCE)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class DocumentationLinks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='lem-docs-check-')
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def failures(self, content):
        source = self.root / 'README.md'
        source.write_text(content, encoding='utf-8')
        return list(CHECK.check_document(source))

    def test_existing_file_and_heading(self):
        (self.root / 'guide.md').write_text('# Build and run\n', encoding='utf-8')
        self.assertEqual(self.failures('[Guide](guide.md#build-and-run)'), [])

    def test_missing_file_is_reported(self):
        self.assertIn('missing file', self.failures('[Guide](missing.md)')[0])

    def test_missing_heading_is_reported(self):
        (self.root / 'guide.md').write_text('# Build\n', encoding='utf-8')
        self.assertIn('missing heading', self.failures('[Guide](guide.md#run)')[0])

    def test_external_urls_and_fenced_examples_are_not_fetched(self):
        self.assertEqual(self.failures('[Web](https://example.invalid/docs)\n```md\n[X](missing.md)\n```'), [])

    def test_duplicate_unicode_headings(self):
        self.assertEqual(CHECK.anchors('# Observações\n# Observações\n'), {'observações', 'observações-1'})

    def test_local_anchor_and_encoded_path(self):
        (self.root / 'my guide.md').write_text('# Notes\n', encoding='utf-8')
        self.assertEqual(self.failures('# Start\n[Here](#start)\n[Guide](my%20guide.md#notes)'), [])

    def test_validation_does_not_modify_source(self):
        source = self.root / 'README.md'
        source.write_text('# Start\n[Here](#start)\n', encoding='utf-8')
        original = source.read_bytes()
        self.assertEqual(list(CHECK.check_document(source)), [])
        self.assertEqual(source.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
