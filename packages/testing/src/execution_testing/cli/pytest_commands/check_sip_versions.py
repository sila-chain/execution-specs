"""CLI entry point for the SIP version checker pytest-based command."""

from typing import Any, List

import click

from .base import PytestCommand, common_pytest_options
from .processors import HelpFlagsProcessor


@click.command(context_settings={"ignore_unknown_options": True})
@common_pytest_options
def check_sip_versions(pytest_args: List[str], **kwargs: Any) -> None:
    """Run pytest with the `spec_version_checker` plugin."""
    del kwargs

    command = PytestCommand(
        config_file="pytest-check-sip-versions.ini",
        argument_processors=[HelpFlagsProcessor("check-sip-versions")],
    )
    command.execute(list(pytest_args))
