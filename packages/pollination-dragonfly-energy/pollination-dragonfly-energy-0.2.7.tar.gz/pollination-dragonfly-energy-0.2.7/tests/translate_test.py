from pollination.dragonfly_energy.translate import ModelToHoneybee, ModelFromGeojson
from queenbee.plugin.function import Function


def test_model_to_honeybee():
    function = ModelToHoneybee().queenbee
    assert function.name == 'model-to-honeybee'
    assert isinstance(function, Function)


def test_model_from_geojson():
    function = ModelFromGeojson().queenbee
    assert function.name == 'model-from-geojson'
    assert isinstance(function, Function)
