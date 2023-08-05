import pathlib
import subprocess
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
import webbrowser


def drivers_path():
    root = pathlib.Path(__file__).parent / "Drivers"
    root.mkdir(exist_ok=True)
    return root


def download_driver():
    return GeckoDriverManager(path=drivers_path()).install()


def is_there() -> bool:
    """
    Checks if the profile is created or not
    :return: True if the profile is created, False otherwise
    """
    return (profile_path() / "parent.lock").exists()  # I feel, this file exists for , that is if we had created profile


def profile_path():
    return drivers_path() / "Profiles"


def check_for_fox():
    path = FirefoxBinary()._start_cmd
    ... if path else webbrowser.open("https://www.mozilla.org/en-US/firefox/")
    assert path, "Unable to find 🔥 + 🦊 browser, Please install it 😊"

    return path


def init():
    binary = check_for_fox()
    return subprocess.run([
        binary, "--profileManager", "--CreateProfile", f"RashDrivers {profile_path()}"
    ], check=True)


def play_and_save():
    binary = check_for_fox()
    return subprocess.run([
        binary, "-P", "RashDrivers"
    ])


def set_preferences():
    profile = FirefoxProfile(profile_path())
    return profile


def get_driver():
    return webdriver.Firefox(set_preferences(), executable_path=download_driver())


if __name__ == "__main__":
    play_and_save() if is_there() else init()
