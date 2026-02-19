let latencyChart, successChart;

document.addEventListener("DOMContentLoaded", () => {
  initCharts();
  loadDashboardData();

  setInterval(loadDashboardData, 30000);
  document.getElementById("refresh-btn").onclick = loadDashboardData;
});

function initCharts() {
  const latencyCtx = document.getElementById("latencyChart").getContext("2d");
  latencyChart = new Chart(latencyCtx, {
    type: "bar",
    data: {
      labels: ["Avg", "P95", "P99"],
      datasets: [{ label: "ms", data: [0, 0, 0] }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  const successCtx = document.getElementById("successChart").getContext("2d");
  successChart = new Chart(successCtx, {
    type: "doughnut",
    data: {
      labels: ["Success", "Errors"],
      datasets: [{ data: [0, 0] }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });
}

async function loadDashboardData() {
  try {
    const resp = await fetch("/api/analytics/kpis");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();

    const ops = data.operational_kpis || {};
    updateKpiCards(ops);
    updateCharts(data);

    document.getElementById("last-update").textContent =
      `Last updated: ${new Date(data.report_timestamp).toLocaleString()}`;
  } catch (e) {
    document.getElementById("last-update").textContent = "Error loading data";
    console.error(e);
  }
}

function updateKpiCards(kpis) {
  document.querySelectorAll(".kpi-card").forEach(card => {
    const key = card.dataset.kpi;
    const val = kpis[key];
    const el = card.querySelector(".kpi-value");
    el.textContent = formatValue(val, key);
  });
}

function updateCharts(report) {
  const ops = report.operational_kpis || {};

  latencyChart.data.datasets[0].data = [
    ops.avg_latency_ms || 0,
    ops.p95_latency_ms || 0,
    ops.p99_latency_ms || 0
  ];
  latencyChart.update();

  const total = ops.total_requests || 0;
  const errorRate = ops.error_rate_percent || 0;
  const errors = Math.round(total * (errorRate / 100.0));
  const success = Math.max(total - errors, 0);

  successChart.data.datasets[0].data = [success, errors];
  successChart.update();
}

function formatValue(v, key) {
  if (v === undefined || v === null) return "--";
  if (key.includes("latency")) return `${Number(v).toFixed(1)} ms`;
  if (key.includes("percent")) return `${Number(v).toFixed(1)}%`;
  if (typeof v === "number") return v.toLocaleString();
  return String(v);
}
