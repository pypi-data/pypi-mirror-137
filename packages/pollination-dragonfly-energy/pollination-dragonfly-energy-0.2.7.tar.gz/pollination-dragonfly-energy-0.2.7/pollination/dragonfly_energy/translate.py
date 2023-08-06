from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class ModelToHoneybee(Function):
    """Translate a Dragonfly Model JSON file into several Honeybee Models."""

    model = Inputs.file(
        description='Dragonfly model in JSON format.', path='model.dfjson',
        extensions=['dfjson', 'json']
    )

    obj_per_model = Inputs.str(
        description='Text to describe how the input Model should be divided across the '
        'output Models. Choose from: District, Building, Story.', default='Story',
        spec={'type': 'string', 'enum': ['District', 'Building', 'Story']}
    )

    use_multiplier = Inputs.str(
        description='A switch to note whether the multipliers on each Building story '
        'should be passed along to the generated Honeybee Room objects or if full '
        'geometry objects should be written for each story in the building.',
        default='full-geometry',
        spec={'type': 'string', 'enum': ['full-geometry', 'multiplier']}
    )

    include_plenum = Inputs.str(
        description='A switch to indicate whether ceiling/floor plenums should be '
        'auto-generated for the Rooms.', default='no-plenum',
        spec={'type': 'string', 'enum': ['no-plenum', 'plenum']}
    )

    shade_dist = Inputs.str(
        description='A number to note the distance beyond which other buildings shade '
        'should be excluded from a given Honeybee Model. This can include the units of '
        'the distance (eg. 100ft) or, if no units are provided, the value will be '
        'interpreted in the dragonfly model units. If 0, shade from all neighboring '
        'buildings will be excluded from the resulting models.', default='50m'
    )

    @command
    def model_to_honeybee(self):
        return 'dragonfly translate model-to-honeybee model.dfjson ' \
            '--obj-per-model {{self.obj_per_model}} --{{self.use_multiplier}} ' \
            '--{{self.include_plenum}} --shade-dist {{self.shade_dist}} ' \
            '--folder output --log-file output/hbjson_info.json'

    hbjson_list = Outputs.dict(
        description='A JSON array that includes information about generated honeybee '
        'models.', path='output/hbjson_info.json'
    )

    output_folder = Outputs.folder(
        description='Output folder with the output HBJSON models.', path='output'
    )


@dataclass
class ModelFromGeojson(Function):
    """Create a Dragonfly model from a geojson file with building footprints.

    Certain attributes of the URBANopt geoJSON schema can be used to assign properties
    to each building footprint.
    (https://docs.urbanopt.net/urbanopt-geojson-gem/schemas/building-properties.html).
    """

    geojson = Inputs.file(
        description='A geoJSON file with building footprints as Polygons or '
        'MultiPolygons.', path='model.geojson', extensions=['geojson', 'json']
    )

    origin_point = Inputs.str(
        description='An optional X and Y coordinate, formatted as two floats separated '
        'by a comma, (eg. "-200,-200"), defining where to place the lower-left corner '
        'of the geoJSON geometry in the space of the dragonfly model. The coordinates '
        'of this point are expected to be in the expected units of this Model.',
        default='0,0'
    )

    all_to_buildings = Inputs.str(
        description='A switch to indicate if all geometries in the geojson file should '
        'be considered buildings. If buildings-only, this method will only generate '
        'footprints from geometries that are defined as a "Building" in the type '
        'field of its corresponding properties.',
        default='buildings-only',
        spec={'type': 'string', 'enum': ['buildings-only', 'all-to-buildings']}
    )

    existing_to_context = Inputs.str(
        description='A switch to indicate whether polygons possessing a building_status '
        'of "Existing" under their properties should be imported as ContextShade '
        'instead of Building objects.',
        default='no-context',
        spec={'type': 'string', 'enum': ['no-context', 'existing-to-context']}
    )

    separate_top_bottom = Inputs.str(
        description='A switch to indicate whether top/bottom stories of the buildings '
        'should not be separated in order to account for different boundary conditions '
        'of the roof and ground floor.',
        default='separate-top-bottom',
        spec={'type': 'string', 'enum': ['separate-top-bottom', 'no-separation']}
    )

    units = Inputs.str(
        description='Text for the units system in which the model geometry exists. '
        'Must be (Meters, Millimeters, Feet, Inches, Centimeters).', default='Meters'
    )

    @command
    def model_from_geojson(self):
        return 'dragonfly translate model-from-geojson model.geojson ' \
            '--point {{self.origin_point}} --{{self.all_to_buildings}} ' \
            '--{{self.existing_to_context}} --{{self.separate_top_bottom}} ' \
            '--units {{self.units}} --output-file model.dfjson'

    model = Outputs.file(
        description='Dragonfly Model JSON generated from the geoJSON building '
        'footprints and their properties.', path='model.dfjson'
    )
