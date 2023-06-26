from pathlib import Path
from typing import *

from typer import Argument, Option, Context

from .app import app
from .renderer import Renderer


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    invoke_without_command=True,
)
def render(
    ctx: Context,
    template_path: Path = Argument(..., help="Template path"),
    output_path: Path = Argument(..., help="Output path"),

    extensions: List[str] = Option(["j2", "jinja2", "jinja"], help="List of templete extensions"),
    case_sensitive: bool = Option(True, help="Case sensitive"),
    
    use_env: bool = Option(False, help="Use env variables"),
    env_prefix: str = Option("", help="Env prefix"),
    
    vars_path: Path = Option(None, help="Data path"),
    section: str = Option(None, help="Vars sections"),
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
        extensions=extensions,
        case_sensitive=case_sensitive,
        use_env=use_env,
        env_prefix=env_prefix,
        vars_path=vars_path,
        section=section,
        output_path=output_path,
    )

    return renderer.render(**cli_data)
