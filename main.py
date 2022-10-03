import click
import commands
import config


@click.group()
@click.version_option(version="0.0.1", prog_name="passm")
def app():
    pass


@click.group(name="create")
def create():
    pass


@click.group("get")
def get():
    pass


@click.command()
@click.password_option(prompt="Enter a Secret Key")
def setup(password):
    config.create_setup(password)


create.add_command(commands.create_password)
create.add_command(commands.create_advance_password)
create.add_command(commands.create_template)

get.add_command(commands.get_apps)
get.add_command(commands.get_details)
get.add_command(commands.get_password)

app.add_command(setup)
app.add_command(create)
app.add_command(get)

app.add_command(commands.save_quick)
app.add_command(commands.save_default)
app.add_command(commands.export)

if __name__ == "__main__":
    app()
