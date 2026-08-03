from xinstaller.common import *
from xinstaller.recipes import *


def install() -> None:
    ctx = Context(prefix=shexpand("$HOME/.local/opt/hdlstuff"))

    AptInstall(ctx, "utils", ["wget", "curl", "tar", "git"])
    AptInstall(ctx, "cpp-stuff", ["g++", "gcc", "gdb", "ninja-build", "make"])
    AptInstall(ctx, "python3-stuff", ["python3", "python3-pip", "python3-venv", "python3-setuptools"])
    AptInstall(ctx, "gtkwave", ["gtkwave"])

    InstallSbtDebian(ctx)

    InstallCMake(ctx, "https://github.com/Kitware/CMake/releases/download/v4.0.2/cmake-4.0.2-linux-aarch64.sh")

    # add other boost dependencies
    InstallBoost(ctx, "https://github.com/boostorg/boost/releases/download/boost-1.87.0/boost-1.87.0-cmake.tar.gz")

    InstallFmt(ctx, "https://github.com/fmtlib/fmt/archive/refs/tags/11.1.4.tar.gz")

    InstallSystemC(ctx, "https://github.com/accellera-official/systemc/archive/refs/tags/3.0.1.tar.gz")

    AptInstall(ctx, "verilator-deps", [
        "git", "help2man", "perl", "python3", "make",
        "g++",  # Both compilers
        "libgz",  # Non-Ubuntu (ignore if gives error)
        "libfl2", "libfl-dev",  # Ubuntu only (ignore if gives error)
        "zlibc", "zlib1g", "zlib1g-dev",  # Ubuntu only (ignore if gives error)
        "ccache",  # If present at build, needed for run
        "mold",  # If present at build, needed for run
        "libgoogle-perftools-dev", "numactl",
        "perl-doc",
        "autoconf", "flex", "bison"
    ])
    InstallVerilator(ctx, "https://github.com/verilator/verilator/archive/refs/tags/v5.034.tar.gz")

    PythonCreateVenv(ctx)

    PythonPipInstallLocal(ctx, "hdlstuff_hdlinfo", "repos/hdlinfo/python", ["hdlinfo"])
    PythonPipInstallLocal(ctx, "hdlstuff_hdlscw", "repos/hdlscw/python", ["hdlscw"])
    PythonPipInstallLocal(ctx, "hdlstuff_chext_test", "repos/chext-test/python", ["chext_test"])
    PythonPipInstallLocal(ctx, "hdlstuff_sctlm", "repos/sctlm/python", ["sctlm"])

    PythonPipInstall(ctx, "plotting_stuff", ["numpy", "matplotlib"])

    CMakeLocal(ctx, "hdlstuff_hdlscw", "repos/hdlscw/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "hdlstuff_hal", "repos/hdlstuff-hal", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "hdlstuff_hdlinfo", "repos/hdlinfo/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "hdlstuff_chext_test", "repos/chext-test/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "hdlstuff_sctlm", "repos/sctlm/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    SbtPublishLocal(ctx, "hdlstuff_hdlinfo", "repos/hdlinfo/scala", [("hdlstuff", "hdlinfo")])
    SbtPublishLocal(ctx, "hdlstuff_chext", "repos/chext", [("hdlstuff", "chext")])

    InstallFiles(ctx, "prefix/ubuntu", ["bin/activate-hdlstuff.sh"])

    ctx.run()
    ctx.log(f"Please activate the environment using: '. {ctx.prefix("bin/activate-hdlstuff.sh")}'")
    ctx.remove_logs()


install()
