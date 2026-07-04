from ..common import *


class InstallVerilator(CMakeTarRemote):
    def __init__(self, context, tar_link, force: bool = False):
        super().__init__(context, "verilator", tar_link, ["-DCMAKE_BUILD_TYPE=Release"], force=force)

    def main(self):
        import os
        os.unsetenv("VERILATOR_ROOT")
        return super().main()


class InstallSystemC(CMakeTarRemote):
    def __init__(self, context, tar_link, force: bool = False):
        super().__init__(context, "systemc", tar_link, [
            "-DENABLE_EXAMPLES=OFF",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DBUILD_SHARED_LIBS=TRUE"
        ], force=force)


class InstallBoost(CMakeTarRemote):
    def __init__(self, context, tar_link, force: bool = False):
        super().__init__(context, "boost", tar_link, [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DBUILD_SHARED_LIBS=TRUE"
        ], force=force)


class InstallFmt(CMakeTarRemote):
    def __init__(self, context, tar_link, force: bool = False):
        super().__init__(context, "fmt", tar_link, [
            "-DCMAKE_BUILD_TYPE=Release",
            "-DFMT_DOC=OFF",
            "-DFMT_TEST=OFF",
            "-DBUILD_SHARED_LIBS=TRUE"
        ], force=force)


__all__ = [
    "InstallVerilator",
    "InstallSystemC",
    "InstallBoost",
    "InstallFmt",
]
