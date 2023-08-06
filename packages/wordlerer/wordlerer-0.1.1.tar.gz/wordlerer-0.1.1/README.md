# Wordlerer

Wordlerer can automatically solve wordle puzzle in the browser.

## Installation

```shell
pip install wordlerer
```

## Usage

### Browser app

```shell
brew install --cask firefox
brew install geckodriver
```

```python
from wordlerer import BrowserApp

BrowserApp().run()
```

### CLI app

```python
from wordlerer import App

App().run()
```
