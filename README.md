# PyBlocks

This is a tetris-like game I wrote in python using the pygame framework.
This was my first "real" python project, and was largely done to teach myself python.
Since it was a learning project, there are many things I would do differently, but I am happy with the way it turned out.

## Setting up the prerequisites
I recommend installing pyenv to enable easy installing, and toggling between, different python versions.
The PyGame framework is particular about python versions. This has been tested with python 3.9.5.

To install the dependencies needed for pygame:
```shell
$ ./setup.sh
```
## Running the game
If the virtualenv is not activated yet (the setup script activates it), run:
```shell
$ source .venv/bin/activate
```
To run the game:
```shell
(.venv) $ python game.py
```

## Gameplay
The default key mappings are:
 - `z` - rotate left
 - `x` - rotate right
 - `space` - drop the piece
 - `esc` - go to menu

 

