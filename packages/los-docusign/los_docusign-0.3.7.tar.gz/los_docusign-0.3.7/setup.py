# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['los_docusign', 'los_docusign.migrations', 'los_docusign.utils']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.13,<4.0.0',
 'PyJWT==1.7.1',
 'django-environ>=0.4.5,<0.5.0',
 'django-lc-utils>=0.2.1,<0.3.0',
 'django-model-utils>=4.1.1,<5.0.0',
 'django-utils-six>=2.0,<3.0',
 'docusign-esign>=3.6.0,<4.0.0',
 'psycopg2-binary>=2.9.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'los-docusign',
    'version': '0.3.7',
    'description': 'Docusign Django Wrapper for integrating DocuSign with Django Application',
    'long_description': '# Django-DocuSign\nDjango wrapper app for DocuSign functionalities\n\n`pip install django-docusign`\n\n## Running Tests\nWe have a unit test defined for testing the los application.\nThis can be executed using the below command.\n\n```\npython manage.py test\n```\n\n## Usage\nIn order to use the system you must add los_docusign.apps.LosDocusignConfig to your installed apps in your settings.py file.\n```python\nINSTALLED_APPS = [\n    \'los_docusign\'\n]\n```\n\nTest file has the sample implementation of the test_app\n\n## Functions in client.py\n1.  generate_docusign_preview_url(dict)\n\n    Params required in dict:\n    -   "envelope_id"\n    -   "authentication_method"\n    -   "email"\n    -   "user_name"\n    -   "client_user_id"\n    -   "return_url"\n\n2. create_envelope(payload)\n\n    Params required:\n    -   DocuSign payload in JSON format\n\n3. download_docusign_document(dict)\n\n    Params required in dict:\n    -   "envelope_id"\n    -   "doc_download_option"\n        -   Valid Values:\n            1. archive - If the document to be downloaded in zip format.\n            2. combined - If the document to be downloaded as a combined document.\n\n4. process_docusign_webhook(xml_string)\n\n    Params required:\n    -   Webhook XML string received from Docusign.\n\n    Response dict:\n        {\n            "envelopeId": "c57ec066-c5fa-4aa0-873d-6f285d70242a",\n            "envelope_status": "sent",\n            "recipients": [\n                {\n                    "recipient_id": "a7f73f21-c4ff-4bcb-97c4-b03c91b8528a",\n                    "email": "test@test.com",\n                    "name": "John Nash",\n                    "status": "autoresponded"\n                },\n                {\n                    "recipient_id": "511b2ad3-6650-4773-a6b4-47f64a0ccdaf",\n                    "email": "jerry@test.com",\n                    "name": "Jerry Tunes",\n                    "status": "created"\n                },\n                {\n                    "recipient_id": "0851505f-5af2-42df-bce4-9e0ebe8bd2e2",\n                    "email": "tom@test.com",\n                    "name": "Tom Tunes",\n                    "status": "created"\n                }\n            ]\n        }\n',
    'author': 'tejasb',
    'author_email': 'tejas@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/Django-DocuSign',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
