from dataclasses import dataclass
from pollination_dsl.function import Inputs, Outputs, Function, command


@dataclass
class WindowsByRatio(Function):
    """Add windows to all outdoor walls of a model given a ratio."""

    model = Inputs.file(
        description='Dragonfly model in JSON format.', path='model.dfjson',
        extensions=['dfjson', 'json']
    )

    ratio = Inputs.str(
        description='A number between 0 and 1 (but not perfectly equal to 1) for the '
        'desired ratio between window area and wall area. If multiple values are '
        'input here (each separated by a space), different WindowParameters will be '
        'assigned based on cardinal direction, starting with north and moving '
        'clockwise.', default='0.4'
    )

    @command
    def windows_by_ratio(self):
        return 'dragonfly edit windows-by-ratio model.dfjson {{self.ratio}} ' \
            '--output-file new_model.dfjson'

    new_model = Outputs.file(
        description='Dragonfly Model JSON with window parameters set based on '
        'the input ratio.', path='new_model.dfjson'
    )
