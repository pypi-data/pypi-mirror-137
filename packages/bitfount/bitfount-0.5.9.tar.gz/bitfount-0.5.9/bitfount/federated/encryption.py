"""Symmetric and asymmetric encryption functions."""
import os
from pathlib import Path
from typing import Optional, Tuple, Union, cast

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPrivateKeyWithSerialization,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

from bitfount.federated.logging import _get_federated_logger

logger = _get_federated_logger(__name__)


def _read_file(file_to_read: Path) -> bytes:
    """Reads given file and returns contents as a byte string."""
    with open(file_to_read, "rb") as f:
        contents = f.read()
    return contents


class _RSAEncryption:
    """Class of functions for dealing with RSA asymmetric encryption."""

    @staticmethod
    def generate_key_pair() -> Tuple[RSAPrivateKey, RSAPublicKey]:
        """Generates a new RSA key pair."""
        logger.debug("Generating RSA key pair")
        # Key size is 4096 bits which means we can only encrypt up to 4096 bits of data
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=4096, backend=default_backend()
        )
        return private_key, private_key.public_key()

    @staticmethod
    def load_private_key(private_key: Union[bytes, Path]) -> RSAPrivateKey:
        """Loads a private key either from a byte string or file path."""
        logger.debug("Attempting to load private key")
        if isinstance(private_key, Path):
            logger.debug(f"Loading private key from path: {private_key}")
            private_key = _read_file(private_key)

        # Try loading from PEM format first
        try:
            logger.debug("Attempting to load private key using PEM Format...")
            loaded_private_key = serialization.load_pem_private_key(
                private_key, password=None, backend=default_backend()
            )

        except ValueError as ve:
            # Otherwise try SSH format
            try:
                logger.debug(
                    "Loading private key using PEM format failed,"
                    " trying to load using SSH format..."
                )
                loaded_private_key = serialization.load_ssh_private_key(
                    private_key, password=None, backend=default_backend()
                )
            except ValueError:
                # If both fail, raise the original error
                raise ve

        logger.debug("Loaded private key")
        return cast(RSAPrivateKey, loaded_private_key)

    @staticmethod
    def serialize_private_key(private_key: RSAPrivateKeyWithSerialization) -> bytes:
        """Serializes a private key to bytes."""
        return private_key.private_bytes(
            Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()
        )

    @staticmethod
    def load_public_key(public_key: Union[bytes, Path]) -> RSAPublicKey:
        """Loads a public key either from a byte string or file path."""
        logger.debug("Attempting to load public key")
        if isinstance(public_key, Path):
            logger.debug(f"Loading public key from path: {public_key}")
            public_key = _read_file(public_key)

        # Try loading from PEM format first
        try:
            logger.debug("Attempting to load public key using PEM Format...")
            loaded_public_key = serialization.load_pem_public_key(
                public_key, backend=default_backend()
            )
        except ValueError as ve:
            # Otherwise try SSH format
            try:
                logger.debug(
                    "Loading public key using PEM format failed, "
                    "trying to load using SSH format..."
                )
                loaded_public_key = serialization.load_ssh_public_key(
                    public_key, backend=default_backend()
                )
            except ValueError:
                # If both fail, raise the original error
                raise ve

        logger.debug("Loaded public key")
        return cast(RSAPublicKey, loaded_public_key)

    @staticmethod
    def serialize_public_key(public_key: RSAPublicKey) -> bytes:
        """Serialize an RSAPublicKey to bytes."""
        return public_key.public_bytes(Encoding.PEM, PublicFormat.PKCS1)

    @staticmethod
    def sign_message(private_key: RSAPrivateKey, message: bytes) -> bytes:
        """Cryptographically signs a message.

        Signs provided `message` with provided `private_key` and returns signature.
        """
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=20,  # padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        return signature

    @staticmethod
    def verify_signature(
        public_key: RSAPublicKey, signature: bytes, message: bytes
    ) -> bool:
        """Verifies that decrypting `signature` with `public_key` === `message`."""
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=20,  # padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except InvalidSignature:
            return False

        logger.debug("Signature verified")
        return True

    @staticmethod
    def encrypt(message: bytes, public_key: RSAPublicKey) -> bytes:
        """Encrypts plaintext.

        Encrypts provided `message` with `public_key` and returns ciphertext.
        """
        try:
            ciphertext = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except ValueError as ve:
            logger.error("RSA Encryption failed: key size is likely too small")
            raise ve
        return ciphertext

    @staticmethod
    def decrypt(
        ciphertext: bytes,
        private_key: RSAPrivateKey,
    ) -> bytes:
        """Decrypts ciphertext.

        Decrypts provided `ciphertext` with `private_key` and returns plaintext
        """
        try:
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
        except ValueError:
            logger.warning("Failed to decrypt ciphertext")
            return b""

        return plaintext


class _AESEncryption:
    """Class of functions for dealing with AES symmetric encryption."""

    @staticmethod
    def generate_key() -> bytes:
        """Generates a symmetric encryption key.

        Generates symmetric key using the GCM algorithm (Galois Counter Mode).

        (More secure than CBC (Cipher Block Chaining)).
        """
        key = AESGCM.generate_key(bit_length=128)  # 128 bits is sufficiently secure
        return key

    @staticmethod
    def encrypt(
        key: bytes, plaintext: bytes, associated_data: Optional[bytes] = None
    ) -> Tuple[bytes, bytes]:
        """Encrypts plaintext.

        Encrypts `plaintext` using `key` and a randomly generated `nonce`.
        If `associated_data` is provided, it is authenticated.
        """
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)  # 12 bytes
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)

        return ciphertext, nonce

    @staticmethod
    def decrypt(
        key: bytes,
        nonce: bytes,
        ciphertext: bytes,
        associated_data: Optional[bytes] = None,
    ) -> bytes:
        """Decrypts ciphertext.

        Decrypts `ciphertext` using `key`, `nonce` and `associated_data` if present.

        If `associated_data` is provided, this must be the same associated data
        used in encryption.

        ***
        NONCE MUST ONLY BE USED ONCE FOR A GIVEN KEY (SAME NONCE AS USED FOR
        ENCRYPTION)
        ***
        """
        aesgcm = AESGCM(key)

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        except InvalidTag:
            logger.warning("Failed to decrypt ciphertext")
            return b""

        return plaintext
