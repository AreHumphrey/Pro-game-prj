// Пространства имён, необходимые для работы с окнами, графикой и событиями
using System;
using System.Drawing;
using System.Windows.Forms;

namespace CheckersWinForms
{
    // Главная форма игры
    public partial class Form1 : Form
    {
        // Размер одной клетки в пикселях
        private const int CellSize = 60;

        // Размер доски: 8x8 клеток
        private const int BoardSize = 8;

        // Игровое поле: двумерный массив клеток
        private Piece[,] board = new Piece[BoardSize, BoardSize];

        // Выбранная пользователем клетка (если есть)
        private Point? selected = null;

        // Чья сейчас очередь: true — красные, false — чёрные
        private bool isRedTurn = true;

        // Счёт для каждой стороны
        private int redScore = 0;
        private int blackScore = 0;

        // Конструктор формы
        public Form1()
        {
            InitializeComponent(); // Инициализация визуальных компонентов

            this.DoubleBuffered = true; // Убирает мерцание при перерисовке

            // Устанавливаем размер формы с учётом панели счёта
            this.ClientSize = new Size(BoardSize * CellSize, BoardSize * CellSize + 40);

            InitBoard(); // Заполняем поле шашками

            // Обработчик отрисовки
            this.Paint += DrawBoard;

            // Обработчик нажатия мыши
            this.MouseClick += HandleClick;
        }

        // Метод для начальной расстановки шашек
        private void InitBoard()
        {
            for (int y = 0; y < BoardSize; y++)
            {
                for (int x = 0; x < BoardSize; x++)
                {
                    // Игровые шашки располагаются только на чёрных клетках
                    if ((x + y) % 2 == 1)
                    {
                        if (y < 3) // Верхние три ряда — чёрные шашки
                            board[y, x] = Piece.Black;
                        else if (y > 4) // Нижние три ряда — красные шашки
                            board[y, x] = Piece.Red;
                        else // Средние два ряда — пустые клетки
                            board[y, x] = Piece.None;
                    }
                    else
                    {
                        board[y, x] = Piece.None; // Белые клетки всегда пустые
                    }
                }
            }
            UpdateScoreLabel(); // Обновляем отображение счёта
        }

        // Метод отрисовки игрового поля
        private void DrawBoard(object sender, PaintEventArgs e)
        {
            for (int y = 0; y < BoardSize; y++)
            {
                for (int x = 0; x < BoardSize; x++)
                {
                    // Вычисляем прямоугольник клетки с отступом по Y (для счёта)
                    var rect = new Rectangle(x * CellSize, y * CellSize + 40, CellSize, CellSize);

                    // Рисуем цвет клетки: светлая или тёмная
                    e.Graphics.FillRectangle(((x + y) % 2 == 0) ? Brushes.Beige : Brushes.Brown, rect);

                    // Подсветка выбранной клетки
                    if (selected.HasValue && selected.Value.X == x && selected.Value.Y == y)
                        e.Graphics.DrawRectangle(Pens.Yellow, rect);

                    // Рисуем шашку, если она есть
                    if (board[y, x] == Piece.Red)
                        e.Graphics.FillEllipse(Brushes.Red, rect);
                    else if (board[y, x] == Piece.Black)
                        e.Graphics.FillEllipse(Brushes.Black, rect);
                }
            }
        }

        // Обработка клика мыши по клетке
        private void HandleClick(object sender, MouseEventArgs e)
        {
            // Вычисляем координаты клетки
            int x = e.X / CellSize;
            int y = (e.Y - 40) / CellSize; // учитываем отступ для счёта

            // Если клик вне поля — ничего не делаем
            if (x < 0 || y < 0 || x >= BoardSize || y >= BoardSize)
                return;

            // Если ничего не выбрано — пробуем выбрать шашку
            if (selected == null)
            {
                // Проверяем, что выбран шашка текущего игрока
                if ((isRedTurn && board[y, x] == Piece.Red) || (!isRedTurn && board[y, x] == Piece.Black))
                {
                    selected = new Point(x, y); // Запоминаем выбор
                    Invalidate(); // Перерисовка
                }
            }
            else
            {
                var from = selected.Value;
                // Пробуем сделать ход
                if (TryMove(from.X, from.Y, x, y))
                {
                    selected = null; // Снимаем выбор
                    isRedTurn = !isRedTurn; // Меняем ход
                    Invalidate(); // Перерисовка
                    UpdateScoreLabel(); // Обновляем счёт
                }
                else
                {
                    selected = null; // Если ход недопустим — снимаем выбор
                    Invalidate();
                }
            }
        }

        // Попытка совершить ход
        private bool TryMove(int fromX, int fromY, int toX, int toY)
        {
            var movingPiece = board[fromY, fromX];

            // Если целевая клетка не пуста — ход невозможен
            if (board[toY, toX] != Piece.None)
                return false;

            int dx = toX - fromX;
            int dy = toY - fromY;

            // Простой ход (на одну клетку по диагонали)
            if (Math.Abs(dx) == 1 && dy == (movingPiece == Piece.Red ? -1 : 1))
            {
                board[toY, toX] = movingPiece;
                board[fromY, fromX] = Piece.None;
                return true;
            }

            // Прыжок через соперника
            if (Math.Abs(dx) == 2 && dy == (movingPiece == Piece.Red ? -2 : 2))
            {
                int midX = fromX + dx / 2;
                int midY = fromY + dy / 2;

                // Проверка: в середине должна быть фигура соперника
                if (board[midY, midX] != Piece.None && board[midY, midX] != movingPiece)
                {
                    // Увеличиваем счёт для стороны, совершившей захват
                    if (board[midY, midX] == Piece.Black) redScore++;
                    else if (board[midY, midX] == Piece.Red) blackScore++;

                    // Обновляем поле
                    board[toY, toX] = movingPiece;
                    board[fromY, fromX] = Piece.None;
                    board[midY, midX] = Piece.None;
                    return true;
                }
            }

            return false; // Недопустимый ход
        }

        // Обновление текста метки со счётом
        private void UpdateScoreLabel()
        {
            scoreLabel.Text = $"Счет: {redScore} - {blackScore}";
        }

        // Перечисление возможных типов клеток
        private enum Piece
        {
            None,   // Пусто
            Red,    // Красная шашка
            Black   // Чёрная шашка
        }
    }
}
