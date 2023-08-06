#!/usr/bin/env python

# pylint: disable=redefined-outer-name,too-many-arguments,too-many-locals

"""The actual fixtures, you found them ;)."""

import logging
import itertools

from base64 import b64encode
from functools import partial
from pathlib import Path
from ssl import create_default_context, SSLContext
from string import Template
from time import sleep, time
from typing import Dict, Generator, List, NamedTuple

import pytest

from lovely.pytest.docker.compose import Services
from _pytest.tmpdir import TempPathFactory

from .utils import (
    check_proxy,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_user_defined_file,
    SQUID_SERVICE,
    SQUID_SERVICE_PATTERN,
    start_service,
)

# Caching is needed, as singular-fixtures and list-fixtures will conflict at scale_factor=1
# This appears to only matter when attempting to start the docker secure squid service
# for the second time.
CACHE = {}

LOGGER = logging.getLogger(__name__)


class SquidCerts(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: Path
    ca_private_key: Path
    certificate: Path
    private_key: Path


class SquidInsecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    docker_compose: Path
    endpoint: str
    service_name: str


# Note: NamedTuple does not support inheritance :(
class SquidSecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    auth_header: Dict[str, str]
    cacerts: Path
    certs: SquidCerts
    docker_compose: Path
    endpoint: str
    htpasswd: Path
    password: str
    service_name: str
    ssl_context: SSLContext
    username: str


def _pdsf_docker_compose_insecure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure squid service.
    """
    cache_key = _pdsf_docker_compose_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = SQUID_SERVICE_PATTERN.format("insecure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            # TODO: lovely-docker-compose uses the file for teardown ...
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def pdsf_docker_compose_insecure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure squid service.
    """
    for lst in _pdsf_docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def pdsf_docker_compose_insecure_list(
    docker_compose_files: List[str],
    pdsf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure squid service.
    """
    yield from _pdsf_docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _pdsf_docker_compose_secure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure squid
    service.
    """
    cache_key = _pdsf_docker_compose_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = SQUID_SERVICE_PATTERN.format("secure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def pdsf_docker_compose_secure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure squid
    service.
    """
    for lst in _pdsf_docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def pdsf_docker_compose_secure_list(
    docker_compose_files: List[str],
    pdsf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure squid
    service.
    """
    yield from _pdsf_docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


@pytest.fixture(scope="session")
def pdsf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 1


def _squid_auth_header(
    *,
    squid_password_list: List[str],
    squid_username_list: List[str],
    scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure squid service."""
    cache_key = _squid_auth_header.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        auth = b64encode(
            f"{squid_username_list[i]}:{squid_password_list[i]}".encode("utf-8")
        ).decode("utf-8")
        result.append({"Proxy-Authorization": f"Basic {auth}"})
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def squid_auth_header(squid_password: str, squid_username: str) -> Dict[str, str]:
    """Provides an HTTP basic authentication header containing credentials for the secure squid service."""
    return _squid_auth_header(
        squid_password_list=[squid_password],
        squid_username_list=[squid_username],
        scale_factor=1,
    )[0]


@pytest.fixture(scope="session")
def squid_auth_header_list(
    squid_password_list: List[str],
    squid_username_list: List[str],
    pdsf_scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure squid service."""
    return _squid_auth_header(
        squid_password_list=squid_password_list,
        squid_username_list=squid_username_list,
        scale_factor=pdsf_scale_factor,
    )


def _squid_cacerts(
    *,
    squid_certs_list: List[SquidCerts],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure squid
    service.
    """
    cache_key = _squid_cacerts.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "cacerts"),
            generate_cacerts(
                tmp_path_factory,
                certificate=squid_certs_list[i].ca_certificate,
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate cacerts!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_cacerts(
    squid_certs: SquidCerts,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure squid
    service.
    """
    for lst in _squid_cacerts(
        squid_certs_list=[squid_certs],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_cacerts_list(
    squid_certs_list: List[SquidCerts],
    pdsf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure squid
    service.
    """
    yield from _squid_cacerts(
        squid_certs_list=squid_certs_list,
        pytestconfig=pytestconfig,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_certs(
    *, scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[SquidCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure squid service."""
    # TODO: Augment to allow for reading certificates from /test ...
    cache_key = _squid_certs.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        tmp_path = tmp_path_factory.mktemp(__name__)
        keypair = generate_keypair()
        squid_cert = SquidCerts(
            ca_certificate=tmp_path.joinpath(f"{SQUID_SERVICE}-ca-{i}.crt"),
            ca_private_key=tmp_path.joinpath(f"{SQUID_SERVICE}-ca-{i}.key"),
            certificate=tmp_path.joinpath(f"{SQUID_SERVICE}-{i}.crt"),
            private_key=tmp_path.joinpath(f"{SQUID_SERVICE}-{i}.key"),
        )
        squid_cert.ca_certificate.write_bytes(keypair.ca_certificate)
        squid_cert.ca_private_key.write_bytes(keypair.ca_private_key)
        squid_cert.certificate.write_bytes(keypair.certificate)
        squid_cert.private_key.write_bytes(keypair.private_key)
        result.append(squid_cert)
    CACHE[cache_key] = result
    yield result
    for squid_cert in result:
        squid_cert.ca_certificate.unlink(missing_ok=True)
        squid_cert.ca_private_key.unlink(missing_ok=True)
        squid_cert.certificate.unlink(missing_ok=True)
        squid_cert.private_key.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def squid_certs(
    tmp_path_factory: TempPathFactory,
) -> Generator[SquidCerts, None, None]:
    """Provides the location of temporary certificate and private key files for the secure squid service."""
    for lst in _squid_certs(scale_factor=1, tmp_path_factory=tmp_path_factory):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_certs_list(
    pdsf_scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[SquidCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure squid service."""
    yield from _squid_certs(
        scale_factor=pdsf_scale_factor, tmp_path_factory=tmp_path_factory
    )


def _squid_htpasswd(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    squid_password_list: List[str],
    squid_username_list: List[str],
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure squid service."""
    cache_key = _squid_htpasswd.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "htpasswd"),
            generate_htpasswd(
                tmp_path_factory,
                username=squid_username_list[i],
                password=squid_password_list[i],
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate htpasswd!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_htpasswd(
    pytestconfig: "_pytest.config.Config",
    squid_password: str,
    squid_username: str,
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the htpasswd file for the secure squid service."""
    for lst in _squid_htpasswd(
        pytestconfig=pytestconfig,
        scale_factor=1,
        squid_password_list=[squid_password],
        squid_username_list=[squid_username],
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_htpasswd_list(
    pdsf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    squid_password_list: List[str],
    squid_username_list: List[str],
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure squid service."""
    yield from _squid_htpasswd(
        pytestconfig=pytestconfig,
        scale_factor=pdsf_scale_factor,
        squid_username_list=squid_username_list,
        squid_password_list=squid_password_list,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_insecure(
    *,
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    squid_squidcfg_insecure_list: List[Path],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[SquidInsecure], None, None]:
    """Provides the endpoint of a local, insecure, squid."""
    cache_key = _squid_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = SQUID_SERVICE_PATTERN.format("insecure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure squid service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_insecure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    # Note: Needed to correctly populate the embedded, consolidated, service template ...
                    "PATH_CERTIFICATE": "/dev/null",
                    "PATH_HTPASSWD": "/dev/null",
                    "PATH_KEY": "/dev/null",
                    "PATH_SQUIDCFG": squid_squidcfg_insecure_list[i],
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting insecure squid service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  squidcfg     : %s", squid_squidcfg_insecure_list[i])

        check_server = partial(check_proxy, protocol="http")
        endpoint = start_service(
            docker_services,
            check_server=check_server,
            docker_compose=path_docker_compose,
            private_port=3128,
            service_name=service_name,
        )
        LOGGER.debug("Insecure squid endpoint [%d]: %s", i, endpoint)

        result.append(
            SquidInsecure(
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                service_name=service_name,
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_insecure(
    docker_services: Services,
    squid_squidcfg_insecure: Path,
    pdsf_docker_compose_insecure: Path,
    tmp_path_factory: TempPathFactory,
) -> Generator[SquidInsecure, None, None]:
    """Provides the endpoint of a local, insecure, squid."""
    for lst in _squid_insecure(
        docker_compose_insecure_list=[pdsf_docker_compose_insecure],
        docker_services=docker_services,
        squid_squidcfg_insecure_list=[squid_squidcfg_insecure],
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_insecure_list(
    docker_services: Services,
    squid_squidcfg_insecure_list: List[Path],
    pdsf_docker_compose_insecure_list: List[Path],
    pdsf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[SquidInsecure], None, None]:
    """Provides the endpoint of a local, insecure, squid."""
    yield from _squid_insecure(
        docker_compose_insecure_list=pdsf_docker_compose_insecure_list,
        docker_services=docker_services,
        squid_squidcfg_insecure_list=squid_squidcfg_insecure_list,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_password(*, scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure squid service."""
    cache_key = _squid_password.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.password.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def squid_password() -> str:
    """Provides the password to use for authentication to the secure squid service."""
    return _squid_password(scale_factor=1)[0]


@pytest.fixture(scope="session")
def squid_password_list(pdsf_scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure squid service."""
    return _squid_password(scale_factor=pdsf_scale_factor)


def _squid_secure(
    *,
    docker_compose_secure_list: List[Path],
    docker_services: Services,
    squid_auth_header_list: List[Dict[str, str]],
    squid_cacerts_list: List[Path],
    squid_certs_list: List[SquidCerts],
    squid_htpasswd_list: List[Path],
    squid_password_list: List[str],
    squid_squidcfg_secure_list: List[Path],
    squid_ssl_context_list: List[SSLContext],
    squid_username_list: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[SquidSecure], None, None]:
    """Provides the endpoint of a local, secure, squid."""
    cache_key = _squid_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = SQUID_SERVICE_PATTERN.format("secure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure squid service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_secure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    "PATH_CERTIFICATE": squid_certs_list[i].certificate,
                    "PATH_HTPASSWD": squid_htpasswd_list[i],
                    "PATH_KEY": squid_certs_list[i].private_key,
                    "PATH_SQUIDCFG": squid_squidcfg_secure_list[i],
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting secure squid service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  ca certificate : %s", squid_certs_list[i].ca_certificate)
        LOGGER.debug("  certificate    : %s", squid_certs_list[i].certificate)
        LOGGER.debug("  squidcfg     : %s", squid_squidcfg_secure_list[i])
        LOGGER.debug("  private key    : %s", squid_certs_list[i].private_key)
        LOGGER.debug("  password       : %s", squid_password_list[i])
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  username       : %s", squid_username_list[i])

        check_server = partial(
            check_proxy,
            auth_header=squid_auth_header_list[i],
            protocol="https",
            ssl_context=squid_ssl_context_list[i],
        )
        endpoint = start_service(
            docker_services,
            check_server=check_server,
            docker_compose=path_docker_compose,
            private_port=3129,
            service_name=service_name,
        )
        LOGGER.debug("Secure squid endpoint [%d]: %s", i, endpoint)

        result.append(
            SquidSecure(
                auth_header=squid_auth_header_list[i],
                cacerts=squid_cacerts_list[i],
                certs=squid_certs_list[i],
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                htpasswd=squid_htpasswd_list[i],
                password=squid_password_list[i],
                service_name=service_name,
                ssl_context=squid_ssl_context_list[i],
                username=squid_username_list[i],
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_secure(
    docker_services: Services,
    squid_auth_header,
    squid_cacerts: Path,
    squid_certs: SquidCerts,
    squid_htpasswd: Path,
    squid_password: str,
    squid_squidcfg_secure: Path,
    squid_ssl_context: SSLContext,
    squid_username: str,
    pdsf_docker_compose_secure: Path,
    tmp_path_factory: TempPathFactory,
) -> Generator[SquidSecure, None, None]:
    """Provides the endpoint of a local, secure, squid."""
    for lst in _squid_secure(
        docker_compose_secure_list=[pdsf_docker_compose_secure],
        squid_auth_header_list=[squid_auth_header],
        squid_cacerts_list=[squid_cacerts],
        squid_certs_list=[squid_certs],
        squid_htpasswd_list=[squid_htpasswd],
        squid_password_list=[squid_password],
        squid_squidcfg_secure_list=[squid_squidcfg_secure],
        squid_ssl_context_list=[squid_ssl_context],
        squid_username_list=[squid_username],
        docker_services=docker_services,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_secure_list(
    docker_services: Services,
    squid_auth_header_list,
    squid_cacerts_list: List[Path],
    squid_certs_list: List[SquidCerts],
    squid_htpasswd_list: List[Path],
    squid_password_list: List[str],
    squid_squidcfg_secure_list: List[Path],
    squid_ssl_context_list: List[SSLContext],
    squid_username_list: List[str],
    pdsf_docker_compose_secure_list: List[Path],
    pdsf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[SquidSecure], None, None]:
    """Provides the endpoint of a local, secure, squid."""
    yield from _squid_secure(
        docker_compose_secure_list=pdsf_docker_compose_secure_list,
        squid_auth_header_list=squid_auth_header_list,
        squid_cacerts_list=squid_cacerts_list,
        squid_certs_list=squid_certs_list,
        squid_htpasswd_list=squid_htpasswd_list,
        squid_password_list=squid_password_list,
        squid_squidcfg_secure_list=squid_squidcfg_secure_list,
        squid_ssl_context_list=squid_ssl_context_list,
        squid_username_list=squid_username_list,
        docker_services=docker_services,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_squidcfg_insecure(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the squid configuration file for the insecure squid service."""
    cache_key = _squid_squidcfg_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "squid.insecure.cfg"),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="squid.insecure.cfg"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find insecure squid.cfg!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_squidcfg_insecure(
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the squid configuration  file for the insecure squid service."""
    for lst in _squid_squidcfg_insecure(
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_squidcfg_insecure_list(
    pdsf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the squid configuration file for the insecure squid service."""
    yield from _squid_squidcfg_insecure(
        pytestconfig=pytestconfig,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_squidcfg_secure(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the squid configuration file for the secure squid service."""
    cache_key = _squid_squidcfg_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "squid.secure.cfg"),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="squid.secure.cfg"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find secure squid.cfg!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def squid_squidcfg_secure(
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the squid configuration  file for the secure squid service."""
    for lst in _squid_squidcfg_secure(
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def squid_squidcfg_secure_list(
    pdsf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the squid configuration file for the secure squid service."""
    yield from _squid_squidcfg_secure(
        pytestconfig=pytestconfig,
        scale_factor=pdsf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _squid_ssl_context(
    *, squid_cacerts_list: List[Path], scale_factor: int
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure squid service.
    """
    cache_key = _squid_ssl_context.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(create_default_context(cafile=str(squid_cacerts_list[i])))
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def squid_ssl_context(squid_cacerts: Path) -> SSLContext:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure squid service.
    """
    return _squid_ssl_context(squid_cacerts_list=[squid_cacerts], scale_factor=1)[0]


@pytest.fixture(scope="session")
def squid_ssl_context_list(
    squid_cacerts_list: List[Path],
    pdsf_scale_factor: int,
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure squid service.
    """
    return _squid_ssl_context(
        squid_cacerts_list=squid_cacerts_list,
        scale_factor=pdsf_scale_factor,
    )


def _squid_username(*, scale_factor: int) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure squid service."""
    cache_key = _squid_username.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.username.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def squid_username() -> str:
    """Retrieve the name of the user to use for authentication to the secure squid service."""
    return _squid_username(scale_factor=1)[0]


@pytest.fixture(scope="session")
def squid_username_list(
    pdsf_scale_factor: int,
) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure squid service."""
    return _squid_username(scale_factor=pdsf_scale_factor)
