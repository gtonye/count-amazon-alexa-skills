# Amazon Alexa Skills Store Counter

## Abstract

> Disclaimer: This is not an Alexa skill

The following repository hosts the codebase for a scrapper that counts the number of Skills available on the skill store.

## Development

#### Requirements

The following are necessary to use the script:
* Python 2.7
* Virtualenv
* [Mozilla firefox Geckodriver](https://github.com/mozilla/geckodriver/releases)

#### Setup

```
# set the geckodriver path in the binaries path
virtualenv .env
source ./env/bin/activate
pip install -r requirements.txt
```

#### Run

```
python count_amazon_skills.py
```

## Description

The code currently uses the amazon.com, and the logic follows the structure of that page.
On the Skill store home, the scrapper will click on the available categories and search for the number of result per category.

## Foreword

#### License

This code is yours.

```
The MIT License (MIT)
Copyright (c) 2018-present gtonye

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

#### F[ea|u]ture

Pull requests are more than welcomed. some of the things that would make this script even better:
* support other regions where scripts are available
* aggregate the count over the regions
