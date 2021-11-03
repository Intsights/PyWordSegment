<p align="center">
    <a href="https://github.com/intsights/pywordsegment">
        <img src="https://raw.githubusercontent.com/intsights/pywordsegment/master/images/logo.png" alt="Logo">
    </a>
    <h3 align="center">
        Concatenated-word segmentation Python library written in Rust
    </h3>
</p>


![license](https://img.shields.io/badge/MIT-License-blue)
![Python](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)
![OS](https://img.shields.io/badge/OS-Mac%20%7C%20Linux%20%7C%20Windows-blue)
![Build](https://github.com/intsights/pywordsegment/workflows/Build/badge.svg)
[![PyPi](https://img.shields.io/pypi/v/pywordsegment.svg)](https://pypi.org/project/pywordsegment/)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
  - [Built With](#built-with)
  - [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)


## About The Project

A fast concatenated-word segmentation library written in Rust, inspired by [wordninja](https://github.com/keredson/wordninja) and [wordsegment](https://github.com/grantjenks/python-wordsegment). The binding uses [pyo3](https://github.com/PyO3/pyo3) to interact with the rust package.


### Built With

* [pyo3](https://github.com/PyO3/pyo3)


### Installation

```sh
pip3 install pywordsegment
```


## Usage

```python
import pywordsegment

# The internal UNIGRAMS & BIGRAMS corpuses are lazy initialized
# once per the whole module. Multiple WordSegmenter instances would
# not create new dictionaries.

# Segments a word to its parts
pywordsegment.WordSegmenter.segment(
    text="theusashops",
)
# ["the", "usa", "shops"]


# This function checks whether the substring exists as a whole segment
# inside text.
pywordsegment.WordSegmenter.exist_as_segment(
    substring="inter",
    text="internationalairport",
)
# False

pywordsegment.WordSegmenter.exist_as_segment(
    substring="inter",
    text="intermilan",
)
# True
```


## License

Distributed under the MIT License. See `LICENSE` for more information.


## Contact

Gal Ben David - gal@intsights.com

Project Link: [https://github.com/intsights/pywordsegment](https://github.com/intsights/pywordsegment)
