# Software Systems Laboratory Badges

> A `pybadges` interface to create custom badges for each of the Software System Laboratory tracked metrics

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)
[![DOI](https://zenodo.org/badge/406267900.svg)](https://zenodo.org/badge/latestdoi/406267900)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-badges/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-badges/actions/workflows/release.yml)
![[https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](https://img.shields.io/badge/license-BSD--3-yellow)

## Table of Contents

- [Software Systems Laboratory Badges](#software-systems-laboratory-badges)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
    - [Python Software](#python-software)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) JSON Converter Project is an interface into the `pybadges` library's ability to create custom, embedable badges for each of the SSL tracked metrics.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project the following software packages are **required**:

### Operating System

This tool **targets** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to run this tool on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

### Python Software

> The software listed in this section is meant for developing tools

All listed Python software assumes that you have downloaded and installed **Python 3.9.6** or greater.

- `pybadges`

You can install all of the Python software with one of the following one-liners:

- `pip install --upgrade pandas pip pybadges`
- `pip install --upgrade pip -r requirements.txt`

## How To Use

### Installation

You can install the tool from PyPi with one of the following one liners:

- `pip install ssl-metrics-meta`
- `pip install ssl-metrics-badges`

### Command Line Arguements

`ssl-metrics-badeges -h`

```shell
options:
  -h, --help            show this help message and exit
  -g GRAPH, --graph GRAPH
                        The graph SVG file to be the badge logo
  -lc LEFT_COLOR, --left-color LEFT_COLOR
                        Left side color
  -lt LEFT_TEXT, --left-text LEFT_TEXT
                        Text to go on the left side of the badge
  -u LINK, --link LINK  Link to a specific URL that will open when the badge is clicked
  -o OUTPUT, --output OUTPUT
                        The output filename of the badge. NOTE: Must end in .svg
  -rt RIGHT_TEXT, --right-text RIGHT_TEXT
                        Text to go on the left side of the badge
  -rc--right-color RC__RIGHT_COLOR
                        Right side color
  -t TITLE, --title TITLE
                        Title of the badge
```
