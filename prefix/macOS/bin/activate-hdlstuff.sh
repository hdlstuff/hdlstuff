#!/bin/bash

declare -A _HDLSTUFF_OLD_ENV_VARS

hdlstuff_set_var() {
    local var_name="$1"
    local new_value="$2"

    if [[ -v "$var_name" && -z "${_HDLSTUFF_OLD_ENV_VARS[$var_name]}" ]]; then
        _HDLSTUFF_OLD_ENV_VARS[$var_name]="${!var_name}"
    fi

    export "$var_name"="$new_value"
}

hdlstuff_reset_var() {
    local var_name="$1"

    if [[ -v "_HDLSTUFF_OLD_ENV_VARS[$var_name]" ]]; then
        export "$var_name"="${_HDLSTUFF_OLD_ENV_VARS[$var_name]}"
        unset "_HDLSTUFF_OLD_ENV_VARS[$var_name]"
    else
        unset "$var_name"
    fi
}

hdlstuff_activate() {
    hdlstuff_set_var "HDLSTUFF_PREFIX" "$(realpath "$(dirname "${BASH_SOURCE[0]}")/..")"
    hdlstuff_set_var "HDLSTUFF_REPO" "$(cat "$HDLSTUFF_PREFIX/.hdlstuff_repo")"

    hdlstuff_set_var "VIRTUAL_ENV" "$HDLSTUFF_PREFIX"
    hdlstuff_set_var "PYTHONHOME" ""

    hdlstuff_set_var "PATH" "$HDLSTUFF_PREFIX/bin:$PATH"
    hdlstuff_set_var "LD_LIBRARY_PATH" "$HDLSTUFF_PREFIX/lib:$LD_LIBRARY_PATH"

    hdlstuff_set_var "SBT_OPTS" "-Dsbt.ivy.home=$HDLSTUFF_PREFIX/.ivy2 $SBT_OPTS"

    hdlstuff_set_var "PS1" "(hdlstuff) $PS1"

    hash -r 2>/dev/null
}

hdlstuff_deactivate() {
    hdlstuff_reset_var "HDLSTUFF_PREFIX"
    hdlstuff_reset_var "HDLSTUFF_REPO"

    hdlstuff_reset_var "VIRTUAL_ENV"
    hdlstuff_reset_var "PYTHONHOME"

    hdlstuff_reset_var "PATH"
    hdlstuff_reset_var "LD_LIBRARY_PATH"

    hdlstuff_reset_var "SBT_OPTS"

    hdlstuff_reset_var "PS1"

    unset hdlstuff_deactivate
    unset hdlstuff_set_var
    unset hdlstuff_reset_var

    hash -r 2>/dev/null
}

if [[ -n "${_HDLSTUFF_OLD_ENV_VARS["PATH"]}" || -n "${_HDLSTUFF_OLD_ENV_VARS["LD_LIBRARY_PATH"]}" ]]; then
    echo "hdlstuff environment is already active."
    return 0
fi

hdlstuff_activate
unset hdlstuff_activate
