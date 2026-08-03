from typing import *

from .framework import *
import os
import re
import shutil


class PythonCreateVenv(Task):
    def __init__(self, context, force: bool = False):
        super().__init__(context, "python:create_venv", True, force=force)

    def main(self):
        self.context.run_command(["python3", "-m", "venv", self.ctx.prefix()])

        import os

        for a, b in zip(
            ["Activate.ps1", "activate.fish", "activate.csh", "activate"],
            ["ActivatePython.ps1", "activate-python.fish", "activate-python.csh", "activate-python"]
        ):
            os.rename(self.ctx.prefix("bin/" + a), self.ctx.prefix("bin/" + b))


class PythonPipInstallLocal(Task):
    def __init__(
        self,
        context: Context,
        name: str,
        src_path: str,
        legacy_packages: Optional[List[str]] = None,
        force: bool = False
    ):
        super().__init__(context, f"python:pip_install_local:{name}", True, force=force)
        self._src_path = src_path
        self._legacy_packages = list(legacy_packages or [])

    def _remove_legacy_metadata(self, source_path: str) -> None:
        # An editable install puts its generated metadata in the source tree.
        # pip uninstall can remove the environment's editable hook without
        # removing that metadata, and the next editable install exposes the
        # stale distribution name again. Remove only metadata matching names
        # explicitly listed for this package migration.
        legacy_names = {
            re.sub(r"[-_.]+", "-", name).lower()
            for name in self._legacy_packages
        }

        for root, dirs, _ in os.walk(source_path):
            for name in list(dirs):
                suffix = next(
                    (
                        suffix
                        for suffix in (".egg-info", ".dist-info")
                        if name.endswith(suffix)
                    ),
                    None
                )
                if suffix is None:
                    continue

                distribution_name = re.sub(
                    r"[-_.]+", "-", name[:-len(suffix)]
                ).lower()
                if distribution_name not in legacy_names:
                    continue

                metadata_path = os.path.join(root, name)
                self.ctx.log(
                    f"removing legacy package metadata: {metadata_path}"
                )
                shutil.rmtree(metadata_path)
                dirs.remove(name)

    def main(self):
        source_path = self.ctx.source(self._src_path)

        if self._legacy_packages:
            self.context.run_command(
                [
                    self.ctx.prefix("bin/python3"),
                    "-m", "pip", "uninstall", "-y"
                ] + self._legacy_packages
            )
            self._remove_legacy_metadata(source_path)

        self.context.run_sh(
            f". {self.ctx.prefix('bin/activate-python')} ; python3 -m pip install -e .",
            cwd=source_path
        )


class PythonPipInstall(Task):
    def __init__(self, context: Context, name: str, packages: str, force: bool = False):
        super().__init__(context, f"python:pip_install:{name}", True, force=force)
        self._packages = packages

    def main(self):
        for package in self._packages:
            if not self.context.run_sh(
                f". {self.ctx.prefix('bin/activate-python')} ; python3 -m pip install --upgrade {package}",
                fail_ok=True
            ):
                self.ctx.log(f"cannot install: {package}")


__all__ = [
    "PythonCreateVenv",
    "PythonPipInstallLocal",
    "PythonPipInstall"
]
