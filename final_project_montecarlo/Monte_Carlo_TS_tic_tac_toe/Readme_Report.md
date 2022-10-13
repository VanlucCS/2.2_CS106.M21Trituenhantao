**report**
# Source code Alpha Zero use Monte Carlo Tree Search - mcts.py
AlphaZero implementation based on ["Mastering the game of Go without human knowledge"](https://www.deepmind.com/publications/mastering-the-game-of-go-without-human-knowledge) and ["Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm"](https://arxiv.org/abs/1712.01815).

***CS106.M21-*-group member:**
`   Trần Văn Lực	        20521587	20521587@gm.uit.edu.vn `
`   Lê Minh Quân	        20520709	20520709@ms.uit.edu.vn `
`   Lê Nguyễn Bảo Hân	        20520174	20520174@gm.uit.edu.vn `
`   Nguyễn Trần Minh Anh	20520394	20520394@gm.uit.edu.vn `

Games implemented:
0) Tic Tac Toe
1) Connect Four

## Requirements
 - TensorFlow
 - NumPy
 - Python 3
 
## Usage 
**To play a game vs the previous best model we trained**:
```
python main.py --load_model 1 --human_play 1 --game 0 --model_directory "./tic_tac_toe/models/"

python main.py --load_model 1 --human_play 1 --game 1 --model_directory "./connect_four/models/"

``` 
**To play game "tic tac toe" with the previous best model we trained but this version have interface**:
```
python main.py --load_model 1 --human_play 1 --game 0 --gameUI_tic_tac_toe 1 --model_directory "./tic_tac_toe/models/"
``` 

**Options**:
* `--model_directory`: Name of the directory to store models.
* `--load_model`: Binary to initialize the network with the best model.
* `--human_play`: Binary to play as a Human vs the AI.
* `--game`: Number of the game. 0: Tic Tac Toe, 1: connect four.
* `--gameUI_tic_tac_toe`: Binary to play as a Human vs the AI with version have interface.