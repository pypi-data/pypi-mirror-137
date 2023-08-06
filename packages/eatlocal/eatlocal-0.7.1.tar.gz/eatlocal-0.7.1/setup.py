# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eatlocal']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'rich>=11.1.0,<12.0.0',
 'selenium>=4.1.0,<5.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['eatlocal = eatlocal.__main__:cli']}

setup_kwargs = {
    'name': 'eatlocal',
    'version': '0.7.1',
    'description': 'eatlocal helps the user solve PyBite code challenges on their local machine',
    'long_description': '# eatlocal\n\nEatlocal helps the user solve [PyBites](https://codechallang.es) code challenges locally. This cli tool allows you to download, unzip, and organize bites according to the expected structure from the directions on the PyBites website. Once you have solved the bite you can use eatlocal to submit and it will open a bowser tab at the correct location.\n\n## Table of Contents\n\n+ [Usage](#Usage)\n+ [Installation](#Installation)\n\t+ [macOS/Linux](#macoslinux)\n\t+ [Windows](#Windows)\n+ [Setup](#Setup)\n\t+ [Install Chrome and Chromedriver](#Install-Chrome-and-Chromedriver)\n\t\t+ [macOS](#macOS)\n\t\t+ [Linux](#Linux)\n\t\t+ [Windows](#Windows-1)\n\t+ [PyBites Credentials](#PyBites-Credentials)\n\t\t+ [macOS/Linux](#macoslinux-1)\n\t\t+ [Windows](#Windows-2)\n\n\n## Usage\n\nNavigate to your local PyBites repo.\n\nDownload and extract bites:\n```bash\neatlocal download <bite number>\n```\n\nDisplay bites in the terminal:\n```bash\neatlocal display <bite number>\n```\n\nSubmit bites:\n```bash\neatlocal submit <bite number>\n```\n\n## Installation\n\n### macOS/Linux\n\n```bash\npip3 install eatlocal\n```\n### Windows\n\n```bash\npip install eatlocal\n```\n\n## Setup\n\n1. Go through the directions on the PyBites website to connect your GitHub account to your PyBites account.\n2. Make sure you have Chrome and chromedriver installed and on `$PATH`.\n3. Setup your PyBites login credentials as environment variables. If you signed up for PyBites by authenticating through GitHub or Google, you may need to set a password manually in order to use eatlocal.\n\n### Install Chrome and Chromedriver\n\n#### macOS\n\nOne option is to use homebrew [homebrew](https://brew.sh/). \n\nInstall chrome:\n\n```bash\nbrew install --cask google-chrome\n```\n\nInstall chromedriver:\n\n```bash\nbrew install chromedriver\n```\n\nBefore you run chromedriver for the first time, you must explicitly give permission since the developer has not been verified. Running the following command in the terminal removes the warning put in place by Apple:\n\n```bash\nxattr -d com.apple.quarantine $(which chromedriver)\n```\n\nHomebrew automatically puts chromedriver on `$PATH` for you. And since homebrew handles both chrome and chromedriver installations for me, I can run `brew update && brew upgrade` to help ensure I have the same version number for both chrome and chromedriver. If you do not go the homebrew route, you must manually ensure that your version of chrome matches the version of chromedriver.\n\n\n#### Linux\n\nUnfortunately, I did not find some fancy package manager for Linux, but I was able to install chrome and chromedriver manually for Linux Mint.\n\nNavigate to the download page for [google chrome](https://www.google.com/chrome/) and download the appropriate version for your system. Then, open up a terminal and navigate to where you downloaded the file. For me it was `~/Downloads`. I ran the following commands to install and check which version I have.\n\n```bash\ncd ~/Downloads\nsudo dpkg -i google-chrome-stable_current_amd64.deb\ngoogle-chrome --version\n```\n\nNext, navigate to the [chromedriver download page](https://chromedriver.chromium.org/downloads) and choose the version that matches the output from `google-chrome --version`. Download that file that matches your system. Head back to your terminal.\n\n1. Ensure that you have unzip installed:\n\n```bash\nsudo apt install unzip\n```\n\n2. Unzip the chromedriver file. For me it was located in the downloads folder: \n\n```bash\nunzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads\n```\n\n3. Make it executable and move to `/usr/local/share`:\n\n```bash\nchmod +x ~/Downloads/chromedriver\nsudo mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver\n```\n\n4. Create symlinks:\n\n```bash\nsudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver\n```\n5. Confirm you have access:\n\n```bash\nwhich chromedriver\n```\n\n#### Windows\n\nIf working in windows powershell you can use [chocolately](https://chocolatey.org/) to install chromedriver.\n\nI\'ve found that in order to install packages I have to use an elevated administrative shell, with `choco install chromedriver`.\n\nI attempted to use `eatlocal` from [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) but there seems to be an issue with `google-chrome` itself. I could not get it to work.\n\n### PyBites Credentials\n\nYou must have your PyBites username and password stored in the environment variables `PYBITES_USERNAME` and `PYBITES_PASSWORD` respectively.\n\n#### macOS/Linux\n\nThere are two methods to handle this in.\n\n**Virtual Environment Method**\n\nA note of warning: If you use this method make sure that your virtual environment is not being pushed to GitHub. If you accidentally push your virtual environment—clearly that has never happened to me—then you have exposed your password and should change it immediately.\n\n1. Create a virtual environment for your PyBites repo:\n\n```bash\npython3 -m venv .venv\n```\n\n2. Add the line `.venv` to your `.gitignore` file.\n\n```bash\necho ".venv" >> .gitignore\n```\n\n3. With the environment deactivated, use your favorite text editor (I use nvim, btw) to open the activate file, e.g., `nvim .venv/bin/activate` and add the following lines:\n\n```bash\nexport PYBITES_USERNAME=<username>\nexport PYBITES_PASSWORD=<password>\n```\n\n4. Activate the environment `source .venv/bin/activate`.\n\n**Shell RC Method**\n\nIf you are not using a virtual environment, you can add the variables directly to your shell config. \n\n1. I use zsh, so I would use my favorite text editor `nvim ~/.zshrc` and set the variables by adding the same two lines as above:\n\n```bash\nexport PYBITES_USERNAME=<username>\nexport PYBITES_PASSWORD=<password>\n```\n\n2. Either exit your terminal completely and reopen, or source your config file with `source ~/.zshrc`.\n\n#### Windows\n\nI don\'t know of a way to do this other than graphically (Booo!). If you like pictures follow this [tutorial](https://windowsloop.com/add-environment-variable-in-windows-10).\n\n1. Open the Start menu by pressing the “Windows Key”.\n2. Type “Environment variables” and click on the “Edit the system environment variables” result.\n3. Click on the "Advanced" tab.\n4. Click "Environment Variables".\n5. Under "User variables" click "New".\n6. In the "Variable name" field enter: PYBITES_USERNAME\n7. In the "Variable value" field enter: <username>\n8. Repeat steps 5-7 for the password variable.\n9. Click "Ok"\n10. Click "Apply"\n11. Restart your computer.\n',
    'author': 'Russell Helmstedter',
    'author_email': 'rhelmstedter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rhelmstedter/eatlocal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
