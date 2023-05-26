import os

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def print_board_and_policy(board, policy, filename="table"):
    cell_width = 80
    cell_height = 30
    with open(f"{filename}.dot", "w") as f:
        # write board 3x4 matrix as a table
        f.write("digraph table {\n")
        # display file name
        f.write(f"  label=\"{filename}\";\n")
        f.write("  labelloc=\"t\";\n")
        f.write("  rankdir=LR;\n")
        f.write("  node [shape=plaintext];\n")
        f.write("  board [label=<\n")
        # cell width and height 100px
        f.write("    <table border='0' cellborder='1' cellspacing='0' cellpadding='2'>\n")
        for y in range(3):
            f.write("      <tr>\n")
            for x in range(4):
                f.write(f"        <td width='{cell_width}' height='{cell_height}'>")
                # write board value with max 3 decimal places
                f.write(f"{board[y, x]:.3f}")
                if policy[y, x] == NORTH:
                    f.write(" ↑")
                elif policy[y, x] == EAST:
                    f.write(" →")
                elif policy[y, x] == SOUTH:
                    f.write(" ↓")
                elif policy[y, x] == WEST:
                    f.write(" ←")
                f.write(f"</td>\n")
            f.write("      </tr>\n")
        f.write("    </table>\n")
        f.write("  >];\n")

        f.write("}\n")

    os.system(f"dot -Tpng {filename}.dot -o {filename}.png")
    os.system(f"rm {filename}.dot")
