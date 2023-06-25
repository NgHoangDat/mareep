from pathlib import Path
from typing import *

from typer import Argument, Option, Context

from .app import app
from .renderer import Renderer


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def render(
    ctx: Context,
    template_path: Path = Argument(..., help="Template path"),
    output_path: Path = Argument(..., help="Output path"),
    data_path: Path = Option(None, "--data", "-d", help="Data path"),
    case_sensitive: bool = Option(True, help="Case sensitive"),
):
    cli_data = {}
    key = None
    val = None
    for extra_arg in ctx.args:
        if extra_arg.startswith("--d"):
            if val is not None:
                cli_data[key] = val

            key = extra_arg[3:]
            val = None
            continue

        val = f"{val} {extra_arg}" if val is not None else extra_arg

    if key is not None and val is not None:
        cli_data[key] = val

    renderer = Renderer(
        template_path=template_path,
        output_path=output_path,
        data_path=data_path,
        case_sensitive=case_sensitive,
    )

    return renderer.render(**cli_data)
