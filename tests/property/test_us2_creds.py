"""Property-based tests for credential manager invariants.
"""
import os
import sys
from hypothesis import given, strategies as st

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.credentials import CredentialManager, Credentials


class TestCredentialManagerInvariants:
    """Property tests for credential manager invariants."""

    @given(
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        st.sampled_from(['api_key', 'session'])
    )
    def test_cache_key_format_invariant(self, provider_id, auth_mode):
        """Cache key must be formatted as '{provider_id}:{auth_mode}'."""
        manager = CredentialManager()
        creds = Credentials(auth_mode=auth_mode, value="test-secret", provider_id=provider_id)
        manager.set_credentials(creds)
        # Retrieved creds must come from cache with same key format
        retrieved = manager.get_credentials(provider_id, auth_mode)
        assert retrieved is not None
        assert retrieved.auth_mode == auth_mode
        assert retrieved.provider_id == provider_id

    @given(
        st.text(min_size=1, max_size=100),
        st.sampled_from(['api_key', 'session']),
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_set_get_roundtrip_invariant(self, secret_value, auth_mode, provider_id):
        """Setting credentials and getting them returns equivalent credentials."""
        manager = CredentialManager()
        original = Credentials(auth_mode=auth_mode, value=secret_value, provider_id=provider_id)
        manager.set_credentials(original)
        retrieved = manager.get_credentials(provider_id, auth_mode)
        assert retrieved is not None
        assert retrieved.auth_mode == original.auth_mode
        assert retrieved.value == original.value
        assert retrieved.provider_id == original.provider_id

    @given(
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
    )
    def test_clear_credentials_removes_provider_keys_invariant(self, provider_id):
        """Clearing credentials for a provider removes all its keys."""
        manager = CredentialManager()
        # Set both auth modes
        manager.set_credentials(Credentials(auth_mode='api_key', value='key1', provider_id=provider_id))
        manager.set_credentials(Credentials(auth_mode='session', value='sess1', provider_id=provider_id))
        # Verify they exist
        assert manager.get_credentials(provider_id, 'api_key') is not None
        assert manager.get_credentials(provider_id, 'session') is not None
        # Clear
        manager.clear_credentials(provider_id)
        # Both should be gone
        assert manager.get_credentials(provider_id, 'api_key') is None
        assert manager.get_credentials(provider_id, 'session') is None

    @given(
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_auth_modes_are_separate_invariant(self, provider_id, secret_value):
        """API key and session auth are stored separately."""
        manager = CredentialManager()
        api_creds = Credentials(auth_mode='api_key', value=f'key-{secret_value}', provider_id=provider_id)
        session_creds = Credentials(auth_mode='session', value=f'sess-{secret_value}', provider_id=provider_id)
        manager.set_credentials(api_creds)
        manager.set_credentials(session_creds)
        retrieved_api = manager.get_credentials(provider_id, 'api_key')
        retrieved_session = manager.get_credentials(provider_id, 'session')
        assert retrieved_api is not None
        assert retrieved_session is not None
        assert retrieved_api.auth_mode == 'api_key'
        assert retrieved_session.auth_mode == 'session'
        assert retrieved_api.value != retrieved_session.value

    @given(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))))
    def test_default_provider_invariant(self, secret_value):
        """Default provider is 'artcraft'."""
        manager = CredentialManager()
        creds = Credentials(auth_mode='api_key', value=secret_value, provider_id='artcraft')
        manager.set_credentials(creds)
        retrieved = manager.get_credentials('artcraft', 'api_key')
        assert retrieved is not None
        assert retrieved.provider_id == 'artcraft'

    @given(
        st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        st.sampled_from(['api_key', 'session'])
    )
    def test_cache_persistence_invariant(self, provider_id, auth_mode):
        """Credentials persist in cache across multiple get calls."""
        manager = CredentialManager()
        creds = Credentials(auth_mode=auth_mode, value='cached-secret', provider_id=provider_id)
        manager.set_credentials(creds)
        first = manager.get_credentials(provider_id, auth_mode)
        second = manager.get_credentials(provider_id, auth_mode)
        assert first is second  # Same object from cache

    @given(st.sampled_from(['api_key', 'session']))
    def test_get_returns_none_when_not_found_invariant(self, auth_mode):
        """get_credentials returns None if credentials not found."""
        manager = CredentialManager()
        result = manager.get_credentials('nonexistent_provider_xyz', auth_mode)
        assert result is None

    @given(
        st.text(min_size=1, max_size=50),
        st.sampled_from(['api_key', 'session']),
        st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_credentials_dataclass_structure_invariant(self, value, auth_mode, provider_id):
        """Credentials must have auth_mode, value, and optional provider_id."""
        creds = Credentials(auth_mode=auth_mode, value=value, provider_id=provider_id)
        assert hasattr(creds, 'auth_mode')
        assert hasattr(creds, 'value')
        assert hasattr(creds, 'provider_id')
        assert creds.auth_mode == auth_mode
        assert creds.value == value
        assert creds.provider_id == provider_id

    @given(
        st.text(min_size=1, max_size=50),
        st.sampled_from(['api_key', 'session'])
    )
    def test_credentials_no_provider_id_optional_invariant(self, value, auth_mode):
        """Credentials can be created without provider_id (optional)."""
        creds = Credentials(auth_mode=auth_mode, value=value)
        assert creds.auth_mode == auth_mode
        assert creds.value == value
        assert creds.provider_id is None
