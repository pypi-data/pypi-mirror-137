from typing import List
import click, textwrap
from pathlib import Path

import slxpy.common.constants as C

@click.group()
@click.option('--debug', is_flag=True, help="Enable debug mode.")
@click.option('--workdir', '-w', default=".", type=click.Path(file_okay=False, resolve_path=True, path_type=Path), help="Working directory, must be empty or nonexistent. (Default to cwd)")
@click.pass_context
def app(ctx: click.Context, workdir: Path, debug: bool):
    ctx.ensure_object(dict)
    ctx.obj["workdir"] = workdir
    ctx.obj["DEBUG"] = debug
    click.echo(f"Working directory: {workdir}")

@app.command()
@click.pass_context
def init(ctx: click.Context):
    """
    Initialize slxpy working directory.
    """
    workdir: Path = ctx.obj["workdir"]

    from slxpy.frontend.init import init_interactive
    init_interactive(workdir)

@app.command()
@click.pass_context
def frontend(ctx: click.Context):
    """
    Execute slxpy frontend.
    Transform simulink metadata and user config into IR.
    """
    workdir: Path = ctx.obj["workdir"]
    ensure_slxpy_project(workdir)

    click.echo("Execute frontend.", nl=False)
    from slxpy.frontend.frontend import adapt_metadata
    adapt_metadata(workdir)
    click.secho(" SUCCESS", fg="green")

@app.command()
@click.pass_context
def backend(ctx: click.Context):
    """
    Execute slxpy backend.
    Transform IR into binding code and build scripts.
    """
    workdir: Path = ctx.obj["workdir"]
    DEBUG: bool = ctx.obj["DEBUG"]
    ensure_slxpy_project(workdir)

    click.echo("Execute backend.", nl=False)
    from slxpy.backend.renderer import render
    render(workdir, DEBUG)
    click.secho(" SUCCESS", fg="green")

@app.command()
@click.option('--build', is_flag=True, help="Also build the project.")
@click.pass_context
def generate(ctx: click.Context, build: bool):
    """
    Execute slxpy frontend and backend.
    Produce a self-contained, portable source project.
    """
    workdir: Path = ctx.obj["workdir"]
    ensure_slxpy_project(workdir)

    ctx.invoke(frontend)
    ctx.invoke(backend)
    if build:
        import subprocess, sys, distutils.util
        args = [sys.executable, "setup.py", "build"]
        click.echo(f"Run \"{' '.join(args)}\" to build extension.")
        cp = subprocess.run(args, cwd=workdir)
        cp.check_returncode()
        plat_name = distutils.util.get_platform()
        # Ported from distutils/command/build.py
        plat_specifier = f".{plat_name}-{sys.version_info.major}.{sys.version_info.minor}"
        libdir = workdir / "build" / f"lib{plat_specifier}"
        click.echo(f"\nBuild successful. Check {libdir} for output.")
    else:
        output_text = textwrap.dedent(f"""\
        To build the extension, run in command line:
            > cd "{workdir}"
            > python setup.py build
        """).strip()
        click.echo(output_text)

@app.command()
@click.option('--all', is_flag=True, help="Complete cleanup, keeping config files only.")
@click.pass_context
def clean(ctx: click.Context, all: bool):
    """
    Clean up working directory.
    """
    workdir: Path = ctx.obj["workdir"]
    ensure_slxpy_project(workdir)

    import shutil
    def rmdir(dir: Path):
        if dir.exists():
            assert dir.is_dir()
            shutil.rmtree(dir)
            click.echo(f"Remove folder: {dir.relative_to(workdir)}")
        else:
            click.echo(f"Skip folder:   {dir.relative_to(workdir)}")
    
    def rmfile(file: Path):
        if file.exists():
            assert file.is_file()
            file.unlink()
            click.echo(f"Remove file:   {file.relative_to(workdir)}")
        else:
            click.echo(f"Skip file:     {file.relative_to(workdir)}")

    rmdir(workdir / "build")
    rmdir(workdir / "include")

    from slxpy.backend.renderer import assets
    generated_files: List[str] = [asset["name"] for asset in assets] + [C.project_ir_name]
    for f in generated_files:
        rmfile(workdir / f)
    
    if all:
        rmdir(workdir / "model")
        rmfile(workdir / C.metadata_name)

@app.command()
@click.option('--build/--no-build', default=False, help="With build folder.")
@click.option('--asset/--no-asset', default=True, help="Without slxpy generated assets.")
@click.option('--model/--no-model', default=True, help="Without Simulink mdoel sources.")
@click.option('--out', default=None, type=click.Path(dir_okay=False, resolve_path=True, path_type=Path), help="Output zip file name.")
@click.pass_context
def pack(ctx: click.Context, build: bool, asset: bool, model: bool, out: Path):
    """
    Pack assets for transfer.
    """
    workdir: Path = ctx.obj["workdir"]
    ensure_slxpy_project(workdir)

    if out is None: out = Path(f"{workdir.name}.zip")
    parentdir = workdir.parent
    import zipfile, glob

    def writedir(z: zipfile.ZipFile, dir: Path):
        assert dir.exists(), f"Folder not exist: {dir.relative_to(workdir)}"
        assert dir.is_dir()
        for p in dir.glob("**/*"):
            if p.is_dir(): continue
            z.write(p, arcname=p.relative_to(parentdir))
        click.echo(f"Add folder: {dir.relative_to(workdir)}")
    def writefile(z: zipfile.ZipFile, file: Path):
        assert file.exists(), f"File not exist: {file.relative_to(workdir)}"
        assert file.is_file()
        z.write(file, arcname=file.relative_to(parentdir))
        click.echo(f"Add file:   {file.relative_to(workdir)}")

    try:
        with zipfile.ZipFile(out, mode="w", compression=zipfile.ZIP_LZMA) as z:
            writefile(z, workdir / C.model_config_name)
            writefile(z, workdir / C.env_config_name)
            if model:
                writedir(z, workdir / C.model_dir)
            if asset:
                from slxpy.backend.renderer import assets
                writedir(z, workdir / "include")
                generated_files: List[str] = [asset["name"] for asset in assets] + [C.project_ir_name]
                for f in generated_files:
                    writefile(z, workdir / f)
            if build:
                writedir(z, workdir / "build")
    except:
        out.unlink()
        raise

def ensure_slxpy_project(workdir: Path):
    # Safe check except init subcommand
    if not (workdir / C.model_config_name).exists() or not (workdir / C.env_config_name).exists():
        raise Exception("Not a slxpy project directory.")

def entry_point():
    try:
        app()
    except Exception as e:
        click.secho(str(e), fg="red", err=True)
        raise
        

if __name__ == '__main__':
    entry_point()
