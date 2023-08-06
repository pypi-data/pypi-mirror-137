# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earhorn']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'httpx>=0.21.1,<0.23.0',
 'loguru>=0.5.3,<0.7.0',
 'more-itertools>=8.10.0,<9.0.0',
 'pydantic>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['earhorn = earhorn.cli:main']}

setup_kwargs = {
    'name': 'earhorn',
    'version': '0.5.2',
    'description': 'Listen, monitor and archive your streams!',
    'long_description': '# earhorn\n\nListen, monitor and archive your streams!\n\n[![](https://mermaid.ink/svg/eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgc3RhdGUgXCJTdGFydCBldmVudCBoYW5kbGVyXCIgYXMgc3RhcnRfaGFuZGxlclxuICAgIFsqXSAtLT4gc3RhcnRfaGFuZGxlclxuXG4gICAgc3RhdGUgXCJDaGVjayByZW1vdGUgc3RyZWFtXCIgYXMgY2hlY2tfc3RyZWFtXG4gICAgc3RhcnRfaGFuZGxlciAtLT4gY2hlY2tfc3RyZWFtXG5cbiAgICBzdGF0ZSBpZl9zdHJlYW1fb2sgPDxjaG9pY2U-PlxuICAgIHN0YXRlIHN0YXJ0IDw8Zm9yaz4-XG4gICAgY2hlY2tfc3RyZWFtIC0tPiBpZl9zdHJlYW1fb2s6IElzIHRoZSBzdHJlYW0gb2sgP1xuXG4gICAgaWZfc3RyZWFtX29rIC0tPiBzdGFydDogWWVzXG4gICAgc3RhdGUgXCJTdGFydCBsaXN0ZW5lclwiIGFzIHN0YXJ0X2xpc3RlbmVyXG4gICAgc3RhdGUgXCJTdGFydCByZWNvcmRlclwiIGFzIHN0YXJ0X3JlY29yZGVyXG4gICAgc3RhcnQgLS0-IHN0YXJ0X2xpc3RlbmVyXG4gICAgc3RhcnQgLS0-IHN0YXJ0X3JlY29yZGVyXG5cbiAgICBzdGF0ZSBcIlNlbmQgZXJyb3IgdG8gZXZlbnQgaGFuZGxlclwiIGFzIHNlbmRfZXJyb3JcbiAgICBzdGF0ZSBcIldhaXQgZm9yIDUgc2Vjb25kc1wiIGFzIHdhaXRfc3RyZWFtX29rXG4gICAgaWZfc3RyZWFtX29rIC0tPiBzZW5kX2Vycm9yOiBOb1xuICAgIHNlbmRfZXJyb3IgLS0-IHdhaXRfc3RyZWFtX29rXG4gICAgd2FpdF9zdHJlYW1fb2sgLS0-IGNoZWNrX3N0cmVhbVxuXG4gICAgc3RhdGUgXCJSdW4gKHVudGlsIGV4aXQgb3IgZXJyb3IgcmFpc2VkKVwiIGFzIHJ1bm5pbmdcbiAgICBzdGFydF9saXN0ZW5lciAtLT4gcnVubmluZ1xuICAgIHN0YXJ0X3JlY29yZGVyIC0tPiBydW5uaW5nXG5cbiAgICBydW5uaW5nIC0tPiBjaGVja19zdHJlYW06IEVycm9yIHJhaXNlZFxuXG4gICAgcnVubmluZyAtLT4gWypdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid.live/edit#eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgc3RhdGUgXCJTdGFydCBldmVudCBoYW5kbGVyXCIgYXMgc3RhcnRfaGFuZGxlclxuICAgIFsqXSAtLT4gc3RhcnRfaGFuZGxlclxuXG4gICAgc3RhdGUgXCJDaGVjayByZW1vdGUgc3RyZWFtXCIgYXMgY2hlY2tfc3RyZWFtXG4gICAgc3RhcnRfaGFuZGxlciAtLT4gY2hlY2tfc3RyZWFtXG5cbiAgICBzdGF0ZSBpZl9zdHJlYW1fb2sgPDxjaG9pY2U-PlxuICAgIHN0YXRlIHN0YXJ0IDw8Zm9yaz4-XG4gICAgY2hlY2tfc3RyZWFtIC0tPiBpZl9zdHJlYW1fb2s6IElzIHRoZSBzdHJlYW0gb2sgP1xuXG4gICAgaWZfc3RyZWFtX29rIC0tPiBzdGFydDogWWVzXG4gICAgc3RhdGUgXCJTdGFydCBsaXN0ZW5lclwiIGFzIHN0YXJ0X2xpc3RlbmVyXG4gICAgc3RhdGUgXCJTdGFydCByZWNvcmRlclwiIGFzIHN0YXJ0X3JlY29yZGVyXG4gICAgc3RhcnQgLS0-IHN0YXJ0X2xpc3RlbmVyXG4gICAgc3RhcnQgLS0-IHN0YXJ0X3JlY29yZGVyXG5cbiAgICBzdGF0ZSBcIlNlbmQgZXJyb3IgdG8gZXZlbnQgaGFuZGxlclwiIGFzIHNlbmRfZXJyb3JcbiAgICBzdGF0ZSBcIldhaXQgZm9yIDUgc2Vjb25kc1wiIGFzIHdhaXRfc3RyZWFtX29rXG4gICAgaWZfc3RyZWFtX29rIC0tPiBzZW5kX2Vycm9yOiBOb1xuICAgIHNlbmRfZXJyb3IgLS0-IHdhaXRfc3RyZWFtX29rXG4gICAgd2FpdF9zdHJlYW1fb2sgLS0-IGNoZWNrX3N0cmVhbVxuXG4gICAgc3RhdGUgXCJSdW4gKHVudGlsIGV4aXQgb3IgZXJyb3IgcmFpc2VkKVwiIGFzIHJ1bm5pbmdcbiAgICBzdGFydF9saXN0ZW5lciAtLT4gcnVubmluZ1xuICAgIHN0YXJ0X3JlY29yZGVyIC0tPiBydW5uaW5nXG5cbiAgICBydW5uaW5nIC0tPiBjaGVja19zdHJlYW06IEVycm9yIHJhaXNlZFxuXG4gICAgcnVubmluZyAtLT4gWypdIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRlZmF1bHRcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)\n\n## Install\n\n```sh\nsudo apt install ffmpeg\npip install earhorn\n```\n\n```sh\nearhorn --archive-path=/to/my/archive https://stream.example.org/live.ogg\n```\n\n### Docker\n\n```sh\ndocker pull ghcr.io/jooola/earhorn\n```\n\n## Usage\n\n```\nUsage: earhorn [OPTIONS] URL\n\n  URL of the stream.\n\nOptions:\n  --hook PATH                       Hook to run to handle events.\n  --archive-path PATH               Path to the archive directory.\n  --archive-segment-size INTEGER    Archive segment size in seconds.  [default: 3600]\n  --archive-segment-filename TEXT   Archive segment filename (without extension).  [default: archive-%Y%m%d_%H%M%S]\n  --archive-segment-format TEXT     Archive segment format.  [default: ogg]\n  --help                            Show this message and exit.\n\n```\n\n## Releases\n\nTo release a new version, first bump the version number in `pyproject.toml` by hand or by using:\n\n```sh\n# poetry version --help\npoetry version <patch|minor|major>\n```\n\nRun the release target:\n\n```sh\nmake release\n```\n\nFinally, push the release commit and tag to publish them to Pypi:\n\n```sh\ngit push --follow-tags\n```\n',
    'author': 'Joola',
    'author_email': 'jooola@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
