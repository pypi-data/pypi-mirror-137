# ✉️💣 LetterBomb

<p align="center">

<h3>A fork of the classic Wii hacking tool from <a href="https://github.com/fail0verflow">fail0verflow</a>.</h3>

<a href="https://gitlab.com/whoatemybutter/letterbomb"><img src="https://i.imgur.com/llzHJiw.png" width="250" align="center"/></a>

<a href="https://gitlab.com/whoatemybutter/letterbomb/-/pipelines"><img src="https://img.shields.io/gitlab/pipeline/whoatemybutter/letterbomb/master?label=ci%2Fcd&style=for-the-badge"></a>
<a href="https://letterbomb.rtfd.io"><img src="https://img.shields.io/readthedocs/letterbomb?style=for-the-badge"></a>
<a href="https://pypi.org/project/letterbomb"><img src="https://img.shields.io/pypi/dd/letterbomb?style=for-the-badge"></a>
<a href="https://pypi.org/project/letterbomb"><img src="https://img.shields.io/pypi/v/letterbomb?style=for-the-badge"></a>

</p>

## Table of Contents

- [Installation](#installation)
    - [PyPi](#pypihttpspypiorgprojectletterbomb-recommended)
    - [Manual](#manual-development)
- [Improvements](#improvements-over-original)
- [Images](#images)
- [Usage](#usage)
    - [Python](#python)
    - [CLI](#cli)
- [Documentation](#documentation)
- [Original source code](#original-source-code)
- [License](#license)

## Installation

#### [PyPi](https://pypi.org/project/letterbomb): **(recommended)**
```shell script
python3 -m pip install -U letterbomb
```

#### Manual: **(development)**
```shell script
git clone https://gitlab.com/whoatemybutter/letterbomb.git
cd letterbomb
python setup.py build
python setup.py install
```

## Improvements over original

|                   | *WhoAteMyButter's*  | fail0verflow's          |
|-------------------|---------------------|-------------------------|
| Networking        | Optional            | Required                |
| CLI               | Yes                 | No                      |
| OS support        | *nix, Windows, Mac  | *nix                    |
| Logging           | Yes, Flask, logging | Yes, dependent on Flask |
| Exceptions        | Yes                 | No                      |
| Packaging         | Gitlab, PyPi        | Git                     |
| Dependencies      | None (Flask for web)| Flask, geoip2           |
| Pylint            | 10.00/10.00         | 4.65/10.00              |
| Python version    | 3.6+                | 2.7 only                |
| License           | GPLv3+              | MIT                     |
| Documentation     | Sphinx, docstrings  | No                      |

## Images

<img src="https://i.imgur.com/B1Wb2uo.png" width=500 height=500 />
<img src="https://i.imgur.com/LjZh24c.png" width=500 height=500 />
<img src="https://i.imgur.com/SCh2cJV.png" width=500 height=500 />
<img src="https://i.imgur.com/YYG9XnU.png" width=500 height=500 />
<img src="https://i.imgur.com/yNqJJsT.png" width=500 height=500 />
<img src="https://i.imgur.com/CmDyovg.png" width=500 height=500 />

## Usage

#### Python:

```pythonstub
# -*- coding: utf-8 -*-
import letterbomb

# Write to file, include BootMii:
letterbomb.write_zip(mac="mac address", region="region letter", pack_bundle=True, output_file="letterbomb.zip")
# Write to file, exclude BootMii:
letterbomb.write_zip(mac="mac address", region="region letter", pack_bundle=False, output_file="letterbomb.zip")

# Write to stream, include BootMii:
letterbomb.write_stream(mac="mac address", region="region letter", pack_bundle=True)
# Write to stream, exclude BootMii:
letterbomb.write_stream(mac="mac address", region="region letter", pack_bundle=True)

# To log debug messages
letterbomb.LOGGING_LEVEL = letterbomb.logging.DEBUG
# To log output to a file
letterbomb.LOGGING_FILE = "log.txt"
```

#### CLI:

```shell script
# Help
python3 -m letterbomb -h

# To include BootMii
python3 -m letterbomb mac_address region -b

# To enable logging debug
python3 -m letterbomb mac_address region -g debug

# To use a file for logging output
python3 -m letterbomb mac_address region -l logfile.txt

# To stream bytes instead, include BootMii
python3 -m letterbomb mac_address region -b -i

# To stream bytes instead, useful for piping
python3 -m letterbomb mac_address region -i
```

## Documentation

**Most casual users should refer to the [ReadTheDocs page](https://letterbomb.rtfd.io).**

Some may want to build the documentation manually. To do this:

```shell script
git clone https://gitlab.com/whoatemybutter/letterbomb.git
cd letterbomb/docs
make html
xdg-open _build/html/index.html
```

If you prefer one-liners, there is one below:

```shell script
git clone https://gitlab.com/whoatemybutter/letterbomb.git && cd letterbomb/docs && make html && xdg-open _build/html/index.html
```

Before re-building the documentation, you should also run `make clean` to prevent stale files from remaining in newer builds.

To read about the exploit itself in more detail, please [read this article](https://wiibrew.org/wiki/LetterBomb).

## Original source code

* The *original* source code can be found at https://github.com/fail0verflow/letterbomb.
* The *original* website can be found at https://please.hackmii.com.

**Note:** *Original code likely will not work out-of-the-box.*

## License

Letterbomb is licensed under [GPLv3+](https://www.gnu.org/licenses/gpl-3.0.txt). ([included file](https://gitlab.com/whoatemybutter/letterbomb/-/raw/master/LICENSE.txt))
