"""Static deployment contracts; run with python3 -m unittest discover -s tests."""
import json
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ('hvac-repair-overland-park', 'ac-installation-kansas-city',
         'water-heater-replacement-kansas-city', 'plumbing-lees-summit')
PAGES = ('index.html',) + tuple(slug + '.html' for slug in SLUGS)

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags, self.schemas, self.schema = [], [], None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.schema = ''
    def handle_data(self, data):
        if self.schema is not None:
            self.schema += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None
    @property
    def ids(self):
        return [a['id'] for _, a in self.tags if 'id' in a]

class SiteContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {name: Document((ROOT / name).read_text()) for name in PAGES + ('thank-you.html',)}

    def test_local_destinations_and_assets_exist(self):
        for name, doc in self.pages.items():
            self.assertEqual(len(doc.ids), len(set(doc.ids)), name)
            for _, attrs in doc.tags:
                for key in ('href', 'src', 'srcset', 'data-img'):
                    value = attrs.get(key)
                    if not value:
                        continue
                    url = urlsplit(value)
                    if url.scheme or url.netloc:
                        continue
                    target = url.path.lstrip('/') or ('index.html' if value.startswith('/') else name)
                    if not Path(target).suffix:
                        target += '.html'
                    with self.subTest(page=name, destination=value):
                        self.assertTrue((ROOT / target).is_file(), target)
                        if url.fragment and target in self.pages:
                            self.assertIn(url.fragment, self.pages[target].ids)

    def test_existing_sections_and_gallery_are_available(self):
        home = self.pages['index.html']
        self.assertTrue({'services', 'beyond', 'plans', 'area', 'gallery', 'reviews', 'contact'} <= set(home.ids))
        photos = {a['data-img'] for _, a in home.tags if 'data-img' in a}
        self.assertEqual(len(photos), 11)
        for name in ('9156', '3116', '9329', '8417', '7684', '3114', '9328', '9692'):
            self.assertIn(f'photos/IMG_{name}.jpg', photos)

    def test_search_metadata_and_verification_survive(self):
        for name in PAGES:
            doc = self.pages[name]
            canonical = [a['href'] for tag, a in doc.tags if tag == 'link' and a.get('rel') == 'canonical']
            suffix = '' if name == 'index.html' else Path(name).stem
            self.assertEqual(canonical, ['https://roselegacyhs.com/' + suffix])
            robots = [a.get('content', '') for tag, a in doc.tags if tag == 'meta' and a.get('name') == 'robots']
            self.assertEqual(robots, ['index, follow'])
            self.assertTrue(doc.schemas)
            self.assertEqual(sum(tag == 'h1' for tag, _ in doc.tags), 1)
        for name in ('robots.txt', 'sitemap.xml', 'google61314bba10e7f9d5.html', 'logo.png'):
            self.assertTrue((ROOT / name).is_file())
        self.assertTrue(any(a.get('name') == 'google-site-verification' for _, a in self.pages['index.html'].tags))

    def test_service_generator_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'build_service_pages.py'
            shutil.copyfile(ROOT / script.name, script)
            subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
            for slug in SLUGS:
                self.assertEqual((ROOT / (slug + '.html')).read_bytes(), (Path(directory) / (slug + '.html')).read_bytes(), slug)

    def test_service_request_posts_to_the_business_inbox(self):
        # Losing method/names would drop inquiry data; GET would expose it in URLs.
        doc = self.pages['index.html']
        forms = [a for tag, a in doc.tags if tag == 'form']
        self.assertEqual(len(forms), 1)
        self.assertEqual(forms[0].get('method', '').lower(), 'post')
        self.assertEqual(forms[0].get('action'), 'https://formsubmit.co/roselegacyhs@icloud.com')
        fields = {a.get('name'): a for tag, a in doc.tags if tag in ('input', 'select', 'textarea')}
        self.assertTrue({'name', 'phone', 'email', 'service', 'area', 'message'} <= fields.keys())
        for name in ('name', 'phone', 'service', 'area'):
            self.assertIn('required', fields[name])
        self.assertEqual(fields['email']['type'], 'email')
        self.assertNotEqual(fields.get('_captcha', {}).get('value'), 'false')
        self.assertIn('_honey', fields)
        destination = urlsplit(fields['_next']['value'])
        self.assertEqual(destination.netloc, 'roselegacyhs.com')
        self.assertTrue((ROOT / destination.path.lstrip('/')).is_file())
        confirmation = self.pages['thank-you.html']
        self.assertTrue(any(a.get('name') == 'robots' and 'noindex' in a.get('content', '')
                            for _, a in confirmation.tags))
        labels = {a.get('for') for tag, a in doc.tags if tag == 'label'}
        for name in ('name', 'phone', 'email', 'service', 'area', 'message'):
            self.assertIn(fields[name].get('id'), labels)


    def test_home_only_video_and_small_downloads(self):
        for name, doc in self.pages.items():
            videos = [a for tag, a in doc.tags if tag == 'video']
            self.assertEqual(len(videos), int(name == 'index.html'))
            for attrs in videos:
                self.assertNotIn('src', attrs)  # JS checks motion/data preferences first.
                self.assertIn('muted', attrs)
        for kind in ('desktop', 'movil'):
            video = ROOT / f'assets/media/roselegacy-mainvideo-{kind}.mp4'
            self.assertGreater(video.stat().st_size, 1000)
            self.assertLess(video.stat().st_size, 3 * 1024 * 1024)

if __name__ == '__main__':
    unittest.main()
