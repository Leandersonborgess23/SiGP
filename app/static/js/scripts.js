document.addEventListener("DOMContentLoaded", function () {

    // ----------------------
    // SIDEBAR
    // ----------------------
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");

    if (toggle && sidebar && content) {
        toggle.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
            content.classList.toggle("expanded");
        });
    }


    // ----------------------
    // GRÁFICO 1
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
    // GRÁFICO 2
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
                        font: { weight: 'bold', size: 12 },
                        formatter: (value, ctx) => {
                            const total = ctx.chart.data.datasets[0].data
                                .reduce((acc, val) => acc + val, 0);
                            return ((value / total) * 100).toFixed(1) + "%";
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
        calendar.render();
    }

    Chart.defaults.plugins.legend.position = 'bottom';
    Chart.defaults.plugins.legend.labels.boxWidth = 12;
    Chart.defaults.maintainAspectRatio = false;


    // ----------------------
    // Mostrar / Ocultar Senhas
    // ----------------------
    function togglePassword(buttonId, inputId) {
        const btn = document.getElementById(buttonId);
        const input = document.getElementById(inputId);

        if (btn && input) {
            btn.addEventListener("click", () => {
                const isPassword = input.type === "password";
                input.type = isPassword ? "text" : "password";

                btn.innerHTML = isPassword
                    ? '<i class="fa-solid fa-eye-slash"></i>'
                    : '<i class="fa-solid fa-eye"></i>';
            });
        }
    }

    // *** CHAMADAS DIRETAS (agora funcionam) ***
    togglePassword("toggleSenhaLogin", "senhaLogin");
    togglePassword("toggleSenhaAtual", "senhaAtual");
    togglePassword("toggleNovaSenha", "novaSenha");
    togglePassword("toggleConfirmarSenha", "confirmarSenha");

    // ========================================
    // DARK MODE
    // ========================================
    const toggleBtn = document.getElementById("darkModeToggle");

    function applyDarkMode(enabled) {
        if (enabled) {
            document.documentElement.classList.add("dark-mode");
            toggleBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        } else {
            document.documentElement.classList.remove("dark-mode");
            toggleBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        }
    }

    // Carregar configuração salva
    const darkModeEnabled = localStorage.getItem("darkMode") === "true";
    applyDarkMode(darkModeEnabled);

    // Alternar ao clicar
    toggleBtn.addEventListener("click", () => {
        const isDark = document.documentElement.classList.contains("dark-mode");
        applyDarkMode(!isDark);
        localStorage.setItem("darkMode", !isDark);
    });


});
