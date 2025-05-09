// Пространство имён для проекта "CheckersWinForms"
namespace CheckersWinForms
{
    // Частичный класс формы Form1
    partial class Form1
    {
        // Контейнер для компонентов формы (например, Label и др.)
        private System.ComponentModel.IContainer components = null;

        // Метка для отображения счёта
        private System.Windows.Forms.Label scoreLabel;

        // Метод освобождения ресурсов формы
        protected override void Dispose(bool disposing)
        {
            // Если нужно освободить управляемые ресурсы и они существуют — удаляем
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            // Вызываем базовый метод Dispose
            base.Dispose(disposing);
        }

        // Метод инициализации элементов интерфейса (вызывается в конструкторе формы)
        private void InitializeComponent()
        {
            // Инициализируем контейнер компонентов
            this.components = new System.ComponentModel.Container();

            // Создаём метку для счёта
            this.scoreLabel = new System.Windows.Forms.Label();

            // Приостанавливаем автоматическую прорисовку формы (оптимизация)
            this.SuspendLayout();

            // === Настройка scoreLabel ===

            // Автоматическая подгонка размера текста
            this.scoreLabel.AutoSize = true;

            // Шрифт и стиль текста метки
            this.scoreLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Bold);

            // Позиция метки на форме (отступ слева и сверху)
            this.scoreLabel.Location = new System.Drawing.Point(10, 10);

            // Имя метки (для кода)
            this.scoreLabel.Name = "scoreLabel";

            // Начальный размер (необязательно, задаётся AutoSize)
            this.scoreLabel.Size = new System.Drawing.Size(100, 20);

            // Порядок перехода по Tab (в данном случае — первый)
            this.scoreLabel.TabIndex = 0;

            // Текст по умолчанию
            this.scoreLabel.Text = "Счет: 0 - 0";

            // Добавляем метку на форму
            this.Controls.Add(this.scoreLabel);

            // === Настройка самой формы ===

            // Масштаб по умолчанию (для DPI и шрифтов)
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;

            // Размер формы (в пикселях)
            this.ClientSize = new System.Drawing.Size(480, 500);

            // Запрещаем изменение размеров окна пользователем
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;

            // Запрещаем кнопку "Развернуть"
            this.MaximizeBox = false;

            // Имя формы (в коде)
            this.Name = "Form1";

            // Текст в заголовке окна
            this.Text = "Checkers";

            // Возобновляем прорисовку интерфейса
            this.ResumeLayout(false);

            // Применяем авторазметку (нужна для Label)
            this.PerformLayout();
        }
    }
}
