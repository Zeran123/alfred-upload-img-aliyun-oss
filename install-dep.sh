#!/bin/bash
pip install --target=. Alfred-Workflow
pip install --target=./lib oss2

# install pngpaste
brew install pngpaste
cp /usr/local/bin/pngpaste .