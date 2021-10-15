$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

try {
  # redirect stderr into stdout
  $p = & { python -V } 2>&1

  if ($p -match "Python") {
    Write-Host "Installing VirtualEnv..."
    # install virtualenv  
    python -m pip install virtualenv

    Write-Host "Creating VirtualEnv..."
    # create virtualenv
    virtualenv .venv

    Write-Host "Activating VirtualEnv..."
    # activate virtualenv
    .\.venv\Scripts\activate

    Write-Host "Installing Dependencies..."
    # install dependencies
    python -m pip install -r .\requirements.txt

    # deactivate virtualenv
    deactivate
  }
  else {
    Write-Host "No Python installation found"
  }
}
finally {
  $prevPwd | Set-Location
}
