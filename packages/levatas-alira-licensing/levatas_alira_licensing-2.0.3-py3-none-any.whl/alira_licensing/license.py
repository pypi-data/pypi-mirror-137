import os
import logging
import json

from datetime import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
    Encoding,
    PublicFormat,
    PrivateFormat,
    BestAvailableEncryption,
)

logger = logging.getLogger(__name__)


METADATA_EXTENSION_OID = x509.ObjectIdentifier("1.2.3.4.5.6.7.8.9.10")


def verify(directory=Path(os.path.abspath("")), current_datetime=datetime.utcnow()):
    try:
        public_key = read_public_key(directory / Path("public.pem"))
        license = read_certificate(directory / Path("license.pem"))

        is_valid = verify_license(license, public_key, current_datetime)

        metadata = json.loads(
            license.extensions.get_extension_for_oid(
                METADATA_EXTENSION_OID
            ).value.value.decode("utf-8")
        )

        return {
            "not_valid_before": license.not_valid_before,
            "not_valid_after": license.not_valid_after,
            "metadata": metadata,
            "active": is_valid,
        }
    except Exception as e:
        logger.exception("There was an error processing the license.")

        return {
            "not_valid_before": None,
            "not_valid_after": None,
            "metadata": None,
            "active": False,
        }


def read_public_key(filename):
    """
    Loads an RSA public key from a file.

    :param filename: Path to file containing the public key
    """

    with open(filename, "rb") as key_file:
        return load_pem_public_key(key_file.read(), backend=default_backend())


def read_private_key(filename, password):
    """
    Loads an RS Private Key from a file.

    :param filename: Path to file
    :param password: Encryption password to decode the key
    """

    with open(filename, "rb") as key_file:
        return load_pem_private_key(
            key_file.read(), password=password, backend=default_backend()
        )


def write_private_key(private_key, filename, password):
    """
    Saves an RSA Private Key to a file with a provided encryption password.

    :param private_key: RSA Private Key
    :param filename: Path to file
    :param password: Encryption password to secure the key
    """

    with open(filename, "wb") as key_file:
        key_file.write(
            private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=BestAvailableEncryption(password),
            )
        )


def write_public_key(public_key, filename):
    """
    Saves an RSA Public Key to a file.

    :param public_key: RSA Public Key
    :param filename: Path to file
    """

    with open(filename, "wb") as key_file:
        key_file.write(
            public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo,
            )
        )


def read_certificate(filename):
    """
    Loads a license certificate from a file.

    :param filename: Path to file containing the license.
    """

    with open(filename, "rb") as cert_file:
        return load_pem_x509_certificate(cert_file.read(), backend=default_backend())


def verify_license(license, public_key, current_datetime=datetime.utcnow()):
    """
    Verify that the license came from the provided public key and the
    certificate is valid.

    :param license: The license certificate
    :param public_key: The public key
    """

    try:
        public_key.verify(
            license.signature,
            license.tbs_certificate_bytes,
            padding.PKCS1v15(),
            license.signature_hash_algorithm,
        )

        are_dates_valid = (
            license.not_valid_before < current_datetime
            and license.not_valid_after > current_datetime
        )

        if not are_dates_valid:
            print(
                "The license is not valid.",
                current_datetime,
                license.not_valid_before,
                license.not_valid_after,
            )
            return False

        expected_attributes = [
            {"oid": NameOID.COUNTRY_NAME, "name": "Country", "expected": u"US"},
            {
                "oid": NameOID.STATE_OR_PROVINCE_NAME,
                "name": "State",
                "expected": u"Florida",
            },
            {
                "oid": NameOID.LOCALITY_NAME,
                "name": "City",
                "expected": u"West Palm Beach",
            },
            {
                "oid": NameOID.ORGANIZATION_NAME,
                "name": "Organization",
                "expected": u"Levatas",
            },
            {
                "oid": NameOID.ORGANIZATIONAL_UNIT_NAME,
                "name": "Organizational Unit",
                "expected": u"Alira Platform",
            },
        ]

        for attribute in expected_attributes:
            for value in license.issuer.get_attributes_for_oid(attribute["oid"]):
                if value.value != attribute["expected"]:
                    print(value.value, attribute["expected"])
                    return False

        return True
    except InvalidSignature as err:
        print("There was an error verifying the certificate")
        return False
