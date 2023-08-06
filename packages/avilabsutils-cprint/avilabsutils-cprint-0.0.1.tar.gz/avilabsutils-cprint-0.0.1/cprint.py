from collections import namedtuple
from typing import List, Optional

import click

Style = namedtuple("Style", ["fg", "bg"])

COLORS = [
    Style(fg=[245, 120, 66], bg=None),
    Style(fg=[132, 245, 66], bg=None),
    Style(fg=[66, 138, 245], bg=None),
    Style(fg=[108, 66, 245], bg=None),
    Style(fg=[245, 66, 161], bg=None),
    Style(fg=[203, 66, 245], bg=None),
    Style(fg=[66, 245, 218], bg=None),
    Style(fg=[245, 218, 66], bg=None),
]


def cprint(color_idx: int, text: str, colors: Optional[List[Style]] = None):
    colors = colors or COLORS
    cidx = color_idx % len(colors)
    click.secho(text, fg=colors[cidx].fg, bg=colors[cidx].bg)


def info_print(text: str) -> None:
    click.secho(text, fg=[66, 135, 245])


def success_print(text: str) -> None:
    click.secho(text, bg=[66, 245, 147], fg="bright_white")


def danger_print(text: str) -> None:
    click.secho(text, bg=[245, 66, 66], fg="bright_white")


def warning_print(text: str) -> None:
    click.secho(text, bg=[245, 132, 66], fg="bright_white")
