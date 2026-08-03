# hdlstuff installer

This repository installs the C++, Python, and Scala parts of the hdlstuff
projects into one prefix. The activation script configures `PATH`,
`CMAKE_PREFIX_PATH`, the Python virtual environment, and sbt's local Ivy
repository so consumers see one coherent development environment.

## Canonical package names

The naming rule is deliberately consistent across packaging systems:

- Installable Python distributions and Scala artifacts use an `hdlstuff_`
  prefix.
- Python import names and Scala package names remain short and idiomatic.
- Installed CMake targets use the `hdlstuff::` namespace.

| Component | CMake package | CMake target | Python distribution / import | sbt dependency / Scala package |
| --- | --- | --- | --- | --- |
| hdlstuff-hal | `hdlstuff_hal` | `hdlstuff::hal` | — | — |
| hdlinfo | `hdlstuff_hdlinfo` | `hdlstuff::hdlinfo` | `hdlstuff_hdlinfo` / `hdlinfo` | `"hdlstuff" %% "hdlstuff_hdlinfo" % "0.1.0"` / `hdlinfo` |
| hdlscw | `hdlscw` | `hdlstuff::hdlscw` | `hdlstuff_hdlscw` / `hdlscw` | — |
| chext-test | `chext_test` | `hdlstuff::chext_test` | `hdlstuff_chext_test` / `chext_test` | — |
| sctlm | `sctlm` | `hdlstuff::sctlm` | `hdlstuff_sctlm` / `sctlm` | — |
| chext | — | — | — | `"hdlstuff" %% "hdlstuff_chext" % "0.2.3"` / `chext` |

### CMake target matrix

The concrete target is used while building a repository; the exported target
is the stable name used by downstream projects after `find_package`.

| Repository | `project()` / concrete target | Kind | Installed library | `find_package` | Exported target |
| --- | --- | --- | --- | --- | --- |
| hdlstuff-hal | `hdlstuff_hal` / `hdlstuff_hal` | static | `libhdlstuff_hal.a` | `hdlstuff_hal` | `hdlstuff::hal` |
| hdlinfo/cpp | `hdlstuff_hdlinfo` / `hdlstuff_hdlinfo` | static | `libhdlstuff_hdlinfo.a` | `hdlstuff_hdlinfo` | `hdlstuff::hdlinfo` |
| hdlscw/cpp | `hdlstuff_hdlscw` / `hdlstuff_hdlscw` | interface | none | `hdlscw` | `hdlstuff::hdlscw` |
| chext-test/cpp | `hdlstuff_chext_test` / `hdlstuff_chext_test` | static | `libhdlstuff_chext_test.a` | `chext_test` | `hdlstuff::chext_test` |
| sctlm/cpp | `hdlstuff_sctlm` / `hdlstuff_sctlm` | static | `libhdlstuff_sctlm.a` | `sctlm` | `hdlstuff::sctlm` |

`chext/sysc_tb` contains local executable targets only; it does not install or
export a CMake library.

The CMake package name is the value passed to `find_package`; it does not have
to match the exported target name. For example:

```cmake
find_package(hdlstuff_hdlinfo REQUIRED)
find_package(hdlscw REQUIRED)
find_package(chext_test REQUIRED)

target_link_libraries(
    my_testbench
    PRIVATE
        hdlstuff::hdlinfo
        hdlstuff::hdlscw
        hdlstuff::chext_test
)
```

Python code continues to use the unprefixed imports:

```python
import chext_test
import hdlinfo
import hdlscw
import sctlm
```

## Install and activate

Run the script for the host platform from this repository, for example:

```sh
python3 ubuntu-24.04-x86_64.py
. "$HOME/.local/opt/hdlstuff/bin/activate-hdlstuff.sh"
```

The default prefix is `$HOME/.local/opt/hdlstuff`. Platform scripts install
the same hdlstuff components and use the canonical names in the table above.

The installer also handles renames during an in-place reinstall. It removes
legacy Python distributions and source-tree `*.egg-info`, old Ivy artifacts,
and stale absolute CMake symlinks before their build directories are replaced.
This prevents an apparently successful reinstall from leaving obsolete package
names or dangling files in the prefix.

## Migration from the old names

Compatibility aliases are intentionally not exported. Update consumers as
follows:

| Ecosystem | Old | Current |
| --- | --- | --- |
| CMake | `hdlstuff::hdlstuff_hal` | `hdlstuff::hal` |
| CMake | `hdlscw::hdlscw` | `hdlstuff::hdlscw` |
| CMake | `chext::chext_test` or `chext_test::chext_test` | `hdlstuff::chext_test` |
| CMake | `sctlm::sctlm` | `hdlstuff::sctlm` |
| Python distribution | `hdlinfo`, `hdlscw`, `chext_test`, `sctlm` | `hdlstuff_hdlinfo`, `hdlstuff_hdlscw`, `hdlstuff_chext_test`, `hdlstuff_sctlm` |
| Scala artifact | `hdlstuff:hdlinfo_2.13` | `hdlstuff:hdlstuff_hdlinfo_2.13` |
| Scala artifact | `hdlstuff:chext_2.13` | `hdlstuff:hdlstuff_chext_2.13` |

The Python imports and Scala package imports do not change.
