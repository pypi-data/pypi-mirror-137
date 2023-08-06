# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gandi_tf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['gandi2tf = gandi_tf.main:generate']}

setup_kwargs = {
    'name': 'gandi-2-terraform',
    'version': '1.1.0',
    'description': 'CLI to read Gandi.net live DNS records and generate corresponding TF gandi_livedns_record resources',
    'long_description': '# Generate Terraform file from Gandi DNS records\n\n[![Pypi version](https://img.shields.io/pypi/v/gandi-2-terraform?color=blue)](https://pypi.org/project/gandi-2-terraform/)\n[![Python versions](https://img.shields.io/pypi/pyversions/gandi-2-terraform.svg)](https://pypi.org/project/gandi-2-terraform/)\n[![Build status](https://github.com/marcaurele/gandi-2-terraform/workflows/Build%20status/badge.svg)](https://github.com/marcaurele/gandi-2-terraform/actions)\n\n\nThis tool aims to simplify managin DNS recods using Terrafom by making the initial import through a single operation.\nIt fetches DNS records from one or multiple domains you own with [Gandi.net](https://gandi.et) and generates TF files with the corresponding records\' resources using `gandi_livedns_record` and defining each record in a set (see the example output).\n\n## Install\n\n```console\n$ pip install gandi-2-terraform\n$ gandi2tf --help\n```\n\n## Configuration\n\nIn order to access the DNS records through the API, you have to provide your API key. It uses the same variable name than the [Gandi Terraform](https://registry.terraform.io/providers/go-gandi/gandi/latest) provider `GANDI_KEY`. See [Gandi authentication documentation](https://api.gandi.net/docs/authentication/) of their API on how to generate one.\n\n## Example\n\n```console\n$ export GANDI_KEY=A1b2C3d4E5f6\n$ gandi-2tf example.com\n```\n\nwill generate a file `example.com.tf` containing:\n\n```hcl\nlocals {\n  example_com_records = {\n    apex_a = {\n      name = "@"\n      type = "A"\n      ttl  = 10800\n      values = [\n        "192.30.252.153",\n        "192.30.252.154",\n      ]\n    }\n    apex_mx = {\n      name = "@"\n      type = "MX"\n      ttl  = 10800\n      values = [\n        "10 spool.mail.gandi.net.",\n        "50 fb.mail.gandi.net.",\n      ]\n    }\n    apex_txt = {\n      name = "@"\n      type = "TXT"\n      ttl  = 10800\n      values = [\n        "\\"v=spf1 include:_mailcust.gandi.net -all\\"",\n      ]\n    }\n    imap_cname = {\n      name = "imap"\n      type = "CNAME"\n      ttl  = 10800\n      values = [\n        "access.mail.gandi.net.",\n      ]\n    }\n    smtp_cname = {\n      name = "smtp"\n      type = "CNAME"\n      ttl  = 10800\n      values = [\n        "relay.mail.gandi.net.",\n      ]\n    }\n    webmail_cname = {\n      name = "webmail"\n      type = "CNAME"\n      ttl  = 10800\n      values = [\n        "webmail.gandi.net.",\n      ]\n    }\n  }\n}\n\nresource "gandi_livedns_record" "example_com" {\n  for_each = local.example_com_records\n\n  zone = "example.com"\n\n  name   = each.value.name\n  ttl    = each.value.ttl\n  type   = each.value.type\n  values = each.value.values\n}\n```\n',
    'author': 'Marc-Aurèle Brothier',
    'author_email': 'm@brothier.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcaurele/gandi-2-terraform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
