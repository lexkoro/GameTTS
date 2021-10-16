#$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

try {
    # activate virtualenv
    .\.venv\Scripts\activate

    # run program
    python .\main.py

    # deactivate virtualenv
    deactivate
}
catch [System.SystemException] { "An error occurred." }

