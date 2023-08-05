# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pterradactyl',
 'pterradactyl.commands',
 'pterradactyl.facter',
 'pterradactyl.facter.woops',
 'pterradactyl.terraform',
 'pterradactyl.util',
 'pterradactyl.validator']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.3,<2.0.0',
 'jinja2>=2.11.1,<3.0.0',
 'jsonpath-ng>=1.5.1,<2.0.0',
 'phiera>=2.0.13,<3.0.0',
 'python-interface>=1.5.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'semantic_version>=2.8.4,<3.0.0']

entry_points = \
{'console_scripts': ['pt = pterradactyl.__main__:main'],
 'pterradactyl.facters': ['arguments = '
                          'pterradactyl.facter.arguments:ArgumentsFacter',
                          'environment = '
                          'pterradactyl.facter.environment:EnvironmentFacter',
                          'jinja = pterradactyl.facter.jinja:JinjaFacter',
                          'regex = pterradactyl.facter.regex:RegexFacter',
                          'shell = pterradactyl.facter.shell:ShellFacter'],
 'pterradactyl.registered_commands': ['apply = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'console = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'destroy = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'env = '
                                      'pterradactyl.commands.env:EnvCommand',
                                      'facts = '
                                      'pterradactyl.commands.dump:DumpFactsCommand',
                                      'fmt = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'force-unlock = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'get = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'graph = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'import = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'lookup = '
                                      'pterradactyl.commands.lookup:LookupCommand',
                                      'output = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'plan = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'providers = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'refresh = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'root-module = '
                                      'pterradactyl.commands.dump:DumpRootModuleCommand',
                                      'show = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'state = '
                                      'pterradactyl.commands.state:StateCommand',
                                      'taint = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'untaint = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'validate = '
                                      'pterradactyl.commands.manifest:ManifestCommand',
                                      'workspace = '
                                      'pterradactyl.commands.manifest:ManifestCommand'],
 'pterradactyl.validators': ['version = '
                             'pterradactyl.validator.version:VersionValidator']}

setup_kwargs = {
    'name': 'pterradactyl',
    'version': '1.2.11',
    'description': 'hiera-inspired terraform wrapper',
    'long_description': 'Pterradactyl\n---\n\n[![codecov](https://codecov.io/gh/Nike-Inc/pterradactyl/branch/master/graph/badge.svg?token=CvHYOh04mZ)](https://codecov.io/gh/Nike-Inc/pterradactyl)\n[![Test](https://github.com/Nike-Inc/pterradactyl/actions/workflows/python-test.yaml/badge.svg)](https://github.com/Nike-Inc/pterradactyl/actions/workflows/python-test.yaml)\n[![PyPi Release](https://github.com/Nike-Inc/pterradactyl/actions/workflows/python-build.yaml/badge.svg)](https://github.com/Nike-Inc/pterradactyl/actions/workflows/python-build.yaml)\n![License](https://img.shields.io/pypi/l/pterradactyl)\n![Python Versions](https://img.shields.io/pypi/pyversions/pterradactyl)\n![Python Wheel](https://img.shields.io/pypi/wheel/pterradactyl)\n\n\nPterradactyl is a library developed to abstract TF configuration from the TF environment setup. Pterradactyl allows to create a hierarchy of TF environments/stacks, hallows an unconstrained number of cloud accounts and stacks to share inherited configuration.\n\nCurrently, multiple TF stacks are managed through different TF environments and var files. But this becomes especially tricky to manage when the stacks are vastly different from one another, or even in the case of slightly different stacks, one could question the DRY principal looking at all the repeat vars in the var file! When stacks deviate from one another, by using just the var files, the TF code quickly becomes unreadable with all the conditionals. Using just environments based TF, there is always room of accidental apply of one stack to the other. You can use bash files to safegaurd against that but then there is always the old faithful way of doing by just completely skipping the bash file ! (#fun-stuff)\n\nPterradactyl takes care of all the pain points described above.\n\nTable of content\n* [Some of the Pterradactyl features](#features)\n* [Installation](#installation)\n* [Usage](#usage)\n* [Unit Tests](#tests)\n* [Examples of creating new projects/prodcuts](#examples)\n* [Pterradactyl Directory Structure](#structure)\n* [Comparison of other well-known Terraform wrappers:](#tf_wrappers)\n\n# <a name="features"></a> Some of the Pterradactyl features:\n\n- Programatically generated Terraform code using hierarchical YAML files structure. Override only what you have to in your stack file and keep the rest in common YAML.\n- Because Pterradactyl uses hierarchy, it becomes simple to provide standard structure to common attributes like `tags` in a uniform manner.\n- Secrets support using _sops_ and _AWS KMS_.\n- Keeps Terraform versions consistent between stacks.\n- As the Terraform file is generated through Pterradactyl, there is no room for the fun `override` :)\n\n\nPterradactyl uses [Phiera](https://github.com/Nike-Inc/phiera), to manage the YAML hierarchy configuration for a terraform code base.\n\nIntegration of terraform with Phiera is achieved through Pterradactyl.\n\nA primer on [Hiera](https://puppet.com/docs/puppet/latest/hiera_intro.html).\n\n\n# <a name="installation"></a> Installation:\n### From PyPi:\n```shell script\npip install pterradactyl\n```\n\n### From GitHub:\n```shell script\npip install git+https://github.com/Nike-Inc/pterradactyl#egg=pterradactyl\n```\n\n### From source\nYou can always install it from wheel, by running the following commands:\n\nBuild package and wheel.\n```python\npoetry install\npoetry build\n```\n\nInstall\n```python\npython3 -m pip install dist/*.whl\n```\n\nOf course, you can always deploy the package to your corporate Artifactory.\n\n# <a name="usage"></a> Usage:\n\nPterradyctal supports all of the terraform commands.\n\n#### basic cli\n```bash\napply `pt apply <stack-name>`\nplan `pt plan <stack-name>`\ndestroy `pt destroy <stack-name>`\ngraph `pt graph <stack-name>`\nshow `pt show <stack-name>`\n```\n\n#### Manipulating state\nPterradyctal supports all state commands and they follow the same argument patter as in TF, here are some examples\n\n```bash\nstate list `pt state list <stack-name>`\nstate show `pt state show <stack-name> -state <target>`\nstate rm `pt state rm <stack-name> -state <statefile>`\n```\n# <a name="tests"></a> Tests:\n\nRun unit tests\n\n```bash\npoetry run pytest\n```\n\nRun unit tests with coverage report in HTML format.\n\n```bash\npoetry run pytest --cov-report=html --cov=pterradactyl --cov-fail-under=80 tests/\n```\n\n# <a name="examples"></a> Examples of creating new projects/prodcuts:\n\nBasic Example [here](https://github.com/Nike-Inc/pterradactyl/blob/master/examples/simple/README.md)\n- Module setup\n- Attribute overriding\n\nAdvanced Example [here](https://github.com/Nike-Inc/pterradactyl/blob/master/examples/complex/README.md)\n- Create infrastructure for a new AWS account\n- Common tag setup\n- KMS encryption\n- Remote backend\n- Module setup\n- Attribute overriding\n\n\n# <a name="structure"></a> Pterradactyl Directory Structure:\n\nAfter running `pt apply` pterradactyl will create below directory structure,\ncontaining downloaded given Terraform version with all required plugins, and workspace containing all metadata for your stack, e.g.:\n\n```\n.pterradactyl\n├── terraform\n│     └── 0.13.1\n│         ├── terraform\n│         └── terraform-provider-kubectl_v1.13.1\n└── workspace\n    └── bt-projectc0-na-useast1\n        ├── facts.json\n        └── main.tf.json\n```\n\n- terraform - directory containing downloaded Terraform given version with downloaded plugins defined in pterra.yaml file.\n- workspace - directory containing metadata information for you stack. Each stack has a separate workspace.\n- facts.json - JSON file with facts generated by Pterradactyl (e.g. deploy_user, state_prefix, aws_account_alias)\n- main.tf.json - metadata information file regarding providers (e.g. aws, kubernetes, helm), moduls (e.g. vpc, kms, eks)and terraform backend information.\n\n\n# <a name="tf_wrappers"></a> Comparison of other well-known Terraform wrappers:\n\n### Terragrunt:\nSome of the key Terragrunt features:\n\n- Execute Terraform commands on multiple modules at once\n- Keep your Terraform configuration DRY\n- Inputs set as env variables.\n- Call custom actions using Before and After Hooks\n- Work with multiple AWS accounts\n- Lock File Handling\n- AWS Auth support\n- Caching folder where commands are being executed.\n- Auto-retry e.g. when installing provider failed due to connection error.\n\n\nMore info [here](https://terragrunt.gruntwork.io/docs/#features)\n\n### Terraspace:\n\nSome of the key Terraspace features:\n\n- Build-in generators\n- Multiple environments\n- Deploy Multiple Stacks with a single command\n- Build-in secrets support for AWS Secret Manager, AWS SSM Parameter Store, Azure Key\n- Configurable CLI Hooks and CLI Args.\n- Allows you to create test harness.\n- Terraform Cloud and Terraform Enterprise support.\n\n\nMore info [here](https://terraspace.cloud/docs/intro/)\n\n### Comparison between Pterradactyl vs Terragrunt vs Terraspace\n\n|  Feature | Pterradactyl  | Terragrunt  |  Terraspace |  Comment |\n|---|---|---|---|---|\n| **Organized Structure** | &check; | &check; | &check; |  |\n| **Multiple environments** | &check; | &check; | &check; |  |\n| **Execute Terraform commands on multiple modules at once** |  &check; |  &check;  |  &check;  |  |\n| **Secrets support** | &check; | &check;  | &check; |  |\n| **CLI Hooks** | &check; | &check;  | &check;  | [More details](https://terraspace.cloud/docs/config/hooks/) |\n| **Automated Backend Creation** | &check; | &check;  | &check;  | |\n| **Built-in Test Framework** | &cross; |  &cross; | &check; | [More details](https://terraspace.cloud/docs/testing/) |\n| **Native Terraform HCL** | &cross; |  &cross; | &check; | [More details](https://terraspace.cloud/docs/vs/terragrunt/) |\n\n### Summary\nIt\'s hard to compare Pterradactyl, Terragrunt and Terraspace on the same level.\\\nOverall all those tools have some major differences. However above gives you a gist of what you can expect in each tool.\\\nIf you are thinking what is more proper for you, simply deep into the details of each tool.\nTerragrut and Pterradactyl are rather thin wrappers for Terraform, whereas Terraspace is rather a huge framework.\n\n',
    'author': 'Rob King',
    'author_email': 'rob.king@nike.com',
    'maintainer': 'Mohamed Abdul Huq Ismail',
    'maintainer_email': 'Abdul.Ismail@nike.com',
    'url': 'https://github.com/Nike-Inc/pterradactyl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
