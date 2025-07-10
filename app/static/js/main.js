document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'ru',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: '/api/events',
        editable: true,
        selectable: true,
        eventClick: function(info) {
            // Обработка клика по событию
        },
        dateClick: function(info) {
            // Обработка клика по дате
        }
    });

    calendar.render();

    // Синхронизация с Яндекс
    document.getElementById('sync-btn').addEventListener('click', async function() {
        try {
            const response = await axios.post('/api/sync');
            if (response.data.status === 'success') {
                calendar.refetchEvents();
                showAlert('Синхронизация завершена', 'success');
            }
        } catch (error) {
            showAlert('Ошибка синхронизации: ' + error.response.data.message, 'danger');
        }
    });

    function showAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container-fluid').prepend(alert);
    }
});