/**
 * ERP_VITTAVENTO основной JavaScript файл
 * Содержит общие функции и обработчики событий
 */

// Выполнение кода после полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    initTooltips();

    // Инициализация обработчиков событий
    initEventHandlers();

    // Инициализация интерактивных таблиц
    initDataTables();

    console.log('ERP_VITTAVENTO JS initialized');
});

/**
 * Инициализация всплывающих подсказок Bootstrap
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Инициализация обработчиков событий
 */
function initEventHandlers() {
    // Обработчик для подтверждения удаления
    document.querySelectorAll('.btn-delete').forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                e.preventDefault();
            }
        });
    });

    // Обработчик для динамического обновления полей формы
    document.querySelectorAll('select[data-dynamic-update]').forEach(function(select) {
        select.addEventListener('change', function() {
            const targetId = this.getAttribute('data-target');
            const url = this.getAttribute('data-url');
            const value = this.value;

            if (targetId && url && value) {
                updateDynamicFields(targetId, url, value);
            }
        });
    });
}

/**
 * Обновление динамических полей формы на основе AJAX-запроса
 *
 * @param {string} targetId - ID целевого элемента для обновления
 * @param {string} url - URL для AJAX-запроса
 * @param {string} value - Значение для передачи в запросе
 */
function updateDynamicFields(targetId, url, value) {
    const target = document.getElementById(targetId);
    if (!target) return;

    // Добавление индикатора загрузки
    target.innerHTML = '<div class="text-center"><div class="spinner-border spinner-border-sm text-primary" role="status"></div></div>';

    // Выполнение AJAX-запроса
    fetch(`${url}?value=${encodeURIComponent(value)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => {
            if (data.html) {
                target.innerHTML = data.html;

                // Повторная инициализация компонентов в обновленном содержимом
                initTooltips();
            } else {
                target.innerHTML = '<div class="alert alert-warning">Данные не найдены</div>';
            }
        })
        .catch(error => {
            console.error('Ошибка при обновлении динамических полей:', error);
            target.innerHTML = '<div class="alert alert-danger">Ошибка при загрузке данных</div>';
        });
}

/**
 * Инициализация интерактивных таблиц
 */
function initDataTables() {
    // Проверка наличия DataTables
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.datatable').DataTable({
            language: {
                url: '/static/js/dataTables.russian.json'
            },
            responsive: true,
            pageLength: 25
        });
    }
}

/**
 * Форматирование числа с разделителями тысяч
 *
 * @param {number} number - Число для форматирования
 * @param {number} decimals - Количество десятичных знаков
 * @param {string} decimalSeparator - Разделитель десятичной части
 * @param {string} thousandSeparator - Разделитель тысяч
 * @returns {string} Отформатированное число
 */
function formatNumber(number, decimals = 2, decimalSeparator = ',', thousandSeparator = ' ') {
    const parts = number.toFixed(decimals).split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousandSeparator);
    return parts.join(decimalSeparator);
}