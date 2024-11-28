import random


def create_board(size, mines):
    board = [['.' for _ in range(size)] for _ in range(size)]
    mine_positions = set()

    while len(mine_positions) < mines:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        mine_positions.add((x, y))

    return board, mine_positions


def display_board(board):
    print("\n".join(" ".join(row) for row in board))


def count_adjacent_mines(x, y, mine_positions, size):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:

        nx, ny = x + dx, y + dy

        if 0 <= nx < size and 0 <= ny < size and (nx, ny) in mine_positions:
            count += 1
    return count


print("Добро пожаловать в игру Сапёр!")

size = int(input("Введите размер игрового поля (например, 5 для 5x5): "))

mines = int(input("Введите количество мин: "))

board, mine_positions = create_board(size, mines)

revealed = set()

while True:
    display_board(board)
    print("Введите координаты клетки (например, 1 1):")

    try:
        x, y = map(int, input().split())

        x, y = x - 1, y - 1
    except ValueError:

        print("Ошибка ввода! Введите два числа через пробел.")
        continue

    if not (0 <= x < size and 0 <= y < size):
        print("Координаты вне игрового поля!")
        continue

    if (x, y) in mine_positions:
        print("БАБАХ! Вы наткнулись на мину. Игра окончена.")

        for mx, my in mine_positions:
            board[mx][my] = '*'
        display_board(board)
        break

    if (x, y) in revealed:
        print("Эта клетка уже открыта.")
        continue

    revealed.add((x, y))
    adjacent_mines = count_adjacent_mines(x, y, mine_positions, size)
    board[x][y] = str(adjacent_mines)

    if len(revealed) == size * size - mines:
        print("Поздравляем! Вы открыли все клетки без мин!")
        display_board(board)
        break
