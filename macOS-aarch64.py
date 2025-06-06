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

    PythonPipInstallLocal(ctx, "hdlinfo_python", "repos/hdlinfo/python")
    PythonPipInstallLocal(ctx, "hdlscw_python", "repos/hdlscw/python")
    PythonPipInstallLocal(ctx, "hdlscw_python", "repos/hdlscw/python")
    PythonPipInstallLocal(ctx, "chext-test_python", "repos/chext-test/python")
    PythonPipInstallLocal(ctx, "sctlm_python", "repos/sctlm/python")

    PythonPipInstall(ctx, "plotting_stuff", ["numpy", "matplotlib"])

    CMakeLocal(ctx, "hdlscw_cpp", "repos/hdlscw/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "chext-test_cpp", "repos/chext-test/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    CMakeLocal(ctx, "sctlm_cpp", "repos/sctlm/cpp", cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ], cmake_install_mode="ABS_SYMLINK")

    SbtPublishLocal(ctx, "hdlinfo_scala", "repos/hdlinfo/scala")
    SbtPublishLocal(ctx, "chext_scala", "repos/chext")

    InstallFiles(ctx, ["bin/activate-hdlstuff.sh"])

    ctx.run()
    ctx.log(f"Please activate the environment using: '. {ctx.prefix("bin/activate-hdlstuff.sh")}'")
    ctx.remove_logs()


install()
