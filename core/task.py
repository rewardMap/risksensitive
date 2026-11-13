import itertools
import pathlib
from typing import Literal

import numpy as np

from rewardgym import check_random_state
from rewardgym.reward_classes import BaseReward, PseudoRandomReward
from rewardgym.tasks.yaml_tools import load_task_from_yaml


def get_task(
    render_backend: Literal["pygame", "psychopy"] | None = None,
    random_state: int | np.random.Generator = 1000,
    key_dict=None,
    **kwargs,
):
    random_state = check_random_state(random_state)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph  = load_task_from_yaml(yaml_file)

    reward_structure = {
        1: BaseReward(reward=[0], random_state=random_state),
        2: BaseReward(reward=[20], random_state=random_state),
        3: BaseReward(reward=[40], random_state=random_state),
        4: PseudoRandomReward(reward_list=[40, 40, 40, 40, 0, 0, 0, 0], random_state=random_state),
        5: PseudoRandomReward(reward_list=[80, 80, 80, 80, 0, 0, 0, 0], random_state=random_state),
    }

    action_space = list(reward_structure.keys())
    action_map = {}
    condition_space = action_space + list(itertools.permutations(action_space, 2))
    for n, ii in enumerate(condition_space):
        if isinstance(ii, tuple):
            action_map[n] = {0: ii[0] - 1, 1: ii[1] - 1}
        else:
            action_map[n] = {0: ii - 1}

    reward_meaning = {
        1: "null",
        2: "save-20",
        3: "save-40",
        4: "risky-40",
        5: "risky-80",
    }

    condition_meaning = {}
    for key, value in action_map.items():
        if len(value) == 2:
            condition_meaning[key] = (
                reward_meaning[value[0] + 1]
                + "_"
                + reward_meaning[value[1] + 1]
            )
        elif len(value) == 1:
            condition_meaning[key] = reward_meaning[value[0] + 1]

    info_dict.update({"condition-meaning": condition_meaning})

    if render_backend is not None:
        from .render import get_render_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        render_dict, _ = get_render_info(random_state=random_state, key_dict=key_dict, fullpoints=info_dict['meta']['fullpoints'])
        info_dict.update(render_dict)

    return environment_graph, reward_structure, info_dict
