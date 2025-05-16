// Подключение пространств имён:
// System — базовые типы и классы (строки, исключения и т.д.)
// System.Drawing — работа с графикой (цвета, прямоугольники, кисти)
// System.Windows.Forms — классы для создания оконных приложений
using System;
using System.Drawing;
using System.Windows.Forms;

namespace CheckersWinForms
{
    // Основной класс формы (окна), содержащий всю логику игры в шашки
    public partial class Form1 : Form
    {
        // Константа: размер одной клетки на доске в пикселях
        private const int CellSize = 60;

        // Константа: доска 8x8 клеток
        private const int BoardSize = 8;

        // Игровое поле: двумерный массив, содержащий состояния клеток
        private Piece[,] board = new Piece[BoardSize, BoardSize];

        // Выбранная клетка игроком (null, если ничего не выбрано)
        private Point? selected = null;

        // Чей сейчас ход: true — красные, false — чёрные
        private bool isRedTurn = true;

        // Очки за съеденные шашки
        private int redScore = 0;
        private int blackScore = 0;

        // Конструктор формы — запускается при создании окна
        public Form1()
        {
            InitializeComponent(); // Генерируется автоматически: создаёт интерфейс

            this.DoubleBuffered = true; // Включаем двойную буферизацию, чтобы убрать мерцание при отрисовке

            // Устанавливаем размеры окна (высота учитывает дополнительную панель со счётом)
            this.ClientSize = new Size(BoardSize * CellSize, BoardSize * CellSize + 40);

            InitBoard(); // Инициализируем начальное расположение шашек

            // Привязываем метод отрисовки доски к событию перерисовки окна
            this.Paint += DrawBoard;

            // Привязываем метод обработки клика мыши к событию нажатия
            this.MouseClick += HandleClick;
        }

        // Метод расставляет шашки в начальной позиции
        private void InitBoard()
        {
            for (int y = 0; y < BoardSize; y++)
            {
                for (int x = 0; x < BoardSize; x++)
                {
                    // Шашки размещаются только на чёрных клетках
                    if ((x + y) % 2 == 1)
                    {
                        if (y < 3)
                            board[y, x] = Piece.Black; // Чёрные шашки вверху
                        else if (y > 4)
                            board[y, x] = Piece.Red;   // Красные шашки внизу
                        else
                            board[y, x] = Piece.None;  // Пустые клетки
                    }
                    else
                    {
                        board[y, x] = Piece.None; // Белые клетки всегда пустые
                    }
                }
            }

            UpdateScoreLabel(); // Обновляем отображение счёта в интерфейсе
        }

        // Метод отрисовки доски и шашек
        private void DrawBoard(object sender, PaintEventArgs e)
        {
            for (int y = 0; y < BoardSize; y++)
            {
                for (int x = 0; x < BoardSize; x++)
                {
                    // Определяем координаты и размеры текущей клетки
                    var rect = new Rectangle(x * CellSize, y * CellSize + 40, CellSize, CellSize);

                    // Рисуем цвет клетки: светлая или тёмная
                    e.Graphics.FillRectangle(((x + y) % 2 == 0) ? Brushes.Beige : Brushes.Brown, rect);

                    // Подсветка клетки, если она выбрана
                    if (selected.HasValue && selected.Value.X == x && selected.Value.Y == y)
                        e.Graphics.DrawRectangle(Pens.Yellow, rect);

                    // Рисуем шашку в клетке, если она есть
                    if (board[y, x] == Piece.Red)
                        e.Graphics.FillEllipse(Brushes.Red, rect);
                    else if (board[y, x] == Piece.Black)
                        e.Graphics.FillEllipse(Brushes.Black, rect);
                }
            }
        }

        // Метод обработки клика мыши по доске
        private void HandleClick(object sender, MouseEventArgs e)
        {
            // Определяем координаты клетки, по которой кликнули
            int x = e.X / CellSize;
            int y = (e.Y - 40) / CellSize; // -40 — чтобы учитывать панель счёта

            // Если клик был за пределами доски — выходим
            if (x < 0 || y < 0 || x >= BoardSize || y >= BoardSize)
                return;

            // Если ничего не выбрано — пробуем выбрать шашку
            if (selected == null)
            {
                // Можно выбрать только свою шашку
                if ((isRedTurn && board[y, x] == Piece.Red) || (!isRedTurn && board[y, x] == Piece.Black))
                {
                    selected = new Point(x, y); // Сохраняем выбор
                    Invalidate(); // Обновляем окно
                }
            }
            else
            {
                // Пользователь уже выбрал шашку и теперь пытается сделать ход
                var from = selected.Value;

                if (TryMove(from.X, from.Y, x, y)) // Пробуем сделать ход
                {
                    selected = null;        // Сбрасываем выбор
                    isRedTurn = !isRedTurn; // Передаём ход
                    Invalidate();           // Перерисовываем доску
                    UpdateScoreLabel();     // Обновляем счёт
                }
                else
                {
                    // Неверный ход — снимаем выбор
                    selected = null;
                    Invalidate();
                }
            }
        }

        // Метод, реализующий логику перемещения шашки
        private bool TryMove(int fromX, int fromY, int toX, int toY)
        {
            var movingPiece = board[fromY, fromX]; // Получаем выбранную шашку

            // Целевая клетка должна быть пустой
            if (board[toY, toX] != Piece.None)
                return false;

            int dx = toX - fromX;
            int dy = toY - fromY;

            // Простой ход на одну клетку по диагонали
            if (Math.Abs(dx) == 1 && dy == (movingPiece == Piece.Red ? -1 : 1))
            {
                board[toY, toX] = movingPiece;
                board[fromY, fromX] = Piece.None;
                return true;
            }

            // Ход с захватом — прыжок через соперника
            if (Math.Abs(dx) == 2 && dy == (movingPiece == Piece.Red ? -2 : 2))
            {
                int midX = fromX + dx / 2;
                int midY = fromY + dy / 2;

                // В середине должна быть шашка противоположного цвета
                if (board[midY, midX] != Piece.None && board[midY, midX] != movingPiece)
                {
                    // Обновляем счёт за захват
                    if (board[midY, midX] == Piece.Black) redScore++;
                    else if (board[midY, midX] == Piece.Red) blackScore++;

                    // Обновляем позиции на доске
                    board[toY, toX] = movingPiece;
                    board[fromY, fromX] = Piece.None;
                    board[midY, midX] = Piece.None;
                    return true;
                }
            }

            return false; // Все остальные случаи — недопустимый ход
        }

        // Обновление метки со счётом в UI
        private void UpdateScoreLabel()
        {
            scoreLabel.Text = $"Счет: {redScore} - {blackScore}";
        }

        // Перечисление возможных состояний клетки
        private enum Piece
        {
            None,   // Клетка пуста
            Red,    // Красная шашка
            Black   // Чёрная шашка
        }
    }
}
