# !/usr/bin/env bash
#

set -u
set -o pipefail
set -e 

env_path="${1:- .venv/game_tts}"
browser="${2:-firefox}"

# changing to this directory
cd "${0%/*}"


if ! which python3.8 &> /dev/null; then
	echo "Please install python3.8 first, then start the script again."
	exit 1
fi 
if [[ ! -f ".installed" ]]; then
	if [[ ! -d "$env_path" ]]; then 
		python3.8 -m venv $env_path
		source $env_path/bin/activate
		pip install -r requirements.txt
		touch ".installed"
		echo "installed dependencies"
	fi
fi

source $env_path/bin/activate
python main.py --browser $browser
