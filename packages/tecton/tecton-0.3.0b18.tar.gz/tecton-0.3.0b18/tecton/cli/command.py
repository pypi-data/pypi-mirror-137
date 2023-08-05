import functools
import sys
from typing import Optional

import click
import pendulum

from tecton._internals.analytics import AnalyticsLogger
from tecton.cli import common
from tecton.cli import printer

analytics = AnalyticsLogger()


def _cluster_url() -> Optional[str]:
    from tecton import conf

    api_service = conf.get_or_none("API_SERVICE")
    if api_service:
        # API_SERVICE URLs of the form <subdomain>.tecton.ai/api are expected so this check
        # ensures an internal DNS address isn't being used or an invalid path is specified.
        if api_service.endswith("/api") and "ingress" not in api_service:
            return api_service[: -len("/api")]
        else:
            printer.safe_print(f"Warning: CLI is configured with non-standard URL: {api_service}", file=sys.stderr)
            return None
    else:
        return None


class TectonCommand(click.Command):

    # used by integration tests
    skip_config_check = False

    """Base class for Click which implements required_auth and uses_workspace behavior, as well as analytics."""

    def __init__(self, *args, callback, requires_auth=True, uses_workspace=False, **kwargs):
        @functools.wraps(callback)
        @click.pass_context
        def wrapper(ctx, *cbargs, **cbkwargs):
            host = _cluster_url()
            cluster_configured = host is not None

            command_names = []
            cur = ctx
            # The top level context is `cli` which we don't want to include.
            while cur:
                command_names.append(cur.command.name)
                cur = cur.parent
            command_names.reverse()

            # Do not try logging events if cluster has never be configured or if user is trying to log in,
            # otherwise the CLI either won't be able to find the MDS or auth token might have expired
            if cluster_configured:
                if uses_workspace:
                    printer.safe_print(f'Using workspace "{common.get_current_workspace()}" on cluster {host}')
                start_time = pendulum.now("UTC")
                state_update_event = ctx.invoke(callback, *cbargs, **cbkwargs)
                execution_time = pendulum.now("UTC") - start_time
                if requires_auth:
                    if state_update_event:
                        # TODO: Include sub-command?
                        analytics.log_cli_event(command_names[1], execution_time, state_update_event)
                        if state_update_event.error_message:
                            sys.exit(1)
                    else:
                        analytics.log_cli_event(command_names[1], execution_time)
            elif not requires_auth or TectonCommand.skip_config_check:
                # Do not try executing anything besides unauthenticated commnds (`login`, `version`) when cluster hasn't been configured.
                state_update_event = ctx.invoke(callback, *cbargs, **cbkwargs)
            else:
                printer.safe_print(
                    f"`{' '.join(command_names)}` requires authentication. Please authenticate using `tecton login`."
                )
                sys.exit(1)

        super().__init__(*args, callback=wrapper, **kwargs)


class TectonGroup(click.Group):
    """Routes group.command calls to use TectonCommand instead of the base Click command"""

    command_class = TectonCommand


TectonGroup.group_class = TectonGroup
