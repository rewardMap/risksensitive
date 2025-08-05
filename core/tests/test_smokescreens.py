try:
    from risksensitive.core import get_configs ,get_pygame_info, get_psychopy_info, get_task, instructions_psychopy
except (ModuleNotFoundError, ImportError):
    try:
        from . import get_configs ,get_pygame_info, get_psychopy_info, get_task, instructions_psychopy

    except (ModuleNotFoundError, ImportError):
        from rewardgym.tasks.risksensitive.core import get_configs ,get_pygame_info, get_psychopy_info, get_task, instructions_psychopy


def test_get_configs():

    if get_configs is not None:
        out = get_configs("1")
        assert isinstance(out, dict)


def test_get_pygame_info():

    if get_pygame_info is not None:
        out = get_pygame_info({0: "left", 1: "right"}, 120)
        assert isinstance(out, dict)


def test_get_psychopy_info():

    if get_pygame_info is not None:
        a, b = get_psychopy_info()
        assert isinstance(a, dict)
        assert isinstance(b, dict)

def test_get_task():

    a, b, c = get_task()

    assert isinstance(a, dict)
    assert isinstance(b, dict)
    assert isinstance(c, dict)


def test_instructions_psychopy():

    if instructions_psychopy is not None:
        a, b = instructions_psychopy()

        assert isinstance(a, list)
        assert isinstance(b, dict)

