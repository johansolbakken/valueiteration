import numpy as np

from printer import *
from PIL import Image


def make_board():
    board = np.zeros((3, 4))
    board[1, 1] = -np.inf
    board[0, 3] = 1
    board[1, 3] = -1
    return board


def make_policy():
    policy = np.zeros((3, 4))
    for y in range(3):
        for x in range(4):
            policy[y, x] = NORTH
    policy[1, 1] = -np.inf
    policy[0, 3] = -np.inf
    policy[1, 3] = -np.inf
    return policy


def get_value(board, direction, x, y):
    if direction == NORTH and y < 0:
        return 0
    if direction == EAST and x > 3:
        return 0
    if direction == SOUTH and y > 2:
        return 0
    if direction == WEST and x < 0:
        return 0
    if board[y, x] == -np.inf:
        return 0
    return board[y, x]


def policy_evaluation_step(board, policy):
    new_board = make_board()
    for y in range(3):
        for x in range(4):
            if board[y, x] == -np.inf or (x == 3 and y == 0) or (x == 3 and y == 1):
                continue
            if policy[y, x] == NORTH:
                new_board[y, x] = 0.8 * get_value(board, NORTH, x, y - 1) + 0.1 * get_value(board, EAST, x + 1,
                                                                                            y) + 0.1 * get_value(board,
                                                                                                                 WEST,
                                                                                                                 x - 1,
                                                                                                                 y)
            elif policy[y, x] == EAST:
                new_board[y, x] = 0.8 * get_value(board, EAST, x + 1, y) + 0.1 * get_value(board, NORTH, x,
                                                                                           y - 1) + 0.1 * get_value(
                    board, SOUTH, x, y + 1)
            elif policy[y, x] == SOUTH:
                new_board[y, x] = 0.8 * get_value(board, SOUTH, x, y + 1) + 0.1 * get_value(board, EAST, x + 1,
                                                                                            y) + 0.1 * get_value(board,
                                                                                                                 WEST,
                                                                                                                 x - 1,
                                                                                                                 y)
            elif policy[y, x] == WEST:
                new_board[y, x] = 0.8 * get_value(board, WEST, x - 1, y) + 0.1 * get_value(board, NORTH, x,
                                                                                           y - 1) + 0.1 * get_value(
                    board, SOUTH, x, y + 1)
            new_board[y, x] = new_board[y, x] * 0.9
    return new_board


def policy_evaluation(board, policy):
    print("---- POLICY EVALUATION ----")
    new_board = policy_evaluation_step(board, policy)
    i = 1
    while not np.allclose(board, new_board):
        board = new_board
        new_board = policy_evaluation_step(board, policy)
        print(f"iteration {i}")
        i += 1
    return new_board


def policy_improvement(board, policy):
    new_policy = make_policy()
    for y in range(3):
        for x in range(4):
            if board[y, x] == -np.inf or (x == 3 and y == 0) or (x == 3 and y == 1):
                continue
            north = 0.8 * get_value(board, NORTH, x, y - 1) + 0.1 * get_value(board, EAST, x + 1, y) + 0.1 * get_value(
                board, WEST, x - 1, y)
            east = 0.8 * get_value(board, EAST, x + 1, y) + 0.1 * get_value(board, NORTH, x, y - 1) + 0.1 * get_value(
                board, SOUTH, x, y + 1)
            south = 0.8 * get_value(board, SOUTH, x, y + 1) + 0.1 * get_value(board, EAST, x + 1, y) + 0.1 * get_value(
                board, WEST, x - 1, y)
            west = 0.8 * get_value(board, WEST, x - 1, y) + 0.1 * get_value(board, NORTH, x, y - 1) + 0.1 * get_value(
                board, SOUTH, x, y + 1)
            if north > east and north > south and north > west:
                new_policy[y, x] = NORTH
            elif east > north and east > south and east > west:
                new_policy[y, x] = EAST
            elif south > north and south > east and south > west:
                new_policy[y, x] = SOUTH
            elif west > north and west > east and west > south:
                new_policy[y, x] = WEST
    return new_policy


def list_of_pngs_to_mp4(images, output_path, duration=200):
    # Create an empty list to store the frames
    frames = []

    for image_path in images:
        # Open each image and convert it to RGBA format
        img = Image.open(image_path).convert("RGBA")
        frames.append(img)

    # Save the frames as an animated GIF
    frames[0].save(output_path, format="GIF",
                   append_images=frames[1:],
                   save_all=True,
                   duration=duration,
                   loop=0)



def policy_iteration():
    img_names = []
    policy = make_policy()
    board = make_board()
    i = 0
    print_board_and_policy(board, policy, f"policy_iteration_{i}")
    img_names.append(f"policy_iteration_{i}.png")
    i += 1
    new_board = policy_evaluation(board, policy)
    new_policy = policy_improvement(new_board, policy)
    print("---- POLICY ITERATION ----")
    while not np.allclose(policy, new_policy):
        policy = new_policy
        board = new_board
        new_board = policy_evaluation(board, policy)
        new_policy = policy_improvement(new_board, policy)
        print_board_and_policy(board, policy, f"policy_iteration_{i}")
        img_names.append(f"policy_iteration_{i}.png")
        i += 1
    list_of_pngs_to_mp4(img_names, "policy_iteration.gif", duration=1000)


def main():
    policy_iteration()


if __name__ == "__main__":
    main()
