import json
import pathlib

from rewardgym.render.routines.passive_routines import InstructionRoutine
from rewardgym.render.stimuli import fixation_cross, make_card_stimulus
from rewardgym.render.stimulus_definitions import ImageDefinition, TextDefinition
from rewardgym.utils import NameCounter

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_en.json"
)
instructions = json.loads(instructions_path.read_text())


def get_instructions(instructions=instructions):
    name = NameCounter()
    fix = fixation_cross()
    card1 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["cross", "X"],
            "shape_pattern": "alternating",
            "color_pattern": "alternating",
            "colors": ((0, 125, 125), (125, 125, 0)),
        },
        height=480,
        width=300,
    )

    card2 = make_card_stimulus(
        {
            "num_tiles": (2, 2),
            "shapes": ["X", "circle"],
            "shape_pattern": "col",
            "color_pattern": "row",
            "colors": ((125, 0, 125), (125, 125, 0)),
        },
        height=480,
        width=300,
    )

    card_shape = (300, 480)

    part_0_0 = TextDefinition(
        name=name.name,
        text=instructions["0.0"],
        height=28,
        pos=(0, 100),
    )

    part_0 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_0_0]
    )

    part_1_0 = TextDefinition(
        name=name.name,
        text=instructions["1.0"],
        height=28,
        pos=(0, 350),
    )

    img_fix = ImageDefinition(name=name.name, image=fix, pos=(0, 0), size=fix.shape[:2])
    img_card = ImageDefinition(name=name.name, image=card1, pos=(-350, 0), size=card_shape)

    part_1 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_1_0, img_card, img_fix]
    )


    part_2_0 = TextDefinition(
        name=name.name,
        text=instructions["2.0"],
        height=28,
        pos=(0, 350),
    )

    img_fix = ImageDefinition(name=name.name, image=fix, pos=(0, 0), size=fix.shape[:2])
    img_card = ImageDefinition(name=name.name, image=card1, pos=(-350, 0), size=card_shape)
    img_card2 = ImageDefinition(name=name.name, image=card2, pos=(350, 0), size=card_shape)

    part_2 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_2_0, img_card, img_fix, img_card2]
    )

    part_3_0 = TextDefinition(
        name=name.name,
        text=instructions["3.0"],
        height=28,
        pos=(0, 0),
    )


    part_3 = InstructionRoutine(
        name=name.name,
        stimulus_definitions=[part_3_0]
    )


    return [part_0, part_1, part_2, part_3], instructions
