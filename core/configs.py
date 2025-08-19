try:
    from rewardgym.utils import check_random_state
    from rewardgym.task.utils import check_conditions_not_following, check_condition_present_or
except ImportError:
    from ...utils import check_conditions_not_following, check_condition_present_or
    from ....utils import check_random_state


def get_configs(stimulus_set: str = "1"):
    """
    Generating randomized stimulus sequences following Rosenbaum et al. 2022.
    Stimulus generation pseudo random for each block and another check is implemented, to not have two forced choices
    following each other and making sure, that one of each forced choices appears in the first 15 trials.


    Three blocks of 61 stimuli each:
    * 66 risky choices
        * 42 with equal EV
        * 24 with sure 20 vs risky 80
    * 75 forced choices (15 each)
    * 42 test trials (i.e. dominated choices, where one option has clearly higher outcome).

    ITIs are drawn from the fixed set [1.5, 2.125, 2.75, 3.375, 4.0].

    Conditions of importance:
    * 0, 1, 2, 3, 4 = forced choice
    Risky trials, with same EV:
     * 20 vs 0 / 40 = 11 and 18
     * 40 vs 0 / 80 = 16 and 23
    Risky trials, not same EV:
     * 20 vs 0 / 80 = 12 and 22
    Dominated
     * 40 vs 0 / 40 = 15 and 19
     * 20 vs 0 = 5 and 9
     * 40 vs 0 = 6 and 13
     * 0 vs 0 / 20 = 7 and 17
     * 0 vs 0 / 40 = 8 and 21
     * 20 vs 40

    All other possible conditions:
    {0: 'null',
     1: 'save-20',
     2: 'save-40',
     3: 'risky-40',
     4: 'risky-80',
     5: 'null_save-20',
     6: 'null_save-40',
     7: 'null_risky-40',
     8: 'null_risky-80',
     9: 'save-20_null',
     10: 'save-20_save-40',
     11: 'save-20_risky-40',
     12: 'save-20_risky-80',
     13: 'save-40_null',
     14: 'save-40_save-20',
     15: 'save-40_risky-40',
     16: 'save-40_risky-80',
     17: 'risky-40_null',
     18: 'risky-40_save-20',
     19: 'risky-40_save-40',
     20: 'risky-40_risky-80',
     21: 'risky-80_null',
     22: 'risky-80_save-20',
     23: 'risky-80_save-40',
     24: 'risky-80_risky-40'}

    """

    random_state = check_random_state(int(stimulus_set))

    blocks = 3

    itis = []
    conditions = []

    condition_dict = {
        # fixed choice:
        "null_none": {0: {0: 1, None: None}},
        "none_null": {0: {None: None, 0: 1}},
        "save-20_none": {0: {1: 2, None: None}},
        "none_save-20": {0: {None: None, 1: 2}},
        "save-40_none": {0: {2: 3, None: None}},
        "none_save-40": {0: {None: None, 2: 3}},
        "risky-40_none": {0: {3: 4, None: None}},
        "none_risky-40": {0: {None: None, 3: 4}},
        "risky-80_none": {0: {4: 5, None: None}},
        "none_risky-80": {0: {None: None, 4: 5}},
        # equal ev:
        "save-20_risky-40": {0: {1: 2, 3: 4}},
        "risky-40_save-20": {0: {3: 4, 1: 2}},
        "save-40_risky-80": {0: {2: 3, 4: 5}},
        "risky-80_save-40": {0: {4: 5, 2: 3}},
        # non equal ev:
        "save-20_risky-80": {0: {1: 2, 4: 5}},
        "risky-80_save-20": {0: {4: 5, 1: 2}},
        # Test trials:
        "save-40_risky-40": {0: {2: 3, 3: 4}},
        "risky-40_save-40": {0: {2: 3, 3: 4}},
        "null_save-20": {0: {0: 1, 1: 2}},
        "save-20_null": {0: {1: 2, 0: 1}},
        "null_save-40": {0: {0: 1, 2: 3}},
        "save-40_null": {0: {2: 3, 0: 1}},
        "null_risky-40": {0: {0: 1, 3: 4}},
        "risky-40_null": {0: {3: 4, 0: 1}},
        "null_risky-80": {0: {0: 1, 4: 5}},
        "risky-80_null": {0: {4: 5, 0: 1}},
        "save-20_save-40": {0: {1: 2, 2: 3}},
        "save-40_save-20": {0: {2: 3, 1: 2}},
    }

    for b in range(blocks):
        risky_equal_ev = [
            "save-20_risky-40",
            "risky-40_save-20",
            "save-40_risky-80",
            "risky-80_save-40",
        ] * 3 + [
            random_state.choice(["save-20_risky-40", "risky-40_save-20"]),
            random_state.choice(["save-40_risky-80", "risky-80_save-40"]),
        ]
        risky_non_equal_ev = ["save-20_risky-80", "risky-80_save-20"] * 4
        forced_choices = (
            [
                "none_null",
                "none_save-20",
                "none_save-40",
                "none_risky-40",
                "none_risky-80",
            ]
            * 2
            + [
                "null_none",
                "save-20_none",
                "save-40_none",
                "risky-40_none",
                "risky-80_none",
            ]
            * 2
            + [
                random_state.choice(["none_null", "null_none"]),
                random_state.choice(["none_save-20", "save-20_none"]),
                random_state.choice(["none_save-40", "save-40_none"]),
                random_state.choice(["none_risky-40", "risky-40_none"]),
                random_state.choice(["none_risky-80", "risky-80_none"]),
            ]
        )

        test_trials = [
            "save-40_risky-40",
            "risky-40_save-40",
            "null_save-20",
            "save-20_null",
            "null_save-40",
            "save-40_null",
            "null_risky-40",
            "risky-40_null",
            "null_risky-80",
            "risky-80_null",
            "save-20_save-40",
            "save-40_save-20",
        ] + [
            random_state.choice(
                [
                    "save-40_risky-40",
                    "risky-40_save-40",
                    "null_save-20",
                    "save-20_null",
                    "null_save-40",
                    "save-40_null",
                ]
            ),
            random_state.choice(
                [
                    "null_risky-40",
                    "risky-40_null",
                    "null_risky-80",
                    "risky-80_null",
                    "save-20_save-40",
                    "save-40_save-20",
                ]
            ),
        ]

        # iti_template = [1.5, 2.125, 2.75, 3.375, 4.0] * 12 + [1.5, 2.75, 4.0]
        iti_template = [0.5, 0.75, 1.0, 1.25, 1.5] * 12 + [0.5, 1.0, 1.5]

        condition_template = (
            forced_choices + risky_equal_ev + risky_non_equal_ev + test_trials
        )

        approve = False

        while not approve:
            conditions_proposal = random_state.permutation(condition_template).tolist()

            approve = (
                all(
                    [check_condition_present_or(conditions_proposal[:10], jj)]
                    for jj in [
                        (["null_none"], ["none_null"]),
                        (["none_save-20"], ["save-20_none"]),
                        (["none_save-40"], ["save-40_none"]),
                        (["none_risky-40"], ["risky-40_none"]),
                        (["none_risky-80"], ["risky-80_none"]),
                    ]
                )
                and all(
                    [
                        check_conditions_not_following(conditions_proposal, jj)
                        for jj in (
                            ["none_null", "null_none"],
                            ["none_save-20", "save-20_none"],
                            ["none_save-40", "save-40_none"],
                            ["none_risky-40", "risky-40_none"],
                            ["none_risky-80", "risky-80_none"],
                        )
                    ]
                )
                and check_conditions_not_following(conditions_proposal, test_trials)
                and all(
                    [
                        check_conditions_not_following(conditions_proposal, [jj])
                        for jj in risky_non_equal_ev + risky_equal_ev
                    ]
                )
            )

        conditions.extend(conditions_proposal)

        iti = random_state.permutation(iti_template).tolist()
        itis.extend(iti)

    config = {
        "name": "risk-sensitive",
        "stimulus_set": stimulus_set,
        "isi": [],
        "iti": itis,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),  # 183
        "update": ["iti"],
        "add_remainder": True,
        "breakpoints": [60, 121],
        "break_duration": 45,
    }

    return config
