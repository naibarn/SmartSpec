"""
Authentication module for SmartSpec Autopilot.

This module provides simple authentication mechanisms to control access
to Autopilot workflows and agents.

For production use, integrate with proper identity providers (OAuth, SAML, etc.)
"""

import os
import hashlib
import hmac
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta


class AuthError(Exception):
    """Base exception for authentication errors."""
    pass


class AuthenticationRequired(AuthError):
    """Raised when authentication is required but not provided."""
    pass


class InvalidCredentials(AuthError):
    """Raised when credentials are invalid."""
    pass


class TokenExpired(AuthError):
    """Raised when authentication token has expired."""
    pass


class SimpleAuth:
    """
    Simple file-based authentication.
    
    For production, replace with proper auth provider (OAuth, SAML, etc.)
    
    This implementation uses:
    - API keys stored in .smartspec/auth/api_keys
    - Simple token-based authentication
    - No external dependencies
    
    Security notes:
    - API keys should be kept secret
    - Use HTTPS in production
    - Rotate keys regularly
    - Consider rate limiting
    """
    
    def __init__(self, auth_dir: str = ".smartspec/auth"):
        self.auth_dir = Path(auth_dir)
        self.auth_dir.mkdir(parents=True, exist_ok=0o700)  # Secure permissions
        
        self.api_keys_file = self.auth_dir / "api_keys"
        self.tokens_file = self.auth_dir / "tokens"
        
        # Create files if they don't exist
        if not self.api_keys_file.exists():
            self.api_keys_file.touch(mode=0o600)  # Owner read/write only
        if not self.tokens_file.exists():
            self.tokens_file.touch(mode=0o600)
    
    def generate_api_key(self, user_id: str) -> str:
        """
        Generate a new API key for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Generated API key
        """
        # Generate random key
        import secrets
        api_key = secrets.token_urlsafe(32)
        
        # Hash the key for storage
        key_hash = self._hash_key(api_key)
        
        # Store user_id -> key_hash mapping
        with open(self.api_keys_file, 'a') as f:
            f.write(f"{user_id}:{key_hash}\n")
        
        return api_key
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """
        Verify an API key and return the associated user ID.
        
        Args:
            api_key: API key to verify
            
        Returns:
            User ID if valid, None otherwise
        """
        if not api_key:
            return None
        
        key_hash = self._hash_key(api_key)
        
        try:
            with open(self.api_keys_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    
                    user_id, stored_hash = line.split(':', 1)
                    
                    # Use constant-time comparison to prevent timing attacks
                    if hmac.compare_digest(stored_hash, key_hash):
                        return user_id
        except FileNotFoundError:
            pass
        
        return None
    
    def create_token(self, user_id: str, expires_in: int = 3600) -> str:
        """
        Create a temporary authentication token.
        
        Args:
            user_id: User identifier
            expires_in: Token lifetime in seconds (default: 1 hour)
            
        Returns:
            Authentication token
        """
        import secrets
        token = secrets.token_urlsafe(32)
        
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        
        # Store token
        with open(self.tokens_file, 'a') as f:
            f.write(f"{token}:{user_id}:{expires_at.isoformat()}\n")
        
        return token
    
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify a token and return the associated user ID.
        
        Args:
            token: Token to verify
            
        Returns:
            User ID if valid and not expired, None otherwise
        """
        if not token:
            return None
        
        try:
            with open(self.tokens_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    
                    parts = line.split(':', 2)
                    if len(parts) != 3:
                        continue
                    
                    stored_token, user_id, expires_str = parts
                    
                    # Check token match (constant-time)
                    if not hmac.compare_digest(stored_token, token):
                        continue
                    
                    # Check expiration
                    expires_at = datetime.fromisoformat(expires_str)
                    if datetime.now() > expires_at:
                        raise TokenExpired(f"Token expired at {expires_at}")
                    
                    return user_id
        except FileNotFoundError:
            pass
        
        return None
    
    def _hash_key(self, key: str) -> str:
        """Hash an API key for secure storage."""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def revoke_api_key(self, user_id: str):
        """
        Revoke all API keys for a user.
        
        Args:
            user_id: User identifier
        """
        try:
            with open(self.api_keys_file, 'r') as f:
                lines = f.readlines()
            
            with open(self.api_keys_file, 'w') as f:
                for line in lines:
                    if not line.startswith(f"{user_id}:"):
                        f.write(line)
        except FileNotFoundError:
            pass
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens from storage."""
        try:
            with open(self.tokens_file, 'r') as f:
                lines = f.readlines()
            
            with open(self.tokens_file, 'w') as f:
                for line in lines:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                    
                    parts = line.split(':', 2)
                    if len(parts) != 3:
                        continue
                    
                    _, _, expires_str = parts
                    expires_at = datetime.fromisoformat(expires_str)
                    
                    # Keep only non-expired tokens
                    if datetime.now() <= expires_at:
                        f.write(line + '\n')
        except FileNotFoundError:
            pass


# Global auth instance
_auth = None


def get_auth() -> SimpleAuth:
    """Get global authentication instance."""
    global _auth
    if _auth is None:
        _auth = SimpleAuth()
    return _auth


def require_auth(func):
    """
    Decorator to require authentication for a function.
    
    Usage:
        @require_auth
        def sensitive_function(user_id: str, ...):
            # user_id is automatically injected
            ...
    
    The function must accept user_id as first parameter.
    Authentication credentials are read from environment variables:
    - SMARTSPEC_API_KEY: API key
    - SMARTSPEC_TOKEN: Authentication token
    """
    def wrapper(*args, **kwargs):
        auth = get_auth()
        
        # Try API key first
        api_key = os.environ.get('SMARTSPEC_API_KEY')
        if api_key:
            user_id = auth.verify_api_key(api_key)
            if user_id:
                return func(user_id, *args, **kwargs)
        
        # Try token
        token = os.environ.get('SMARTSPEC_TOKEN')
        if token:
            user_id = auth.verify_token(token)
            if user_id:
                return func(user_id, *args, **kwargs)
        
        # No valid credentials
        raise AuthenticationRequired(
            "Authentication required. Set SMARTSPEC_API_KEY or SMARTSPEC_TOKEN environment variable."
        )
    
    return wrapper


def check_auth() -> Optional[str]:
    """
    Check if current request is authenticated.
    
    Returns:
        User ID if authenticated, None otherwise
    """
    auth = get_auth()
    
    # Try API key
    api_key = os.environ.get('SMARTSPEC_API_KEY')
    if api_key:
        user_id = auth.verify_api_key(api_key)
        if user_id:
            return user_id
    
    # Try token
    token = os.environ.get('SMARTSPEC_TOKEN')
    if token:
        user_id = auth.verify_token(token)
        if user_id:
            return user_id
    
    return None


def is_authenticated() -> bool:
    """Check if current request is authenticated."""
    return check_auth() is not None


# For production, replace SimpleAuth with proper auth provider:
#
# class OAuthProvider:
#     """OAuth 2.0 authentication provider"""
#     def __init__(self, client_id, client_secret, ...):
#         ...
#     
#     def verify_token(self, token: str) -> Optional[Dict]:
#         # Verify with OAuth provider
#         ...
#
# class SAMLProvider:
#     """SAML authentication provider"""
#     ...
