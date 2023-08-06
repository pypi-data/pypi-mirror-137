import sys

from nubia import Nubia, Options  # type: ignore
from nubia.internal import context

from ftt.cli.handlers.prepare_environment_handler import (
    PrepareEnvironmentHandler,
)
from ftt.cli.plugin import Plugin


class ENVIRONMENT:
    production = "production"
    development = "development"
    test = "test"


APPLICATION_NAME = "ftt"


class Application:
    @classmethod
    def initialize(cls, test_mode: bool = False) -> None:
        from ftt.cli import commands

        plugin = Plugin()
        shell = Nubia(
            name=APPLICATION_NAME,
            command_pkgs=[commands],
            plugin=plugin,
            options=Options(
                persistent_history=False, auto_execute_single_suggestions=False
            ),
        )
        environment = ENVIRONMENT.test
        if not test_mode:
            opts_parser = plugin.get_opts_parser()
            args, extra = opts_parser.parse_known_args(args=sys.argv)
            if args.dev:
                environment = ENVIRONMENT.development
            elif args.test:
                environment = ENVIRONMENT.test
            else:
                environment = ENVIRONMENT.production

        result = PrepareEnvironmentHandler().handle(
            environment=environment, application_name=APPLICATION_NAME
        )
        cnt = context.get_context()
        cnt.set_environment(environment)

        if result.is_err():
            cnt.console.print(result.unwrap_err())
            exit(1)

        if result.value.first_run:
            cnt.console.print(
                "First run detected, running database structure initialization"
            )

        return shell

    @classmethod
    def initialize_and_run(cls) -> None:
        sys.exit(cls.initialize().run())
