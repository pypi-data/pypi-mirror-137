import logging

from pubtools.pluggy import task_context, pm

from .signature_remover import SignatureRemover
from .quay_client import QuayClient
from .untag_images import untag_images
from .utils.misc import (
    setup_arg_parser,
    add_args_env_variables,
    send_umb_message,
    get_internal_container_repo_name,
)

LOG = logging.getLogger("pubtools.quay")

CLEAR_REPO_ARGS = {
    ("--repositories",): {
        "help": "External repositories to clear as CSV.",
        "required": True,
        "type": str,
    },
    ("--quay-org",): {
        "help": "Quay organization in which repositories reside.",
        "required": True,
        "type": str,
    },
    ("--quay-api-token",): {
        "help": "OAuth token for Quay REST API.",
        "required": False,
        "type": str,
        "env_variable": "QUAY_API_TOKEN",
    },
    ("--quay-user",): {
        "help": "Username for Quay login.",
        "required": True,
        "type": str,
    },
    ("--quay-password",): {
        "help": "Password for Quay. Can be specified by env variable QUAY_PASSWORD.",
        "required": False,
        "type": str,
        "env_variable": "QUAY_PASSWORD",
    },
    ("--pyxis-server",): {
        "help": "Pyxis service hostname",
        "required": True,
        "type": str,
    },
    ("--pyxis-ssl-crtfile",): {
        "help": "Path to .crt file for the SSL authentication",
        "required": True,
        "type": str,
    },
    ("--pyxis-ssl-keyfile",): {
        "help": "Path to .key file for the SSL authentication",
        "required": True,
        "type": str,
    },
    ("--send-umb-msg",): {
        "help": "Flag of whether to send a UMB message",
        "required": False,
        "type": bool,
    },
    ("--umb-url",): {
        "help": "UMB URL. More than one can be specified.",
        "required": False,
        "type": str,
        "action": "append",
    },
    ("--umb-cert",): {
        "help": "Path to the UMB certificate for SSL authentication.",
        "required": False,
        "type": str,
    },
    ("--umb-client-key",): {
        "help": "Path to the UMB private key for accessing the certificate.",
        "required": False,
        "type": str,
    },
    ("--umb-ca-cert",): {
        "help": "Path to the UMB CA certificate.",
        "required": False,
        "type": str,
    },
    ("--umb-topic",): {
        "help": "UMB topic to send the message to.",
        "required": False,
        "type": str,
        "default": "VirtualTopic.eng.pub.quay_clear_repositories",
    },
}


def construct_kwargs(args):
    """
    Construct a kwargs dictionary based on the entered command line arguments.

    Args:
        args (argparse.Namespace):
            Parsed command line arguments.

    Returns (dict):
        Keyword arguments for the 'clear_repositories' function.
    """
    kwargs = args.__dict__

    # in args.__dict__ unspecified bool values have 'None' instead of 'False'
    for name, attributes in CLEAR_REPO_ARGS.items():
        if attributes["type"] is bool:
            bool_var = name[0].lstrip("-").replace("-", "_")
            if kwargs[bool_var] is None:
                kwargs[bool_var] = False

    # some exceptions have to be remapped
    kwargs["umb_urls"] = kwargs.pop("umb_url")

    return kwargs


def verify_clear_repo_args(send_umb_msg, umb_urls, umb_cert):
    """
    Verify the presence and correctness of input parameters.

    Args:
        send_umb_msg (bool):
            Whether to send UMB messages about the untagged images.
        umb_urls ([str]):
            AMQP broker URLs to connect to.
        umb_cert (str):
            Path to a certificate used for UMB authentication.
    """
    if send_umb_msg:
        if not umb_urls:
            raise ValueError("UMB URL must be specified if sending a UMB message was requested.")
        if not umb_cert:
            raise ValueError(
                "A path to a client certificate must be provided when sending a UMB message."
            )


def clear_repositories(
    repositories,
    quay_org,
    quay_api_token,
    quay_user,
    quay_password,
    pyxis_server,
    pyxis_ssl_crtfile,
    pyxis_ssl_keyfile,
    send_umb_msg=False,
    umb_urls=[],
    umb_cert=None,
    umb_client_key=None,
    umb_ca_cert=None,
    umb_topic="VirtualTopic.eng.pub.quay_clear_repositories",
):
    """
    Clear Quay repository.

    Args:
        repository (str):
            External repositories to clear. Comma separated values.
        quay_org (str):
            Quay organization in which repositories reside.
        quay_api_token (str):
            OAuth token for authentication of Quay REST API.
        quay_user (str):
            Quay username for Docker HTTP API.
        quay_password (str):
            Quay password for Docker HTTP API.
        pyxis_server (str):
            Pyxis service hostname:
        pyxis_ssl_crtfile (str):
            Path to .crt file for SSL authentication.
        pyxis_ssl_keyfile (str):
            Path to .key file for SSL authentication.
        send_umb_msg (bool):
            Whether to send UMB messages about the untagged images.
        umb_urls ([str]):
            AMQP broker URLs to connect to.
        umb_cert (str):
            Path to a certificate used for UMB authentication.
        umb_client_key (str):
            Path to a client key to decrypt the certificate (if necessary).
        umb_ca_cert (str):
            Path to a CA certificate (for mutual authentication).
        umb_topic (str):
            Topic to send the UMB messages to.
    """
    parsed_repositories = repositories.split(",")
    verify_clear_repo_args(send_umb_msg, umb_urls, umb_cert)

    LOG.info("Clearing repositories '{0}'".format(repositories))
    quay_client = QuayClient(quay_user, quay_password)

    sig_remover = SignatureRemover()
    sig_remover.set_quay_client(quay_client)

    refrences_to_remove = []
    for repository in parsed_repositories:
        sig_remover.remove_repository_signatures(
            repository,
            quay_org,
            pyxis_server,
            pyxis_ssl_crtfile,
            pyxis_ssl_keyfile,
        )

        internal_repo = "{0}/{1}".format(quay_org, get_internal_container_repo_name(repository))
        repo_data = quay_client.get_repository_tags(internal_repo)

        for tag in repo_data["tags"]:
            refrences_to_remove.append("{0}/{1}:{2}".format("quay.io", internal_repo, tag))

    untag_images(
        sorted(refrences_to_remove),
        quay_api_token,
        remove_last=True,
        quay_user=quay_user,
        quay_password=quay_password,
        send_umb_msg=send_umb_msg,
        umb_urls=umb_urls,
        umb_cert=umb_cert,
        umb_client_key=umb_client_key,
        umb_ca_cert=umb_ca_cert,
    )

    LOG.info("Repositories have been cleared")
    pm.hook.quay_repositories_cleared(repository_ids=sorted(parsed_repositories))

    if send_umb_msg:
        LOG.info("Sending a UMB message")
        props = {"cleared_repositories": parsed_repositories}
        send_umb_message(
            umb_urls,
            props,
            umb_cert,
            umb_topic,
            client_key=umb_client_key,
            ca_cert=umb_ca_cert,
        )


def setup_args():
    """Set up argparser without extra parameters, this method is used for auto doc generation."""
    return setup_arg_parser(CLEAR_REPO_ARGS)


def clear_repositories_main(sysargs=None):
    """Entrypoint for clearing repositories."""
    logging.basicConfig(level=logging.INFO)

    parser = setup_args()
    if sysargs:
        args = parser.parse_args(sysargs[1:])
    else:
        args = parser.parse_args()  # pragma: no cover"
    args = add_args_env_variables(args, CLEAR_REPO_ARGS)

    if not args.quay_api_token:
        raise ValueError("--quay-api-token must be specified")
    if not args.quay_password:
        raise ValueError("--quay-password must be specified")

    kwargs = construct_kwargs(args)

    with task_context():
        clear_repositories(**kwargs)
