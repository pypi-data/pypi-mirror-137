import os
import typer
from .utils.aws import get_matching_s3_keys, s3resource, s3client
from humanize import naturalsize
import tqdm
from typing import Optional
from .count import app as count
from .size import app as size

app = typer.Typer(add_completion=False)
app.add_typer(count, name="count")
app.add_typer(size, name="size")
# TODO: enable verbose mode globally...

@app.command()
def download(bucket: str, destination: str, prefix: Optional[str] = typer.Argument("")):
    if not os.path.isdir(os.path.dirname(destination)):
        os.makedirs(os.path.dirname(destination))
    f = open(destination, 'ab+')
    keys = []
    total_size = 0
    for obj in s3resource.Bucket(bucket).objects.filter(Prefix=prefix):
        keys.append(obj.key)
        total_size += obj.size
    typer.echo(f"found {len(keys)} matching keys")
    typer.echo(f"downloading {naturalsize(total_size)} of data")
    progress = tqdm.tqdm(unit="MB", total=len(keys))
    # TODO: multiprocess the request to get the objects
    for key in keys:
        obj = s3client.get_object(Bucket=bucket,Key=key)
        data = obj['Body'].read()
        f.write(data)
        progress.update(len(data)/1024/1024)
    f.close()

def cli():
  app()
