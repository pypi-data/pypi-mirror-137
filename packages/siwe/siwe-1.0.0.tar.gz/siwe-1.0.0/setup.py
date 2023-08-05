# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siwe', 'siwe.grammars']

package_data = \
{'': ['*']}

install_requires = \
['abnf==1.1.1',
 'eth-account>=0.5.6,<0.6.0',
 'python-dateutil==2.8.2',
 'web3>=5.26.0,<6.0.0']

setup_kwargs = {
    'name': 'siwe',
    'version': '1.0.0',
    'description': 'A Python implementation of Sign-In with Ethereum (EIP-4361).',
    'long_description': '# Sign-In with Ethereum\n\nThis package provides a Python implementation of EIP-4631: Sign In With Ethereum.\n\n## Installation\n\nSIWE can be easily installed in any Python project with pip:\n\n```bash\npip install siwe\n```\n\n## Usage\n\nSIWE provides a `SiweMessage` class which implements EIP-4361.\n\n### Parsing a SIWE Message\n\nParsing is done by initializing a `SiweMessage` object with an EIP-4361 formatted string:\n\n``` python\nmessage: SiweMessage = SiweMessage(message=eip_4361_string)\n```\n\nAlternatively, initialization of a `SiweMessage` object can be done with a dictionary containing expected attributes:\n\n``` python\nmessage: SiweMessage = SiweMessage(message={"domain": "login.xyz", "address": "0x1234...", ...})\n```\n\n### Verifying and Authenticating a SIWE Message\n\nVerification and authentication is performed via EIP-191, using the `address` field of the `SiweMessage` as the expected signer. The validate method checks message structural integrity, signature address validity, and time-based validity attributes. \n\n``` python\ntry:\n    message.validate()\nexcept siwe.ValidationError:\n    # Invalid\n```\n\n### Serialization of a SIWE Message\n\n`SiweMessage` instances can also be serialized as their EIP-4361 string representations via the `sign_message` method:\n\n``` python\nprint(message.sign_message())\n```\n\n## Example\n\nParsing and verifying a `SiweMessage` is easy:\n\n``` python\ntry:\n    message: SiweMessage = SiweMessage(message=eip_4361_string)\n    message.validate():\nexcept siwe.ValueError:\n    # Invalid message\n    print("Authentication attempt rejected.")\nexcept siwe.ExpiredMessage:\n    print("Authentication attempt rejected.")\nexcept siwe.MalformedSession as e:\n    # e.missing_fields contains the missing information needed for validation\n    print("Authentication attempt rejected.")\nexcept siwe.InvalidSignature:\n    print("Authentication attempt rejected.")\n    \n# Message has been validated. Authentication complete. Continue with authorization/other.\n```\n\n## TODOs\n\n- Support for contract wallets.\n\n## See Also\n\n- [Sign-In with Ethereum: TypeScript](https://github.com/spruceid/siwe)\n- [Example SIWE application: login.xyz](https://login.xyz)\n- [EIP-4361 Specification Draft](https://eips.ethereum.org/EIPS/eip-4361)\n- [EIP-191 Specification](https://eips.ethereum.org/EIPS/eip-191)\n\n## Disclaimer\n\nOur Python library for Sign-In with Ethereum has not yet undergone a formal\nsecurity audit. We welcome continued feedback on the usability, architecture,\nand security of this implementation.\n',
    'author': 'Spruce Systems, Inc.',
    'author_email': 'hello@spruceid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://login.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
