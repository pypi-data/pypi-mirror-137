# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rigol_ds1000z']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.11.3,<2.0.0', 'matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.2,<2.0.0']

entry_points = \
{'console_scripts': ['rigol-ds1000z = scripts.cli:main']}

setup_kwargs = {
    'name': 'rigol-ds1000z',
    'version': '0.1.0',
    'description': 'Python library for interfacing with Rigol DS1000Z series oscilloscopes.',
    'long_description': '# rigol-ds1000z\n\nPython library for interfacing with Rigol DS1000Z series oscilloscopes.\n\nThis package differs from the alternatives by:\n1. Flattening the communication interface with the test equipment so that code can be written in a more compact form.\n2. Providing a command line interface for easy display and waveform data capture.\n\nThis package strives to maintain the verbiage used in the [Rigol DS1000Z programming manual](https://beyondmeasure.rigoltech.com/acton/attachment/1579/f-0386/1/-/-/-/-/DS1000Z_Programming%20Guide_EN.pdf) as closely as possible. Aside from basic type-casting, command arguments are not validated and instrument responses are not post-processed. Separate utility routines are provided for post-processing display and waveform data.\n\nA function call will send commands associated with the arguments provided and a data structure is always returned with the queried values that belong under that function\'s domain. Not all interfaces are fully implemented. The basic write, read, and query commands are provided for the user to use in the abscense of a functional interface.\n\nAll commands are issued once at a time with a wait after instruction appended. The autoscale and IEEE reset commands enforce a ten and five second sleep respectively to avoid a VISA serial communication timeout or other odd behavior.\n\nExtensive hardware testing has been performed with a Rigol DS1054Z oscilloscope.\n\nInspired by similar packages iteratively developed by [@jtambasco](https://github.com/jtambasco/RigolOscilloscope), [@jeanyvesb9](https://github.com/jeanyvesb9/Rigol1000z), and [@AlexZettler](https://github.com/AlexZettler/Rigol1000z).\n\n## Usage\n\nThis package is available on [PyPI](https://pypi.org/): `pip install rigol-ds1000z`.\n\nThe command line interface saves to file a display capture or waveform data from a Rigol DS1000Z series oscilloscope. The first valid VISA address identified is utilized by default.\n\n```shell\nrigol-ds1000z --help\nrigol-ds1000z --display path/to/file.png\nrigol-ds1000z --waveform src path/to/file.csv\n```\n\nExample code is shown below and also provided as part of this repository. See the status section for the summary of the implemented functional interfaces or browse the generated documentation [here](https://htmlpreview.github.io/?https://github.com/amosborne/rigol-ds1000z/blob/main/docs/rigol_ds1000z/index.html).\n\n```python\nfrom rigol_ds1000z import Rigol_DS1000Z\nfrom rigol_ds1000z import find_visa, process_display, process_waveform\n\n# find visa address\nvisa = find_visa()\n\nwith Rigol_DS1000Z(visa) as oscope:\n    # run and autoscale\n    oscope.run()\n    oscope.autoscale()\n\n    # reset, self-test, return queried ieee values\n    ieee = oscope.ieee(rst=True, tst=True)\n    print(ieee.idn)\n\n    # configure channels, return queried channel values\n    ch2 = oscope.channel(2, probe=10, coupling="AC", bwlimit=True)\n    ch3 = oscope.channel(3, display=True)\n    print(ch2.scale, ch3.scale)\n\n    # send SCPI command to clear the display\n    oscope.write(":DISP:CLE")\n\n```\n\n## Status\n\nThe following SCPI commands are implemented as functional interfaces:\n- All base-level commands (ex. `AUT`, `RUN`, `STOP`).\n- All IEEE488.2 common commands (ex. `IDN?`, `*RST`, `TST?`).\n- All channel commands (ex. `:CHAN1:PROB`).\n- All timebase commands (ex. `:TIM:MOD`, `:TIM:DEL:SCAL`).\n- All waveform commands (ex. `:WAV:SOUR`, `:WAV:DATA?`).\n- The display data query `:DISP:DATA?`.\n\n## Development Notes\n\n- Package management by [Poetry](https://python-poetry.org/).\n- Automated processing hooks by [pre-commit](https://pre-commit.com/).\n- Code formatting in compliance with [PEP8](https://www.python.org/dev/peps/pep-0008/) by [isort](https://pycqa.github.io/isort/), [black](https://github.com/psf/black), and [flake8](https://gitlab.com/pycqa/flake8).\n- Static type checking in compliance with [PEP484](https://www.python.org/dev/peps/pep-0484/) by [mypy](http://www.mypy-lang.org/).\n- Test execution with random ordering and code coverage analysis by [pytest](https://docs.pytest.org/en/6.2.x/).\n- Automated documentation generation by [pdoc](https://github.com/pdoc3/pdoc).\n\nInstalling the development environment requires running the following command sequence.\n\n```shell\npoetry install\npoetry run pre-commit install\n```\n\nIn order for all tests to pass, an oscilloscope must be connected and channel 2 must be connected to the calibration square wave.\n',
    'author': 'amosborne',
    'author_email': 'amosborne@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amosborne/rigol-ds1000z',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
