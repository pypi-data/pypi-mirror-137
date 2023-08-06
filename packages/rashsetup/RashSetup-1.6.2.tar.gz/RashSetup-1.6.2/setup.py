from setuptools import setup, find_packages
from setuptools.command.install import install
import pathlib


class AfterInstallation(install):
    def run(self):
        super().run()

        from RashSetup.drivers import init, download_driver

        download_driver()
        init()


setup(
    name="RashSetup",
    version="1.6.2",
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
