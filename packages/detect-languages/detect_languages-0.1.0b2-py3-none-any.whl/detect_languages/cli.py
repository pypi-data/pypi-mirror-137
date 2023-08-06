from typing import List

import click
from tabulate import tabulate

from detect_languages.detect import DetectLanguages


@click.group()
def cli():
    pass

debug_option = click.option("--debug/--no-debug", "-d", default=False, help="Debug", show_default=True)
path_option = click.option("--path", "-p", type=click.Path(exists=True), default=".", help="Path to project", show_default=True)
language_types_option = click.option("--language-types", "-lt", multiple=True, default=["programming", "prose", "data", "markup"], help="Language types", show_default=True)
exclude_dirs_option = click.option("--exclude-dirs", "-ed", multiple=True, default=[], help="Exclude dirs", show_default=True)
exclude_dirs_recursively_option = click.option("--exclude-dirs-recursively/--no-exclude-dirs-recursively", "-edr", default=False, help="Exclude dirs recursively", show_default=True)
output_option = click.option("--output", "-o", type=click.Choice(["json", "tabulate"]), default="tabulate", help="Output format", show_default=True)


@cli.command()
@debug_option
@path_option
@language_types_option
@exclude_dirs_option
@exclude_dirs_recursively_option
@output_option
def main(debug: bool, path: str, language_types: List[str], exclude_dirs: List[str], exclude_dirs_recursively: bool, output: str):
    detect_languages = DetectLanguages(debug, path, language_types, exclude_dirs, exclude_dirs_recursively)
    if output == "tabulate":
        headers = ["Language", "Size B", "Percentage %"]
        values = [[detect_languages.main_language, *detect_languages.all_languages[detect_languages.main_language].values()]]
        click.echo(tabulate(values, headers=headers, tablefmt="fancy_grid"))
    else:
        main_language = {detect_languages.main_language: detect_languages.all_languages[detect_languages.main_language]}
        click.echo(main_language)


@cli.command()
@debug_option
@path_option
@language_types_option
@exclude_dirs_option
@exclude_dirs_recursively_option
@output_option
def all(debug: bool, path: str, language_types: List[str], exclude_dirs: List[str], exclude_dirs_recursively: bool, output: str):
    detect_languages = DetectLanguages(debug, path, language_types, exclude_dirs, exclude_dirs_recursively)
    if output == "tabulate":
        headers = ["Language", "Size B", "Percentage %"]
        values = [[language, *inner.values()] for language, inner in detect_languages.all_languages.items()]
        click.echo(tabulate(values, headers=headers, tablefmt="fancy_grid"))
    else:
        click.echo(detect_languages.all_languages)


if __name__ == "__main__":
    cli()
