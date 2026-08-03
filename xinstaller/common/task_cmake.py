from typing import *

from .framework import *
import os
import shutil


class CMakeTarRemote(Task):
    def __init__(
        self,
        context: Context,
        basename: str,
        tar_link: str,
        cmake_args: List[str],
        cmake_install_mode: str = "COPY",
        force: bool = False
    ):
        super().__init__(context, f"cmake:tar_remote:{basename}", force=force)

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
        cmake_install_mode: str = "COPY",
        cleanup_build_dir: bool = False,
        force: bool = False
    ):
        super().__init__(context, f"cmake:local:{basename}", force=force)

        self._src_path = src_path
        self._cmake_args = list(cmake_args)
        self._cmake_install_mode = cmake_install_mode
        self._cleanup_build_dir = cleanup_build_dir

    # ABS_SYMLINK installs point package configs and libraries into the build
    # tree. Removing that tree can leave stale config-variant links (for
    # example, targets-noconfig beside a new targets-release file), which CMake
    # still discovers and then fails to include. Remove every installed link
    # owned by this build tree before configuring and installing it again.
    def _remove_installed_build_symlinks(self, build_path: str) -> None:
        prefix_path = os.path.realpath(self.ctx.prefix())
        build_path = os.path.realpath(build_path)

        if not os.path.isdir(prefix_path):
            return

        for root, dirs, files in os.walk(prefix_path):
            for name in dirs + files:
                link_path = os.path.join(root, name)
                if not os.path.islink(link_path):
                    continue

                link_target = os.readlink(link_path)
                if not os.path.isabs(link_target):
                    link_target = os.path.join(root, link_target)
                link_target = os.path.realpath(link_target)

                try:
                    points_into_build = os.path.commonpath(
                        [build_path, link_target]
                    ) == build_path
                except ValueError:
                    points_into_build = False

                if points_into_build:
                    self.ctx.log(
                        f"removing installed build symlink: {link_path}"
                    )
                    os.unlink(link_path)

    def main(self) -> None:
        self.ctx.needs_command("cmake")
        self.ctx.needs_command("ninja")

        source_path = self.ctx.source(self._src_path)
        build_path = f"{source_path}/build"
        prefix_path = self.ctx.prefix()

        if self._cleanup_build_dir:
            if os.path.isdir(build_path):
                self.ctx.log(f"removing existing build directory: {build_path}")
                shutil.rmtree(build_path)
            self._remove_installed_build_symlinks(build_path)

        self.ctx.run_sh(f"mkdir -p '{build_path}'")

        self.ctx.run_command(
            [
                "cmake",
                "-S", source_path,
                "-B", build_path,
                "-G", "Ninja",
                f"-DCMAKE_INSTALL_PREFIX={prefix_path}",
                f"-DCMAKE_PREFIX_PATH={prefix_path}",
            ] + self._cmake_args
        )

        self.ctx.run_sh(
            f"CMAKE_INSTALL_MODE={self._cmake_install_mode} ninja install/strip",
            cwd=build_path
        )


__all__ = [
    "CMakeTarRemote",
    "CMakeLocal"
]
