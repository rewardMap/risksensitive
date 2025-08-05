
try:
    from ....pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
    from ....pygame_render.task_stims import FormatTextRiskSensitive, feedback_block
except ImportError:
    from rewardgym.pygame_render.stimuli import BaseAction, BaseDisplay, BaseText
    from rewardgym.pygame_render.task_stims import FormatTextRiskSensitive, feedback_block

def get_pygame_info(action_map, window_size = 256):

    base_position = (window_size // 2, window_size // 2)

    reward_disp, earnings_text = feedback_block(base_position)

    stim = FormatTextRiskSensitive(
        "{0} --------- {1}",
        50,
        condition_text=action_map,
        textposition=base_position,
    )

    final_display = [
        BaseDisplay(None, 1),
        reward_disp,
        earnings_text,
    ]

    pygame_dict = {
        0: {
            "pygame": [
                BaseDisplay(None, 1),
                BaseText("+", 500, textposition=base_position),
                BaseDisplay(None, 1),
                stim,
                BaseAction(),
            ]
        },
        1: {"pygame": final_display},
        2: {"pygame": final_display},
        3: {"pygame": final_display},
        4: {"pygame": final_display},
        5: {"pygame": final_display},
    }

    return pygame_dict