from linguadoc import LinguaDoc
import click
import hashlib
import os
import json

@click.command()
@click.option("--sourcejson", prompt="source json file path", help="Specify the source json file path")
@click.option("--lang", prompt="language", help="Specify the language")
@click.option("--destdocx", prompt="destination docx file path", help="Specify the docx file path")
@click.option("--title", default="test", help="Specify doc title")
def gen_lingua_docx(sourcejson, lang, destdocx, title):
  phase = {"step": 1, "msg": "Start doc generation"}
  print(json.dumps(phase))

  doc = LinguaDoc(sourcejson, lang)
  doc.gen_doc(title, destdocx)

  phase = {"step": 2, "msg": "Finish doc generation"}
  print(json.dumps(phase))

