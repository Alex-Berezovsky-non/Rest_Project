document.addEventListener('DOMContentLoaded', function() {
    const BASE_URL = '/api/reservations/'; 

    const loadTables = async () => {
        try {
            const date = document.getElementById('map-date').value;
            const time = document.getElementById('map-time').value;
            
            const response = await fetch(
                `${BASE_URL}api/tables/availability/?date=${date}&time=${time}`,
                {
                    headers: {
                        'Accept': 'application/json'
                    }
                }
            );
            
            if (!response.ok) {
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
            
            const tables = await response.json();
            renderTables(tables);
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Ошибка загрузки. Проверьте консоль (F12 > Console)');
        }
    };

    const renderTables = (tables) => {
        const container = document.getElementById('tables-container');
        container.innerHTML = '';
        
        tables.forEach(table => {
            const tableEl = document.createElement('div');
            tableEl.className = `table ${table.is_vip ? 'vip' : ''} ${table.is_reserved ? 'booked' : 'free'}`;
            tableEl.style.cssText = `
                left: ${table.x_pos}px;
                top: ${table.y_pos}px;
                transform: rotate(${table.rotation}deg);
                background-color: ${table.color};
            `;
            tableEl.innerHTML = `
                <div class="table-number">${table.number}</div>
                <div class="table-seats">${table.seats} мест</div>
            `;
            
            container.appendChild(tableEl);
        });
    };

    // Инициализация
    loadTables();
    document.getElementById('update-map').addEventListener('click', loadTables);
});