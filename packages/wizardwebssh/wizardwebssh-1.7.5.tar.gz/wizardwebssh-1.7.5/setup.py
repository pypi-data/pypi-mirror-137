# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wizardwebssh']

package_data = \
{'': ['*'],
 'wizardwebssh': ['static/css/*',
                  'static/css/fonts/*',
                  'static/img/*',
                  'static/js/*',
                  'templates/*']}

install_requires = \
['paramiko>=2.9.2,<3.0.0', 'tomlkit>=0.9.0,<0.10.0', 'tornado==6.1']

extras_require = \
{'pyqt6': ['PyQt6>=6.2.3,<7.0.0',
           'PyQt6-Qt6>=6.2.3,<7.0.0',
           'PyQt6-sip>=13.2.1,<14.0.0',
           'PyQt6-WebEngine>=6.2.1,<7.0.0',
           'PyQt6-WebEngine-Qt6>=6.2.3,<7.0.0']}

entry_points = \
{'console_scripts': ['wssh = wizardwebssh.main:main']}

setup_kwargs = {
    'name': 'wizardwebssh',
    'version': '1.7.5',
    'description': 'Web based ssh client',
    'long_description': '## Wizard Web SSH\n\n[![ci](https://github.com/meramsey/wizardwebssh/workflows/ci/badge.svg)](https://github.com/meramsey/wizardwebssh/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://meramsey.github.io/wizardwebssh/)\n[![pypi version](https://img.shields.io/pypi/v/wizardwebssh.svg)](https://pypi.org/project/wizardwebssh/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/wizardwebssh/community)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nWeb based ssh client\n\n## Requirements\n\nwizardwebssh requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install wizardwebssh\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 wizardwebssh\n```\n\n### Introduction\n\nA simple web application to be used as an ssh client to connect to your ssh servers. It is written in Python, base on tornado, paramiko and xterm.js.\n\n### Features\n\n* SSH password authentication supported, including empty password.\n* SSH public-key authentication supported, including DSA RSA ECDSA Ed25519 keys.\n* SSH Agent Support\n* Sqlite DB support for SSH Config.\n* PyQT5 MultiTabbed Terminal Widget for embedding into PyQT5 apps.\n* Encrypted keys supported.\n* Two-Factor Authentication (time-based one-time password, Duo Push Auth) supported.\n* Fullscreen terminal supported.\n* Terminal window resizable.\n* Auto detect the ssh server\'s default encoding.\n* Modern browsers including Chrome, Firefox, Safari, Edge, Opera supported.\n\n\n### Preview\n\n![Login](https://gitlab.com/mikeramsey/wizardwebssh/raw/master/preview/login.png)\n![Terminal](https://gitlab.com/mikeramsey/wizardwebssh/raw/master/preview/terminal.png)\n![PyQT5 MultiTabbed Terminal Widget](https://gitlab.com/mikeramsey/wizardwebssh/raw/master/preview/multitabbedterminalwidget.png)\n![PyQT5 MultiTabbed DarkMode Terminal Widget](https://gitlab.com/mikeramsey/wizardwebssh/raw/master/preview/TabbedTerminal_Example1.png)\n![PyQT5 MultiTabbed DarkMode Terminal Widget Login](https://gitlab.com/mikeramsey/wizardwebssh/raw/master/preview/TabbedTerminal_Example2.png)\n\n\n### How it works\n```\n+---------+     http     +--------+    ssh    +-----------+\n| browser | <==========> | wizardwebssh | <=======> | ssh server|\n+---------+   websocket  +--------+    ssh    +-----------+\n```\n\n### Requirements\n\n* Python 2.7/3.4+\n\n\n### Quickstart\n\n1. Install this app, run command `pip install wizardwebssh`\n2. Start a webserver, run command `wssh`\n3. Open your browser, navigate to `127.0.0.1:8889`\n4. Input your data, submit the form.\n\n\n### Server options\n\n```bash\n# start a http server with specified listen address and listen port\nwssh --address=\'2.2.2.2\' --port=8000\n\n# start a https server, certfile and keyfile must be passed\nwssh --certfile=\'/path/to/cert.crt\' --keyfile=\'/path/to/cert.key\'\n\n# missing host key policy\nwssh --policy=reject\n\n# logging level\nwssh --logging=debug\n\n# log to file\nwssh --log-file-prefix=main.log\n\n# more options\nwssh --help\n```\n\n### Browser console\n\n```javascript\n// connect to your ssh server\nwssh.connect(hostname, port, username, password, privatekey, passphrase, totp);\n\n// pass an object to wssh.connect\nvar opts = {\n  hostname: \'hostname\',\n  port: \'port\',\n  username: \'username\',\n  password: \'password\',\n  privatekey: \'the private key text\',\n  passphrase: \'passphrase\',\n  totp: \'totp\'\n};\nwssh.connect(opts);\n\n// without an argument, wssh will use the form data to connect\nwssh.connect();\n\n// set a new encoding for client to use\nwssh.set_encoding(encoding);\n\n// reset encoding to use the default one\nwssh.reset_encoding();\n\n// send a command to the server\nwssh.send(\'ls -l\');\n```\n\n### Custom Font\n\nTo use custom font, put your font file in the directory `wizardwebssh/static/css/fonts/` and restart the server.\n\n### URL Arguments\n\nSupport passing arguments by url (query or fragment) like following examples:\n\nPassing form data (password must be encoded in base64, privatekey not supported)\n```bash\nhttp://localhost:8889/?hostname=xx&username=yy&password=str_base64_encoded\n```\n\nPassing a terminal background color\n```bash\nhttp://localhost:8889/#bgcolor=green\n```\n\nPassing a user defined title\n```bash\nhttp://localhost:8889/?title=my-ssh-server\n```\n\nPassing an encoding\n```bash\nhttp://localhost:8889/#encoding=gbk\n```\n\nPassing a command executed right after login\n```bash\nhttp://localhost:8889/?command=pwd\n```\n\nPassing a terminal type\n```bash\nhttp://localhost:8889/?term=xterm-256color\n```\n\n### Use Pyqt5 SSH Terminal Widget\n\nStart up the wizardwebssh ssh service\n```\nclass WizardWebssh(object):\n    """ Threading example class\n    The run() method will be started and it will run in the background\n    until the application exits.\n    """\n\n    def __init__(self, interval=1):\n        """ Constructor\n        :type interval: int\n        :param interval: Check interval, in seconds\n        """\n        self.interval = interval\n\n        thread = threading.Thread(target=self.run, args=())\n        thread.daemon = True  # Daemonize thread\n        thread.start()  # Start the execution\n\n    def run(self):\n        """ Method that runs forever """\n        while True:\n            # Start WebSSH Service in background.\n            print(\'Starting SSH websocket server in the background\')\n            import asyncio\n\n            asyncio.set_event_loop(asyncio.new_event_loop())\n            from wizardwebssh.main import main as wssh\n            wssh()\n            print(\'Stopped SSH websocket server in the background\')\n            QApplication.processEvents()\n            time.sleep(self.interval)\n\n\n    wizardwebssh_service = WizardWebssh()\n    time.sleep(.300)\n```\n\nEmbed the widget as desired\n```\n    win = TabbedTerminal()\n    win.show()\n```\n\nReview tabbedbterminal.py for full standalone working example of SSH terminal widget.\n\n\n### Use Docker\n\nStart up the app\n```\ndocker-compose up\n```\n\nTear down the app\n```\ndocker-compose down\n```\n\n### Tests\n\nRequirements\n```\npip install pytest pytest-cov codecov flake8 mock\n```\n\nUse unittest to run all tests\n```\npython -m unittest discover tests\n```\n\nUse pytest to run all tests\n```\npython -m pytest tests\n```\n\n### Deployment\n\nRunning behind an Nginx server\n\n```bash\nwssh --address=\'127.0.0.1\' --port=8889 --policy=reject\n```\n```nginx\n# Nginx config example\nlocation / {\n    proxy_pass http://127.0.0.1:8889;\n    proxy_http_version 1.1;\n    proxy_read_timeout 300;\n    proxy_set_header Upgrade $http_upgrade;\n    proxy_set_header Connection "upgrade";\n    proxy_set_header Host $http_host;\n    proxy_set_header X-Real-IP $remote_addr;\n    proxy_set_header X-Real-PORT $remote_port;\n}\n```\n\nRunning as a standalone server\n```bash\nwssh --port=8080 --sslport=4433 --certfile=\'cert.crt\' --keyfile=\'cert.key\' --xheaders=False --policy=reject\n```\n\n\n### Tips\n\n* For whatever deployment choice you choose, don\'t forget to enable SSL.\n* By default plain http requests from a public network will be either redirected or blocked and being redirected takes precedence over being blocked.\n* Try to use reject policy as the missing host key policy along with your verified known_hosts, this will prevent man-in-the-middle attacks. The idea is that it checks the system host keys file("~/.ssh/known_hosts") and the application host keys file("./known_hosts") in order, if the ssh server\'s hostname is not found or the key is not matched, the connection will be aborted.\n',
    'author': 'Michael Ramsey',
    'author_email': 'mike@hackerdise.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/meramsey/wizardwebssh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
