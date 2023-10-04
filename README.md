# Game Theory: Battle Bots

## Installation

This project is using **Python v3.12.0** which is bundled with the conda environment.

### Setup

- Fork this repository and clone it on to your computer.

- Create the environment
```bash
$ conda create --file environment.yml
$ conda activate battle-bots
```

### Contribution

- Update the repository and activate the environment

```bash
$ git pull
$ conda activate battle-bots
$ conda env update
```

- Make a directory within the game directory

```bash
$ mkdir <game>/<your_name>
```

- Once finished, export the environment if you used any new libraries and push the repository.

```bash
$ conda env export --no-builds --file environment.yml
$ git push
```

## Evaluation

```bash
$ python <game>/evaluate.py
```
