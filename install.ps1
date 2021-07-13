$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

try {
  # redirect stderr into stdout
  $p = & { python -V } 2>&1

  if ($p -match "Python") {
    # upgrade pip to its latest version  
    python -m pip install --upgrade pip   
    
    # install virtualenv  
    python -m pip install virtualenv

    # create virtualenv
    python -m virtualenv .venv

    # activate virtualenv
    .\.venv\Scripts\activate

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
