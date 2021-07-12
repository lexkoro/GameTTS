# redirect stderr into stdout
$p = &{python -V} 2>&1

if ($p -match "Python"){
    # upgrade pip to its latest version  
    python -m pip install --upgrade pip   
  
    # install virtualenv  
    python -m pip install virtualenv

    # install dependencies
    python -m pip install -r .\requirements.txt
}else{
    Write-Host "No Python installation found"
}
