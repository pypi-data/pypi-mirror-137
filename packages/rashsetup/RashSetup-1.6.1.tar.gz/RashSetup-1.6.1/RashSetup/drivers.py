import pathlib
import shutil
import subprocess
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
import webbrowser
import typing


def _test(function: typing.Callable, use_test_case: bool = __name__ == "__main__") -> typing.Callable:
    def paths():
        path = function()
        return (path.parent / ("_" + path.stem)) if use_test_case else path

    return paths


@_test
def drivers_path() -> pathlib.Path:
    root = pathlib.Path(__file__).parent / "Drivers"
    root.mkdir(exist_ok=True)
    (root / "Profiles").mkdir(exist_ok=True)
    return root


def clear_cache() -> typing.NoReturn:
    shutil.rmtree(profile_path())


def default_name() -> str:
    return ("_" if __name__ == "__main__" else "") + "RashDrivers"


def download_driver() -> str:
    """
    Using webdriver_manager, it auto downloads the latest version of the 🦊 driver
    :return: Path for the Driver
    """
    return GeckoDriverManager(path=drivers_path()).install()


def is_there() -> bool:
    """
    Checks if the profile is created or not
    :return: True if the profile is created, False otherwise
    """
    return (profile_path() / "parent.lock").exists()  # I feel, this file exists for , that is if we had created profile


@_test
def profile_path() -> pathlib.Path:
    return drivers_path() / "Profiles"


def check_for_fox() -> str:
    path = FirefoxBinary()._start_cmd
    ... if path else webbrowser.open("https://www.mozilla.org/en-US/firefox/")
    assert path, "Unable to find 🔥 + 🦊 browser, Please install it 😊"

    return path


def _run_fox(*args) -> subprocess.CompletedProcess:
    binary = check_for_fox()
    return subprocess.run([
        binary, *args
    ], check=True)


def init() -> subprocess.CompletedProcess:
    """

    :return:
    """
    return _run_fox("--profileManager", "--CreateProfile", f"{default_name()} {profile_path()}")


def play_and_save() -> subprocess.CompletedProcess:
    return _run_fox("-P", default_name())


def manager() -> subprocess.CompletedProcess:
    return _run_fox("--profileManager")


def set_preferences() -> FirefoxProfile:
    profile = FirefoxProfile(profile_path())
    return profile


def get_driver() -> webdriver.Firefox:
    return webdriver.Firefox(set_preferences(), executable_path=download_driver())


if __name__ == "__main__":
    ... if is_there() else init()
    play_and_save()
