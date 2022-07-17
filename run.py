#!/usr/bin/python3

from os import getcwd
import sys

sys.path.append(getcwd())
from chat_app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)