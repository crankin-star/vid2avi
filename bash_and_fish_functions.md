Yep — bash is essentially the same as zsh for this use case. fish is different enough that the syntax changes.

Bash
run_my_script() {
    source "/path/to/venv/bin/activate"
    python "/path/to/script.py"
    local exit_code=$?
    deactivate
    return $exit_code
}


Or, as with PowerShell, you can skip activation entirely:

run_my_script() {
    "/path/to/venv/bin/python" "/path/to/script.py"
}


The latter is generally my preferred version. The script inherits the shell's current working directory, so there's no cd involved.

Fish

Fish's syntax is different:

function run_my_script
    source "/path/to/venv/bin/activate.fish"
    python "/path/to/script.py"
    set exit_code $status
    deactivate
    return $exit_code
end


And again, activation isn't actually necessary:

function run_my_script
    "/path/to/venv/bin/python" "/path/to/script.py"
end

One small distinction

The activation versions are useful if the script launches subprocesses that expect things like VIRTUAL_ENV or the virtual environment's bin/Scripts directory to be on PATH.

If all you need is "run this particular Python script using this particular venv," then the direct-interpreter versions are cleaner:

bash/zsh: /path/to/venv/bin/python
fish: /path/to/venv/bin/python
PowerShell: C:\path\to\venv\Scripts\python.exe

And in all three cases, the script's cwd remains whatever directory you were in when you invoked the function.
