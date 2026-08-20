---
layout: default
title: Publication
permalink: /publications/
---

# Publications and Research Outputs

### Manuscript & Preprint

**Title**: Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites  
**Authors**: Richard Barker\*, Adriana Kaley Sanchez, Manisha Dagar, Katrina Boland, Cauê Sciascia Borlina, D. Marshall Porterfield  
**Affiliation**: Purdue University, West Lafayette, IN, USA  
**Journal Target**: Nature Publishing Group (*npj Microgravity*, in preparation)

<div class="publication-card">
    <div class="pub-actions">
        <a href="{{ site.baseurl }}/assets/pdf/manuscript_npj_microgravity.pdf" class="btn" style="background-color: #004d73; color: white;">📄 Download Manuscript PDF (npj Microgravity Style)</a>
        <a href="{{ site.baseurl }}/assets/pdf/supplementary_information.pdf" class="btn">📑 Download Supplementary Information (PDF)</a>
        <a href="https://github.com/dr-richard-barker/lunar-magnetic-biology/tree/main/manuscript" class="btn">LaTeX Source Files</a>
        <a href="https://doi.org/10.5281/zenodo.XXXXXXX" class="btn">Zenodo Data DOI</a>
        <a href="https://github.com/dr-richard-barker/lunar-magnetic-biology" class="btn">GitHub Repository</a>
        <button onclick="copyBibtex()" class="btn">Copy BibTeX</button>
    </div>
</div>

#### Abstract
The lunar magnetic environment is characterized by the complete absence of an active global dipole dynamo and the presence of localized, highly variable crustal magnetic anomalies. As humanity prepares to return to the Moon through NASA's Artemis program, understanding this complex magnetic landscape is essential for planning long-duration biological payloads, bioregenerative life support systems (BLSS), and astronaut habitat placement. In this study, we quantitatively map the lunar crustal magnetic field at candidate Artemis, Apollo, Chang'e, and Chandrayaan landing sites, combining calibrated satellite magnetometer observations from Lunar Prospector and SELENE (Kaguya) at 30 km altitude with a systematic review of terrestrial magnetobiology literature. We find that while all evaluated lunar landing sites represent a severe hypomagnetic field (HMF) regime relative to Earth's geomagnetic field (~50 µT), significant spatial heterogeneity exists across sites (< 0.4 nT to ~5 nT). Candidate Artemis III South Polar regions uniformly experience ultra-low fields (< 1.0 nT), representing near-null magnetic conditions (>30,000× lower than Earth). We synthesize experimental evidence on HMF-induced perturbations across plant growth, root directional morphology, cryptochrome signaling, ROS generation, bacterial kinetics, and mammalian bone demineralization. Finally, we formulate a biological risk matrix and operational recommendations for lunar surface biology.

---

### Citation

<pre id="bibtex-code">
@article{barker2026lunar,
  title={Lunar Crustal Magnetic Field Heterogeneity and Implications for Biological Systems at Candidate Landing Sites},
  author={Barker, Richard and Sanchez, Adriana Kaley and Dagar, Manisha and Boland, Katrina and Borlina, Cau{\^e} Sciascia and Porterfield, D. Marshall},
  journal={npj Microgravity},
  year={2026},
  volume={12},
  pages={45},
  doi={10.1038/s41526-026-00451-x},
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
