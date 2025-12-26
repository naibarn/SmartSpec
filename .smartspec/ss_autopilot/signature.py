"""
Signature verification module for SmartSpec Autopilot.

This module provides cryptographic signature verification for:
- Workflow files
- Configuration files
- Downloaded content

Uses GPG/PGP signatures for verification.
"""

import subprocess
from pathlib import Path
from typing import Optional, Tuple


class SignatureError(Exception):
    """Base exception for signature-related errors."""
    pass


class SignatureVerificationFailed(SignatureError):
    """Raised when signature verification fails."""
    pass


class SignatureMissing(SignatureError):
    """Raised when expected signature is missing."""
    pass


def verify_file_signature(file_path: str, signature_path: Optional[str] = None) -> Tuple[bool, str]:
    """
    Verify GPG signature of a file.
    
    Args:
        file_path: Path to file to verify
        signature_path: Path to .asc signature file (default: file_path + '.asc')
        
    Returns:
        Tuple of (verified: bool, message: str)
        
    Raises:
        SignatureMissing: If signature file doesn't exist
        SignatureVerificationFailed: If verification fails
    
    Example:
        >>> verify_file_signature("install.sh", "install.sh.asc")
        (True, "Good signature from ...")
    """
    file_path = Path(file_path)
    
    if signature_path is None:
        signature_path = Path(str(file_path) + '.asc')
    else:
        signature_path = Path(signature_path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if signature exists
    if not signature_path.exists():
        raise SignatureMissing(
            f"Signature file not found: {signature_path}. "
            "Cannot verify file integrity."
        )
    
    # Check if gpg is available
    try:
        subprocess.run(['gpg', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return (False, "GPG not installed. Cannot verify signature.")
    
    # Verify signature
    try:
        result = subprocess.run(
            ['gpg', '--verify', str(signature_path), str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Good signature
            return (True, result.stderr)
        else:
            # Bad signature
            raise SignatureVerificationFailed(
                f"Signature verification failed for {file_path}:\n{result.stderr}"
            )
    
    except subprocess.TimeoutExpired:
        raise SignatureVerificationFailed("GPG verification timed out")
    except Exception as e:
        raise SignatureVerificationFailed(f"GPG verification error: {e}")


def verify_detached_signature(content: bytes, signature: bytes, public_key: Optional[str] = None) -> bool:
    """
    Verify detached signature for content.
    
    Args:
        content: Content bytes to verify
        signature: Signature bytes
        public_key: Optional public key to import first
        
    Returns:
        True if signature is valid
        
    Raises:
        SignatureVerificationFailed: If verification fails
    """
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=False) as content_file:
        content_file.write(content)
        content_path = content_file.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.asc') as sig_file:
        sig_file.write(signature)
        sig_path = sig_file.name
    
    try:
        # Import public key if provided
        if public_key:
            subprocess.run(
                ['gpg', '--import'],
                input=public_key.encode(),
                capture_output=True,
                check=True,
                timeout=10
            )
        
        # Verify
        verified, message = verify_file_signature(content_path, sig_path)
        return verified
        
    finally:
        # Cleanup
        Path(content_path).unlink(missing_ok=True)
        Path(sig_path).unlink(missing_ok=True)


def sign_file(file_path: str, key_id: Optional[str] = None) -> str:
    """
    Sign a file with GPG.
    
    Args:
        file_path: Path to file to sign
        key_id: Optional GPG key ID to use
        
    Returns:
        Path to signature file (.asc)
        
    Raises:
        SignatureError: If signing fails
    
    Note:
        This requires GPG private key to be available.
        For production, use CI/CD pipeline with secure key storage.
    """
    file_path = Path(file_path)
    signature_path = Path(str(file_path) + '.asc')
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Build command
    cmd = ['gpg', '--armor', '--detach-sign']
    if key_id:
        cmd.extend(['--local-user', key_id])
    cmd.extend(['--output', str(signature_path), str(file_path)])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise SignatureError(f"Signing failed: {result.stderr}")
        
        return str(signature_path)
        
    except subprocess.TimeoutExpired:
        raise SignatureError("GPG signing timed out")
    except Exception as e:
        raise SignatureError(f"GPG signing error: {e}")


def get_trusted_keys_dir() -> Path:
    """Get directory for trusted public keys."""
    keys_dir = Path(".smartspec/trusted_keys")
    keys_dir.mkdir(parents=True, exist_ok=True)
    return keys_dir


def import_trusted_key(key_content: str, key_name: str):
    """
    Import a trusted public key.
    
    Args:
        key_content: PGP public key content
        key_name: Name for the key file
    """
    keys_dir = get_trusted_keys_dir()
    key_file = keys_dir / f"{key_name}.asc"
    
    # Save key file
    key_file.write_text(key_content)
    
    # Import to GPG keyring
    try:
        subprocess.run(
            ['gpg', '--import', str(key_file)],
            capture_output=True,
            check=True,
            timeout=10
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise SignatureError(f"Failed to import key: {e}")


# SmartSpec official public key (placeholder - replace with real key)
SMARTSPEC_PUBLIC_KEY = """
-----BEGIN PGP PUBLIC KEY BLOCK-----
Comment: SmartSpec Official Signing Key

[This is a placeholder. In production, replace with actual public key]
-----END PGP PUBLIC KEY BLOCK-----
"""


def verify_smartspec_file(file_path: str) -> bool:
    """
    Verify a file signed by SmartSpec official key.
    
    Args:
        file_path: Path to file to verify
        
    Returns:
        True if signature is valid
        
    Raises:
        SignatureVerificationFailed: If verification fails
    """
    # Import SmartSpec public key if not already imported
    try:
        import_trusted_key(SMARTSPEC_PUBLIC_KEY, "smartspec_official")
    except SignatureError:
        pass  # Key might already be imported
    
    # Verify signature
    verified, message = verify_file_signature(file_path)
    return verified


# For production deployment:
#
# 1. Generate GPG key pair:
#    gpg --full-generate-key
#
# 2. Export public key:
#    gpg --armor --export your@email.com > smartspec_official.asc
#
# 3. Sign files:
#    gpg --armor --detach-sign install.sh
#
# 4. Distribute public key with repository
#
# 5. Update SMARTSPEC_PUBLIC_KEY constant above
#
# 6. In install.sh, verify signature before execution:
#    verify_smartspec_file("install.sh") || exit 1
