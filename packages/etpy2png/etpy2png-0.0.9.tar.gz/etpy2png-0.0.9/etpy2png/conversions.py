import subprocess
import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Zunächst zwei globale Konstanten als Jupyter-Notebook Vorlage:

NOTEBOOK_1 = """
{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "dbu1337",
   "metadata": {},
   "source": [
    "```python\\n",
"""

NOTEBOOK_2 = """
    "```"
]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
"""

def convert_py2ipynb(file):
    """
    Konvertiert ein Python-File in eine Jupyter-Notebook. Das Notebook enthält eine Markdownzelle mit dem Code
    als Python-Codeblock für das Syntaxhighlighting.
    
    Parameter:
    ---------
    file: Pfad zum Python-File. Mit .py-Endung.
    
    Anmerkung: Es wird auf die globalen Konstanten zugegriffen
    """
    with open(file.replace("py", "ipynb"), mode = "w", encoding="utf-8") as fout:
        with open(file, encoding="utf-8") as fin:
            fout.write(NOTEBOOK_1)
            
            for nummer, zeile in enumerate(fin, start=1):
                fout.write("    " + f'"{nummer}'.ljust(5) + zeile.replace("\n","\\n").replace('"', '\\"') + '",\n')
            # Einrückung zu Beginn für Leserlichkeit.
            # Anführung fürs Dateiformat, eigenständig Zeilennummerierung hinzuschreiben per f-String und auf 5 Zeichen padden
            # Aus der eingelesenen Zeile werden Zeilenumbrüche und Anführungszeichen mit Escapezeichen versehen
            # Für das Dateiformat mit Anführungszeichen und Komma enden

            fout.write(NOTEBOOK_2)

def convert_ipynb2html(file):
    """
    Konvertiert ein Jupyter-Notebook in HTML und legt es in den gleichen Ordner.
    Verwendet nbconvert als CLI-Tool. Daher ist Jupyter Installationsvoraussetzung in der aktiven Umgebung.
    
    Parameter:
    ---------
    file: Pfad zum Notebook-File. Mit .ipynb-Endung.
    """
    # Suche zunächst den Ordner der aktiven Python-Umgebung
    py_path = os.path.dirname(sys.executable)
   
    # Unterscheidungen, ob das Modul in einer Venv installiert wurde
    if py_path.endswith("Scripts"):
        jupyter_path = py_path
    else:
        jupyter_path = os.path.join(py_path, "Scripts")
    
    # Das CLI-Kommando für die Konvertierung 
    cmd = f"{jupyter_path}\\jupyter-nbconvert \"{file}\" --to html"
    subprocess.run(cmd)

def convert_html2png(file):
    """
    Nimmt einen Screenshot aus dem relevanten Teil des HTMLs auf und legt ihn in den gleichen Ordner.
    Verwendet Selenium und den Firefox-Geckodriver. Daher ist Selenium Installationsvoraussetzung in der
    aktiven Umgebung.

    Paramter:
    --------
    file: Pfad zum HTML-file. Mit .html-Endung.
    """
    # Keine GUI-Variante des Browsers muss aufpoppen
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')

    # Öffnen des Browsers und Zugriff auf die HTML-Datei
    HERE = os.path.abspath(os.path.dirname(__file__))
    DRIVER_PATH = os.path.join(HERE, "driver", "geckodriver.exe")

    browser=webdriver.Firefox(executable_path=DRIVER_PATH, options=options)
    html = os.path.join(os.getcwd(), file)
    browser.get(os.path.abspath(html))
    
    # Kurzes Warten, damit eine eingeblendete Mathjax-Loading Nachricht im Browser verschwindet
    time.sleep(1)

    # Lokalisierung des entscheidenden Elements
    notebook = browser.find_element(By.CLASS_NAME, 'jp-Notebook')
    code_cell = notebook.find_elements(By.XPATH,"*")[1]
    cell_wrapper = code_cell.find_elements(By.XPATH,"*")[0]
    cell_area = cell_wrapper.find_elements(By.XPATH,"*")[1]
    input_area = cell_area.find_elements(By.XPATH,"*")[1]

    # Screenshot erstellen und Browser schließen
    input_area.screenshot(file.replace("html", "png"))
    browser.quit()   
    
def check_pfad(file):
    """
    Prüft, ob Umlaute im Ordnerpfad oder Filenamen enthalten sind. 
    Sollte dies der Fall sein, kann das HTML nicht im Browser geöffnet werden.

    Parameter:
    ---------
    file: Pfad zum Python-File. Mit .py-Endung.
    """
    
    html_datei = os.path.abspath(os.path.join(os.getcwd(), file.replace(".py"), ".html"))
    umlaute = "ÄÜÖßäüö"
    if any([x in html_datei for x in umlaute]):
        raise FileNotFoundError("Dateinamen und Ordnerpfad dürfen keine Umlaute beinhalten!")


def convert(file):
    """
    Verknüpfung aller Umwandlungen.

    Parameter:
    ---------
    file: Pfad zum Python-File. Mit .py-Endung.
    """
    # Umlaute sind im File-Namen fürs HTML nicht erlaubt
    check_pfad(file)

    convert_py2ipynb(file)
    convert_ipynb2html(file.replace("py", "ipynb"))
    convert_html2png(file.replace("py", "html"))



