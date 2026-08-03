from xinstaller.common import *
from xinstaller.recipes import *


def install() -> None:
    ctx = Context(prefix=shexpand("$HOME/.local/opt/hdlstuff"))

    print("NOTE: Xcode Command Line Tools should be installed, we should automate this check later.")

    BrewInstall(ctx, "deps", [
        "wget",
        "ninja",
        "cmake",
        "scala@2.13",
        "sbt",
        "boost",
        "fmt",
        "verilator",
        "systemc"
    ])

    PythonCreateVenv(ctx)

    PythonPipInstall(ctx, "python-tools", ["setuptools", "pip"])

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

    InstallFiles(ctx, "prefix/macOS", ["bin/activate-hdlstuff.sh"])

    ctx.run()
    ctx.log(f"Please activate the environment using: '. {ctx.prefix("bin/activate-hdlstuff.sh")}'")
    ctx.remove_logs()


install()
