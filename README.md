# go-heuristic

Convolutional neural network based heuristic for Go Game, with minimax search algorithm and Alpha-Beta Pruning.

## Quick Start

Setup virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Start go game GUI
```
python3 main.py
```

GUI with minimax search algorithm and Alpha-Beta Pruning
* heavy computation, expect lag between each game play
```
python3 main.py --minimax --pruning
```

## Model Training

In `model` directory, run
* heavy computation, change settings in `main.py` for faster execution
```
python3 main.py
```

For testing with minimax search algorithm
* heavy computation, each simulated game will take around 2 minutes
```
python3 minimax.py
```
