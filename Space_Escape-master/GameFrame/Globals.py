
class Globals:

    running = True
    FRAMES_PER_SECOND = 30

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 644
    



    # - Set the starting number of lives - #
    #Mr Hurwood, set it higher for your own sanity (i know i needed it)
    LIVES = 30
    #this is the starting number of lives, set it too be equal to LIVES
    total_lives = 30



    # - Set the Window display name - #
    window_name = "Joe's Escape"

    # - Set the order of the rooms - #
    levels = ["splash","lvl1","lvl2","lvl3","lvl4","lvl5","end_splash","end_splash_fail"]

    # - Set the starting level - #
    start_level = 0

    # - Set this number to the level you want to jump to when the game ends - #
    end_game_level = 7
    
    # - This variable keeps track of the room that will follow the current room - #
    # - Change this value to move through rooms in a non-sequential manner - #
    next_level = 1

    # - Change variable to True to exit the program - #
    exiting = False


# ############################################################# #
# ###### User Defined Global Variables below this line ######## #
# ############################################################# #

    total_count = 0
    destroyed_count = 0
    score = 0
    monster_speed = 2
