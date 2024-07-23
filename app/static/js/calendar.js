document.addEventListener('DOMContentLoaded', function() {
    let currentDate = new Date();
    updateCalendar(currentDate);

    document.getElementById('prevMonth').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        updateCalendar(currentDate);
    });

    document.getElementById('nextMonth').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        updateCalendar(currentDate);
    });
});

function updateCalendar(date) {
    const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
    const dayNames = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"];
    
    document.getElementById('currentMonth').textContent = `${monthNames[date.getMonth()]} ${date.getFullYear()}`;

    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1);
    const lastDayOfMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0);
    
    const dateHeaders = document.querySelectorAll('.date-header');
    const reservationCells = document.querySelectorAll('.reservation-cell');

    dateHeaders.forEach((header, index) => {
        if (index < lastDayOfMonth.getDate()) {
            const cellDate = new Date(firstDayOfMonth);
            cellDate.setDate(index + 1);
            header.textContent = `${dayNames[cellDate.getDay()]} ${cellDate.getDate()}`;
            header.dataset.fullDate = cellDate.toISOString().split('T')[0];
            header.style.display = '';
        } else {
            header.style.display = 'none';
        }
    });

    reservationCells.forEach((cell, index) => {
        const roomIndex = Math.floor(index / 31);
        const dayIndex = index % 31;
        if (dayIndex < lastDayOfMonth.getDate()) {
            cell.dataset.date = new Date(date.getFullYear(), date.getMonth(), dayIndex + 1).toISOString().split('T')[0];
            cell.style.display = '';
        } else {
            cell.style.display = 'none';
        }
    });

    loadReservations(firstDayOfMonth, lastDayOfMonth);
}

function loadReservations(startDate, endDate) {
    // Cette fonction devrait faire une requête AJAX à votre serveur
    // pour obtenir les réservations du mois et les afficher dans le calendrier
    fetch(`/api/reservations?start=${startDate.toISOString()}&end=${endDate.toISOString()}`)
        .then(response => response.json())
        .then(reservations => {
            reservations.forEach(reservation => {
                const cell = document.querySelector(`.reservation-cell[data-room="${reservation.room_name}"][data-date="${reservation.date}"]`);
                if (cell) {
                    cell.textContent = reservation.initials;
                    cell.classList.add('reserved');
                }
            });
        });
}