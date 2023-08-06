from pollination.dragonfly_energy.edit import WindowsByRatio
from queenbee.plugin.function import Function


def test_windows_by_ratio():
    function = WindowsByRatio().queenbee
    assert function.name == 'windows-by-ratio'
    assert isinstance(function, Function)
