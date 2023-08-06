import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import pathlib
import logging


class AfterInstallation(install):
    def run(self):
        super().run()
        from RashSetup.drivers import init, download_driver
        logging.info("CREATING PROFILE...")

        try:
            init()
        except AssertionError as _:
            subprocess.run([sys.executable, '-m', "pip", "uninstall", "RashSetup", "-y"])

        logging.info("DOWNLOADING DRIVER...")
        try:
            download_driver()
        except Exception as _:
            logging.error("Please Report this issue, if download_driver fails again", exc_info=True)


setup(
    name="RashSetup",
    version="1.6.1",
    description="RashSetup sets up some Rash Things for us",
    author="RahulARanger",
    maintainer="RahulARanger",
    author_email="saihanumarahul66@gmail.com",
    maintainer_email="saihanumarahul66@gmail.com",
    platforms=[
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    include_package_data=True,
    packages=find_packages(".", exclude=["Greetings", "Installer"]),
    install_requires=(pathlib.Path(__file__).parent / "requirements.txt").read_text().splitlines(),
    cmdclass={
        "install": AfterInstallation,
    }
)
