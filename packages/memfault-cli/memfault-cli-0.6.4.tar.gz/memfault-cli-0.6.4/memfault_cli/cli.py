import http.client
import logging
import os
from base64 import b64decode
from typing import List, Type

import click

from ._version import version
from .chunk import MemfaultChunk
from .context import MemfaultCliClickContext
from .deploy import Deployer
from .upload import (
    AndroidAppSymbolsUploader,
    AospSymbolDirectoryUploader,
    AospSymbolUploader,
    BugreportUploader,
    CoredumpUploader,
    MarUploader,
    McuSdkElfSymbolUploader,
    ReleaseArtifactUploader,
    Uploader,
    XedUploader,
)

pass_memfault_cli_context = click.make_pass_decorator(MemfaultCliClickContext, ensure=True)
click_argument_path = click.argument("path", type=click.Path(exists=True))
click_option_concurrency = click.option(
    "--concurrency",
    required=False,
    default=8,
    type=int,
    help="Max number of concurrent web requests",
)
click_option_revision = click.option(
    "--revision", help="Revision SHA or # (git, SVN, etc.)", required=False
)


@click.group()
@click.option("--email", help="Account email to authenticate with")
@click.password_option(
    "--password", prompt=False, help="Account password or user API key to authenticate with"
)
@click.option("--project-key", help="Memfault Project Key")
@click.option("--org-token", help="Organization Auth Token")
@click.option("--org", help="Organization slug")
@click.option("--project", help="Project slug")
@click.option("--url", hidden=True)
@click.option("--verbose", help="Log verbosely", is_flag=True)
@click.version_option(version=version)
@pass_memfault_cli_context
def cli(ctx: MemfaultCliClickContext, **kwargs):
    ctx.obj.update(kwargs)

    if ctx.verbose:
        click.echo(f"version: {version}")

        logging.basicConfig(level=logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

        httpclient_logger = logging.getLogger("http.client")
        httpclient_logger.setLevel(logging.DEBUG)

        def httpclient_log(*args) -> None:
            httpclient_logger.log(logging.DEBUG, " ".join(args))

        http.client.print = httpclient_log  # type: ignore[attr-defined]
        http.client.HTTPConnection.debuglevel = 1  # type: ignore[attr-defined]


def _do_upload_or_raise(
    ctx: MemfaultCliClickContext, path: str, uploader_cls: Type[Uploader]
) -> None:
    authenticator = ctx.authenticator
    ctx.check_required_cli_args(authenticator=authenticator)

    uploader = uploader_cls(ctx=ctx, file_path=path, authenticator=authenticator)
    if not uploader.can_upload_file():
        raise click.exceptions.UsageError("Upload failed!")
    uploader.upload()


@cli.command(name="upload-coredump")
@click_argument_path
@pass_memfault_cli_context
def upload_coredump(ctx: MemfaultCliClickContext, path: str):
    """Upload an MCU coredump for analysis.

    Coredumps can be added to an MCU platform by integrating the Memfault C SDK:
    https://github.com/memfault/memfault-firmware-sdk
    """
    _do_upload_or_raise(ctx, path, CoredumpUploader)


@cli.command(name="upload-xed")
@click.option(
    "--hardware-version",
    required=True,
    help="Required for MCU builds, see https://mflt.io/34PyNGQ",
)
@click.option(
    "--device-serial",
    required=True,
    help="The unique identifier of a device",
)
@click.option(
    "--attribute",
    type=click.Tuple([str, str]),
    multiple=True,
    help="""
    Attribute associated with the uploaded file. Multiple attributes can be passed.
    The value argument is attempted to be interpreted as a JSON string first, if that
    fails, the value is interpreted as a string value as-is. Note however that only
    number, boolean, string or null values are allowed (objects and arrays are not allowed).

    Examples:

    Key "my_int" with numeric value 1234:

    --attribute my_int 1234

    Key "my_string" with string value 'hello':

    --attribute my_string hello

    Key "my_bool" with boolean true value:

    --attribute my_bool true
    """,
)
@click_argument_path
@pass_memfault_cli_context
def upload_xed(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload an .xed or .xcd file for analysis."""
    ctx.obj.update(**kwargs)

    _do_upload_or_raise(ctx, path, XedUploader)


@cli.command(name="upload-bugreport")
@click_argument_path
@pass_memfault_cli_context
def upload_bugreport(ctx: MemfaultCliClickContext, path: str):
    """Upload an Android Bug Report for analysis by Memfault."""
    uploader_cls = BugreportUploader
    _do_upload_or_raise(ctx, path, uploader_cls)


@cli.command(name="upload-symbols")
@click.option(
    "--software-type",
    required=False,
    help="Required for MCU builds, see https://mflt.io/34PyNGQ",
)
@click.option(
    "--software-version",
    required=False,
    help="Required for MCU builds, see https://mflt.io/34PyNGQ",
)
@click_option_revision
@click_option_concurrency
@click_argument_path
@pass_memfault_cli_context
def upload_symbols(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """[DEPRECATED] Upload symbols for an MCU or Android build.

    Please use upload-aosp-symbols or upload-mcu-symbols instead!
    """
    ctx.obj.update(**kwargs)

    uploader: Type[Uploader]
    if os.path.isdir(path):
        uploader = AospSymbolDirectoryUploader
    elif ctx.software_info is None:
        uploader = AospSymbolUploader
    else:
        uploader = McuSdkElfSymbolUploader

    _do_upload_or_raise(ctx, path, uploader)


@cli.command(name="upload-mar")
@click.option(
    "--hardware-version",
    required=True,
    help="Required to identify the type of Android hardware, see https://mflt.io/34PyNGQ/#android. By default the ro.product.board property is used.",
)
@click.option(
    "--software-type",
    required=True,
    help="Required to identify the Android system software, see https://mflt.io/34PyNGQ/#android-1",
)
@click.option(
    "--software-version",
    required=True,
    help="Required to identify single builds on Android devices, see https://mflt.io/34PyNGQ/#software-version",
)
@click.option(
    "--device-serial",
    required=True,
    help="The unique identifier of a device",
)
@click_argument_path
@pass_memfault_cli_context
def upload_mar(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload a Memfault Archive File (mar) file for analysis."""
    ctx.obj.update(**kwargs)
    _do_upload_or_raise(ctx, path, MarUploader)


@cli.command(name="upload-mcu-symbols")
@click.option(
    "--software-type",
    required=False,
    help="Required for MCU symbols without Build Id, see https://mflt.io/symbol-file-build-ids",
)
@click.option(
    "--software-version",
    required=False,
    help="Required for MCU symbols without Build Id, see https://mflt.io/symbol-file-build-ids",
)
@click_option_revision
@click_argument_path
@pass_memfault_cli_context
def upload_mcu_symbols(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload symbols for an MCU build.

    Memfault will use the Build Id in the symbol file to identify it and match
    it with data sent by that build. See https://mflt.io/symbol-file-build-ids
    for more information on enabling Build Id in your project.

    In case a Build Id cannot be found in the symbol file, a `--software-type`
    and `--software-version` must be passed. This will then be used as
    identifying information instead of a Build Id.

    Even if a Build Id is available, it is possible to pass a `--software-type`
    and `--software-version`. This will link the symbol file with the specified
    Software Version, which can be useful to easily retrieve the symbol file by
    Software Version through the Memfault UI.

    \b
    Example MCU Symbols Upload:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink \\
            upload-mcu-symbols \\
            build/symbols.elf

    \b
    Example MCU Symbols Upload, associating it with a Software Version:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink \\
            upload-mcu-symbols \\
            --software-type stm32-fw \\
            --software-version 1.0.0-alpha \\
            --revision 89335ffade90ff7697e2ce5238bd4c68978b6d6e \\
            build/symbols.elf
    """
    ctx.obj.update(**kwargs)

    _do_upload_or_raise(ctx, path, McuSdkElfSymbolUploader)


@cli.command(name="upload-aosp-symbols")
@click_option_concurrency
@click_argument_path
@pass_memfault_cli_context
def upload_aosp_symbols(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload symbols for an Android OS/AOSP build.

    \b
    Example AOSP Symbol Upload:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink
            upload-aosp-symbols \\
            out/target/product/generic/symbols

        Reference: https://mflt.io/android-os-symbol-files
    """
    ctx.obj.update(**kwargs)

    uploader: Type[Uploader]
    if os.path.isdir(path):
        uploader = AospSymbolDirectoryUploader
    else:
        uploader = AospSymbolUploader

    _do_upload_or_raise(ctx, path, uploader)


@cli.command(name="upload-android-app-symbols")
@click.option(
    "--build-variant",
    required=True,
    help="The build variant for which to upload the Android app symbols",
)
@click.option(
    "--package",
    required=False,
    help="The package identifier of the app. When not specified, it is read from the .apk",
)
@click.option(
    "--version-name",
    required=False,
    help="The version name of the app. When not specified, it is read from the .apk",
)
@click.option(
    "--version-code",
    required=False,
    help="The version code of the app. When not specified, it is read from the .apk",
)
@click.option(
    "--mapping-txt",
    required=False,
    help="The path to the Proguard/R8 mapping.txt file. When not specified, the default locations are searched.",
)
@click_option_concurrency
@click_argument_path
@pass_memfault_cli_context
def upload_android_app_symbols(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload symbols & R8/ProGuard mapping for an Android app build.

    Pass the root 'build' directory of the Android app as argument, for example:

    memfault upload-android-app-symbols --build-variant=release ~/my/app/build

    The command will automatically try to locate the mapping.txt and extract the
    version and package identifier from the .apk file.

    If this automatic behavior does not work in your use case, consider using
    option flags (i.e. --version-code, --version-name, --package, etc.) to specify
    the required information directly.
    """
    ctx.obj.update(**kwargs)
    uploader: Type[Uploader] = AndroidAppSymbolsUploader
    _do_upload_or_raise(ctx, path, uploader)


@cli.command(name="upload-ota-payload")
@click.option("--hardware-version", required=True)
@click.option("--software-type", required=True)
@click.option(
    "--software-version",
    required=False,
    help="Make the OTA Payload a Full Release payload for this version.",
)
@click.option(
    "--delta-from",
    required=False,
    help="Pass --delta-from FROM_VERSION make the OTA Payload a Delta Release payload from the version FROM_VERSION. Use alongside --delta-to TO_VERSION",
)
@click.option(
    "--delta-to",
    required=False,
    help="Pass --delta-to TO_VERSION to make the OTA Payload a Delta Release payload to version TO_VERSION. Use alongside --delta-from FROM_VERSION.",
)
@click.option("--notes", default="", help="Optional release notes.")
@click.option(
    "--must-pass-through",
    required=False,
    is_flag=True,
    help="When the Release is deployed to a Cohort, forces a device to update through this version even if a newer version has also been deployed to the Cohort.",
)
@click_option_revision
@click_argument_path
@pass_memfault_cli_context
def upload_ota_payload(ctx: MemfaultCliClickContext, path: str, **kwargs):
    """Upload a binary to be used for an OTA update.

    See https://mflt.io/34PyNGQ for details about 'hardware-version',
    'software-type' and 'software-version' nomenclature.

    When deployed, this is the binary that will be returned from the Memfault /latest endpoint
    which can be used for an Over The Air (OTA) update.

    \b
    Example OTA Upload:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink \\
            upload-ota-payload \\
            --hardware-version mp \\
            --software-type stm32-fw \\
            --software-version 1.0.0-alpha \\
            --revision 89335ffade90ff7697e2ce5238bd4c68978b6d6e \\
            build/stm32-fw.bin

    \b
    Example Delta OTA Upload:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink \\
            upload-ota-payload \\
            --hardware-version mp \\
            --software-type stm32-fw \\
            --delta-from 0.9.0 \\
            --delta-to 1.0.0-alpha \\
            --revision 89335ffade90ff7697e2ce5238bd4c68978b6d6e \\
            build/stm32-fw-delta.bin

    Reference: https://mflt.io/create-release
    """
    ctx.obj.update(**kwargs)
    ctx.check_required_either(
        {"software_version"}, {"delta_from", "delta_to"}, mutually_exclusive=True
    )
    _do_upload_or_raise(ctx, path, ReleaseArtifactUploader)


@cli.command(name="deploy-release")
@click.option("--release-version", type=str, required=False)
@click.option("--delta-from", required=False)
@click.option("--delta-to", required=False)
@click.option("--cohort", type=str, required=True)
@click.option(
    "--rollout-percent",
    type=int,
    show_default=True,
    default=100,
    help="The (randomly sampled) percentage of devices in the Cohort to rollout the release to.",
)
@pass_memfault_cli_context
def deploy_release(ctx: MemfaultCliClickContext, cohort: str, rollout_percent: int, **kwargs):
    """Publish a Release to a Cohort.

    \b
    Example Release Deployment:
    \b
        $ memfault --org-token $ORG_TOKEN \\
                   --org acme-inc --project smart-sink \\
                   deploy-release \\
                   --release-version 1.0.0-alpha \\
                   --cohort default
    """
    ctx.obj.update(**kwargs)

    ctx.check_required_cli_args(authenticator=ctx.authenticator)
    ctx.check_required_either(
        {"release_version"}, {"delta_from", "delta_to"}, mutually_exclusive=True
    )
    release_version = ctx.obj.get("release_version") or (
        ctx.obj["delta_from"],
        ctx.obj["delta_to"],
    )
    deployer = Deployer(ctx=ctx, authenticator=ctx.authenticator)
    deployer.deploy(cohort=cohort, release_version=release_version, rollout_percent=rollout_percent)


def _do_post_chunks_or_raise(ctx: MemfaultCliClickContext, chunks: List[bytes]):
    authenticator = ctx.authenticator
    ctx.check_required_cli_args(authenticator=authenticator)
    if not authenticator.project_key_auth():
        raise click.exceptions.UsageError("A '--project-key' is required")

    MemfaultChunk(ctx, authenticator).batch_post(chunks)
    click.echo("Success")


@cli.command("post-chunk")
@click.option("--device-serial", show_default=True, default="TESTSERIAL")
@click.option(
    "--encoding",
    type=click.Choice(["hex", "base64", "bin", "sdk_data_export"]),
    required=True,
    help="The format DATA is encoded in.",
)
@click.argument("data")
@pass_memfault_cli_context
def post_chunk(ctx: MemfaultCliClickContext, encoding, data, **kwargs):
    """Sends data generated by the memfault-firmware-sdk ("chunks") to the Memfault cloud.

    The command can operate on binary data encoded in the following formats:

    \b
    1. Hex String:
      memfault --project-key ${YOUR_PROJECT_KEY} post-chunk --encoding hex 0802a702010301076a5445535453455249414c0a6d746573742d736f667477617265096a312e302e302d74657374066d746573742d686172647761726504a101a1726368756e6b5f746573745f737563636573730131e4

    \b
    2. Base64 Encoded String
      memfault --project-key ${YOUR_PROJECT_KEY} post-chunk --encoding base64 CAKnAgEDAQdqVEVTVFNFUklBTAptdGVzdC1zb2Z0d2FyZQlqMS4wLjAtdGVzdAZtdGVzdC1oYXJkd2FyZQShAaFyY2h1bmtfdGVzdF9zdWNjZXNzATHk

    \b
    3. Binary File
      memfault --project-key ${YOUR_PROJECT_KEY} post-chunk --encoding bin chunk_v2_single_chunk_msg.bin

    \b
    4. memfault-firmware-sdk data export
      memfault --project-key ${YOUR_PROJECT_KEY} post-chunk --encoding sdk_data_export data_export.txt

    Reference: https://mflt.io/chunk-api-integration
    """

    ctx.obj.update(**kwargs)
    if encoding == "hex":
        chunks = [bytes.fromhex(data)]
    elif encoding == "base64":
        chunks = [b64decode(data)]
    elif encoding == "bin":
        with click.open_file(data, "rb") as f:
            chunks = [f.read()]
    elif encoding == "sdk_data_export":
        with click.open_file(data, "r") as f:
            exported_data = f.read()
        chunks = MemfaultChunk.extract_exported_chunks(exported_data)
        if len(chunks) == 0:
            raise click.exceptions.UsageError(f"No Memfault chunks found in {data}")
        click.echo(f"Found {len(chunks)} Chunks. Sending Data ...")

    _do_post_chunks_or_raise(ctx, chunks)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    cli(auto_envvar_prefix="MEMFAULT")


if __name__ == "__main__":
    main()
