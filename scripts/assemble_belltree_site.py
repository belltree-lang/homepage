"""Package only the public corporate site, using the Python standard library."""

import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'internal' / 'belltree-home'
PUBLIC_DIRS = frozenset({
    'about', 'assets', 'contact', 'decor', 'faq', 'news', 'partners',
    'privacy-policy', 'pro', 'q', 'recruit', 'services', 'solutions', 'team',
})
PUBLIC_FILES = frozenset({
    '404.html', 'index.html', 'colors_and_type.css', 'image-slot.js',
    'google5d7a489c1ad1189f.html', 'robots.txt', 'llms.txt', 'sitemap.xml',
    '_headers', 'CNAME',
})
PUBLIC_SUFFIXES = frozenset({
    '.html', '.css', '.js', '.xml', '.svg', '.png', '.webp', '.jpg', '.jpeg',
    '.gif', '.ico', '.woff', '.woff2', '.pdf',
})
PRIVATE_NAMES = frozenset({
    'internal', 'governance', 'reports', 'tasks', 'agents', 'scripts', 'docs',
    'templates', 'node_modules', 'secrets',
})


def publishable(relative, target):
    parts = relative.parts
    if any(p.startswith(('.', '_')) or p.lower() in PRIVATE_NAMES for p in parts):
        return parts == ('_headers',)
    if relative.name == 'CNAME':
        return parts == ('CNAME',) and target == 'github'
    if len(parts) == 1:
        return relative.name in PUBLIC_FILES
    return (parts[0] in PUBLIC_DIRS
            and relative.suffix.lower() in PUBLIC_SUFFIXES
            and not relative.name.upper().startswith(('PROMPT-', 'AGENTS.', 'CLAUDE.')))


def assemble(source, output, target):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output == source or source in output.parents or output in source.parents:
        raise ValueError('Output must be separate from the source tree.')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; existing files are never deleted.')
    files = []

    def collect(directory):
        for item in sorted(directory.iterdir()):
            relative = item.relative_to(source)
            # Never follow links/junctions, including ones pointing outside the source.
            if item.is_symlink() or (hasattr(item, 'is_junction') and item.is_junction()):
                raise ValueError('Links are not allowed in the publish source.')
            if item.is_dir():
                if (relative.parts[0] in PUBLIC_DIRS
                        and all(not p.startswith(('.', '_')) and p.lower() not in PRIVATE_NAMES
                                for p in relative.parts)):
                    collect(item)
            elif publishable(relative, target):
                files.append(item)

    collect(source)
    required = {'index.html', '404.html', '_headers'}
    if target == 'github':
        required.add('CNAME')
    if not required <= {p.relative_to(source).as_posix() for p in files}:
        raise ValueError('Required public files are missing.')
    output.mkdir(parents=True, exist_ok=True)
    for item in files:
        destination = output / item.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item, destination)
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', choices=['github', 'cloudflare'], required=True)
    args = parser.parse_args()
    count = assemble(SOURCE, ROOT / '_site', args.target)
    print(f'Packaged {count} public files for {args.target}.')
