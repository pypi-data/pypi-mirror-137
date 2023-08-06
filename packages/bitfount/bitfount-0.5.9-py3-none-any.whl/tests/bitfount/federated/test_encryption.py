"""Tests `bitfount/federated/encryption.py`."""
import base64
from pathlib import Path

from _pytest.logging import LogCaptureFixture
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
import pytest
from pytest import fixture

from bitfount.federated.encryption import _AESEncryption, _read_file, _RSAEncryption
from tests.bitfount import TEST_SECURITY_FILES
from tests.utils.helper import (
    PRIVATE_KEY,
    PRIVATE_SSH_KEY,
    PUBLIC_KEY,
    PUBLIC_SSH_KEY,
    unit_test,
)

MAX_BYTE_VALUE = 255
PUBLIC_KEY_PATH = TEST_SECURITY_FILES / "test_public.testkey"


@unit_test
class TestEncryptionUtils:
    """Tests encryption utility functions."""

    def test_read_file(self) -> None:
        """Tests `read_file` returns bytes."""
        contents = _read_file(PUBLIC_KEY_PATH)
        assert contents is not None
        assert isinstance(contents, bytes)


@unit_test
class TestRSAEncryption:
    """Tests for RSAEncryption class."""

    @fixture
    def private_key_file(self) -> Path:
        """Returns private key file."""
        return TEST_SECURITY_FILES / "test_private.testkey"

    @fixture
    def public_key_file(self) -> Path:
        """Returns public key file."""
        return TEST_SECURITY_FILES / "test_public.testkey"

    @fixture
    def signature_file(self) -> Path:
        """Returns signature file."""
        return TEST_SECURITY_FILES / "test_signature.sign"

    @fixture
    def private_key_bytes(self) -> bytes:
        """Returns private key bytes."""
        return PRIVATE_KEY.encode()

    @fixture
    def public_key_bytes(self) -> bytes:
        """Returns public key bytes."""
        return PUBLIC_KEY.encode()

    @fixture
    def private_ssh_key_file(self) -> Path:
        """Returns private ssh key file."""
        return TEST_SECURITY_FILES / "test_ssh_key_rsa.sshtestkey"

    @fixture
    def public_ssh_key_file(self) -> Path:
        """Returns public ssh key file."""
        return TEST_SECURITY_FILES / "test_ssh_key_rsa.pub.sshtestkey"

    @fixture
    def private_ssh_key_bytes(self) -> bytes:
        """Returns private ssh key bytes."""
        return PRIVATE_SSH_KEY.encode()

    @fixture
    def public_ssh_key_bytes(self) -> bytes:
        """Returns public ssh key bytes."""
        return PUBLIC_SSH_KEY.encode()

    def test_generate_key_pair_produces_rsa_keys(self) -> None:
        """Checks that an RSAPublicKey and an RSAPrivateKey are generated."""
        private_key, public_key = _RSAEncryption.generate_key_pair()

        assert private_key.key_size >= 2048

        assert isinstance(private_key, RSAPrivateKey)
        assert isinstance(public_key, RSAPublicKey)

    def test_load_public_key(
        self, public_key_bytes: bytes, public_key_file: Path
    ) -> None:
        """Tests loading of PEM public key from file and bytes."""
        public_key = _RSAEncryption.load_public_key(public_key_file)
        assert public_key is not None
        assert isinstance(public_key, RSAPublicKey)

        public_key = _RSAEncryption.load_public_key(public_key_bytes)
        assert public_key is not None
        assert isinstance(public_key, RSAPublicKey)

    def test_load_public_ssh_key(
        self, public_ssh_key_bytes: bytes, public_ssh_key_file: Path
    ) -> None:
        """Tests loading of SSH public key from file and bytes."""
        public_key = _RSAEncryption.load_public_key(public_ssh_key_file)
        assert public_key is not None
        assert isinstance(public_key, RSAPublicKey)

        public_key = _RSAEncryption.load_public_key(public_ssh_key_bytes)
        assert public_key is not None
        assert isinstance(public_key, RSAPublicKey)

    def test_serialized_and_deserialized_public_key_is_same_key(self) -> None:
        """Checks serialization and deserialization for PEM-format public keys."""
        _, public_key = _RSAEncryption.generate_key_pair()

        reloaded_key = _RSAEncryption.load_public_key(
            _RSAEncryption.serialize_public_key(public_key)
        )

        assert public_key.public_numbers() == reloaded_key.public_numbers()

    def test_load_private_key(
        self, private_key_bytes: bytes, private_key_file: Path
    ) -> None:
        """Tests loading of PEM private key from file and bytes."""
        private_key = _RSAEncryption.load_private_key(private_key_file)
        assert private_key is not None
        assert isinstance(private_key, RSAPrivateKey)

        private_key = _RSAEncryption.load_private_key(private_key_bytes)
        assert private_key is not None
        assert isinstance(private_key, RSAPrivateKey)

    def test_load_private_ssh_key(
        self, private_ssh_key_bytes: bytes, private_ssh_key_file: Path
    ) -> None:
        """Tests loading of SSH private key from file and bytes."""
        private_key = _RSAEncryption.load_private_key(private_ssh_key_file)
        assert private_key is not None
        assert isinstance(private_key, RSAPrivateKey)

        private_key = _RSAEncryption.load_private_key(private_ssh_key_bytes)
        assert private_key is not None
        assert isinstance(private_key, RSAPrivateKey)

    def test_serialized_and_deserialized_private_key_is_same_key(self) -> None:
        """Checks serialization and deserialization for PEM-format private keys."""
        private_key, _ = _RSAEncryption.generate_key_pair()

        reloaded_key = _RSAEncryption.load_private_key(
            _RSAEncryption.serialize_private_key(private_key)
        )

        assert private_key.private_numbers() == reloaded_key.private_numbers()

    def test_sign_message(self, private_key_file: Path) -> None:
        """Tests message signing produces byte signatures."""
        private_key = _RSAEncryption.load_private_key(private_key_file)
        message = b"Test*123"
        signature = _RSAEncryption.sign_message(private_key, message)
        assert signature is not None
        assert isinstance(signature, bytes)

    def test_verify_javascript_signed_signature(
        self, public_key_file: Path, signature_file: Path
    ) -> None:
        """Checks message signature verification using external values.

        Uses signatures and message from javascript tests.
        """
        message = "Test*123".encode("ascii")
        with open(signature_file, "r") as f:
            signature = f.readline().encode("ascii")
            signature = base64.b64decode(signature)
        public_key = _RSAEncryption.load_public_key(public_key_file)
        result = _RSAEncryption.verify_signature(public_key, signature, message)
        assert result

    def test_verify_signature(
        self, private_key_file: Path, public_key_file: Path
    ) -> None:
        """Checks message signature verification works."""
        message = b"Hello world"
        private_key = _RSAEncryption.load_private_key(private_key_file)
        signature = _RSAEncryption.sign_message(private_key, message)
        public_key = _RSAEncryption.load_public_key(public_key_file)
        result = _RSAEncryption.verify_signature(public_key, signature, message)
        assert result

        # Try again with a different message but same signature
        message = b"Goodbye world"
        result = _RSAEncryption.verify_signature(public_key, signature, message)
        assert result is False

    def test_rsa_correct_decryption(
        self, private_key_file: Path, public_key_file: Path
    ) -> None:
        """Tests encryption-decryption cycle in RSAEncryption."""
        message = b"Hello world"
        private_key = _RSAEncryption.load_private_key(private_key_file)
        public_key = _RSAEncryption.load_public_key(public_key_file)
        ciphertext = _RSAEncryption.encrypt(message, public_key)

        # Assert Decryption is correct
        plaintext = _RSAEncryption.decrypt(ciphertext, private_key)
        assert message == plaintext

    def test_rsa_failed_decryption(
        self, private_key_file: Path, public_key_file: Path
    ) -> None:
        """Checks decryption returns empty string if incorrect ciphertext."""
        message = b"Hello world"
        private_key = _RSAEncryption.load_private_key(private_key_file)
        public_key = _RSAEncryption.load_public_key(public_key_file)
        ciphertext = _RSAEncryption.encrypt(message, public_key)

        ciphertext = bytearray(ciphertext)
        ciphertext[1] = MAX_BYTE_VALUE - ciphertext[1]
        ciphertext = bytes(ciphertext)
        plaintext = _RSAEncryption.decrypt(ciphertext, private_key)
        assert not plaintext

    def test_rsa_failed_encryption_key_too_small(
        self, caplog: LogCaptureFixture, public_key_file: Path
    ) -> None:
        """Checks encryption fails if key is too small."""
        message = b"Hello world" * 100
        public_key = _RSAEncryption.load_public_key(public_key_file)
        with pytest.raises(ValueError):
            _RSAEncryption.encrypt(message, public_key)

        assert "RSA Encryption failed: key size is likely too small" in caplog.text


@unit_test
class TestAESEncryption:
    """Tests AESEncryption class."""

    @fixture
    def key(self) -> bytes:
        """An AESEncryption key to use in tests."""
        return _AESEncryption.generate_key()

    @fixture
    def message(self) -> bytes:
        """Plaintext message to encrypt."""
        return b"Hello world"

    def test_aes_correct_encryption_decryption(
        self, key: bytes, message: bytes
    ) -> None:
        """Tests encryption-decryption cycle in AESEncryption."""
        ciphertext, nonce = _AESEncryption.encrypt(key, message)
        plaintext = _AESEncryption.decrypt(key, nonce, ciphertext)
        assert plaintext == message

    def test_aes_wrong_nonce_decryption(self, key: bytes, message: bytes) -> None:
        """Checks decryption returns empty string if incorrect nonce."""
        ciphertext, nonce = _AESEncryption.encrypt(key, message)
        wrong_nonce = bytes((MAX_BYTE_VALUE - i) for i in nonce)
        plaintext = _AESEncryption.decrypt(key, wrong_nonce, ciphertext)
        assert not plaintext

    def test_aes_failed_decryption(self, key: bytes, message: bytes) -> None:
        """Checks decryption returns empty string if incorrect ciphertext."""
        ciphertext, nonce = _AESEncryption.encrypt(key, message)
        ciphertext = bytearray(ciphertext)
        ciphertext[1] = MAX_BYTE_VALUE - ciphertext[1]
        ciphertext = bytes(ciphertext)
        plaintext = _AESEncryption.decrypt(key, nonce, ciphertext)
        assert not plaintext
