<!--Response from chatGPT, because I don't care enough about zsh to write this myself-->

Absolutely. Since the script should run against the current working directory, you don't need to cd anywhere. A simple zsh function is:

run_my_script() {
    source "/path/to/your/venv/bin/activate"
    python "/path/to/your/script.py"
    deactivate
}


However, there's one improvement I'd recommend: use "$VIRTUAL_ENV/bin/python" rather than relying on the python command after activation. This makes it explicit that you're running the Python interpreter from that virtual environment:

run_my_script() {
    source "/path/to/your/venv/bin/activate"
    python "/path/to/your/script.py"
    local exit_code=$?
    deactivate
    return $exit_code
}


The exit_code bit is useful because it ensures that if the script fails, the function still deactivates the environment and then returns the script's original exit status.

Put the function in ~/.zshrc, replacing the two paths with your actual paths, then run:

source ~/.zshrc


After that, just run:

run_my_script


Your current directory remains unchanged throughout.
