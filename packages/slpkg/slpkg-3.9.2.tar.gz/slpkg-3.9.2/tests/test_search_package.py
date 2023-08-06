import pytest
from slpkg.binary.search import search_pkg
from slpkg.sbo.search import sbo_search_pkg


@pytest.mark.skip(reason="no way of currently testing in Gitlab")
def test_search():
    """Testing found the name from binaries repos
    """
    name = "vlc"
    repo = "alien"
    test = search_pkg(name, repo)
    assert name == test


@pytest.mark.skip(reason="no way of currently testing in Gtilab")
def test_sbo_search():
    """Testing found the name from binaries repos
    """
    name = "slpkg"
    test = sbo_search_pkg(name).split("/")[-2]
    assert name == test