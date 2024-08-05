# ChessBot using OpenCV and Stockfish

ChessBot is an intelligent chess-playing application that leverages OpenCV to read the screen, detect a chessboard, and interact with a chess engine (Stockfish) to play moves based on the bot's color.

## Features

- **Screen Reading**: Uses OpenCV to capture the screen and detect the chessboard.
- **Move Detection**: Identifies the current state of the board and detects the opponent's moves.
- **Bot Interaction**: Interacts with the Stockfish chess engine to calculate and play the best move.
- **Color-Based Play**: Configurable to play as either white or black.

## Requirements

- Python 3.x
- OpenCV
- Stockfish engine
- chess library
- numpy

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/sakthilkv/chessbot.git
    cd chessbot
    ```

2. **Install dependencies**:
    ```sh
    pip install opencv-python chess numpy
    ```

3. **Download Stockfish**:
    Download the Stockfish engine from the [official website](https://stockfishchess.org/download/) and place the executable in the project directory.

## Usage

1. **Setup and Run**:
    ```sh
    python chessbot.py
    ```

2. **Input Bot Color**:
    When prompted, input the bot's color:
    - `w` for white
    - `b` for black

## How It Works

1. **Screen Reading**:
    - Captures the screen using OpenCV.
    - Detects the chessboard and extracts the current state.

2. **Move Detection**:
    - Compares the current state with the previous state to detect moves.
    - Uses the `chess` library to validate moves and update the board state.

3. **Bot Interaction**:
    - Configures and interacts with the Stockfish engine to get the best move.
    - Plays the calculated move on the screen using OpenCV.

4. **Color-Based Play**:
    - The bot plays according to the specified color and waits for the opponent's move before making the next move.

## Acknowledgments

- [Stockfish](https://stockfishchess.org) for providing the powerful chess engine.
- [OpenCV](https://opencv.org) for the computer vision library.
- The Python [chess](https://python-chess.readthedocs.io/) library for chess-related functionalities.
