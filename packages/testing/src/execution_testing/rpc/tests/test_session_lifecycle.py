"""Test the HTTP session lifecycle of `BaseRPC` clients."""

from unittest.mock import patch

from execution_testing.rpc import SilRPC


def test_close_closes_session() -> None:
    """`close()` closes the underlying HTTP session."""
    rpc = SilRPC("http://localhost:8545")
    with patch.object(rpc.session, "close") as session_close:
        rpc.close()
    session_close.assert_called_once_with()


def test_context_manager_closes_session() -> None:
    """The context manager yields the instance and closes on exit."""
    rpc = SilRPC("http://localhost:8545")
    with patch.object(rpc.session, "close") as session_close:
        with rpc as entered:
            assert entered is rpc
            session_close.assert_not_called()
    session_close.assert_called_once_with()
