import click
import yaml
import pathlib
from notebook import notebookapp
filepaths = notebookapp.jupyter_config_path()

@click.command()
@click.option('--name', '-n', prompt="Name of the connection")
@click.option('--hostname', '-h', prompt="Hostname of your openBIS instance")
@click.option('--verfiy/--no-verify', default=True, prompt="Verify server certificate")
@click.option('--https/--no-https', default=True, prompt="Use secure connection?")
@click.option('--username', '-u', default='', prompt="Username to connect to the openBIS instance")
@click.option('--password', '-p', default='', prompt="Password to connect to the openBIS instance")
@click.option('--destination', '-d', type=click.Choice(filepaths), show_default=True, default=filepaths[0], prompt="Destination where you want to store the configuration")
@click.pass_context
def cli(ctx, name=None, hostname=None, verfiy=True, https=True, username=None, password=None, destination=None):
    """Generate an openBIS connection file for use in Jupyter notebooks.
    """

    config_filepath = pathlib.Path(destination) / 'openbis-connections.yaml'
    if config_filepath.exists():
        if not click.confirm(f"A configuration file already exists in {config_filepath}. Do you want to overwrite?"):
            ctx.exit(code=0)

    connection = {
        "name"                : name,
        "url"                 : hostname,
        "verify_certificates" : verfiy, 
    }
    if username: connection['username'] = username
    if password: connection['password'] = password
    if not https: connection['http_only'] = True
    
    template = {}
    template['connections'] = [connection]

    yaml_object = yaml.dump(template)
    with open(config_filepath, "w") as outfile:
        outfile.write(yaml_object)
    print(f"sample openBIS connection file written to {config_filepath}")

if __name__ == '__main__':
    cli()
