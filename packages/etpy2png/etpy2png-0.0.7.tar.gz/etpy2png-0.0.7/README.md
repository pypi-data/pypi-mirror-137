# etpy2png

Package to convert .py Code-Files to .png with Code-Highlighting. 

Writes .py to Markdown in .ipynb and uses jupyter-nbconvert to convert to html with Code Highlighting (via pygments). Runs Selenium to capture a screenshot of the located html-element.

## Usage
```python
from etpy2png import convert

file = "sample.py"
convert(file)
```
