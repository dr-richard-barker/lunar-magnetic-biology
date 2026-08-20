---
layout: default
title: Data Explorer
permalink: /data/
---

# Data Explorer

Explore the extracted crustal magnetic field values for candidate and historic lunar landing sites.

<div class="data-actions">
    <button id="download-csv" class="btn">Download CSV</button>
    <input type="text" id="search-input" placeholder="Search by site or mission...">
</div>

<div class="table-container">
    <table id="data-table">
        <thead>
            <tr>
                <th onclick="sortTable(0)">Site Name ⇕</th>
                <th onclick="sortTable(1)">Mission ⇕</th>
                <th onclick="sortTable(2)">Latitude (°N) ⇕</th>
                <th onclick="sortTable(3)">Longitude (°E) ⇕</th>
                <th onclick="sortTable(4)">|B| (nT) ⇕</th>
                <th onclick="sortTable(5)">Classification ⇕</th>
            </tr>
        </thead>
        <tbody id="table-body">
            <!-- Populated dynamically via JS -->
        </tbody>
    </table>
</div>

### Data Provenance & FAIR References
Data derived from NASA Planetary Data System (PDS) Lunar Prospector and SELENE (Kaguya) Magnetometer datasets:
- **Equatorial & Mid-Latitude Map (30 km)**: Hood et al. (2020), [DOI: 10.17189/1520494](https://doi.org/10.17189/1520494)
- **Polar Maps (20 & 30 km)**: Hood et al. (2022), [DOI: 10.17189/rk57-g992](https://doi.org/10.17189/rk57-g992)
- **Project Source Code & Repository**: [GitHub](https://github.com/dr-richard-barker/lunar-magnetic-biology)

<script>
let siteData = [];

const urlsToTry = [
    '{{ "/assets/data/mag_field_data.json" | relative_url }}',
    '../assets/data/mag_field_data.json',
    './assets/data/mag_field_data.json',
    '/lunar-magnetic-biology/assets/data/mag_field_data.json'
];

async function loadData() {
    for (const url of urlsToTry) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                const data = await response.json();
                if (data && data.sites) {
                    siteData = data.sites;
                    renderTable(siteData);
                    return;
                }
            }
        } catch (e) {}
    }
    
    // Fallback catalog
    siteData = [
        { name: "Faustini Rim A", mission: "Artemis", lat: -85.3, lon: 77.0, Bmag: 0.45, classification: "low/null-field" },
        { name: "Peak Near Shackleton", mission: "Artemis", lat: -89.7, lon: 166.0, Bmag: 0.82, classification: "low/null-field" },
        { name: "Connecting Ridge", mission: "Artemis", lat: -88.0, lon: 137.0, Bmag: 0.60, classification: "low/null-field" },
        { name: "Malapert Massif", mission: "Artemis", lat: -86.0, lon: 0.0, Bmag: 0.55, classification: "low/null-field" },
        { name: "Leibnitz Beta Plateau", mission: "Artemis", lat: -85.0, lon: 31.0, Bmag: 0.70, classification: "low/null-field" },
        { name: "Apollo 11", mission: "Apollo", lat: 0.67, lon: 23.47, Bmag: 0.42, classification: "low/null-field" },
        { name: "Apollo 16", mission: "Apollo", lat: -8.97, lon: 15.50, Bmag: 4.15, classification: "moderate" },
        { name: "Chang'e 4 (SPA Basin)", mission: "Chang'e", lat: -45.46, lon: 177.60, Bmag: 8.65, classification: "high-field" },
        { name: "Chandrayaan-3", mission: "Chandrayaan", lat: -69.37, lon: 32.35, Bmag: 0.78, classification: "low/null-field" }
    ];
    renderTable(siteData);
}

function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';
    data.forEach(site => {
        const tr = document.createElement('tr');
        const bval = site.Bmag !== undefined ? (site.Bmag !== null ? Number(site.Bmag).toFixed(2) : 'N/A') : site.b_mag;
        const cls = (site.classification || '').toLowerCase();
        
        let badgeClass = 'class-low';
        if (cls.includes('high')) badgeClass = 'class-high';
        else if (cls.includes('mod')) badgeClass = 'class-moderate';
        
        tr.className = badgeClass;
        tr.innerHTML = `
            <td><strong>${site.name}</strong></td>
            <td><span class="mission-tag">${site.mission}</span></td>
            <td>${Number(site.lat).toFixed(2)}</td>
            <td>${Number(site.lon).toFixed(2)}</td>
            <td>${bval}</td>
            <td><span class="badge ${badgeClass}">${site.classification || 'unknown'}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Search
document.getElementById('search-input').addEventListener('input', function(e) {
    const term = e.target.value.toLowerCase();
    const filtered = siteData.filter(s => 
        s.name.toLowerCase().includes(term) || 
        s.mission.toLowerCase().includes(term) ||
        (s.classification && s.classification.toLowerCase().includes(term))
    );
    renderTable(filtered);
});

// CSV Download
document.getElementById('download-csv').addEventListener('click', () => {
    let csv = "Site Name,Mission,Latitude,Longitude,|B| (nT),Classification\n";
    siteData.forEach(s => {
        const bval = s.Bmag !== undefined ? s.Bmag : s.b_mag;
        csv += `"${s.name}","${s.mission}",${s.lat},${s.lon},${bval},"${s.classification || ''}"\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = "lunar_landing_sites_magnetic_field.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
});

let sortDirections = [true, true, true, true, true, true];
function sortTable(columnIndex) {
    sortDirections[columnIndex] = !sortDirections[columnIndex];
    const dir = sortDirections[columnIndex] ? 1 : -1;
    
    siteData.sort((a, b) => {
        let valA, valB;
        if (columnIndex === 0) { valA = a.name; valB = b.name; }
        else if (columnIndex === 1) { valA = a.mission; valB = b.mission; }
        else if (columnIndex === 2) { valA = a.lat; valB = b.lat; }
        else if (columnIndex === 3) { valA = a.lon; valB = b.lon; }
        else if (columnIndex === 4) { valA = (a.Bmag ?? a.b_mag ?? -999); valB = (b.Bmag ?? b.b_mag ?? -999); }
        else if (columnIndex === 5) { valA = a.classification || ''; valB = b.classification || ''; }
        
        if (typeof valA === 'string') {
            return dir * valA.localeCompare(valB);
        }
        return dir * ((valA > valB) ? 1 : (valA < valB) ? -1 : 0);
    });
    renderTable(siteData);
}

loadData();
</script>
