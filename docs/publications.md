---
layout: default
title: Publication
permalink: /publications/
---

# Publications and Research Outputs

### Manuscript & Preprint

**Title**: Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites  
**Authors**: Richard Barker et al.  
**Target Venue**: Nature Publishing Group (*npj Microgravity* / *Communications Biology*)

<div class="publication-card">
    <div class="pub-actions">
        <a href="https://github.com/dr-richard-barker/lunar-magnetic-biology/tree/main/manuscript" class="btn">LaTeX Source & Draft</a>
        <a href="https://doi.org/10.5281/zenodo.XXXXXXX" class="btn">Zenodo Data DOI</a>
        <a href="https://github.com/dr-richard-barker/lunar-magnetic-biology" class="btn">GitHub Repository</a>
        <button onclick="copyBibtex()" class="btn">Copy BibTeX</button>
    </div>
</div>

#### Abstract
The lunar magnetic environment is characterized by the absence of a global dipole and the presence of localized crustal magnetic anomalies. As humanity prepares to return to the Moon through the Artemis program, understanding this highly heterogeneous magnetic environment is crucial for biological systems and astronaut health. In this study, we map the lunar crustal magnetic field at candidate Artemis, Apollo, and Chang'e landing sites, combining satellite magnetometer data from Lunar Prospector and SELENE (Kaguya) with a systematic review of magnetobiology literature. We find that while all lunar landing sites present a hypomagnetic field (HMF) environment relative to Earth's geomagnetic field, significant heterogeneity exists. Some sites exhibit fields $< 1\text{ nT}$, whereas others present localized fields up to $\sim 20\text{ nT}$ at 30 km altitude. We synthesize existing evidence on the effects of HMF on plant growth, microbiome stability, and biological development, and discuss the implications for future lunar surface operations. Our findings provide a framework for integrating magnetic field heterogeneity into site selection and experimental design for upcoming lunar biological investigations.

---

### Citation

<pre id="bibtex-code">
@article{barker2026lunar,
  title={Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites},
  author={Barker, Richard and collaborators},
  journal={npj Microgravity / BioRxiv Preprint},
  year={2026},
  doi={10.5281/zenodo.XXXXXXX},
  url={https://github.com/dr-richard-barker/lunar-magnetic-biology}
}
</pre>

<script>
function copyBibtex() {
    const text = document.getElementById("bibtex-code").innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert("BibTeX citation copied to clipboard!");
    });
}
</script>
