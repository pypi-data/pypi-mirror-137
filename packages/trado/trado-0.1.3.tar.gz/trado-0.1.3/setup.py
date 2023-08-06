# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['trado']
install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['trado = trado:main']}

setup_kwargs = {
    'name': 'trado',
    'version': '0.1.3',
    'description': 'Dumb and dirty docker-compose files generator for traefik exposing',
    'long_description': '# trado\nDumb and dirty docker-compose files generator for traefik exposing\n\nAll services described in one services.yml file and converted to more or less docker-compose compatible blocks. \nTop-level keys is services name, images, environment, volumes, ports is mirrored to docker-compose.\nImportant part is `url` key, which is used to generate traefik labels.\n`url` signature is:\n```yaml\nurl: <host>[/<path>][@port]\n```\n\n- `host` directly used as hostname in traefik labels. TLS with letsencrypt is enabled by default.\n- `path` is optional and used as path in traefik. New service will be exposed with `https://host/path` but after proxing the path will be truncated.\n   Be careful, `host` without path must be configured in a diffrenent service at least once.\n- `port`: it\'s a hint for traefik to find a proper port for proxying\n\nNotice, that default `networks` for all services with `url` defined is `traefik`.\n\n```yaml\ngitea:\n  image: gitea/gitea:latest\n  append:\n    environment:\n      - USER_UID=1000\n      - USER_GID=1000\n    volumes:\n      - ./data:/data\n    ports:\n      - "3000:3000"\n      - "2222:22"\n  url: git.rubedo.cloud @ 3000\n  expose: 3000\nasdf:\n  image: containous/whoami\n  url: asdf.rubedo.cloud\nwhoami2:\n  image: containous/whoami\n  url: git.rubedo.cloud /test\n  append:\n    restart: unless-stopped\n    labels:\n      - "testlabel=true"\nblah:\n  image: containous/whoami # not exposed to traefik at all\n```',
    'author': 'Grigory Bakunov',
    'author_email': 'thebobuk@ya.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
