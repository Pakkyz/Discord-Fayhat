import discord
from discord import message
from discord.ext import commands
import random
import asyncio

board = []
num_of_rows = 18
num_of_cols = 10
empty_square = ':black_large_square:'
blue_square = ':blue_square:'
brown_square = ':brown_square:'
orange_square = ':orange_square:'
yellow_square = ':yellow_square:'
green_square = ':green_square:'
purple_square = ':purple_square:'
red_square = ':red_square:'
embed_colour = 0x077ff7
points = 0
lines = 0
down_pressed = False
rotate_clockwise = False
rotation_pos = 0
h_movement = 0
is_new_shape = False
start_higher = False
game_over = False
index = 0


class Tetronimo:
    def __init__(self, starting_pos, colour, rotation_points):
        self.starting_pos = starting_pos
        self.colour = colour
        self.rotation_points = rotation_points


main_wall_kicks = [
    [[0, 0], [0, -1], [-1, -1], [2, 0], [2, -1]],
    [[0, 0], [0, 1], [1, 1], [-2, 0], [-2, 1]],
    [[0, 0], [0, 1], [-1, 1], [2, 0], [2, 1]],
    [[0, 0], [0, -1], [1, -1], [-2, 0], [-2, -1]]
]

i_wall_kicks = [
    [[0, 0], [0, -2], [0, 1], [1, -2], [-2, 1]],
    [[0, 0], [0, -1], [0, 2], [-2, -1], [1, 2]],
    [[0, 0], [0, 2], [0, -1], [-1, 2], [2, -1]],
    [[0, 0], [0, 1], [0, -2], [2, 1], [-1, -2]]
]

rot_adjustments = {

    ':blue_square:': [[0, 1], [-1, -1], [0, 0], [-1, 0]],

    ':brown_square:': [[0, 0], [0, 1], [0, 0], [0, -1]],

    ':orange_square:': [[0, -1], [0, 0], [-1, 1], [0, 0]],

    ':yellow_square:': [[0, 0], [0, 0], [0, 0], [0, 0]],

    ':green_square:': [[0, 0], [0, 0], [0, 0], [0, 0]],

    ':purple_square:': [[0, 0], [1, 1], [0, -1], [0, 1]],

    ':red_square:': [[1, -1], [-1, -1], [0, 2], [-1, -1]]
}

shape_I = Tetronimo([[0, 3], [0, 4], [0, 5], [0, 6]], blue_square, [1, 1, 1, 1])
shape_J = Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 3]], brown_square, [1, 1, 2, 2])
shape_L = Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 5]], orange_square, [1, 2, 2, 1])
shape_O = Tetronimo([[0, 4], [0, 5], [-1, 4], [-1, 5]], yellow_square, [1, 1, 1, 1])
shape_S = Tetronimo([[0, 3], [0, 4], [-1, 4], [-1, 5]], green_square, [2, 2, 2, 2])
shape_T = Tetronimo([[0, 3], [0, 4], [0, 5], [-1, 4]], purple_square, [1, 1, 3, 0])
shape_Z = Tetronimo([[0, 4], [0, 5], [-1, 3], [-1, 4]], red_square, [0, 1, 0, 2])


def make_empty_board():
    for row in range(num_of_rows):
        board.append([])
        for col in range(num_of_cols):
            board[row].append(empty_square)


def fill_board(emoji):
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            if board[row][col] != emoji:
                board[row][col] = emoji


def format_board_as_str():
    board_as_str = ''
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            board_as_str += (board[row][col])
            if col == num_of_cols - 1:
                board_as_str += "\n "
    return board_as_str


def get_random_shape():
    global index

    shapes = [shape_I, shape_J, shape_L, shape_O, shape_S, shape_T, shape_Z]
    random_shape = shapes[random.randint(0, 6)]
    index += 1
    if start_higher == True:
        for s in random_shape.starting_pos[:]:
            s[0] = s[0] - 1
    else:
        starting_pos = random_shape.starting_pos[:]
    random_shape = [random_shape.starting_pos[:], random_shape.colour, random_shape.rotation_points]
    global is_new_shape
    is_new_shape = True
    return random_shape


def do_wall_kicks(shape, old_shape_pos, shape_colour, attempt_kick_num):
    new_shape_pos = []

    if shape_colour == blue_square:
        kick_set = main_wall_kicks[rotation_pos]
    else:
        kick_set = i_wall_kicks[rotation_pos]

    print('Kick set: ' + str(kick_set))
    for kick in kick_set:
        print('Kick: ' + str(kick))
        for square in shape:
            square_row = square[0]
            square_col = square[1]
            new_square_row = square_row + kick[0]
            new_square_col = square_col + kick[1]
            if (0 <= new_square_col < num_of_cols) and (0 <= new_square_row < num_of_rows):
                square_checking = board[new_square_row][new_square_col]
                if (square_checking != empty_square) and ([new_square_row, new_square_col] not in old_shape_pos):

                    new_shape_pos = []
                    break
                else:
                    new_shape_pos.append([new_square_row, new_square_col])
                    print('New shape: ' + str(new_shape_pos))
                    if len(new_shape_pos) == 4:
                        print('Returned new shape after doing kicks')
                        return new_shape_pos
            else:

                new_shape_pos = []
                break

    print('Returned old, unrotated shape')
    return old_shape_pos


def rotate_shape(shape, direction, rotation_point_index, shape_colour):
    rotation_point = shape[rotation_point_index]
    new_shape = []

    for square in shape:
        square_row = square[0]
        square_col = square[1]
        if direction == 'clockwise':
            new_square_row = (square_col - rotation_point[1]) + rotation_point[0] + \
                             rot_adjustments.get(shape_colour)[rotation_pos - 1][0]
            print('Adjustment made: ' + str(rot_adjustments.get(shape_colour)[rotation_pos - 1][0]))
            new_square_col = -(square_row - rotation_point[0]) + rotation_point[1] + \
                             rot_adjustments.get(shape_colour)[rotation_pos - 1][1]
            print('Adjustment made: ' + str(rot_adjustments.get(shape_colour)[rotation_pos - 1][1]))
        elif direction == 'anticlockwise':
            new_square_row = -(square_col - rotation_point[1]) + rotation_point[0]
            new_square_col = (square_row - rotation_point[0]) + rotation_point[1]
        new_shape.append([new_square_row, new_square_col])
        if (0 <= square_col < num_of_cols) and (0 <= square_row < num_of_rows):
            board[square_row][square_col] = empty_square

    new_shape = do_wall_kicks(new_shape, shape, shape_colour, 0)

    new_shape = sorted(new_shape, key=lambda l: l[0], reverse=True)
    print('Rotated shape: ' + str(new_shape))

    if new_shape != shape:
        for square in new_shape:
            square_row = square[0]
            square_col = square[1]
            board[square_row][square_col] = shape_colour

    return new_shape


def clear_lines():
    global board
    global points
    global lines
    lines_to_clear = 0
    for row in range(num_of_rows):
        row_full = True
        for col in range(num_of_cols):
            if board[row][col] == empty_square:
                row_full = False
                break
        if row_full:
            lines_to_clear += 1

            board2 = board[:]
            for r in range(row, 0, -1):
                if r == 0:
                    for c in range(num_of_cols):
                        board2[r][c] = empty_square
                else:
                    for c in range(num_of_cols):
                        board2[r][c] = board[r - 1][c]
            board = board2[:]
    if lines_to_clear == 1:
        points += 100
        lines += 1
    elif lines_to_clear == 2:
        points += 300
        lines += 2
    elif lines_to_clear == 3:
        points += 500
        lines += 3
    elif lines_to_clear == 4:
        points += 800
        lines += 4


def get_next_pos(cur_shape_pos):
    global h_movement
    global start_higher
    global game_over

    movement_amnt = 1

    if down_pressed == False:
        amnt_to_check = 1
    else:
        amnt_to_check = num_of_rows

    for i in range(amnt_to_check):
        square_num_in_shape = -1
        for square in cur_shape_pos:
            next_space_free = True
            square_num_in_shape += 1
            square_row = square[0]
            square_col = square[1]
            if (0 <= square_col < num_of_cols):
                if not (0 <= square_col + h_movement < num_of_cols):
                    h_movement = 0
                if (0 <= square_row + movement_amnt < num_of_rows):
                    square_checking = board[square_row + movement_amnt][square_col + h_movement]
                    if (square_checking != empty_square) and ([square_row + movement_amnt,
                                                               square_col + h_movement] not in cur_shape_pos):  # if square is not empty / won't be when other parts of shape have moved

                        h_movement = 0
                        square_checking = board[square_row + movement_amnt][square_col + h_movement]
                        if (square_checking != empty_square) and (
                                [square_row + movement_amnt, square_col + h_movement] not in cur_shape_pos):
                            if movement_amnt == 1:
                                next_space_free = False
                                print('Detected a space that isnt free')
                                print('Square checking: ' + str(square_row + movement_amnt) + ', ' + str(
                                    square_col + h_movement))
                                if is_new_shape:
                                    if start_higher == True:
                                        game_over = True
                                    else:
                                        start_higher = True
                            elif movement_amnt > 1:
                                movement_amnt -= 1
                            return [movement_amnt, next_space_free]
                    elif down_pressed == True:
                        if square_num_in_shape == 3:
                            movement_amnt += 1
                elif square_row + movement_amnt >= num_of_rows:
                    if movement_amnt == 1:
                        next_space_free = False
                        print('Detected a space that isnt free')
                    elif movement_amnt > 1:
                        movement_amnt -= 1
                    return [movement_amnt, next_space_free]
                elif down_pressed == True:
                    if square_num_in_shape == 3:
                        movement_amnt += 1

    return [movement_amnt, next_space_free]


async def run_game(msg, cur_shape):
    global is_new_shape
    global h_movement
    global rotate_clockwise
    global rotation_pos

    cur_shape_pos = cur_shape[0]
    cur_shape_colour = cur_shape[1]

    if rotate_clockwise == True and cur_shape_colour != yellow_square:
        cur_shape_pos = rotate_shape(cur_shape_pos, 'clockwise', cur_shape[2][rotation_pos], cur_shape_colour)
        cur_shape = [cur_shape_pos, cur_shape_colour, cur_shape[2]]

    next_pos = get_next_pos(cur_shape_pos)[:]
    movement_amnt = next_pos[0]
    next_space_free = next_pos[1]

    square_num_in_shape = -1
    if next_space_free:
        for square in cur_shape_pos:
            square_num_in_shape += 1
            square_row = square[0]
            square_col = square[1]
            if (0 <= square_row + movement_amnt < num_of_rows):
                square_changing = board[square_row + movement_amnt][square_col + h_movement]
                board[square_row + movement_amnt][square_col + h_movement] = cur_shape_colour
                if is_new_shape == True:
                    is_new_shape = False
                if square_row > -1:
                    board[square_row][square_col] = empty_square
                cur_shape_pos[square_num_in_shape] = [square_row + movement_amnt, square_col + h_movement]
            else:
                cur_shape_pos[square_num_in_shape] = [square_row + movement_amnt, square_col + h_movement]
    else:
        global down_pressed
        down_pressed = False
        clear_lines()
        cur_shape = get_random_shape()
        rotation_pos = 0
        print('Changed shape.')

    if not game_over:

        embed = discord.Embed(description=format_board_as_str(), color=embed_colour)
        h_movement = 0
        rotate_clockwise = False
        await msg.edit(embed=embed)
        if not is_new_shape:
            await asyncio.sleep(1)
        await run_game(msg, cur_shape)
    else:
        print('GAME OVER')
        desc = 'Score: {} \n Lines: {} \n \n Press ▶ to play again.'.format(points, lines)
        embed = discord.Embed(title='GAME OVER', description=desc, color=embed_colour)
        await msg.edit(embed=embed)
        await msg.remove_reaction("⬅", client.user)
        await msg.remove_reaction("⬇", client.user)
        await msg.remove_reaction("➡", client.user)
        await msg.remove_reaction("🔃", client.user)
        await msg.add_reaction("▶")


async def reset_game():
    global down_pressed
    global rotate_clockwise
    global rotation_pos
    global h_movement
    global is_new_shape
    global start_higher
    global game_over
    global points
    global lines
    fill_board(empty_square)
    down_pressed = False
    rotate_clockwise = False
    rotation_pos = 0
    h_movement = 0
    is_new_shape = False
    start_higher = False
    game_over = False
    next_space_free = True
    points = 0
    lines = 0


make_empty_board()

# -------------------------------------------------------------------------------

client = commands.Bot(command_prefix='v!')


@client.event
async def on_ready():
    print("tetris bot started poggies")


@client.command()
async def test(ctx):
    await ctx.send('test working poggies pogchamp')


@client.command()
async def start(ctx):
    await reset_game()
    embed = discord.Embed(title='Tetris in Discord', description=format_board_as_str(), color=embed_colour)
    embed.add_field(name='How to Play:',
                    value='Use ⬅ ⬇ ➡ to move left, down, and right respectively. \n  \n Use 🔃 to rotate the shape clockwise. \n \n Press ▶ to Play.',
                    inline=False)

    msg = await ctx.send(embed=embed)

    await msg.add_reaction("▶")


@client.event
async def on_reaction_add(reaction, user):
    global h_movement
    global rotation_pos
    if user != client.user:
        msg = reaction.message
        if str(reaction.emoji) == "▶":
            print('User pressed play')
            await reset_game()
            await msg.remove_reaction("❌", client.user)
            embed = discord.Embed(description=format_board_as_str(), color=embed_colour)
            await msg.remove_reaction("▶", user)
            await msg.remove_reaction("▶", client.user)
            await msg.edit(embed=embed)
            await msg.add_reaction("⬅")
            await msg.add_reaction("⬇")
            await msg.add_reaction("➡")
            await msg.add_reaction("🔃")
            await msg.add_reaction("❌")
            starting_shape = get_random_shape()
            await run_game(msg, starting_shape)

        if str(reaction.emoji) == "⬅":
            print('Left button pressed')
            h_movement = -1
            await msg.remove_reaction("⬅", user)
        if str(reaction.emoji) == "➡":
            print('Right button pressed')
            h_movement = 1
            await msg.remove_reaction("➡", user)
        if str(reaction.emoji) == "⬇":
            print('Down button pressed')
            global down_pressed
            down_pressed = True
            await msg.remove_reaction("⬇", user)
        if str(reaction.emoji) == "🔃":
            print('Rotate clockwise button pressed')
            global rotate_clockwise
            rotate_clockwise = True
            if rotation_pos < 3:
                rotation_pos += 1
            else:
                rotation_pos = 0
            await msg.remove_reaction("🔃", user)
        if str(reaction.emoji) == "❌":
            await reset_game()
            await msg.delete()
        if str(reaction.emoji) == "🔴":
            await message.edit(content="")



client.run('MTAwNDg3ODgxNTUyMjIwMTcwMQ.GkP4jc.J8zp1GPFS2ck4rXPuUSkPjtCnUialigDFpJF4A')