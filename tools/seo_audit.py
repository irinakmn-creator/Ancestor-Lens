"""Read-only static-site SEO audit. Run: python3 tools/seo_audit.py --output docs/seo/current

Uses only Python's standard library. Flags are review candidates, not ranking scores.
"""
import argparse
import collections
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://ancestor-lens.com/'


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.links, self.images, self.headings = [], [], [], []
        self.heading = None
        self.ids = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'meta':
            self.meta.append(data)
        if tag in ('a', 'link', 'script'):
            self.links.append((tag, data))
        if tag == 'img':
            self.images.append(data)
        if tag in ('title', 'h1', 'h2', 'h3'):
            self.heading = [tag, '']
            self.headings.append(self.heading)

    def handle_endtag(self, tag):
        if self.heading and self.heading[0] == tag:
            self.heading = None

    def handle_data(self, data):
        if self.heading:
            self.heading[1] += data


def local_path(url):
    parsed = urlsplit(url)
    if parsed.scheme and parsed.netloc != 'ancestor-lens.com':
        return None
    if parsed.scheme not in ('', 'http', 'https'):
        return None
    path = parsed.path.lstrip('/')
    return ROOT / (path or 'index.html')


def walk(data):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from walk(value)
    elif isinstance(data, list):
        for value in data:
            yield from walk(value)


def audit():
    rows = []
    for file in sorted(ROOT.glob('*.html')):
        source = file.read_text()
        page = Page()
        page.feed(source)
        meta = {m.get('name', m.get('property', m.get('http-equiv', ''))).lower(): m.get('content', '') for m in page.meta}
        redirect = meta.get('refresh', '')
        canonical = [a['href'] for t, a in page.links if t == 'link' and a.get('rel') == 'canonical']
        title = next((v.strip() for k, v in page.headings if k == 'title'), '')
        h1 = [v.strip() for k, v in page.headings if k == 'h1']
        issues, schemas = [], []
        for match in re.finditer(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>', source, re.S):
            try:
                schemas.append(json.loads(match.group(1)))
            except ValueError as exc:
                issues.append('Invalid JSON-LD: ' + str(exc))
        if not redirect:
            if len(h1) != 1:
                issues.append('Expected one H1')
            if not meta.get('description'):
                issues.append('Missing description')
            if len(canonical) != 1:
                issues.append('Expected one canonical')
        if canonical and canonical[0] != DOMAIN + ('' if file.name == 'index.html' else file.name) and not redirect:
            issues.append('Canonical differs from page URL')
        for tag, attrs in page.links:
            url = attrs.get('href', attrs.get('src', ''))
            target = local_path(url)
            if url and target and not target.exists():
                issues.append('Missing link/resource: ' + url)
            if tag == 'a' and url.startswith('#') and len(url) > 1 and url[1:] not in page.ids:
                issues.append('Missing fragment: ' + url)
        for image in page.images:
            target = local_path(image.get('src', ''))
            if target and not target.exists():
                issues.append('Missing image: ' + image.get('src', ''))
            if 'alt' not in image:
                issues.append('Missing image alt')
        for schema in schemas:
            for node in walk(schema):
                for key in ('url', 'item'):
                    value = node.get(key)
                    if isinstance(value, str) and value.startswith(DOMAIN):
                        target = local_path(value)
                        if target and not target.exists():
                            issues.append('Missing schema resource: ' + value)
                image = node.get('image')
                for url in ([image] if isinstance(image, str) else image if isinstance(image, list) else []):
                    if isinstance(url, str):
                        target = local_path(url)
                        if target and not target.exists():
                            issues.append('Missing schema image: ' + url)
        duplicate_ids = [v for v, n in collections.Counter(page.ids).items() if n > 1]
        if duplicate_ids:
            issues.append('Duplicate IDs: ' + ', '.join(duplicate_ids))
        rows.append(dict(file=file.name, url=DOMAIN + ('' if file.name == 'index.html' else file.name), title=title, titleLength=len(title), description=meta.get('description', ''), descriptionLength=len(meta.get('description', '')), h1=h1, headings=page.headings, canonical=canonical, robots=meta.get('robots', 'default index,follow'), redirect=redirect, hreflang=[a for t, a in page.links if a.get('hreflang')], schemaTypes=[n.get('@type') for s in schemas for n in walk(s) if n.get('@type') in ('Article', 'BlogPosting', 'SoftwareApplication', 'BreadcrumbList', 'FAQPage')], missingDimensions=sum(not (i.get('width') and i.get('height')) for i in page.images), links=[a.get('href', '') for t, a in page.links if t == 'a'], cards=[a['href'] for t, a in page.links if t == 'a' and 'blog-card' in a.get('class', '').split()], issues=sorted(set(issues))))
    ns = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    urls = [e.text for e in sitemap.getroot().iter(ns + 'loc')]
    indexable = [r for r in rows if not r['redirect'] and 'noindex' not in r['robots']]
    summary = dict(htmlPages=len(rows), contentPages=len(indexable), existingRedirects=[r['file'] for r in rows if r['redirect']], sitemapUrls=len(urls), duplicateSitemapUrls=[u for u, n in collections.Counter(urls).items() if n > 1], missingFromSitemap=[r['file'] for r in indexable if r['url'] not in urls], redirectInSitemap=[r['file'] for r in rows if r['redirect'] and r['url'] in urls], sitemapMissingFiles=[u for u in urls if local_path(u) and not local_path(u).exists()], duplicateTitles=[v for v, n in collections.Counter(r['title'] for r in indexable).items() if n > 1], duplicateDescriptions=[v for v, n in collections.Counter(r['description'] for r in indexable).items() if n > 1], missingImageDimensions=sum(r['missingDimensions'] for r in rows), duplicateBlogCards=[v for r in rows if r['file'] == 'blog.html' for v, n in collections.Counter(r['cards']).items() if n > 1], articlesMissingFromBlog=[r['file'] for r in indexable if r['file'].startswith('blog-') and r['file'] not in next(x['cards'] for x in rows if x['file'] == 'blog.html')])
    return {'summary': summary, 'pages': rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='docs/seo/current')
    args = parser.parse_args()
    result = audit()
    destination = ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    with destination.with_suffix('.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['URL', 'Title', 'Title length', 'Description', 'Description length', 'H1', 'Canonical', 'Robots', 'Existing redirect', 'Schemas', 'Images without dimensions', 'Review flags'])
        for row in result['pages']:
            writer.writerow([row['url'], row['title'], row['titleLength'], row['description'], row['descriptionLength'], ' | '.join(row['h1']), ' | '.join(row['canonical']), row['robots'], row['redirect'], ' | '.join(row['schemaTypes']), row['missingDimensions'], '; '.join(row['issues'])])
    print(json.dumps(result['summary'], indent=2))


if __name__ == '__main__':
    main()
