from pprint import pprint
from state import GameStateAPI
import os

n = 3

def EXPECT_TRUE(condition: bool) -> None:
    if not condition:
        os.abort()
    

game_state_api = GameStateAPI(
    game_id="1", 
    players=["vincent", "huy"],
    n=n
)

def case1(): ## test win diagonals
    game_state_api.clear_game()
    print("--TEST CASE 1--")
    game_state_api.play(0,2,2)
    game_state_api.play(0,0,0)
    game_state_api.play(0,1,1)
    pprint(game_state_api.board)
    print("The winner is", game_state_api.check_winner())

    game_state_api.clear_game()
    game_state_api.play(1,0,2)
    game_state_api.play(1,2,0)
    game_state_api.play(1,1,1)
    pprint(game_state_api.board)
    print("The winner is", game_state_api.check_winner())

def case2(): ## test win row
    print("--TEST CASE 2--")
    for i in range(n):
        game_state_api.clear_game()
        game_state_api.play(0,i,0)
        game_state_api.play(0,i,1)
        game_state_api.play(0,i,2)
        print(game_state_api.board)
        print("The winner is", game_state_api.check_winner())
    
def case3(): ## test win col
    print("--TEST CASE 3--")
    for i in range(n):
        game_state_api.clear_game()
        game_state_api.play(1,0,i)
        game_state_api.play(1,1,i)
        game_state_api.play(1,2,i)
        # some other moves
        print(game_state_api.board)
        print("The winner is", game_state_api.check_winner())

if __name__ == "__main__":
    case1()
    case2()
    case3()