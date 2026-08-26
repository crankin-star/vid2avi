Yes. In PowerShell, you can activate the virtual environment, run the script from its path while preserving the current working directory, then deactivate it afterward:

function Run-MyScript {
    & "C:\path\to\venv\Scripts\Activate.ps1"
    python "C:\path\to\script.py"
    $exitCode = $LASTEXITCODE
    deactivate
    return $exitCode
}


However, there's an even cleaner approach: you don't actually need to activate the environment to run its Python interpreter. This avoids any issues with activation/deactivation state:

function Run-MyScript {
    & "C:\path\to\venv\Scripts\python.exe" "C:\path\to\script.py"
    return $LASTEXITCODE
}


I'd recommend the second version. It:

Uses the Python interpreter from the virtual environment.
Runs the script with the current directory unchanged, so cwd is exactly where you invoked the function.
Doesn't modify your PowerShell environment.
Preserves the Python script's exit code.
Doesn't require Activate.ps1 or deactivate.

If you specifically want the activation/deactivation behavior for other reasons, the first version is fine.
