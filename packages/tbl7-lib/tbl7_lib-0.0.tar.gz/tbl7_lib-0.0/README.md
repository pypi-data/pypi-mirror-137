# Initial version of my own package: 
I created this first version by following this article: 
https://towardsdatascience.com/make-your-own-python-package-6d08a400fc2d


#####Onderstaande is slecht er voorbeeld:

# Cmotions Readability package

a package with functionality to help performing NLP tasks regarding the analysis of the readability of a text

## How does it work?

We want to help anyone who has written a text to help to analyze the readability of this text. Where readability is defined as how easy it is to read and interpret the text. This package contains all data preparation steps needed to clean an input text, furthermore it also contains the possibility to retrieve a trained model and use this on the cleaned input text.

## Instructions

The easiest way to install this package and to easily update it in the future is to use pip.

```bash
pip install --upgrade git+https://deploy-token-cmotions-readability:y93tyysvzyZ-_UD4xxBG@gitlab.com/cmotions/ProjectFriday_TextFacts_Readability.git@production
```

## Development

When you develop new features please directly add accompanying tests in order for the package to stay robust, and for
better code. Also, when you make changes to the current codebase always run the tests afterwards to make sure you did
not break something. If you come across unexpected behaviour of the code, edge cases, or other related incidents during
development please add these directly to the test suite.
You can run the tests locally using the following command:

```bash
python -m pytest tests/ --verbose
```

### CI Pipeline

Please note that the tests, in the future, will also be part of the CI pipeline of this project (`gitlab-ci.yml`). If you're changes fail to
pass the tests, they cannot be merged with the `development` or the `production` branch.