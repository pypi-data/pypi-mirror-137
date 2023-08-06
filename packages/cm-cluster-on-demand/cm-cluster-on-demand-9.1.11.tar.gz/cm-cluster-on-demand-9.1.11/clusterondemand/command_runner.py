# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, print_function

import logging
import pdb
import string
import sys
from itertools import chain

from clusterondemand import tracing
from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandconfig import (
    UnknownCLIArgumentError,
    UnknownConfigFileParameterError,
    check_for_unknown_config_parameters,
    determine_invoked_command,
    explain_parameter,
    global_configuration,
    human_readable_config_dump,
    load_boot_configuration_for_command,
    load_configuration_for_command,
    print_help,
    print_help_for_positionals_missing_required_value,
    print_help_for_unknown_parameters,
    validate_configuration
)
from clusterondemandconfig.exceptions import ConfigLoadError

from . import accept_eula
from .configuration import get_enforcing_config_files, get_system_config_files
from .import_utils import load_module_attribute
from .setup_logging import setup_logging, temporarily_logging_all_statements_to_syslog
from .utils import setup_signal_handlers
from .version import print_version_info

log = logging.getLogger("cluster-on-demand")


def run_invoked_command(
        command_context,
        additional_included_config_files=None,
        additional_system_config_files=None):
    """Pass the control to the appropriate tool, specified in 'name' argument.

    Handles the exception, and stack trace printing
    """
    setup_logging()

    with temporarily_logging_all_statements_to_syslog(log):
        log.debug(" ".join(sys.argv))

    non_ascii_chars_used = _check_for_non_ascii_chars_in_arguments()

    # FIXME: clusterondemandconfig doesn't allow us to have this in a clean way
    if "--version" in sys.argv and len(sys.argv) == 2:
        print_version_info()
        sys.exit(0)

    system_config_files = get_system_config_files(additional_included_config_files, additional_system_config_files)
    enforcing_config_files = get_enforcing_config_files()
    (command, clean_sys_argv) = determine_invoked_command(command_context)
    try:
        with sys_argv(clean_sys_argv):
            boot_configuration = load_boot_configuration_for_command(command)

            with global_configuration(boot_configuration):
                configuration = load_configuration_for_command(
                    command, system_config_files=system_config_files, enforcing_config_files=enforcing_config_files
                )
                if configuration["check_config"]:
                    _check_for_unknown_config_parameters(configuration,
                                                         system_config_files=system_config_files,
                                                         enforcing_config_files=enforcing_config_files,
                                                         parameters=command.parameters)

    except UnknownCLIArgumentError as e:
        print_help_for_unknown_parameters(command, e.flags)
        sys.exit(1)
    except CODException as e:
        _log_cod_exception(e)
        sys.exit(1)

    try:
        if non_ascii_chars_used and configuration["only_ascii_arguments"]:
            raise UserReportableException("Aborting because of a non-ASCII character in an argument. You can use "
                                          "'--no-only-ascii-arguments' to ignore this error.")

        if configuration["help"] or configuration["advanced_help"]:
            print_help(command, configuration)
        elif configuration["explain"]:
            explain_parameter(command, command_context, configuration["explain"])
        elif configuration["show_configuration"]:
            print(human_readable_config_dump(configuration, show_secrets=configuration["show_secrets"]))
        elif configuration.required_positionals_with_missing_values():
            print_help_for_positionals_missing_required_value(command, configuration)
            sys.exit(1)
        elif command.require_eula and not accept_eula.user_accepts_eula(configuration):
            sys.exit(1)
        else:
            try:
                validate_configuration(configuration)
                configuration.lock()
            except RuntimeError as e:
                print(e)
                sys.exit(1)
            setup_signal_handlers()
            with global_configuration(configuration):
                command_name = command.group.name + " " + command.name
                with tracing.trace_events(command_name):
                    command.run_command()
    except UserReportableException as e:
        _post_mortem(configuration)
        _log_user_reportable_exception(e)

        sys.exit(1)
    except (ConfigLoadError, CODException) as e:
        _post_mortem(configuration)
        _log_cod_exception(e)
        # TODO If it's useful, CODException could contain the error code
        sys.exit(1)
    except Exception as e:
        _post_mortem(configuration)
        # TODO Notify us that this happened somehow
        log.error("Unhandled exception")
        # TODO (CM-23030) Replace the next lines for `raise e` in future
        if not configuration["verbose"]:
            log.error("(use '-v' to show the stack trace)")
        log.debug(e, exc_info=True)
        log.error("%s: %s" % (e.__class__.__name__, e))
        sys.exit(1)


def _check_for_non_ascii_chars_in_arguments():
    found = False

    for arg in sys.argv:
        if not all(char in string.printable for char in arg):
            found = True
            log.warning("Argument '{argument}' contains a non-ASCII character. This might cause "
                        "unforeseen behavior.".format(argument=arg))

    return found


def _check_for_unknown_config_parameters(configuration, system_config_files, enforcing_config_files,
                                         parameters=None):
    def load_module_parameters(module_name, commands_name):
        commands = load_module_attribute(module_name, commands_name)
        return [] if commands is None else commands.parameters()

    check_all_commands = configuration["check_config_for_all_commands"]
    if parameters is None or check_all_commands:
        aws_parameters = load_module_parameters("clusterondemandaws.cli", "aws_commands")
        azure_parameters = load_module_parameters("clusterondemandazure.cli", "azure_commands")
        openstack_parameters = load_module_parameters("clusterondemandopenstack.cli", "openstack_commands")
        vmware_parameters = load_module_parameters("clusterondemandvmware.cli", "vmware_commands")
        parameters = chain(aws_parameters, azure_parameters, openstack_parameters, vmware_parameters)

    try:
        check_for_unknown_config_parameters(
            parameters,
            system_config_files=system_config_files,
            enforcing_config_files=enforcing_config_files,
            ignore_unknown_namespaces=not check_all_commands,
        )
    except UnknownConfigFileParameterError:
        raise CODException("Some configuration files have problems. Use --no-check-config"
                           " to disable this check.")


def _post_mortem(configuration):
    if configuration["pdb_on_error"]:
        pdb.post_mortem()


def _log_cod_exception(exception):
    log.debug(exception, exc_info=True)
    if getattr(exception, "caused_by", None):
        log.debug("Caused by: %s \n %s", exception.caused_by, exception.caused_by_trace)
    log.error(str(exception))


def _log_user_reportable_exception(exception):
    log.debug(exception, exc_info=True)
    # We have to show "UserReportableException: " here because that's how the portal identifies the error message
    log.error("UserReportableException: %s" % (exception))


def _determine_thing_to_explain(configuration):
    index = sys.argv.index("--explain")

    if configuration["explain"]:
        return configuration["explain"][0]
    elif index == len(sys.argv) - 1:
        return None
    elif "--" == sys.argv[1 + index]:
        return None
    else:
        return sys.argv[1 + index]


class sys_argv(object):
    """Temporarily replace the contents of sys.argv with the given string."""
    def __init__(self, new_argv):
        self.new_argv = new_argv.strip().split(" ") if isinstance(new_argv, str) else new_argv

    def __enter__(self):
        self.old_argv, sys.argv = sys.argv, self.new_argv

    def __exit__(self, _exception_type, _exception_value, _traceback):
        sys.argv = self.old_argv

    def __call__(self, func):
        def wrapper(_self, *args, **kwargs):
            with self:
                return func(_self, *args, **kwargs)
        return wrapper
