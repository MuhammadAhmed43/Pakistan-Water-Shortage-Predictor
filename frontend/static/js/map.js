// Map page: form submission, Leaflet map + markers, summary metrics, table.
(function () {
    const form = document.getElementById("map-form");
    const irrigation = document.getElementById("m-irrigation");
    const irrigationValue = document.getElementById("m-irrigation-value");
    const statusEl = document.getElementById("map-status");
    const tableBody = document.getElementById("map-table-body");

    const SEVERITY_HEX = {
        "No Shortage": "#2F7D4F",
        "Mild": "#6DA579",
        "Moderate": "#D6A848",
        "Severe": "#C7702C",
        "Critical": "#8E2A1F"
    };
    const SEVERITY_RADIUS = {
        "No Shortage": 8,
        "Mild": 10,
        "Moderate": 12,
        "Severe": 14,
        "Critical": 18
    };

    irrigation.addEventListener("input", () => {
        irrigationValue.textContent = irrigation.value;
    });

    const map = L.map("map", { zoomControl: true, scrollWheelZoom: true })
        .setView(window.__PAKISTAN_CENTER__, window.__MAP_ZOOM__);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: "abcd",
        maxZoom: 19
    }).addTo(map);

    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png", {
        attribution: '',
        subdomains: "abcd",
        maxZoom: 19,
        pane: "shadowPane"
    }).addTo(map);

    let markerLayer = L.layerGroup().addTo(map);

    function fmt(value, digits) {
        if (value === null || value === undefined || Number.isNaN(value)) return "—";
        return Number(value).toFixed(digits);
    }

    function clearMarkers() { markerLayer.clearLayers(); }

    function addMarker(row) {
        if (row.lat === null || row.lon === null) return;
        const color = SEVERITY_HEX[row.severity] || "#999";
        const radius = SEVERITY_RADIUS[row.severity] || 10;
        const circle = L.circleMarker([row.lat, row.lon], {
            radius,
            color: "#ffffff",
            weight: 2,
            fillColor: color,
            fillOpacity: 0.85
        });
        const popup =
            '<div style="min-width:200px">' +
                '<div style="font-family:JetBrains Mono,monospace;font-size:10px;text-transform:uppercase;color:#717970;letter-spacing:0.05em;margin-bottom:4px">' + row.severity + '</div>' +
                '<div style="font-family:Source Serif 4,serif;font-size:18px;font-weight:600;color:#00290f;margin-bottom:8px">' + row.district + '</div>' +
                '<div style="display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:12px">' +
                    '<span style="color:#717970">WSI</span><span style="font-variant-numeric:tabular-nums;text-align:right">' + fmt(row.wsi, 1) + '%</span>' +
                    '<span style="color:#717970">Rainfall</span><span style="font-variant-numeric:tabular-nums;text-align:right">' + fmt(row.rainfall_pred, 1) + ' mm</span>' +
                    '<span style="color:#717970">Demand</span><span style="font-variant-numeric:tabular-nums;text-align:right">' + fmt(row.crop_demand, 1) + ' mm</span>' +
                    '<span style="color:#717970">Temp</span><span style="font-variant-numeric:tabular-nums;text-align:right">' + fmt(row.temperature, 1) + '°C</span>' +
                '</div>' +
            '</div>';
        circle.bindPopup(popup);
        circle.bindTooltip(row.district + " · " + row.severity, { direction: "top", offset: [0, -8], opacity: 0.95 });
        markerLayer.addLayer(circle);
    }

    function renderTable(rows) {
        if (!rows.length) {
            tableBody.innerHTML = '<tr><td colspan="6" class="p-8 text-center text-on-surface-variant">No data.</td></tr>';
            return;
        }
        const sorted = [...rows].sort((a, b) => a.wsi - b.wsi);
        tableBody.innerHTML = "";
        sorted.forEach(r => {
            const tr = document.createElement("tr");
            tr.className = "border-b border-outline-variant hover:bg-surface-container-low";
            const color = SEVERITY_HEX[r.severity];
            tr.innerHTML =
                '<td class="p-4 font-bold">' + r.district + '</td>' +
                '<td class="p-4 text-right tnum">' + fmt(r.wsi, 1) + '</td>' +
                '<td class="p-4"><span class="inline-flex items-center gap-2"><span class="w-2 h-2 rounded-full" style="background:' + color + '"></span>' + r.severity + '</span></td>' +
                '<td class="p-4 text-right tnum">' + fmt(r.rainfall_pred, 1) + '</td>' +
                '<td class="p-4 text-right tnum">' + fmt(r.crop_demand, 1) + '</td>' +
                '<td class="p-4 text-right tnum">' + fmt(r.temperature, 1) + '</td>';
            tableBody.appendChild(tr);
        });
    }

    function renderSummary(summary) {
        document.getElementById("s-avg-wsi").textContent = fmt(summary.avg_wsi, 1);
        document.getElementById("s-critical").textContent = summary.critical_count;
        document.getElementById("s-rainfall").textContent = fmt(summary.avg_rainfall, 1);
        document.getElementById("s-temp").textContent = fmt(summary.avg_temperature, 1);
    }

    async function runMap() {
        const payload = {
            crop: form.crop.value,
            soil: form.soil.value,
            month: parseInt(form.month.value, 10),
            year: parseInt(form.year.value, 10),
            irrigation_mm: parseFloat(form.irrigation.value || "0")
        };
        statusEl.textContent = "Generating predictions…";
        try {
            const res = await fetch("/api/map", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (!res.ok) {
                statusEl.textContent = "Error: " + (data.detail || "unknown");
                return;
            }
            clearMarkers();
            data.rows.forEach(addMarker);
            renderSummary(data.summary);
            renderTable(data.rows);
            statusEl.textContent = data.rows.length + " districts forecasted";
        } catch (err) {
            statusEl.textContent = "Error: " + err.message;
        }
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        runMap();
    });

    // Auto-run on first load so the page never looks empty.
    runMap();
})();
