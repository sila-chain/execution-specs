"""Test release parsing given the github repository release JSON data."""

import json
import os
import time
from datetime import timedelta
from os.path import realpath
from pathlib import Path
from typing import Any, Dict, List

import pytest
import requests

from .. import releases
from ..releases import (
    SUPPORTED_REPOS,
    NoSuchReleaseError,
    ReleaseInformation,
    ReleaseTag,
    download_release_information,
    get_release_page_url,
    get_release_url,
    get_release_url_from_release_information,
    is_release_url,
    parse_release_information_from_file,
)

CURRENT_FILE = Path(realpath(__file__))
CURRENT_FOLDER = CURRENT_FILE.parent


@pytest.fixture(scope="session")
def release_information() -> List[ReleaseInformation]:
    """Return the release information from a file."""
    return parse_release_information_from_file(
        CURRENT_FOLDER / "release_information.json"
    )


RELEASES_DOWNLOAD = (
    "https://github.com/sila-chain/execution-specs/releases/download/"
)


@pytest.mark.parametrize(
    "release_name,expected_release_download_url",
    [
        # The `tests` feature tags as `tests@vX.Y.Z` and ships a plain
        # `fixtures.tar.gz` asset.
        ("tests@v20.0.0", "tests%40v20.0.0/fixtures.tar.gz"),
        ("tests@v21.0.0", "tests%40v21.0.0/fixtures.tar.gz"),
        ("tests@latest", "tests%40v21.0.0/fixtures.tar.gz"),
        # A bare `latest` or `vX.Y.Z` resolves the `tests` release.
        ("latest", "tests%40v21.0.0/fixtures.tar.gz"),
        ("v20.0.0", "tests%40v20.0.0/fixtures.tar.gz"),
    ],
)
def test_sels_release_parsing(
    release_name: str,
    expected_release_download_url: str,
    release_information: List[ReleaseInformation],
) -> None:
    """Test resolving the `tests@vX.Y.Z` releases of sila-chain."""
    assert (
        RELEASES_DOWNLOAD + expected_release_download_url
    ) == get_release_url_from_release_information(
        release_name, release_information
    )


@pytest.mark.parametrize(
    "release_name,tag,matches",
    [
        # Other features tag as `tests-<feature>@vX.Y.Z`; both the friendly
        # feature name and the full tag are accepted.
        ("bal@v7.3.1", "tests-bal@v7.3.1", True),
        ("tests-bal@v7.3.2", "tests-bal@v7.3.2", True),
        ("bal@latest", "tests-bal@v7.3.2", True),
        ("bal@v7.3.1", "tests-bal@v7.3.2", False),
        ("bal@latest", "tests-bal-devnet@v8.0.0", False),
        ("benchmark@latest", "tests-benchmark@v0.0.9", True),
        ("tests@latest", "tests-benchmark@v0.0.9", False),
        # A bare `vX.Y.Z` is shorthand for `tests@vX.Y.Z` and never matches
        # a spec-package release tagged plain `vX.Y.Z`.
        ("v2.20.0", "v2.20.0", False),
        ("tests@v2.20.0", "v2.20.0", False),
    ],
)
def test_release_tag_matching(
    release_name: str, tag: str, matches: bool
) -> None:
    """Test the `tests[-<feature>]@vX.Y.Z` tag scheme."""
    assert ReleaseTag.from_string(release_name).matches_tag(tag) is matches


@pytest.mark.parametrize(
    "release_name,asset_name",
    [
        ("tests@latest", "fixtures.tar.gz"),
        ("latest", "fixtures.tar.gz"),
        ("bal@latest", "fixtures_bal.tar.gz"),
        ("tests-benchmark@v0.0.9", "fixtures_benchmark.tar.gz"),
    ],
)
def test_release_asset_name(release_name: str, asset_name: str) -> None:
    """Test the fixture asset name of each feature."""
    assert ReleaseTag.from_string(release_name).asset_name == asset_name


def test_latest_resolves_highest_version(
    release_information: List[ReleaseInformation],
) -> None:
    """
    `latest` resolves the highest version, not the most recently published.

    Publish `tests@v20.0.0` after `tests@v21.0.0`: the newer release line
    must still win.
    """
    republished = [
        release.model_copy(
            update={"published_at": release.published_at + timedelta(days=30)}
        )
        if release.tag_name == "tests@v20.0.0"
        else release
        for release in release_information
    ]
    assert get_release_url_from_release_information(
        "tests@latest", republished
    ) == (RELEASES_DOWNLOAD + "tests%40v21.0.0/fixtures.tar.gz")


@pytest.mark.parametrize(
    "release_name",
    [
        "tests@v2.20.0",
        "v2.20.0",
        # There are no `stable`/`develop` releases.
        "stable@latest",
        "develop@latest",
    ],
)
def test_unknown_releases_do_not_resolve(
    release_name: str,
    release_information: List[ReleaseInformation],
) -> None:
    """Test that release descriptors without a release do not resolve."""
    with pytest.raises(NoSuchReleaseError):
        get_release_url_from_release_information(
            release_name, release_information
        )


def test_is_release_url_covers_supported_repos(
    release_information: List[ReleaseInformation],
) -> None:
    """
    All entries in `SUPPORTED_REPOS` must be matched by `is_release_url`.

    A repo missing from `SUPPORTED_REPOS` falls through to the unversioned
    `cache_folder / "other" / archive_name` path of
    `FixtureDownloader.get_cache_path`, which silently shadows newer
    releases with the same archive filename.
    """
    for release in release_information:
        for asset in release.assets.root:
            assert is_release_url(asset.url)
    for repo in SUPPORTED_REPOS:
        assert is_release_url(f"https://github.com/{repo}/releases/download/")


@pytest.mark.parametrize(
    "url",
    [
        # A source archive, not a release asset.
        "https://github.com/sila-chain/execution-specs/archive/refs/tags/"
        "tests@v21.0.0.tar.gz",
        # Local path, not a URL.
        "./fixtures",
    ],
)
def test_is_release_url_rejects_other_inputs(url: str) -> None:
    """Test that inputs other than release assets are not release URLs."""
    assert not is_release_url(url)


def test_supported_repos() -> None:
    """The fixture releases are hosted by the sila-chain repositories."""
    assert SUPPORTED_REPOS == [
        "sila-chain/execution-specs",
        "sila-chain/sila-tests",
        "sila-chain/sila-legacytests",
    ]


class FakeResponse:
    """A minimal stand-in for `requests.Response`."""

    def __init__(
        self, payload: List[Dict], rate_limited: bool = False
    ) -> None:
        """Initialize with a JSON payload or a rate-limited failure."""
        self.payload = payload
        self.rate_limited = rate_limited
        self.headers: Dict[str, str] = {}

    def json(self) -> List[Dict]:
        """Return the JSON payload."""
        return self.payload

    def raise_for_status(self) -> None:
        """Raise an `HTTPError` if the response is rate-limited."""
        if self.rate_limited:
            raise requests.exceptions.HTTPError(
                "403 Client Error: rate limit exceeded"
            )


def manifest() -> List[Dict]:
    """Load the GitHub API release entries of the test manifest."""
    with open(CURRENT_FOLDER / "release_information.json") as file:
        return json.load(file)


def manifest_release(tag_name: str) -> Dict:
    """Return the GitHub API release entry of `tag_name`."""
    return next(r for r in manifest() if r["tag_name"] == tag_name)


@pytest.fixture
def release_cache_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Path:
    """
    Redirect the release-information cache to a temporary path.

    Also disable the CI/Docker detection so the freshness check applies
    (in CI, the cache never expires).
    """
    cache_file = tmp_path / "release_information.json"
    monkeypatch.setattr(
        releases, "CACHED_RELEASE_INFORMATION_FILE", cache_file
    )
    monkeypatch.setattr(releases, "is_docker_or_ci", lambda: False)
    return cache_file


@pytest.fixture
def release_information_cache(release_cache_path: Path) -> Path:
    """
    Populate the redirected cache with the test manifest up to v20.0.0.

    `tests@v21.0.0` is left out so the tests can publish it later.
    """
    release_cache_path.write_text(
        json.dumps([manifest_release("tests@v20.0.0")])
    )
    return release_cache_path


def make_stale(cache_file: Path) -> None:
    """Age the cache file's mtime beyond the 4-hour freshness window."""
    stale_time = time.time() - 5 * 60 * 60
    os.utime(cache_file, (stale_time, stale_time))


def block_api(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make any GitHub API request fail the test."""

    def no_api(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        pytest.fail("The GitHub API must not be hit")

    monkeypatch.setattr(releases.requests, "get", no_api)


def rate_limited_get(*args: Any, **kwargs: Any) -> FakeResponse:
    """Return a rate-limited (403) GitHub API response."""
    del args, kwargs
    return FakeResponse([], rate_limited=True)


def new_release_get(*args: Any, **kwargs: Any) -> FakeResponse:
    """Return a single-page response with the `tests@v21.0.0` release."""
    del args, kwargs
    return FakeResponse([manifest_release("tests@v21.0.0")])


def test_pinned_release_resolves_from_stale_cache_without_api(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    A pinned version already resolvable from the cache must not refresh.

    Release tags are immutable, so a cached entry for an exact version
    cannot be outdated, no matter how old the cache file is. Regression
    test for `consume --input=tests@vX.Y.Z` raising INTERNALERROR when
    the unauthenticated GitHub API rate limit is exhausted, even though
    the (stale) cache resolved the release.
    """
    make_stale(release_information_cache)
    block_api(monkeypatch)
    assert get_release_url("tests@v20.0.0") == (
        RELEASES_DOWNLOAD + "tests%40v20.0.0/fixtures.tar.gz"
    )
    assert get_release_page_url("tests@v20.0.0") == (
        "https://github.com/sila-chain/execution-specs/releases/tag/"
        "tests%40v20.0.0"
    )
    assert release_information_cache.exists()


def test_fresh_cache_resolves_latest_without_api(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A fresh cache resolves unpinned lookups without an API request."""
    del release_information_cache
    block_api(monkeypatch)
    assert get_release_url("tests@latest").endswith(
        "tests%40v20.0.0/fixtures.tar.gz"
    )


def test_rate_limited_refresh_falls_back_to_stale_cache(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    A failed refresh must fall back to the stale cache, not delete it.

    Previously the stale cache file was deleted before the download was
    attempted, so a rate-limited refresh crashed the run and left no
    cache at all, forcing every subsequent run onto the API.
    """
    make_stale(release_information_cache)
    monkeypatch.setattr(releases.requests, "get", rate_limited_get)
    assert get_release_url("tests@latest").endswith(
        "tests%40v20.0.0/fixtures.tar.gz"
    )
    assert release_information_cache.exists()


def test_rate_limited_refresh_without_cache_raises(
    release_cache_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without a cache file, a failed refresh is a hard error."""
    del release_cache_path
    monkeypatch.setattr(releases.requests, "get", rate_limited_get)
    with pytest.raises(requests.exceptions.HTTPError):
        get_release_url("tests@latest")


def test_unpinned_release_refreshes_stale_cache(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    An unpinned lookup with a stale cache must refresh from the API.

    `latest` and bare feature names can resolve to a newer release at
    any time, so the pinned-release fast path must not apply to them.
    """
    make_stale(release_information_cache)
    calls: List[str] = []

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        calls.append(url)
        return new_release_get(url, **kwargs)

    monkeypatch.setattr(releases.requests, "get", fake_get)
    assert get_release_url("tests@latest").endswith(
        "tests%40v21.0.0/fixtures.tar.gz"
    )
    assert len(calls) == len(SUPPORTED_REPOS)
    assert "tests@v21.0.0" in release_information_cache.read_text()


def test_pinned_release_not_in_stale_cache_refreshes(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    A pinned version missing from the stale cache must refresh.

    The pinned-release fast path only applies when the cache already
    resolves the requested version.
    """
    make_stale(release_information_cache)
    monkeypatch.setattr(releases.requests, "get", new_release_get)
    assert get_release_url("tests@v21.0.0").endswith(
        "tests%40v21.0.0/fixtures.tar.gz"
    )


def test_corrupt_cache_file_is_refreshed(
    release_information_cache: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """
    A corrupt cache file must be re-downloaded, not crash the run.

    A partially-written download (e.g. a killed process) must not wedge
    every subsequent run until the file is manually deleted.
    """
    release_information_cache.write_text("{ not json")
    monkeypatch.setattr(releases.requests, "get", new_release_get)
    assert get_release_url("tests@v21.0.0").endswith(
        "tests%40v21.0.0/fixtures.tar.gz"
    )


@pytest.mark.parametrize(
    "environment,expected_token",
    [
        pytest.param({}, None, id="unauthenticated"),
        pytest.param(
            {"GITHUB_TOKEN": "ghp_test_token"},
            "ghp_test_token",
            id="github_token",
        ),
        pytest.param(
            {"GH_TOKEN": "gho_test_token"},
            "gho_test_token",
            id="gh_token",
        ),
        pytest.param(
            {"GITHUB_TOKEN": "ghp_test_token", "GH_TOKEN": "gho_other"},
            "ghp_test_token",
            id="github_token_wins",
        ),
    ],
)
def test_download_release_information_github_token(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    environment: Dict[str, str],
    expected_token: str | None,
) -> None:
    """
    Authenticate GitHub API requests iff a GitHub token is set.

    `GITHUB_TOKEN` (preferred) or `GH_TOKEN` (the gh CLI's name)
    authenticates the request: 5000 requests/hour instead of the
    unauthenticated 60 requests/hour per IP.
    """
    for variable in ("GITHUB_TOKEN", "GH_TOKEN"):
        monkeypatch.delenv(variable, raising=False)
    for variable, token in environment.items():
        monkeypatch.setenv(variable, token)
    seen_headers: List[Dict[str, str]] = []

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        seen_headers.append(kwargs.get("headers") or {})
        return new_release_get(url, **kwargs)

    monkeypatch.setattr(releases.requests, "get", fake_get)
    download_release_information(tmp_path / "release_information.json")
    expected_headers = (
        {}
        if expected_token is None
        else {"Authorization": f"Bearer {expected_token}"}
    )
    assert seen_headers == [expected_headers] * len(SUPPORTED_REPOS)
