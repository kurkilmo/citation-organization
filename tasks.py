from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def test(ctx):
    ctx.run("pytest src", pty=True)
    ctx.run("robot src", pty=True)
    # pty pistää värit takas päälle, ilman ei tuu väriä
