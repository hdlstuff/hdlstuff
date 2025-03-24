from ..common import *

import os

class InstallFiles(Task):
    def __init__(self, context: Context, files: List[str]):
        super().__init__(context, "install:files")

        self._files = list(files)

    def main(self):
        self.ctx.needs_command("bash")
        self.ctx.needs_command("ln")

        for file in self._files:
            source_file = self.ctx.source("prefix/" + file)
            target_file = self.ctx.prefix(file)

            os.makedirs(os.path.dirname(target_file), exist_ok=True)

            self.ctx.run_command(
                ["ln", "-sf", source_file, target_file]
            )

        with open(self.ctx.prefix(".hdlstuff_repo"), "w") as f:
            f.write(self.ctx.source("."))


__all__ = ["InstallFiles"]
