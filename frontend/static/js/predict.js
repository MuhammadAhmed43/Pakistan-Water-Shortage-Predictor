// Predict page: form submission, results rendering, seasonal chart, CSV export.
(function () {
    const form = document.getElementById("predict-form");
    const irrigationInput = document.getElementById("irrigation");
    const irrigationValue = document.getElementById("irrigation-value");
    const emptyState = document.getElementById("empty-state");
    const loadingState = document.getElementById("loading-state");
    const errorState = document.getElementById("error-state");
    const errorMessage = document.getElementById("error-message");
    const results = document.getElementById("results");
    const resetButton = document.getElementById("reset-button");
    const exportButton = document.getElementById("export-button");

    const SEVERITY_STYLES = {
        "No Shortage": { bar: "bg-severity-none", badgeBg: "bg-severity-none/15 text-severity-none border-severity-none/30", icon: "check_circle" },
        "Mild":        { bar: "bg-severity-mild", badgeBg: "bg-severity-mild/15 text-severity-mild border-severity-mild/40", icon: "water_drop" },
        "Moderate":    { bar: "bg-severity-moderate", badgeBg: "bg-severity-moderate/15 text-severity-moderate border-severity-moderate/40", icon: "warning" },
        "Severe":      { bar: "bg-severity-severe", badgeBg: "bg-severity-severe/15 text-severity-severe border-severity-severe/40", icon: "priority_high" },
        "Critical":    { bar: "bg-severity-critical", badgeBg: "bg-severity-critical/15 text-severity-critical border-severity-critical/50", icon: "crisis_alert" }
    };

    irrigationInput.addEventListener("input", () => {
        irrigationValue.textContent = irrigationInput.value;
    });

    resetButton?.addEventListener("click", () => {
        results.classList.add("hidden");
        emptyState.classList.remove("hidden");
        errorState.classList.add("hidden");
    });

    function readForm() {
        return {
            district: form.district.value,
            crop: form.crop.value,
            soil: form.soil.value,
            month: parseInt(form.month.value, 10),
            year: parseInt(form.year.value, 10),
            irrigation_mm: parseFloat(form.irrigation.value || "0")
        };
    }

    function show(el) { el.classList.remove("hidden"); }
    function hide(el) { el.classList.add("hidden"); }

    function fmt(value, digits = 1) {
        if (value === null || value === undefined || Number.isNaN(value)) return "—";
        return Number(value).toFixed(digits);
    }

    const MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];

    function renderHeadline(input, result) {
        const monthName = MONTH_NAMES[input.month - 1];
        const wsiClamped = Math.max(0, Math.min(160, result.wsi));
        document.getElementById("wsi-value").textContent = fmt(wsiClamped, 1);

        const sev = result.severity;
        const styles = SEVERITY_STYLES[sev];
        const badge = document.getElementById("severity-badge");
        badge.className = "absolute top-6 right-6 px-3 py-1 rounded text-label-caps font-label-caps uppercase tracking-wide flex items-center gap-1 border " + styles.badgeBg;
        document.getElementById("severity-icon").textContent = styles.icon;
        document.getElementById("severity-text").textContent = sev;

        const bar = document.getElementById("severity-bar");
        bar.className = "absolute top-0 left-0 h-full w-1.5 " + styles.bar;

        const headlineMap = {
            "No Shortage": "Supply meets demand for " + input.crop + " in " + input.district + ".",
            "Mild":        "Mild deficit expected for " + input.crop + " in " + input.district + ".",
            "Moderate":    "Moderate water shortage expected for " + input.crop + " in " + input.district + ".",
            "Severe":      "Severe shortage projected for " + input.crop + " in " + input.district + ".",
            "Critical":    "Critical shortage — crop-failure risk for " + input.crop + " in " + input.district + "."
        };
        document.getElementById("headline-text").textContent =
            headlineMap[sev] + " " + monthName + " " + input.year + ".";

        const deficit = Math.max(0, result.crop_demand - result.effective_supply);
        document.getElementById("headline-sub").textContent =
            "Predicted effective supply is " + fmt(result.effective_supply, 1) + " mm against a demand of "
            + fmt(result.crop_demand, 1) + " mm. " +
            (deficit > 0 ? "Net deficit: " + fmt(deficit, 1) + " mm." : "No net deficit.");
    }

    function renderMetrics(input, result) {
        document.getElementById("m-rainfall").textContent = fmt(result.rainfall_pred, 1);
        document.getElementById("m-irrigation").textContent = fmt(result.irrigation_added, 0);
        document.getElementById("m-supply").textContent = fmt(result.effective_supply, 1);
        document.getElementById("m-demand").textContent = fmt(result.crop_demand, 1);
        document.getElementById("m-temp").textContent = fmt(result.temperature, 1);
        document.getElementById("m-humidity").textContent = fmt(result.humidity, 0);
        document.getElementById("m-wind").textContent = fmt(result.wind, 1);
        document.getElementById("m-solar").textContent = fmt(result.solar, 1);
    }

    function renderBar(result) {
        const total = Math.max(result.crop_demand, result.effective_supply);
        const supplyPct = total > 0 ? Math.min(100, (result.effective_supply / total) * 100) : 0;
        const deficitPct = total > 0 ? Math.max(0, 100 - supplyPct) : 0;
        document.getElementById("bar-supply").style.width = supplyPct.toFixed(1) + "%";
        document.getElementById("bar-deficit").style.width = deficitPct.toFixed(1) + "%";
        document.getElementById("bar-summary").textContent =
            fmt(result.effective_supply, 1) + " / " + fmt(result.crop_demand, 1) + " mm";
    }

    function renderRecommendations(recs) {
        const grid = document.getElementById("recommendations");
        grid.innerHTML = "";
        recs.forEach(r => {
            const card = document.createElement("div");
            card.className = "bg-surface-container-lowest border border-outline-variant rounded-lg p-5 flex gap-4";
            card.innerHTML =
                '<div class="text-secondary mt-1"><span class="material-symbols-outlined text-[22px]">check_circle</span></div>' +
                '<div><h5 class="text-body-lg font-body-lg text-primary font-bold mb-1"></h5>' +
                '<p class="text-body-md font-body-md text-on-surface-variant"></p></div>';
            card.querySelector("h5").textContent = r.title;
            card.querySelector("p").textContent = r.body;
            grid.appendChild(card);
        });
    }

    // Simple SVG line chart for seasonal trend.
    function renderTrend(trend, selectedMonth) {
        const container = document.getElementById("trend-chart");
        container.innerHTML = "";
        const rain = trend.rainfall || [];
        const demand = trend.demand || [];
        if (!rain.length && !demand.length) {
            container.innerHTML = '<p class="text-body-md font-body-md text-on-surface-variant py-8 text-center">No historical data available for this district / crop.</p>';
            return;
        }

        const W = container.clientWidth || 800;
        const H = 260;
        const pad = { l: 48, r: 16, t: 24, b: 36 };

        const allValues = [...rain.map(r => r.rainfall), ...demand.map(d => d.demand)];
        const yMax = Math.max(...allValues, 1) * 1.1;
        const yMin = 0;

        const xScale = m => pad.l + ((m - 1) / 11) * (W - pad.l - pad.r);
        const yScale = v => pad.t + (1 - (v - yMin) / (yMax - yMin)) * (H - pad.t - pad.b);

        const svgNS = "http://www.w3.org/2000/svg";
        const svg = document.createElementNS(svgNS, "svg");
        svg.setAttribute("viewBox", "0 0 " + W + " " + H);
        svg.setAttribute("width", "100%");
        svg.setAttribute("height", H);

        // Gridlines
        const yTicks = 4;
        for (let i = 0; i <= yTicks; i++) {
            const y = pad.t + (i / yTicks) * (H - pad.t - pad.b);
            const value = yMax - (i / yTicks) * yMax;
            const line = document.createElementNS(svgNS, "line");
            line.setAttribute("x1", pad.l);
            line.setAttribute("x2", W - pad.r);
            line.setAttribute("y1", y);
            line.setAttribute("y2", y);
            line.setAttribute("stroke", "#e1e3dd");
            line.setAttribute("stroke-width", "1");
            svg.appendChild(line);

            const label = document.createElementNS(svgNS, "text");
            label.setAttribute("x", pad.l - 8);
            label.setAttribute("y", y + 4);
            label.setAttribute("text-anchor", "end");
            label.setAttribute("font-size", "10");
            label.setAttribute("font-family", "JetBrains Mono, monospace");
            label.setAttribute("fill", "#717970");
            label.textContent = Math.round(value);
            svg.appendChild(label);
        }

        // X axis labels
        ["J","F","M","A","M","J","J","A","S","O","N","D"].forEach((m, i) => {
            const x = xScale(i + 1);
            const lbl = document.createElementNS(svgNS, "text");
            lbl.setAttribute("x", x);
            lbl.setAttribute("y", H - 12);
            lbl.setAttribute("text-anchor", "middle");
            lbl.setAttribute("font-size", "10");
            lbl.setAttribute("font-family", "JetBrains Mono, monospace");
            lbl.setAttribute("fill", "#717970");
            lbl.textContent = m;
            svg.appendChild(lbl);
        });

        // Selected month marker
        const markerX = xScale(selectedMonth);
        const marker = document.createElementNS(svgNS, "line");
        marker.setAttribute("x1", markerX);
        marker.setAttribute("x2", markerX);
        marker.setAttribute("y1", pad.t);
        marker.setAttribute("y2", H - pad.b);
        marker.setAttribute("stroke", "#01411C");
        marker.setAttribute("stroke-width", "1");
        marker.setAttribute("stroke-dasharray", "4 4");
        marker.setAttribute("opacity", "0.4");
        svg.appendChild(marker);

        function drawLine(points, color, width) {
            if (!points.length) return;
            const path = document.createElementNS(svgNS, "path");
            const d = points.map((p, i) => (i === 0 ? "M" : "L") + xScale(p.month) + " " + yScale(p.value)).join(" ");
            path.setAttribute("d", d);
            path.setAttribute("fill", "none");
            path.setAttribute("stroke", color);
            path.setAttribute("stroke-width", String(width));
            path.setAttribute("stroke-linecap", "round");
            path.setAttribute("stroke-linejoin", "round");
            svg.appendChild(path);

            points.forEach(p => {
                const dot = document.createElementNS(svgNS, "circle");
                dot.setAttribute("cx", xScale(p.month));
                dot.setAttribute("cy", yScale(p.value));
                dot.setAttribute("r", "3");
                dot.setAttribute("fill", color);
                svg.appendChild(dot);
            });
        }

        drawLine(rain.map(r => ({ month: r.month, value: r.rainfall })), "#00290f", 2);
        drawLine(demand.map(d => ({ month: d.month, value: d.demand })), "#D6A848", 2);

        container.appendChild(svg);
    }

    async function runForecast() {
        const payload = readForm();
        hide(emptyState);
        hide(errorState);
        hide(results);
        show(loadingState);

        try {
            const res = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            hide(loadingState);

            if (!res.ok) {
                errorMessage.textContent = data.detail || "Unknown error";
                show(errorState);
                return;
            }

            renderHeadline(payload, data.result);
            renderMetrics(payload, data.result);
            renderBar(data.result);
            renderRecommendations(data.recommendations);
            renderTrend(data.trend, payload.month);
            show(results);
        } catch (err) {
            hide(loadingState);
            errorMessage.textContent = err.message || "Network error";
            show(errorState);
        }
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        runForecast();
    });

    exportButton?.addEventListener("click", async () => {
        const payload = readForm();
        const res = await fetch("/api/predict/csv", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            errorMessage.textContent = data.detail || "CSV export failed";
            show(errorState);
            return;
        }
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "forecast_" + payload.district + "_" + payload.crop + "_"
            + payload.year + "-" + String(payload.month).padStart(2, "0") + ".csv";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
})();
