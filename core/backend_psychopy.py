from copy import deepcopy

from rewardgym.stimuli import (
    STIMULUS_DEFAULTS,
    fixation_cross,
    generate_stimulus_properties,
    make_card_stimulus,
)

from rewardgym import check_random_state

from rewardgym.render.passive_routines import PresentationRoutine, StateBasedDisplay, FeedBackRoutine
from rewardgym.render import ImageDefinition
from rewardgym.render.response_routines import NAFCRoutine


def risksensitive_stimuli(random_state, stim_defaults=STIMULUS_DEFAULTS):
    random_state = check_random_state(random_state)
    stim_properties = []

    stim_defaults = deepcopy(stim_defaults)
    for _ in range(5):
        st_p = generate_stimulus_properties(
            random_state,
            colors=stim_defaults["colors"],
            shapes=stim_defaults["shapes"],
        )
        stim_properties.append(st_p)
        # Filtering colors used, but keeping background color (which is at -1,
        # not an ideal solution).
        stim_defaults["colors"] = [
            i
            for i in stim_defaults["colors"]
            if (i not in st_p["colors"] or i == stim_defaults["colors"][-1])
        ]
        stim_defaults["shapes"] = [
            i for i in stim_defaults["shapes"] if i != st_p["shapes"]
        ]

    image_map = {}
    stimuli = {}

    for n in range(5):
        image_map[n] = make_card_stimulus(stim_properties[n])
        stimuli[n] = stim_properties[n]

    return image_map, stimuli


def get_psychopy_info(
    random_state=111, key_dict={"left": 0, "right": 1}, external_stimuli=None, fullpoints=None, **kwargs
):
    random_state = check_random_state(random_state)

    if external_stimuli is None:
        image_map, stimuli = risksensitive_stimuli(random_state=random_state)
    else:
        image_map, stimuli = external_stimuli

    image_map = {
        key: ImageDefinition(name=key, image=imap) for key, imap in image_map.items()
    }

    reward_feedback = FeedBackRoutine(
        duration=1.0, name="reward", bar_total=fullpoints, rl_label="reward"
    )

    base_stim = PresentationRoutine(
        stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=True)], duration=0.1, name="fixation"
    )

    fix_iti = PresentationRoutine(duration=1.5, name="iti", rl_label='obs')

    selection_disp = NAFCRoutine(
        name="response",
        duration=2.0,
        key_dict=key_dict,
        rl_label="action",
        stimulus_mapping=image_map,
        presentation_settings={
            "rl_label_before": "obs",
            "name_before": "cue",
            "duration_after": 1.5,
            "present_after": True,
            "name_after": "selection"
        },
        positions = {0: (-350, 0), 1: (350, 0)},
        highlight_selected=True
    )

    final_step = [
        PresentationRoutine(
                stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=False)], duration=0.5, name="reward-delay"
            ),
        reward_feedback,
        fix_iti,
    ]

    info_dict = {
        0: {
            "psychopy": [
                base_stim,
                selection_disp,
            ]
        },
        1: {"psychopy": final_step},
        2: {"psychopy": final_step},
        3: {"psychopy": final_step},
        4: {"psychopy": final_step},
        5: {"psychopy": final_step},
    }

    return info_dict, stimuli
