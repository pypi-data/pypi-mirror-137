import typer
import os
import sys
from .utils.aws import get_matching_s3_keys
from typing import Optional

app = typer.Typer()

@app.command()
def lines(path: str):
  """ counts number of lines in an object """
  if os.path.isfile(path):
    count = sum(1 for line in open(path))
    typer.echo(f"{count}")
    return
  typer.echo(f"{path} is not valid")
  sys.exit(1)

@app.command()
def keys(bucket: str, prefix: Optional[str] = typer.Argument("")):
  """ counts number of keys in a bucket by prefix """
  count = 0
  for key in get_matching_s3_keys(bucket, prefix):
      count += 1
  typer.echo(f"{count}")
