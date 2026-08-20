---
layout: default
title: Interactive Globe
permalink: /globe/
---

# Interactive 3D Lunar Magnetic Globe

Use your mouse to rotate and zoom the moon. Click on a landing site marker to focus on it. Hover over markers to see site details.

<div class="globe-container-wrapper">
    <div id="globe-container"></div>
    
    <div class="control-panel">
        <h3>Controls</h3>
        <div class="control-group">
            <label for="layer-select">Magnetic Layer:</label>
            <select id="layer-select">
                <option value="magnitude">|B| Magnitude</option>
                <option value="br">Br Component</option>
                <option value="none">None</option>
            </select>
        </div>
        <div class="control-group">
            <label>
                <input type="checkbox" id="toggle-markers" checked> Show Landing Sites
            </label>
        </div>
        <div id="colorbar-legend" class="colorbar-legend">
            <div class="legend-labels">
                <span id="legend-min">0 nT</span>
                <span id="legend-max">Max nT</span>
            </div>
            <div class="legend-gradient"></div>
        </div>
        <div id="site-info" class="site-info">
            <p><em>Hover over a site for details.</em></p>
        </div>
    </div>
</div>

<div id="tooltip" class="tooltip" style="display: none;"></div>

<!-- Load Lunar Globe Script -->
<script type="module" src="{{ '/assets/js/lunar_globe.js' | relative_url }}"></script>
