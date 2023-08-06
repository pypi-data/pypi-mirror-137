#!/usr/bin/env python
import argparse
import os
import random
import sys
import tempfile
import time
from typing import Text, Tuple, List, Optional

import click
import progressbar
from pydantic import BaseModel

from cnside import metadata, errors
from cnside.authenticator import Authenticator, AuthenticatorConfig, OAUTHToken
from cnside.cli import APIClient, APIClientConfig
from cnside.cli.core import PrintColors, execute_cli_parsed_command, execute_subprocess_popen_command
from cnside.cli.documents import AnalyzeRequestDoc, CLIParsedCommand
from cnside.errors import FailedToLoadToken, FailedToRefreshToken, LockfileNotFoundError, ManifestNotFoundError, \
    LockfileGenerateFailed, TerminateRequest
from cnside.storage import StorageHandlerConfig, StorageHandler
from cnside.storage.handlers import ManifestData


class Joker:
    def __init__(self):
        self.colors = PrintColors()

    def ill_let_myself_out(self):
        if not random.randint(0, 1000):
            time.sleep(1)
            self.colors.point_warning("ENCRYPTING ALL YOUR COMPUTER FILES!")
            time.sleep(3)
            self.colors.point_fail("SYKE!!! THE FILE ENCRYPTION MODE IS DISABLED. 😑")
            time.sleep(1)
            self.colors.point("TIP: To enable file encryption mode run 'cnside --enable-encrypt-my-file'")


class Messages:
    LOGGED_IN = ""
    LOGGED_OUT = ""
    TOKEN_LOAD_FAILED = "Failed to load token."
    AUTH_REQUIRED = "Authentication required. Please run: 'cnside illustria auth'."
    UNHANDLED_AUTH_ERROR = "Unhandled authentication error."
    UNHANDLED_REQUEST_ERROR = "Unhandled package request error."
    LIBRARY_REJECTED = "LIBRARY REJECTED"
    LIBRARY_APPROVED = "LIBRARY APPROVED"
    FAILED_REFRESH_TOKEN = "Failed to refresh authentication token."


class CLIConfig(BaseModel):
    cnside_base_url: Text = "https://cnside.illustria.io"
    cnside_npm_repo: Text = "https://repo.illustria.io/repository/cnside_npm_hosted/"
    cnside_pypi_repo: Text = "https://repo.illustria.io/repository/cnside_pypi_hosted/simple"
    auth_url: Text = "https://illustria.frontegg.com/oauth/authorize"
    token_url: Text = "https://illustria.frontegg.com/oauth/token"
    client_id: Text = "cf890130-015c-41b0-bd3d-ea03fa393b41"
    # max_attempts: Optional[int] = 500
    request_interval: Optional[int] = 3


class CLIInterface:
    def __init__(self, config: CLIConfig):
        self.colors = PrintColors()
        self.config = config

        self.storage_handler = StorageHandler(StorageHandlerConfig())
        self.authenticator = Authenticator(
            config=AuthenticatorConfig(auth_url=config.auth_url, token_url=config.token_url,
                                       storage_handler=self.storage_handler, client_id=self.config.client_id)
        )

        self._npm_lockfile_generate_command = ["npm", "i", "--package-lock-only"]
        self._v2_package_managers = [
            metadata.packages.PackageManagers.NPM,
            metadata.packages.PackageManagers.YARN
        ]

    @staticmethod
    def parse_cli_arguments() -> CLIParsedCommand:
        """
        Provides script interface for end user.

        """
        # todo: build a hierarchical parser for all commands
        parser = argparse.ArgumentParser(description="cnside (see-inside) is the secure package manager wrapper by "
                                                     "illustria. for more information please visit "
                                                     "https://illustria.io.")
        parser.add_argument("--skip-install", help="Skip installation when package approved", action='store_true')
        parser.add_argument("--examine-all", help="Examine the whole lockfile and not only diffs", action='store_true')
        parser.add_argument("manager", help="package manager (supported: pip, npm, illustria)")
        parser.add_argument("action", help="action (install, auth)")
        parser.add_argument('arguments', nargs=argparse.REMAINDER)
        # parser.add_argument('-v', '--version', action='version', version='')
        args = parser.parse_args()
        cli_command = CLIParsedCommand(package_manager=args.manager, action=args.action, arguments=args.arguments,
                                       skip_install=args.skip_install)
        return cli_command

    def run(self, command: CLIParsedCommand):
        skip_install: bool = command.skip_install
        examine_all: bool = command.examine_all

        if command.package_manager == "illustria":
            index = {
                "auth": self.authenticator.authenticate
            }
            index[command.action]()
        else:
            # Analyze
            self.analyze_environment(command=command)

            # Preprocess Dependency Tree
            data, resolved_data = self.preprocess_package_resolution(command=command)

            # Set request variables
            analyzer_version = 2 if command.package_manager in self._v2_package_managers else 1

            # Generate request documents and request from illustria
            # TODO: set project name: https://gitlab.com/illustria/cnside-cli/-/issues/6
            request_document = AnalyzeRequestDoc(
                package_manager=command.package_manager,
                packages=command.packages,
                install_manifest=command.install_manifest,
                manifest=data.manifest,
                lockfile=data.lockfile,
                resolved_lockfile=resolved_data.lockfile,
                analyzer_version=analyzer_version
            )

            if examine_all:
                request_document.lockfile = None

            approved, failed_checks = self.request_packages(request_document=request_document)

            if approved:
                self.colors.point_ok(Messages.LIBRARY_APPROVED)
            else:
                self.colors.point("Issues Found:")
                for i in failed_checks:
                    if i:
                        for b in i:
                            self.colors.point(
                                f"{b['upid_str']} - "
                                f"{b['policy_id'].split('-')[0]} - "
                                f"{b['policy_category']} - "
                                f"{b['policy_rule_id']} - "
                                f"{b['failed_labels']}"
                            )

                self.colors.point_fail(Messages.LIBRARY_REJECTED)

            self.colors.header("Installation")
            if skip_install:
                self.colors.point("Skipping Installation (--skip_install)")
            else:
                install = click.confirm("[Q] Would you like to install packages?", default=True if approved else False)

                if install:
                    self.colors.point("Installing packages (Using package manager).")
                    std_out, std_err = execute_cli_parsed_command(command=command)
                    self.colors.point("Package manager output:")
                    for line in std_out:
                        self.colors.out_data(line)

                    for line in std_err:
                        self.colors.err_data(line)

                    self.colors.point_ok("INSTALLED. (Please Verify Output)")
                else:
                    self.colors.point("Skipping installation.")
                    self.colors.point_fail("INSTALL ABORTED")

            self.colors.footer("FINISHED")

    def gen_api_client(self):
        token = self.load_token()
        config = APIClientConfig(
            base_url=self.config.cnside_base_url,
            headers={"Authorization": f"{token.token_type} {token.access_token}"}
        )
        api_client = APIClient(config=config)
        return api_client

    def _generate_npm_package_lock_json(self):

        _, std_err = execute_subprocess_popen_command(command=self._npm_lockfile_generate_command)
        if std_err:
            raise LockfileGenerateFailed(
                command=self._npm_lockfile_generate_command,
                suggestion=["npm", "i", "--package-lock-only", "--legacy-peer-deps"],
                caution="If install command is needed to solve the issue, make sure to skip download by appending "
                        "'--package-lock-only' to the command.",
                std_err=std_err
            )

    def _generate_lock_file(self, package_manager: Text):
        generators_index = {
            metadata.packages.PackageManagers.NPM: self._generate_npm_package_lock_json
        }

        generators_index[package_manager]()

    def _npm_temp_dir_package_resolution(self, data: ManifestData, command: CLIParsedCommand) -> ManifestData:
        with tempfile.TemporaryDirectory(prefix="cnside") as temp_dir_path:

            npm_init_command = ["npm", "init", "-y"]
            npm_install_command = ["npm", "i", "--package-lock-only"]
            manifest_path = os.path.join(temp_dir_path, metadata.packages.ManifestNames.get(command.package_manager))
            lockfile_path = os.path.join(temp_dir_path, metadata.packages.LockfileNames.get(command.package_manager))

            # Building the installation command
            for upid in command.packages:
                npm_install_command.append(upid.pm_repr())

            # Saving manifest and lockfile if they exist or generating them if needed.
            if data.manifest:
                with open(manifest_path, "w+") as fp:
                    fp.write(data.manifest)
            else:
                execute_subprocess_popen_command(npm_init_command, cwd=temp_dir_path)

            if data.lockfile:
                with open(lockfile_path, "w+") as fp:
                    fp.write(data.lockfile)

            # Resolving tree
            execute_subprocess_popen_command(npm_install_command, cwd=temp_dir_path)

            resolved_data = self.storage_handler.manifest.get(package_manager=command.package_manager,
                                                              base_dir=temp_dir_path)

            # Instead of validating Popen output we just make sure that the files have been generated.
            # TODO: turn into a custom error.
            assert all([resolved_data.manifest, resolved_data.lockfile]), "Failed to resolve dependencies"

        return resolved_data

    def preprocess_package_resolution(self, command: CLIParsedCommand) -> Tuple[ManifestData, ManifestData]:
        """
        Resolves the tree for analyzer version 2 package managers.

        :param command:
        :return:
        """
        self.colors.header("Resolving Dependency Tree")
        data = self.storage_handler.manifest.get(package_manager=command.package_manager)

        if all([command.package_manager in self._v2_package_managers, command.packages]):
            self.colors.point("Using: Temporary directory for dependency resolution.")
            # Create temp directory, save the manifest and lockfile in there, resolve the tree and request it.
            resolved_data = self._npm_temp_dir_package_resolution(data=data, command=command)
        else:
            resolved_data = data

        self.colors.point_ok("Dependency Tree Resolved!")

        return data, resolved_data

    def analyze_environment(self, command: CLIParsedCommand):
        self.colors.header("Analyzing Command & Environment")
        try:
            # Load and evaluate manifest and lockfile data. They both must exist for package resolution to work
            # correctly when requesting a package from illustria cloud in analyzer_mode version 2. In order to
            # prevent any package name or version discrepancy between what illustria is checking and what the client
            # is receiving, the whole package resolution must happen within the client itself. This is done by
            # generating a lockfile is a manifest file exists.
            manifest_data = self.storage_handler.manifest.get(package_manager=command.package_manager)

            # validating that the manifest exists if the user asked to install it.
            if command.install_manifest and not manifest_data.manifest:
                raise ManifestNotFoundError(
                    f"Manifest install requested but no manifest file found ({manifest_data.manifest_name}).")

            # Setting lockfile_exists as true for package managers that have no lockfile.
            lockfile_exists = True \
                if command.package_manager in metadata.packages.LockfileNames.non_lockfile_managers() \
                else manifest_data.lockfile

            # Generating a lockfile if there is a manifest and the lockfile doesn't exist - with users' permission.
            if all([manifest_data.manifest, not lockfile_exists]):
                self.colors.point_warning_prefix(f"Lockfile not found: {manifest_data.lockfile_name}")
                self.colors.point("Lockfile needed to continue...")
                if click.confirm(
                        f"[Q] Would you like us to generate a lockfile for you? ({manifest_data.lockfile_name})",
                        default=True):
                    try:
                        self.colors.point("Generating a lock file...")
                        self._generate_lock_file(command.package_manager)
                        self.colors.point("Lockfile generated!")
                    except LockfileGenerateFailed as e:
                        self.colors.point_fail(
                            f"Error: Failed to generate a lockfile, using this command: '{' '.join(e.command)}'")
                        for line in e.std_err:
                            self.colors.err_data(line)
                        self.colors.point_warning(f"NOTICE!: {e.caution}")
                        sys.exit()
                else:
                    self.colors.point_warning(
                        "Caution: Generating a lockfile by yourself might result in packages being downloaded. It "
                        "is best to let us do it for you.")
                    raise LockfileNotFoundError()

            self.colors.point_ok("Command & Environment OK!")

        except (ManifestNotFoundError, LockfileNotFoundError) as e:
            self.colors.point_fail_prefix(f"Error: {e}")
            sys.exit()
        except Exception as e:
            raise e

        return manifest_data

    def request_packages(self, request_document: AnalyzeRequestDoc) -> Tuple[bool, List]:
        try:
            self.colors.header("Requesting packages from CNSIDE System")
            # generating request document

            api_client = self.gen_api_client()

            self.colors.point(f"Analyzer Version: {request_document.analyzer_version}")
            if request_document.analyzer_version == 1:
                self.colors.point(f"Packages: {request_document.packages}")

            try:
                # requesting to analyze package
                try:
                    analyze_response_doc = api_client.post_analyze_request(request_document=request_document)
                except errors.api.TokenExpired:
                    api_client.close()

                    try:
                        token = self.authenticator.load_token()
                        token = self.authenticator.refresh_token(token=token)
                        self.storage_handler.token.save(token)
                    except FailedToRefreshToken:
                        self.colors.point_fail(Messages.FAILED_REFRESH_TOKEN)
                        self.colors.point_fail(Messages.AUTH_REQUIRED)
                        sys.exit()

                    api_client = self.gen_api_client()
                    analyze_response_doc = api_client.post_analyze_request(request_document=request_document)

                # handling check status
                # todo: https://gitlab.com/illustria/cnside-cli/-/issues/9
                workflow_id = analyze_response_doc.workflow_id

                approved = False
                failed_checks = []

                finished = False
                bar_initiated = False
                bar: progressbar.ProgressBar

                self.colors.point("Waiting for request analysis (this might take a few seconds)")
                while not finished:
                    time.sleep(self.config.request_interval)

                    data = api_client.get_analyze_status(workflow_id=workflow_id)
                    if data.status == "PROCESSING":
                        if not bar_initiated:
                            self.colors.point(f"Total packages requested: {data.total_packages}")
                            self.colors.point(f"New packages to process: {data.new_packages}")
                            self.colors.point("Processing...")
                            bar = progressbar.ProgressBar(
                                maxval=data.total_stages,
                                widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()],
                                fd=sys.stdout
                            )
                            bar.start()
                            bar_initiated = True

                        # noinspection PyUnboundLocalVariable
                        bar.update(data.total_stages - data.remaining_stages)
                    if data.status == "COMPLETED":
                        if bar_initiated:
                            bar.update(data.total_stages - data.remaining_stages)
                            bar.finish()
                        approved = data.accepted
                        failed_checks = data.failed_checks
                        finished = True

                api_client.close()

                return approved, failed_checks

            except errors.api.RemoteServerError as e:
                self.colors.point_fail(f"Error: Remote Server Error:\n\tStatus Code: {e.data.status_code}")
                raise TerminateRequest()
            except Exception as e:
                raise e
            finally:
                api_client.close()

        except (KeyboardInterrupt, TerminateRequest):
            sys.exit()
        except Exception as e:
            self.colors.point_fail(Messages.UNHANDLED_REQUEST_ERROR)
            self.colors.point_fail(e)
            sys.exit()

    def load_token(self) -> OAUTHToken:
        try:
            token = self.authenticator.load_token()
        except FailedToLoadToken:
            self.colors.point_fail(Messages.TOKEN_LOAD_FAILED)
            self.colors.point_fail(Messages.AUTH_REQUIRED)
            sys.exit()
        except Exception as e:
            self.colors.point_fail(Messages.UNHANDLED_AUTH_ERROR)
            self.colors.point_fail(e)
            sys.exit()

        return token


def main():
    cli_interface = CLIInterface(config=CLIConfig())
    command = cli_interface.parse_cli_arguments()
    cli_interface.run(command=command)


# todo: add report error functionality - when error happens
# todo: save to config file


if __name__ == '__main__':
    main()
