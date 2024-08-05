import cv2
import numpy as np

def find_square_number(x, y, board_x, board_y, square_size):
    relative_x = x - board_x
    relative_y = y - board_y
    col = relative_x // square_size
    row = relative_y // square_size
    if 0 <= col < 8 and 0 <= row < 8:
        square_number = row * 8 + col
        return square_number
    else:
        return None

def template_match(board_image, template_path, threshold):
    img_rgb = cv2.imread(board_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    
    piece_positions = []
    marked_image = img_rgb.copy()
    
    for pt in zip(*loc[::-1]):
        piece_positions.append((pt[0], pt[1]))
        cv2.rectangle(marked_image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    
    return piece_positions, marked_image

def get_piece_positions(board_image, templates_and_thresholds, board_x, board_y, square_size):
    piece_map = {}
    final_image = cv2.imread(board_image)  # Read the original image to modify
    
    for template_path, threshold, piece_char in templates_and_thresholds:
        positions, marked_image = template_match(board_image, "pieces/" + template_path, threshold)
        for pos in positions:
            piece_number = find_square_number(pos[0], pos[1], board_x, board_y, square_size)
            if piece_number is not None:
                piece_map[piece_number] = piece_char
        
        # Overlay the marked image onto the final image
        final_image = cv2.bitwise_or(final_image, marked_image)
    
    return piece_map, final_image
    
def position_to_fen(piece_map):
    # Create an 8x8 chessboard with empty strings
    board = [['.' for _ in range(8)] for _ in range(8)]
    
    # Place pieces on the board
    for pos, piece in piece_map.items():
        row = (pos // 8)
        col = pos % 8
        board[row][col] = piece
    
    # Convert board to FEN
    fen_rows = []
    for row in board:
        empty_count = 0
        fen_row = ''
        for square in row:
            if square == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += square
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    
    return '/'.join(fen_rows)



import pyautogui

def get_square_coordinates(board_x, board_y, square_size, square_number):
    row = square_number // 8
    col = square_number % 8
    x = board_x + col * square_size + square_size // 2
    y = board_y + row * square_size + square_size // 2
    return (x, y)

def move_piece(source_square_number, destination_square_number, board_x, board_y, square_size):
    # Get coordinates for source and destination squares
    src_x, src_y = get_square_coordinates(board_x, board_y, square_size, source_square_number)
    dest_x, dest_y = get_square_coordinates(board_x, board_y, square_size, destination_square_number)
    
    # Perform the clicks using pyautogui
    pyautogui.click(src_x, src_y)  # Click on the source square
    pyautogui.click(dest_x, dest_y)  # Click on the destination square



def chess_notation_to_square_number(file, rank):
    # Convert chess notation to square number
    return (8 - int(rank)) * 8 + (ord(file) - ord('a'))

def uci_move_to_source_and_destination(uci_move):
    # UCI move format is usually like 'e2e4'
    source_square_notation = uci_move[:2]
    destination_square_notation = uci_move[2:]

    # Extract file and rank from notation
    src_file, src_rank = source_square_notation[0], source_square_notation[1]
    dest_file, dest_rank = destination_square_notation[0], destination_square_notation[1]

    # Convert to square numbers
    source_square_number = chess_notation_to_square_number(src_file, src_rank)
    destination_square_number = chess_notation_to_square_number(dest_file, dest_rank)

    return source_square_number, destination_square_number

board_x, board_y = 106, 186
square_size = 58

def make_move(uci_move):
	source_square, destination_square = uci_move_to_source_and_destination(uci_move)
	move_piece(source_square, destination_square, board_x, board_y, square_size)

def get_fen():
	screenshot = pyautogui.screenshot()
	screenshot.save('board.png')
	board_image = 'board.png'

	templates_and_thresholds = [
	    ('bp.png', 0.7, 'p'),
	    ('br.png', 0.705, 'r'),
	    ('bn.png', 0.660, 'n'),
	    ('bb.png', 0.679, 'b'),
	    ('bq.png', 0.685, 'q'),
	    ('bk.png', 0.670, 'k'),
	    ('wp.png', 0.657, 'P'),
	    ('wr.png', 0.705, 'R'),
	    ('wn.png', 0.660, 'N'),
	    ('wb.png', 0.679, 'B'),
	    ('wq.png', 0.685, 'Q'),
	    ('wk.png', 0.670, 'K')
	]

	piece_map, result_image = get_piece_positions(board_image, templates_and_thresholds, board_x, board_y, square_size)
	return position_to_fen(piece_map)
