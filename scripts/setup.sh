#!/usr/bin/env bash

echo "[*] Starting setup..."

echo "[*] Checking dependencies..."
if [[ "$OSTYPE" == "win32" ]];
then
  echo "[!] Unable to setup on windows. Sorry.";
  exit 1;
fi

which python 1> /dev/null || {
  echo "[!] Please install python before setup.";
  exit 1;
};

which poetry 1> /dev/null || {
  echo "[!] Please install poetry before setup.";
  exit 1;
};

which direnv 1> /dev/null || {
  echo "[!] Please install direnv before setup.";
};


echo "[*] Installing developer libraries..."
version=$(python -V | awk -F ' ' '{print $2}');
poetry env use "${version}";
poetry install --with=dev
pre-commit install
echo "[*] In the Age of Ancients the world was unformed, shrouded by fog..."
