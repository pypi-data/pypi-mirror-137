# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gefyra', 'gefyra.api', 'gefyra.cluster', 'gefyra.local']

package_data = \
{'': ['*'], 'gefyra.local': ['cargo/*']}

install_requires = \
['docker>=5.0.3,<6.0.0', 'kubernetes>=19.15.0,<20.0.0']

entry_points = \
{'console_scripts': ['gefyra = gefyra.__main__:main']}

setup_kwargs = {
    'name': 'gefyra',
    'version': '0.2.0',
    'description': "Gefyra runs all developer machine side components of Gefyra's Kubernetes-based development infrastructure",
    'long_description': '# Gefyra\nGefyra gives Kubernetes-("cloud-native")-developers a completely new way of writing and testing their applications. \nGone are the times of custom Docker-compose setups, Vagrants, custom scrips or other scenarios in order to develop (micro-)services\nfor Kubernetes.  \n\n# Gefyra Client\nThe Gefyra client contains the developer machine side. Its main tasks are installation of the Gefyra Operator and\nthe setup of the docker network and the Cargo sidecar in order to prepare Gefyra\'s development infrastructure.\n\n## Tasks\n- install Operator into cluster\n- create Docker network on the developer machine\n- deploy app container into local docker network\n- deploy Cargo sidecar into local docker network\n- create a bridge to intercept cluster traffic and bring it to the local development container\n\n## Commands\n- `up`: setup local development infrastructure\n- `run`: deploy a new app container into the cluster\n- `bridge`: intercept the traffic to a container that\'s running in the cluster and send it to the development container\n- `unbridge`: remove active traffic intercepts and reset the cluster to its original state\n- `down`: remove Gefyra\'s development infrastructure\n- `list`: list running containers and active bridges\n- `check`: check local system dependencies \n\n## Run new app container in cluster\nThe Gefyra client can run a new app container in the Kubernetes cluster with `gefyra run ...`. \nA typical use case is a completely new application that doesn\'t have any deployed containers in the cluster yet.\n\nRequirements:\n- running local cluster or available remote cluster\n- `kubectl` connection to development cluster is active\n- successful `gefyra up`\n\n## Bridge a container\nThe Gefyra client can bridge (i.e. intercept) a container that is already running in the Kubernetes cluster with `gefyra bridge`.\nThe container needs to be specified and can be any deployed container of any pod.\n\nRequirements:\n- running local cluster or available remote cluster\n- `kubectl` connection to development cluster is active\n- successful `gefyra up`\n- successful `gefyra run ...`\n\nTasks:\n- fetch wireguard connection secrets from Kubernetes secret\n- deploy cargo sidecar into local docker network\n- deploy app container into local docker network\n- create _InterceptRequest_ \n\n\n# More Information\nFind more information on Github: https://github.com/Schille/gefyra',
    'author': 'Michael Schilonka',
    'author_email': 'michael@blueshoe.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Schille/gefyra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
