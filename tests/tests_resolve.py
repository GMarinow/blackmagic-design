from blackmagic_design.Resolve import Resolve


def test_initialize_resolve_nogui_success():
    assert Resolve().open(gui='-nogui') == 'DaVinci Resolve opened successfully.'
    Resolve().kill()

def test_initialize_resolve_success():
    assert Resolve().open() == 'DaVinci Resolve opened successfully.'

def test_resolve_already_running():
    assert Resolve().open() == 'DaVinci Resolve is already running.'
    Resolve().kill()

def test_initialize_wrong_executable_path():
    executable_path = 'D:/wrong/path/Resolve.exe'
    assert Resolve().open(executable_path=executable_path) == f"Error: Resolve executable not found at '{executable_path}'. Please check the path and try again."

