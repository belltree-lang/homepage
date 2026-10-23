"""Offline checks for the public artifact boundary; no third-party packages."""

from pathlib import Path
import shutil
import unittest
import uuid

from assemble_belltree_site import ROOT, SOURCE, assemble


class PublishTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / 'tmp'
        scratch.mkdir(exist_ok=True)
        # Inherit workspace ACLs; Windows sandbox accounts cannot reopen mode-0700
        # TemporaryDirectory folders created by another security identity.
        self.base = scratch / ('publish-test-' + uuid.uuid4().hex)
        self.base.mkdir()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        if self.base.resolve().parent != (ROOT / 'tmp').resolve():
            raise ValueError('Refusing cleanup outside the test workspace.')
        shutil.rmtree(self.base)

    def fixture(self):
        source = self.base / 'source'
        source.mkdir()
        for name in ['index.html', '404.html', 'CNAME', '_headers']:
            (source / name).write_text('fixture', encoding='utf-8')
        return source

    def test_internal_and_secret_files_never_publish(self):
        source = self.fixture()
        forbidden = [
            'AGENTS.md', 'governance/a.html', 'reports/a.html', 'tasks/a.html',
            'agents/a.html', 'internal/a.html', '.env', '.env.production', '.dev.vars',
            'assets/.env', 'assets/.dev.vars', 'assets/governance/a.html',
            'assets/AGENTS.md', 'assets/CLAUDE.md', 'assets/PROMPT-a.html',
            'assets/note.md', 'assets/script.py', 'assets/backup.json',
            '_scripts/build.py', '_articles/draft.html', 'news/_draft/a.html',
            'news/.hidden/a.html', 'unapproved/a.html',
        ]
        for name in forbidden + ['assets/logo.svg', 'news/published/index.html']:
            path = source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture', encoding='utf-8')
        output = self.base / 'output'
        assemble(source, output, 'cloudflare')
        actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
        self.assertEqual(actual, {'index.html', '404.html', '_headers', 'assets/logo.svg',
                                  'news/published/index.html'})

    def test_both_hosts_receive_identical_content_except_cname(self):
        gh, cf = self.base / 'github', self.base / 'cloudflare'
        assemble(SOURCE, gh, 'github')
        assemble(SOURCE, cf, 'cloudflare')
        names = lambda root: {p.relative_to(root) for p in root.rglob('*') if p.is_file()}
        self.assertEqual(names(gh) - {Path('CNAME')}, names(cf))
        for path in names(cf):
            self.assertEqual((cf / path).read_bytes(), (gh / path).read_bytes())
            self.assertEqual((cf / path).read_bytes(), (SOURCE / path).read_bytes())
        # Representative published routes/assets must survive. Do not demand that
        # future draft HTML under private folders appear in either artifact.
        expected = {Path(p) for p in [
            'index.html', 'about/index.html', 'contact/index.html',
            'services/home-visit/index.html', 'q/fit/index.html',
            'colors_and_type.css', 'assets/js/form-handler.js',
            'assets/belltree-mark.svg', 'news/feed.xml', 'sitemap.xml',
        ]}
        self.assertTrue(expected <= names(cf))

    def test_refuse_overwrite_and_output_inside_source(self):
        source = self.fixture()
        output = self.base / 'output'
        output.mkdir()
        sentinel = output / 'keep.txt'
        sentinel.write_text('keep', encoding='utf-8')
        with self.assertRaises(ValueError):
            assemble(source, output, 'cloudflare')
        self.assertEqual(sentinel.read_text(), 'keep')
        with self.assertRaises(ValueError):
            assemble(source, source / 'output', 'cloudflare')

    def test_refuse_missing_required_files(self):
        source = self.base / 'empty-source'
        source.mkdir()
        with self.assertRaises(ValueError):
            assemble(source, self.base / 'output', 'cloudflare')

    def test_refuse_symlinks(self):
        source = self.fixture()
        try:
            (source / 'assets').symlink_to(ROOT / 'governance', target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks requires an OS privilege unavailable here.')
        with self.assertRaises(ValueError):
            assemble(source, self.base / 'output', 'cloudflare')


if __name__ == '__main__':
    unittest.main()
