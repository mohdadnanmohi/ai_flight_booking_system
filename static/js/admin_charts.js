// Admin Dashboard Analytics Charts

document.addEventListener('DOMContentLoaded', function() {
    const chartWrapper = document.getElementById('analyticsDataWrapper');
    if (!chartWrapper) return;

    // Load data from DOM data attributes
    const revenueData = JSON.parse(chartWrapper.dataset.revenueTrend || '[]');
    const bookingsData = JSON.parse(chartWrapper.dataset.bookingsTrend || '[]');
    const routesData = JSON.parse(chartWrapper.dataset.popularRoutes || '{}');
    const occupancyData = JSON.parse(chartWrapper.dataset.occupancy || '[]');
    const airlinesData = JSON.parse(chartWrapper.dataset.airlinesShare || '{}');

    // Chart.js global defaults for Light Theme
    Chart.defaults.color = '#334155';
    Chart.defaults.borderColor = 'rgba(0, 0, 0, 0.06)';
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    // Helper to extract values
    const revenueLabels = revenueData.map(item => item.date);
    const revenueValues = revenueData.map(item => item.amount);

    const bookingsLabels = bookingsData.map(item => item.date);
    const bookingsValues = bookingsData.map(item => item.count);

    const routeLabels = Object.keys(routesData);
    const routeValues = Object.values(routesData);

    const flightNumbers = occupancyData.map(item => item.flight_number);
    const occupancyPercentages = occupancyData.map(item => item.occupancy);

    const airlineLabels = Object.keys(airlinesData);
    const airlineValues = Object.values(airlinesData);

    // Color definitions
    const primaryColor = '#4f46e5';
    const secondaryColor = '#06b6d4';
    const accentColor = '#d946ef';
    const alertSuccess = '#10b981';

    // 1. Revenue Trend Chart (Line Chart)
    const ctxRevenue = document.getElementById('revenueChart');
    if (ctxRevenue) {
        new Chart(ctxRevenue, {
            type: 'line',
            data: {
                labels: revenueLabels.length > 0 ? revenueLabels : ['No Data'],
                datasets: [{
                    label: 'Revenue ($)',
                    data: revenueValues.length > 0 ? revenueValues : [0],
                    borderColor: secondaryColor,
                    backgroundColor: 'rgba(6, 182, 212, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.35,
                    pointBackgroundColor: secondaryColor,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { callback: v => '$' + v } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // 2. Bookings Trend Chart (Bar Chart)
    const ctxBookings = document.getElementById('bookingsChart');
    if (ctxBookings) {
        new Chart(ctxBookings, {
            type: 'bar',
            data: {
                labels: bookingsLabels.length > 0 ? bookingsLabels : ['No Data'],
                datasets: [{
                    label: 'Bookings Count',
                    data: bookingsValues.length > 0 ? bookingsValues : [0],
                    backgroundColor: primaryColor,
                    hoverBackgroundColor: '#6366f1',
                    borderRadius: 6,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { precision: 0 } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // 3. Popular Routes Chart (Horizontal Bar Chart)
    const ctxRoutes = document.getElementById('routesChart');
    if (ctxRoutes) {
        new Chart(ctxRoutes, {
            type: 'bar',
            data: {
                labels: routeLabels.length > 0 ? routeLabels : ['No Data'],
                datasets: [{
                    label: 'Bookings per Route',
                    data: routeValues.length > 0 ? routeValues : [0],
                    backgroundColor: accentColor,
                    hoverBackgroundColor: '#e879f9',
                    borderRadius: 6,
                    borderWidth: 0
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(0, 0, 0, 0.04)' }, ticks: { precision: 0 } },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    // 4. Seat Occupancy Chart (Bar Chart)
    const ctxOccupancy = document.getElementById('occupancyChart');
    if (ctxOccupancy) {
        new Chart(ctxOccupancy, {
            type: 'bar',
            data: {
                labels: flightNumbers.length > 0 ? flightNumbers : ['No Data'],
                datasets: [{
                    label: 'Occupancy Rate (%)',
                    data: occupancyPercentages.length > 0 ? occupancyPercentages : [0],
                    backgroundColor: alertSuccess,
                    borderRadius: 6,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { 
                        grid: { color: 'rgba(0, 0, 0, 0.04)' }, 
                        min: 0,
                        max: 100,
                        ticks: { callback: v => v + '%' } 
                    },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // 5. Top Airlines Chart (Doughnut Chart)
    const ctxAirlines = document.getElementById('airlinesChart');
    if (ctxAirlines) {
        new Chart(ctxAirlines, {
            type: 'doughnut',
            data: {
                labels: airlineLabels.length > 0 ? airlineLabels : ['No Data'],
                datasets: [{
                    data: airlineValues.length > 0 ? airlineValues : [1],
                    backgroundColor: [
                        '#4f46e5', '#06b6d4', '#d946ef', '#10b981', 
                        '#f59e0b', '#ef4444', '#6366f1', '#a855f7'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { boxWidth: 12, padding: 15 }
                    }
                },
                cutout: '65%'
            }
        });
    }
});
