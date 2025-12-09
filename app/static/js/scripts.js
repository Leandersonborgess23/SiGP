document.addEventListener("DOMContentLoaded", function () {

    // ----------------------
    // SIDEBAR
    // ----------------------
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");

    if (toggle && sidebar) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
        });
    }

    // ----------------------
    // GRÁFICO 1 — Servidores por Secretaria
    // ----------------------
    const ctx1 = document.getElementById('graficoServidoresSecretaria');
    if (ctx1 && typeof Chart !== "undefined") {
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
    if (ctx2 && typeof Chart !== "undefined") {
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
                    legend: { position: 'bottom' }
                }
            },
            plugins: [ChartDataLabels]
        });
    }

    // ----------------------
    // CALENDÁRIO
    // ----------------------
    const calendarEl = document.getElementById('calendar');
    if (calendarEl && typeof FullCalendar !== "undefined") {

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'pt-br',
            height: 520,
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: ''
            },
            events: "/api/eventos" 
        });
    }

});