"""
The boilerplate implementation of an application
"""
import sys
from typing import Type
from common.config import Config
from .app_base import ApplicationBase


def application_entrypoint(application_class: Type[ApplicationBase], config: Config):
    """
    The main entry point of the application.
    """
    # Parses the CLI arguments, and merge them into the configuration
    config.apply_cli_args(sys.argv[1:])

    if config.get("DUMP_CONFIG"):
        config.dump()

    # Create an application instance
    app = application_class(config)

    # Run the application until a shutdown signal arrives
    app.run()
