# TODO add SbtPublishLocal task here
# Make sure that .ivy2 path is set correctly

# also create a scripts directory for activating stuff
# and maybe the kernel driver and the pci hot plug thingy

from typing import *
from .framework import *
import os
import re
import shutil


class SbtPublishLocal(Task):
    def __init__(
        self,
        context: Context,
        name: str,
        proj_dirpath: str,
        legacy_artifacts: Optional[List[Tuple[str, str]]] = None,
        force: bool = False
    ):
        super().__init__(context, f"sbt:publish_local:{name}", True, force=force)
        self._proj_dirpath = proj_dirpath
        self._legacy_artifacts = list(legacy_artifacts or [])

    def _remove_legacy_artifacts(self) -> None:
        # publishLocal writes versioned artifacts below Ivy's local repository.
        # Renaming an artifact does not remove the old coordinate, so it can
        # continue to resolve accidentally. Remove only explicitly listed
        # legacy artifacts from this install prefix before publishing.
        ivy_local = self.ctx.prefix(".ivy2/local")

        for organization, artifact in self._legacy_artifacts:
            organization_path = os.path.join(ivy_local, organization)
            if not os.path.isdir(organization_path):
                continue

            for name in os.listdir(organization_path):
                is_cross_versioned = re.fullmatch(
                    rf"{re.escape(artifact)}_(?:2|3)(?:\.\d+)*",
                    name
                ) is not None
                if name != artifact and not is_cross_versioned:
                    continue

                artifact_path = os.path.join(organization_path, name)
                if not os.path.isdir(artifact_path):
                    continue

                self.ctx.log(
                    f"removing legacy Ivy artifact: {artifact_path}"
                )
                shutil.rmtree(artifact_path)

    def main(self):
        self.ctx.needs_command("sbt")
        self._remove_legacy_artifacts()
        self.ctx.run_command(
            [
                "sbt",
                f"-Dsbt.ivy.home={self.ctx.prefix(".ivy2")}",
                "publishLocal"
            ],
            cwd=self.ctx.source(self._proj_dirpath)
        )


__all__ = [
    "SbtPublishLocal"
]
