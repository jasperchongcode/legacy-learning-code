import chess
import chess.engine
import os
import sys

arguments = sys.argv
pondertime = float(arguments[1]) #first argument: ponder time in sec
maxmoves = int(arguments[2]) #2nd argument: max number of desired moves
gamecount = int(arguments[3]) #3rd argument: max number of games to play
#here we assume the engine file is in same folder as our python script
path = os.getcwd()
#Now make sure you give the correct location for your stockfish engine file
#...in the line that follows by correctly defining path
engine = chess.engine.SimpleEngine.popen_uci(path+'/'+'Stockfish-sf_15.1')

dictsidetomove = {True:'white',False:'black'}
notationdict = {True:'.', False:'...'}

for i in range(gamecount):
    board = chess.Board() #give whatever starting position here
    while not board.is_game_over() and board.fullmove_number<=maxmoves:
        result = engine.play(board,chess.engine.Limit(time=pondertime))
        print(dictsidetomove[board.turn]+' played '+str(board.fullmove_number)+notationdict[board.turn]+str(board.san(result.move)))
        board.push(result.move)
    print('Iteration '+str(i+1)+'-----')
    print(board)
    print('Final position FEN: ',board.fen())
    print('-----')

engine.quit()