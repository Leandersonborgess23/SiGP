document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");

    if (toggle && sidebar) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
        });
    }
});

// ----------------------
// GRÁFICO 1 — Servidores por Secretaria
// ----------------------
const ctx1 = document.getElementById('graficoServidoresSecretaria');
if (ctx1) {
    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: servidoresLabels,
            datasets: [{
                label: 'Servidores',
                data: servidoresData,
                backgroundColor: 'rgba(54, 162, 235, 0.6)'
            }]
        }
    });
}

// ----------------------
// GRÁFICO 2 — Distribuição de Cargos
// ----------------------
const ctx2 = document.getElementById('graficoCargos');
if (ctx2) {
    new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: cargosLabels,
            datasets: [{
                label: 'Quantidade',
                data: cargosData,
                backgroundColor: [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6610f2', '#6f42c1'
                ]
            }]
        },
        options: {
            plugins: {
                datalabels: {
                    color: '#fff',
                    font: {
                        weight: 'bold',
                        size: 12
                    },
                    formatter: (value, ctx) => {
                        const total = ctx.chart.data.datasets[0].data
                            .reduce((acc, val) => acc + val, 0);

                        const percentage = ((value / total) * 100).toFixed(1);  
                        return percentage + "%";
                    }
                },
                legend: {
                    position: 'bottom'
                }
            }
        },
        plugins: [ChartDataLabels]
    });
}

// ----------------------
// Calendário
// ----------------------
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    if (calendarEl) {

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'pt-br',
            events: [
                {
                    title: 'Reunião na Prefeitura',
                    start: '2025-02-10'
                },
                {
                    title: 'Pagamento Servidores',
                    start: '2025-02-25'
                },
                {
                    title: 'Aniversário de Pureza',
                    start: '2025-03-05',
                    backgroundColor: '#28a745',
                    borderColor: '#28a745'
                }
            ]
        });

        calendar.render();
    }
});
