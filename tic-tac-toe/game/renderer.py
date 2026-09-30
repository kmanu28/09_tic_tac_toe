"""
renderer: all pygame drawing lives here.
"""

import pygame

WIDTH = 400
HEIGHT = 600

BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_TOP = 120

WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)
COLOR_RESULT = (180, 40, 40)


def board_pos_to_cell(pos):
    x, y = pos
    board_y = y - BOARD_TOP

    if not (0 <= x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE):
        return None

    col = int(x // CELL_SIZE)
    row = int(board_y // CELL_SIZE)

    return row, col


def draw_board(surface, board):
    surface.fill(COLOR_BG)

    for index in range(1, 3):
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (index * CELL_SIZE, BOARD_TOP),
            (index * CELL_SIZE, BOARD_TOP + BOARD_SIZE),
            4,
        )

        pygame.draw.line(
            surface,
            COLOR_LINE,
            (0, BOARD_TOP + index * CELL_SIZE),
            (BOARD_SIZE, BOARD_TOP + index * CELL_SIZE),
            4,
        )

    for row in range(3):
        for col in range(3):
            symbol = board[row][col]

            if symbol is None:
                continue

            center = (
                col * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2,
            )

            if symbol == "X":
                offset = CELL_SIZE // 3

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (center[0] - offset, center[1] - offset),
                    (center[0] + offset, center[1] + offset),
                    7,
                )

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (center[0] + offset, center[1] - offset),
                    (center[0] - offset, center[1] + offset),
                    7,
                )

            elif symbol == "O":
                pygame.draw.circle(
                    surface,
                    COLOR_O,
                    center,
                    CELL_SIZE // 3,
                    7,
                )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_result(surface, font, text):
    result_font = pygame.font.SysFont("consolas", 20)
    rendered_text = result_font.render(text, True, COLOR_RESULT)

    rect = rendered_text.get_rect(
        center=(WIDTH // 2, BOARD_TOP + BOARD_SIZE + 24)
    )

    surface.blit(rendered_text, rect)


def draw_controls(surface, font, starter_text):
    controls_font = pygame.font.SysFont("consolas", 16)

    starter_surface = controls_font.render(
        starter_text,
        True,
        COLOR_TEXT,
    )

    starter_rect = starter_surface.get_rect(
        center=(WIDTH // 2, BOARD_TOP + BOARD_SIZE + 52)
    )

    surface.blit(starter_surface, starter_rect)

    controls_surface = controls_font.render(
        "X/O: Starter    R: Round    M: Match",
        True,
        COLOR_TEXT,
    )

    controls_rect = controls_surface.get_rect(
        center=(WIDTH // 2, BOARD_TOP + BOARD_SIZE + 78)
    )

    surface.blit(controls_surface, controls_rect)