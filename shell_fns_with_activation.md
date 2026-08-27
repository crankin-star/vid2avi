<!-- Copied from chatGPT 'cause I don't care enough about these languages to figure all this out. -->
Yep. I'd make --activate an option consumed by the shell function, with everything else passed through to Python. That means, for example:

run_my_script --dir ./foo --format json csv
run_my_script --activate --dir ./foo --format json csv

zsh
run_my_script() {
    local activate=false

    if [[ "$1" == "--activate" ]]; then
        activate=true
        shift
    fi

    if $activate; then
        source "/path/to/venv/bin/activate"
        python "/path/to/script.py" "$@"
        local exit_code=$?
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" "$@"
    fi
}

Bash
run_my_script() {
    local activate=false

    if [[ "$1" == "--activate" ]]; then
        activate=true
        shift
    fi

    if $activate; then
        source "/path/to/venv/bin/activate"
        python "/path/to/script.py" "$@"
        local exit_code=$?
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" "$@"
    fi
}

Fish
function run_my_script
    set activate false

    if test "$argv[1]" = "--activate"
        set activate true
        set -e argv[1]
    end

    if $activate
        source "/path/to/venv/bin/activate.fish"
        python "/path/to/script.py" $argv
        set exit_code $status
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" $argv
    end
end

PowerShell
function Run-MyScript {
    param(
        [switch]$Activate,
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$ScriptArgs
    )

    if ($Activate) {
        & "C:\path\to\venv\Scripts\Activate.ps1"
        python "C:\path\to\script.py" @ScriptArgs
        $exitCode = $LASTEXITCODE
        deactivate
        return $exitCode
    }
    else {
        & "C:\path\to\venv\Scripts\python.exe" "C:\path\to\script.py" @ScriptArgs
        return $LASTEXITCODE
    }
}

Usage

Without activation:

run_my_script --dir ./some-directory --format foo bar baz


With activation:

run_my_script --activate --dir ./some-directory --format foo bar baz


The shift/argument removal in the Unix shells and the -Activate parameter in PowerShell ensure that --activate doesn't get passed to Python.

One nice property of this setup is that --format can consume as many arguments as your Python argparse configuration allows; the shell function doesn't need to know or care about its syntax.
