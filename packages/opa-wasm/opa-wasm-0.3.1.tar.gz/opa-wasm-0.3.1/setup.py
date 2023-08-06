# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opa_wasm']

package_data = \
{'': ['*']}

install_requires = \
['wasmer>=1.0.0,<2.0.0']

extras_require = \
{'cranelift': ['wasmer-compiler-cranelift>=1.0.0,<2.0.0'],
 'llvm': ['wasmer-compiler-llvm>=1.0.0,<2.0.0']}

setup_kwargs = {
    'name': 'opa-wasm',
    'version': '0.3.1',
    'description': 'Open Policy Agent WebAssembly SDK for Python',
    'long_description': '# Open Policy Agent WebAssembly SDK for Python\n\nThis is the source for the\n[opa-wasm](https://pypi.org/project/opa-wasm/)\nPython module which is an SDK for using WebAssembly (wasm) compiled \n[Open Policy Agent](https://www.openpolicyagent.org/) Rego policies using [wasmer-python](https://github.com/wasmerio/wasmer-python).\n\n# Getting Started\n## Install the module\n\nYou may choose to use either the `cranelift` or `llvm` compiler package as follows: \n\n```\npip install opa-wasm[cranelift]\n```\nor\n```\npip install opa-wasm[llvm]\n```\n\nFor builds that target AWS Lambda as an execution environment, it is recommended to use cranelift. This avoids \nthe need to bundle additional binary dependencies as part of the lambda package.\n\nSee the [wasmer-python](https://github.com/wasmerio/wasmer-python) docs for more information\n\n## Usage\n\nThere are only a couple of steps required to start evaluating the policy.\n\n\n```python\n# Import the module\nfrom opa_wasm import OPAPolicy\n\n# Load a policy by specifying its file path\npolicy = OPAPolicy(\'./policy.wasm\')\n\n# Optional: Set policy data\npolicy.set_data({"company_name": "ACME"})\n\n# Evaluate the policy\ninput = {"user": "alice"}\nresult = policy.evaluate(input)\n```\n\n## Writing the policy\n\nSee [https://www.openpolicyagent.org/docs/latest/how-do-i-write-policies/](https://www.openpolicyagent.org/docs/latest/how-do-i-write-policies/)\n\n## Compiling the policy\n\nEither use the [Compile REST API](https://www.openpolicyagent.org/docs/latest/rest-api/#compile-api) or `opa build` CLI tool.\n\nFor example, with OPA v0.20.5+:\n\n```bash\nopa build -t wasm -e \'example/allow\' example.rego\n```\nWhich compiles the `example.rego` policy file with the result set to\n`data.example.allow`. The result will be an OPA bundle with the `policy.wasm`\nbinary included. \n\nSee `opa build --help` for more details.\n\n## Credits\n\nThis project was inspired by the equivalent NPM Module [@open-policy-agent/opa-wasm](https://github.com/open-policy-agent/npm-opa-wasm)',
    'author': 'Imtiaz Mangerah',
    'author_email': 'Imtiaz_Mangerah@a2d24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a2d24/python-opa-wasm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
