from typing import *
from .framework import *


class BrewInstall(Task):
    def __init__(self, context: Context, name: str, package_names: List[str]):
        super().__init__(context, "brew:install:" + name)
        self._package_names = list(package_names)

    def main(self):
        self.ctx.needs_command("brew")
        self.ctx.run_command(["brew", "update"])

        for package in self._package_names:
            if not self.ctx.run_command(["brew", "install", package]):
                self.ctx.log(f"cannot install: {package}")


class BrewUpgrade(Task):
    def __init__(self, context: Context):
        super().__init__(context, "brew:upgrade")

    def main(self):
        self.ctx.needs_command("brew")
        self.ctx.run_command(["brew", "upgrade"])


___all__ = [
    "BrewInstall",
    "BrewUpgrade"
]
