from typing import *

from .framework import *
import os


class CMakeTarRemote(Task):
    def __init__(
        self,
        context: Context,
        basename: str,
        tar_link: str,
        cmake_args: List[str],
        cmake_install_mode: str = "COPY"
    ):
        super().__init__(context, f"cmake:tar_remote:{basename}")

        self._tar_link = tar_link
        self._cmake_args = list(cmake_args)
        self._cmake_install_mode = cmake_install_mode

    def main(self) -> None:
        import tempfile

        self.ctx.needs_command("cmake")
        self.ctx.needs_command("tar")
        self.ctx.needs_command("ninja")

        with tempfile.TemporaryDirectory() as temp_dir:
            self.ctx.run_command(
                ["wget", self._tar_link, "-O", f"{temp_dir}/source.tar.gz"],
                cwd=temp_dir
            )

            self.ctx.run_command(
                ["tar", "-xzf", f"{temp_dir}/source.tar.gz",
                    "-C", f"{temp_dir}/"]
            )

            dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(
                os.path.join(temp_dir, d))]
            assert len(dirs) == 1

            os.rename(os.path.join(temp_dir, dirs[0]), os.path.join(
                temp_dir, "source"))

            self.ctx.run_command(
                ["mkdir", "-p", f"{temp_dir}/build"]
            )

            self.ctx.run_command(
                [
                    "cmake",
                    "-S", f"{temp_dir}/source",
                    "-B", f"{temp_dir}/build",
                    "-G", f"Ninja",
                    f"-DCMAKE_INSTALL_PREFIX={self.ctx.prefix()}",
                    f"-DCMAKE_PREFIX_PATH={self.ctx.prefix()}"
                ] + self._cmake_args
            )

            self.ctx.run_command(
                [
                    "cmake",
                    "--build", "."
                ],
                cwd=f"{temp_dir}/build"
            )

            self.ctx.run_sh(
                f"CMAKE_INSTALL_MODE={self._cmake_install_mode} cmake --install . --strip",
                cwd=f"{temp_dir}/build"
            )


class CMakeLocal(Task):
    def __init__(
        self,
        context: Context,
        basename: str,
        src_path: str,
        cmake_args: List[str],
        cmake_install_mode: str = "COPY"
    ):
        super().__init__(context, f"cmake:local:{basename}")

        self._src_path = src_path
        self._cmake_args = list(cmake_args)
        self._cmake_install_mode = cmake_install_mode

    def main(self) -> None:
        self.ctx.needs_command("cmake")
        self.ctx.needs_command("ninja")

        source_path = self.ctx.source(self._src_path)
        build_path = f"{source_path}/build"
        prefix_path = self.ctx.prefix()

        self.ctx.run_sh(f"mkdir -p '{build_path}'")

        self.ctx.run_sh(
            f"cmake -S '{source_path}' -B '{build_path}' -G Ninja '-DCMAKE_INSTALL_PREFIX={prefix_path}' '-DCMAKE_PREFIX_PATH={prefix_path}'"
        )

        self.ctx.run_sh(
            f"CMAKE_INSTALL_MODE={self._cmake_install_mode} ninja install/strip",
            cwd=build_path
        )


__all__ = [
    "CMakeTarRemote",
    "CMakeLocal"
]
