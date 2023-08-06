#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from base64 import b64decode
from pathlib import Path
from ssl import SSLContext
from typing import Dict, List
from urllib import request as urllibrequest
from urllib3 import ProxyManager, Retry
from urllib3.exceptions import MaxRetryError

import pytest

from pytest_docker_squid_fixtures import (
    __version__,
    SquidCerts,
    SquidInsecure,
    SquidSecure,
    SQUID_SERVICE_PATTERN,
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def get_headers() -> Dict[str, str]:
    """Provides HTTP headers to be used when testing."""
    return {"User-Agent": f"pytest-docker-squid-fixtures/{__version__}"}


@pytest.fixture()
def known_good_endpoint() -> str:
    """Provides a known good endpoint for testing HTTP and HTTPS."""
    return "www.google.com"


# Override fixture for testing
@pytest.fixture(scope="session")
def pdsf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 4


def no_duplicates(lst: List) -> bool:
    """Tests if a list contains duplicate values."""
    return len(lst) == len(set(lst))


def test_pdsf_docker_compose_insecure(pdsf_docker_compose_insecure: Path):
    """Test that the embedded docker-compose for insecure squid can be copied to a temporary file."""
    service_name = SQUID_SERVICE_PATTERN.format("insecure", 0)
    assert service_name in pdsf_docker_compose_insecure.read_text()


def test_pdsf_docker_compose_insecure_list(
    pdsf_docker_compose_insecure_list: List[Path], pdsf_scale_factor: int
):
    """Test that the embedded docker-compose for insecure squid can be copied to a temporary file."""
    for i in range(pdsf_scale_factor):
        service_name = SQUID_SERVICE_PATTERN.format("insecure", i)
        assert service_name in pdsf_docker_compose_insecure_list[i].read_text()
    assert no_duplicates(pdsf_docker_compose_insecure_list)


def test_pdsf_docker_compose_secure(pdsf_docker_compose_secure: Path):
    """Test that the embedded docker-compose for secure squid can be copied to a temporary file."""
    service_name = SQUID_SERVICE_PATTERN.format("secure", 0)
    assert service_name in pdsf_docker_compose_secure.read_text()


def test_pdsf_docker_compose_secure_list(
    pdsf_docker_compose_secure_list: List[Path], pdsf_scale_factor: int
):
    """Test that the embedded docker-compose for secure squid can be copied to a temporary file."""
    for i in range(pdsf_scale_factor):
        service_name = SQUID_SERVICE_PATTERN.format("secure", i)
        assert service_name in pdsf_docker_compose_secure_list[i].read_text()
    assert no_duplicates(pdsf_docker_compose_secure_list)


def test_squid_auth_header(
    squid_auth_header,
    squid_password: str,
    squid_username: str,
):
    """Test that an HTTP basic authentication header can be provided."""
    assert "Proxy-Authorization" in squid_auth_header
    string = b64decode(
        squid_auth_header["Proxy-Authorization"].split()[1].encode("utf-8")
    ).decode("utf-8")
    assert squid_password in string
    assert squid_username in string


def test_squid_auth_header_list(
    squid_auth_header_list,
    squid_password_list: List[str],
    squid_username_list: List[str],
    pdsf_scale_factor: int,
):
    """Test that an HTTP basic authentication header can be provided."""
    for i in range(pdsf_scale_factor):
        assert "Proxy-Authorization" in squid_auth_header_list[i]
        string = b64decode(
            squid_auth_header_list[i]["Proxy-Authorization"].split()[1].encode("utf-8")
        ).decode("utf-8")
        assert squid_password_list[i] in string
        assert squid_username_list[i] in string
    assert no_duplicates([str(i) for i in squid_auth_header_list])
    assert no_duplicates(squid_password_list)
    assert no_duplicates(squid_username_list)


def test_squid_cacerts(squid_cacerts: Path, squid_certs: SquidCerts):
    """Test that a temporary CA certificate trust store can be provided."""
    assert squid_cacerts.exists()
    cacerts = squid_cacerts.read_text("utf-8")

    ca_cert = squid_certs.ca_certificate.read_text("utf-8")
    assert ca_cert in cacerts

    ca_key = squid_certs.ca_private_key.read_text("utf-8")
    assert ca_key not in cacerts

    cert = squid_certs.certificate.read_text("utf-8")
    assert cert not in cacerts

    key = squid_certs.private_key.read_text("utf-8")
    assert key not in cacerts


def test_squid_cacerts_list(
    squid_cacerts_list: List[Path],
    squid_certs_list: List[SquidCerts],
    pdsf_scale_factor: int,
):
    """Test that a temporary CA certificate trust store can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_cacerts_list[i].exists()
        cacerts = squid_cacerts_list[i].read_text("utf-8")

        ca_cert = squid_certs_list[i].ca_certificate.read_text("utf-8")
        assert ca_cert in cacerts

        ca_key = squid_certs_list[i].ca_private_key.read_text("utf-8")
        assert ca_key not in cacerts

        cert = squid_certs_list[i].certificate.read_text("utf-8")
        assert cert not in cacerts

        key = squid_certs_list[i].private_key.read_text("utf-8")
        assert key not in cacerts
    assert no_duplicates(squid_cacerts_list)
    assert no_duplicates(squid_certs_list)


def test_squid_certs(squid_certs: SquidCerts):
    """Test that a certificate and private key can be provided."""
    assert squid_certs.ca_certificate.exists()
    assert "BEGIN CERTIFICATE" in squid_certs.ca_certificate.read_text("utf-8")
    assert squid_certs.ca_private_key.exists()
    assert "BEGIN PRIVATE KEY" in squid_certs.ca_private_key.read_text("utf-8")
    assert squid_certs.certificate.exists()
    assert "BEGIN CERTIFICATE" in squid_certs.certificate.read_text("utf-8")
    assert squid_certs.private_key.exists()
    assert "BEGIN PRIVATE KEY" in squid_certs.private_key.read_text("utf-8")


def test_squid_certs_list(squid_certs_list: List[SquidCerts], pdsf_scale_factor: int):
    """Test that a certificate and private key can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_certs_list[i].ca_certificate.exists()
        assert "BEGIN CERTIFICATE" in squid_certs_list[i].ca_certificate.read_text(
            "utf-8"
        )
        assert squid_certs_list[i].ca_private_key.exists()
        assert "BEGIN PRIVATE KEY" in squid_certs_list[i].ca_private_key.read_text(
            "utf-8"
        )
        assert squid_certs_list[i].certificate.exists()
        assert "BEGIN CERTIFICATE" in squid_certs_list[i].certificate.read_text("utf-8")
        assert squid_certs_list[i].private_key.exists()
        assert "BEGIN PRIVATE KEY" in squid_certs_list[i].private_key.read_text("utf-8")
    assert no_duplicates(squid_certs_list)


def test_squid_htpasswd(
    squid_htpasswd: Path,
    squid_password: str,
    squid_username: str,
):
    """Test that a htpasswd can be provided."""
    assert squid_htpasswd.exists()
    content = squid_htpasswd.read_text("utf-8")
    assert squid_username in content
    assert squid_password not in content


def test_squid_htpasswd_list(
    squid_htpasswd_list: List[Path],
    squid_password_list: List[str],
    squid_username_list: List[str],
    pdsf_scale_factor: int,
):
    """Test that a htpasswd can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_htpasswd_list[i].exists()
        content = squid_htpasswd_list[i].read_text("utf-8")
        assert squid_username_list[i] in content
        assert squid_password_list[i] not in content
    assert no_duplicates(squid_htpasswd_list)
    assert no_duplicates(squid_password_list)
    assert no_duplicates(squid_username_list)


@pytest.mark.online
def test_squid_insecure(
    get_headers: Dict[str, str],
    squid_insecure: SquidInsecure,
    known_good_endpoint: str,
):
    """Test that an insecure squid can be instantiated."""
    assert "127.0.0.1" in squid_insecure.endpoint

    request = urllibrequest.Request(
        headers=get_headers, method="HEAD", url=f"http://{known_good_endpoint}/"
    )
    request.set_proxy(host=squid_insecure.endpoint, type="http")
    with urllibrequest.urlopen(url=request) as response:
        assert response.code == 200


@pytest.mark.online
def test_squid_insecure_content(
    get_headers: Dict[str, str],
    squid_insecure: SquidInsecure,
    known_good_endpoint: str,
):
    """Test that an insecure squid can be instantiated."""
    assert "127.0.0.1" in squid_insecure.endpoint

    request = urllibrequest.Request(
        headers=get_headers, url=f"http://{known_good_endpoint}/"
    )
    request.set_proxy(host=squid_insecure.endpoint, type="http")
    with urllibrequest.urlopen(url=request) as response:
        assert response.code == 200
        # TODO: Why doesn't decoding to utf-8 work?
        assert "doctype" in str(response.read()).lower()


@pytest.mark.online
def test_squid_insecure_proxymanager(
    get_headers: Dict[str, str],
    squid_insecure: SquidInsecure,
    known_good_endpoint: str,
):
    """Test that an insecure squid can be instantiated."""
    assert "127.0.0.1" in squid_insecure.endpoint

    retry = Retry(total=0)

    proxy_manager = ProxyManager(
        headers=get_headers,
        proxy_headers=get_headers,
        proxy_url=f"http://{squid_insecure.endpoint}/",
    )
    response = proxy_manager.request(
        method="HEAD", retries=retry, url=f"http://{known_good_endpoint}/"
    )
    assert response.status == 200


@pytest.mark.online
def test_squid_insecure_list(
    get_headers: Dict[str, str],
    squid_insecure_list: List[SquidInsecure],
    known_good_endpoint: str,
    pdsf_scale_factor: int,
):
    """Test that an insecure squid can be instantiated."""
    for i in range(pdsf_scale_factor):
        assert "127.0.0.1" in squid_insecure_list[i].endpoint

        request = urllibrequest.Request(
            headers=get_headers, method="HEAD", url=f"http://{known_good_endpoint}/"
        )
        request.set_proxy(host=squid_insecure_list[i].endpoint, type="http")
        with urllibrequest.urlopen(url=request) as response:
            assert response.code == 200

    assert no_duplicates([str(i) for i in squid_insecure_list])


def test_squid_password(squid_password: str):
    """Test that a password can be provided."""
    assert squid_password


def test_squid_password_list(squid_password_list: List[str], pdsf_scale_factor: int):
    """Test that a password can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_password_list[i]
    assert no_duplicates(squid_password_list)


@pytest.mark.online
def test_squid_secure(
    get_headers: Dict[str, str],
    squid_secure: SquidSecure,
    known_good_endpoint: str,
):
    """Test that an secure squid can be instantiated."""
    assert "127.0.0.1" in squid_secure.endpoint

    squid_secure.ssl_context.check_hostname = False
    retry = Retry(total=0)

    proxy_manager = ProxyManager(
        headers=get_headers,
        proxy_headers={**get_headers, **squid_secure.auth_header},
        proxy_ssl_context=squid_secure.ssl_context,
        proxy_url=f"https://{squid_secure.endpoint}/",
    )
    response = proxy_manager.request(
        method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
    )
    assert response.status == 200

    # Error: Unauthenticated
    with pytest.raises(MaxRetryError) as exception_info:
        proxy_manager = ProxyManager(
            headers=get_headers,
            proxy_headers=get_headers,
            proxy_ssl_context=squid_secure.ssl_context,
            proxy_url=f"https://{squid_secure.endpoint}/",
        )
        proxy_manager.request(
            method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
        )
    assert "407" in str(exception_info.value)

    # Error: CA not trusted
    with pytest.raises(MaxRetryError) as exception_info:
        proxy_manager = ProxyManager(
            headers=get_headers,
            proxy_headers={**get_headers, **squid_secure.auth_header},
            proxy_url=f"https://{squid_secure.endpoint}/",
        )
        proxy_manager.request(
            method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
        )
    assert "CERTIFICATE_VERIFY_FAILED" in str(exception_info.value)


@pytest.mark.online
def test_squid_secure_content(
    get_headers: Dict[str, str],
    squid_secure: SquidSecure,
    known_good_endpoint: str,
):
    """Test that an secure squid can be instantiated."""
    assert "127.0.0.1" in squid_secure.endpoint

    squid_secure.ssl_context.check_hostname = False
    retry = Retry(total=0)

    proxy_manager = ProxyManager(
        headers=get_headers,
        proxy_headers={**get_headers, **squid_secure.auth_header},
        proxy_ssl_context=squid_secure.ssl_context,
        proxy_url=f"https://{squid_secure.endpoint}/",
    )
    response = proxy_manager.request(
        method="GET", retries=retry, url=f"https://{known_good_endpoint}/"
    )
    assert response.status == 200
    # TODO: Why doesn't decoding to utf-8 work?
    assert "doctype" in str(response.data).lower()


@pytest.mark.online
def test_squid_secure_list(
    get_headers: Dict[str, str],
    squid_secure_list: List[SquidSecure],
    known_good_endpoint: str,
    pdsf_scale_factor: int,
):
    """Test that an secure squid can be instantiated."""
    for i in range(pdsf_scale_factor):
        assert "127.0.0.1" in squid_secure_list[i].endpoint

        squid_secure_list[i].ssl_context.check_hostname = False
        retry = Retry(total=0)

        proxy_manager = ProxyManager(
            headers=get_headers,
            proxy_headers={**get_headers, **squid_secure_list[i].auth_header},
            proxy_ssl_context=squid_secure_list[i].ssl_context,
            proxy_url=f"https://{squid_secure_list[i].endpoint}/",
        )
        response = proxy_manager.request(
            method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
        )
        assert response.status == 200

        # Error: Unauthenticated
        with pytest.raises(MaxRetryError) as exception_info:
            proxy_manager = ProxyManager(
                headers=get_headers,
                proxy_headers=get_headers,
                proxy_ssl_context=squid_secure_list[i].ssl_context,
                proxy_url=f"https://{squid_secure_list[i].endpoint}/",
            )
            proxy_manager.request(
                method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
            )
        assert "407" in str(exception_info.value)

        # Error: CA not trusted
        with pytest.raises(MaxRetryError) as exception_info:
            proxy_manager = ProxyManager(
                headers=get_headers,
                proxy_headers={**get_headers, **squid_secure_list[i].auth_header},
                proxy_url=f"https://{squid_secure_list[i].endpoint}/",
            )
            proxy_manager.request(
                method="HEAD", retries=retry, url=f"https://{known_good_endpoint}/"
            )
        assert "CERTIFICATE_VERIFY_FAILED" in str(exception_info.value)
    assert no_duplicates([str(i) for i in squid_secure_list])


def test_squid_squidcfg_insecure(
    squid_squidcfg_insecure: Path,
):
    """Test that an insecure squid.cfg can be provided."""
    assert squid_squidcfg_insecure.exists()
    content = squid_squidcfg_insecure.read_text("utf-8")
    assert len(content) > 0


def test_squid_squidcfg_insecure_list(
    squid_squidcfg_insecure_list: List[Path],
    pdsf_scale_factor: int,
):
    """Test that an insecure squid.cfg can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_squidcfg_insecure_list[i].exists()
        content = squid_squidcfg_insecure_list[i].read_text("utf-8")
        assert len(content) > 0
    assert no_duplicates(squid_squidcfg_insecure_list)


def test_squid_squidcfg_secure(squid_squidcfg_secure: Path):
    """Test that a secure squid.cfg can be provided."""
    assert squid_squidcfg_secure.exists()
    content = squid_squidcfg_secure.read_text("utf-8")
    assert len(content)


def test_squid_squidcfg_secure_list(
    squid_squidcfg_secure_list: List[Path], pdsf_scale_factor: int
):
    """Test that a secure squid.cfg can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_squidcfg_secure_list[i].exists()
        content = squid_squidcfg_secure_list[i].read_text("utf-8")
        assert len(content)
    assert no_duplicates(squid_squidcfg_secure_list)


def test_squid_ssl_context(squid_ssl_context: SSLContext):
    """Test that an ssl context can be provided."""
    assert isinstance(squid_ssl_context, SSLContext)


def test_squid_ssl_context_list(
    squid_ssl_context_list: List[SSLContext], pdsf_scale_factor: int
):
    """Test that an ssl context can be provided."""
    for i in range(pdsf_scale_factor):
        assert isinstance(squid_ssl_context_list[i], SSLContext)
    assert no_duplicates(squid_ssl_context_list)


def test_squid_username(squid_username: str):
    """Test that a username can be provided."""
    assert squid_username


def test_squid_username_list(squid_username_list: List[str], pdsf_scale_factor: int):
    """Test that a username can be provided."""
    for i in range(pdsf_scale_factor):
        assert squid_username_list[i]
    assert no_duplicates(squid_username_list)
