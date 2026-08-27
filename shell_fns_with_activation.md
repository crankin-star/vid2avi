<!-- Copied from chatGPT 'cause I don't care enough about these languages to figure all this out. -->
Yep. I'd make --activate an option consumed by the shell function, with everything else passed through to Python. That means, for example:

```
run_my_script --dir ./foo --format json csv
run_my_script --activate --dir ./foo --format json csv
```

### zsh

```{zsh}
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
```

### Bash

``` {bash}
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
```

### Fish

```{fish}
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
```

### PowerShell

```{PowerShell}
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
```

## Usage

Without activation:

```{shell}
run_my_script --dir ./some-directory --format foo bar baz
```

With activation:

```{shell}
run_my_script --activate --dir ./some-directory --format foo bar baz
```

The shift/argument removal in the Unix shells and the -Activate parameter in PowerShell ensure that --activate doesn't get passed to Python.

One nice property of this setup is that --format can consume as many arguments as your Python argparse configuration allows; the shell function doesn't need to know or care about its syntax.

---

Yes — in that case we can make --activate a shell-only flag that can appear anywhere, and strip it out before passing the remaining arguments to Python.

For example, all of these would behave identically:

```{shell}
run_my_script --activate --dir ./foo --format json csv
run_my_script --dir ./foo --activate --format json csv
run_my_script --dir ./foo --format json csv --activate
```

### zsh
```{zsh}
run_my_script() {
    local activate=false
    local args=()

    for arg in "$@"; do
        if [[ "$arg" == "--activate" ]]; then
            activate=true
        else
            args+=("$arg")
        fi
    done

    if $activate; then
        source "/path/to/venv/bin/activate"
        python "/path/to/script.py" "${args[@]}"
        local exit_code=$?
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" "${args[@]}"
    fi
}
```

### Bash

```{bash}
run_my_script() {
    local activate=false
    local args=()

    for arg in "$@"; do
        if [[ "$arg" == "--activate" ]]; then
            activate=true
        else
            args+=("$arg")
        fi
    done

    if $activate; then
        source "/path/to/venv/bin/activate"
        python "/path/to/script.py" "${args[@]}"
        local exit_code=$?
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" "${args[@]}"
    fi
}
```

### Fish

```{fish}
function run_my_script
    set activate false
    set args

    for arg in $argv
        if test "$arg" = "--activate"
            set activate true
        else
            set -a args "$arg"
        end
    end

    if $activate
        source "/path/to/venv/bin/activate.fish"
        python "/path/to/script.py" $args
        set exit_code $status
        deactivate
        return $exit_code
    else
        "/path/to/venv/bin/python" "/path/to/script.py" $args
    end
end
```

### PowerShell

PowerShell can use a switch parameter, but to allow --activate anywhere while also forwarding arbitrary arguments, I'd handle it explicitly:


```{PowerShell}
function Run-MyScript {
    $activate = $false
    $scriptArgs = @()

    foreach ($arg in $args) {
        if ($arg -eq "--activate") {
            $activate = $true
        }
        else {
            $scriptArgs += $arg
        }
    }

    if ($activate) {
        & "C:\path\to\venv\Scripts\Activate.ps1"
        python "C:\path\to\script.py" @scriptArgs
        $exitCode = $LASTEXITCODE
        deactivate
        return $exitCode
    }
    else {
        & "C:\path\to\venv\Scripts\python.exe" "C:\path\to\script.py" @scriptArgs
        return $LASTEXITCODE
    }
}
```

One thing I particularly like about this approach is that the Python script never knows about --activate. The shell function consumes it completely, regardless of where it occurs.

So this:

```
run_my_script --dir ./foo --format json csv --activate
```

ultimately becomes equivalent to Python receiving:

```
--dir
./foo
--format
json
csv
```

with the venv activated while Python runs.
