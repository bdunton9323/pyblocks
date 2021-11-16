#!/bin/bash
set -e

pyenv local 3.9.5
#sudo apt-get install --yes python3-venv

sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev python3-setuptools python3-dev python3 libportmidi-dev
sudo apt-get build-dep libsdl2 libsdl2-image libsdl2-mixer libsdl2-ttf libfreetype6 python3 libportmidi0

python -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install wheel
pip install pygame
pip install nose

echo "Use python game.py to start the game"
