document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('tables-container');
    const dateInput = document.getElementById('map-date');
    const timeInput = document.getElementById('map-time');
    const updateBtn = document.getElementById('update-map');

    // Установка текущей даты по умолчанию
    if (!dateInput.value) {
        const today = new Date();
        dateInput.value = today.toISOString().split('T')[0];
    }

    // Загружает столики при открытии страницы
    loadTables();

    // Обновляет при изменении времени
    updateBtn.addEventListener('click', loadTables);

    async function loadTables() {
        const date = dateInput.value;
        const time = timeInput.value;
        
        try {
            const response = await fetch(`/api/reservations/tables/availability/?date=${date}&time=${time}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const tables = await response.json();
            
            if (!Array.isArray(tables)) {
                throw new Error('Invalid data format');
            }
            
            renderTables(tables);
        } catch (error) {
            console.error('Ошибка загрузки столиков:', error);
            alert('Не удалось загрузить данные о столиках. Проверьте консоль для деталей.');
        }
    }

    function renderTables(tables) {
        container.innerHTML = '';
        
        tables.forEach(table => {
            const tableEl = document.createElement('div');
            tableEl.className = `table ${table.is_vip ? 'vip' : ''} ${table.is_reserved ? 'booked' : 'free'}`;
            tableEl.style.cssText = `
                left: ${table.x_pos}px;
                top: ${table.y_pos}px;
                transform: rotate(${table.rotation}deg);
            `;
            tableEl.innerHTML = `
                <div class="table-number">${table.number}</div>
                <div class="table-seats">${table.seats} мест</div>
            `;
            tableEl.title = `Столик №${table.number} (${table.seats} мест)`;
            
            tableEl.addEventListener('click', () => {
                if (!table.is_reserved) {
                    window.location.href = `/reservations/create/?table=${table.id}&date=${dateInput.value}&time=${timeInput.value}`;
                } else {
                    alert('Этот столик уже занят на выбранное время');
                }
            });
            
            container.appendChild(tableEl);
        });
    }
});