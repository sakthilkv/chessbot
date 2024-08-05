import chess
import chess.engine
from board_reader import get_fen, make_move
import time

active_player = input().strip()

engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")
engine.configure({"Skill Level": 20})
previous_fen = None

while True:
    try:
        current_fen = get_fen() + f" {active_player} - - 0 1"
        if current_fen != previous_fen:
            print("Current FEN:", current_fen)
            board = chess.Board(current_fen)
            result = engine.play(board, chess.engine.Limit(time=10.0))
            print("Best move:", result.move)
            make_move(str(result.move))
            previous_fen = current_fen
        time.sleep(5)
    except (chess.engine.EngineError, chess.engine.EngineTerminatedError, chess.engine.EngineStateError) as e:
        print(f"Engine error: {e}. Skipping this loop iteration.")
        continue
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Skipping this loop iteration.")
        continue

engine.quit()
