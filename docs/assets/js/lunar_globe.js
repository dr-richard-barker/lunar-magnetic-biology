import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class LunarGlobe {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.width = this.container.clientWidth || 800;
        this.height = this.container.clientHeight || 600;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(45, this.width / this.height, 0.1, 100);
        this.camera.position.set(0, 0, 3.2);
        
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(this.width, this.height);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);
        
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enablePan = false;
        this.controls.minDistance = 1.3;
        this.controls.maxDistance = 6.0;
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.autoRotate = true;
        this.controls.autoRotateSpeed = 0.4;
        
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        
        this.globeRadius = 1.0;
        this.markers = [];
        this.data = null;
        this.overlayMesh = null;
        
        this.tooltip = document.getElementById('tooltip');
        this.siteInfo = document.getElementById('site-info');
        
        this.initLighting();
        this.initGlobe();
        this.addStars();
        
        this.loadData();
        
        window.addEventListener('resize', this.onWindowResize.bind(this));
        this.renderer.domElement.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.renderer.domElement.addEventListener('mousedown', () => { this.controls.autoRotate = false; });
        this.renderer.domElement.addEventListener('click', this.onClick.bind(this));
        
        this.animate();
        this.setupControls();
    }
    
    initLighting() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);
        
        const dirLight1 = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight1.position.set(5, 3, 5);
        this.scene.add(dirLight1);

        const dirLight2 = new THREE.DirectionalLight(0x8899bb, 0.6);
        dirLight2.position.set(-5, -2, -3);
        this.scene.add(dirLight2);
    }
    
    initGlobe() {
        const geometry = new THREE.SphereGeometry(this.globeRadius, 128, 64);
        
        const material = new THREE.MeshStandardMaterial({ 
            color: 0x999999,
            roughness: 0.85,
            metalness: 0.05
        });
        
        this.moon = new THREE.Mesh(geometry, material);
        this.scene.add(this.moon);
        
        const textureLoader = new THREE.TextureLoader();
        const moonTextureUrl = 'https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/moon_1024.jpg';
        
        textureLoader.load(moonTextureUrl, (texture) => {
            material.map = texture;
            material.needsUpdate = true;
        }, undefined, () => {
            console.log("Using procedural/fallback lunar color.");
        });
    }
    
    addStars() {
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 1200;
        const posArray = new Float32Array(starsCount * 3);
        
        for(let i = 0; i < starsCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 30;
        }
        
        starsGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const starsMaterial = new THREE.PointsMaterial({ size: 0.02, color: 0xddddff });
        const starMesh = new THREE.Points(starsGeometry, starsMaterial);
        this.scene.add(starMesh);
    }
    
    async loadData() {
        const urlsToTry = [
            '../assets/data/mag_field_data.json',
            './assets/data/mag_field_data.json',
            '/lunar-magnetic-biology/assets/data/mag_field_data.json',
            '../assets/js/mag_field_data.json',
            './assets/js/mag_field_data.json'
        ];

        for (const url of urlsToTry) {
            try {
                const response = await fetch(url);
                if (response.ok) {
                    this.data = await response.json();
                    break;
                }
            } catch (e) {
                // try next
            }
        }

        if (!this.data) {
            console.warn('Could not load external mag_field_data.json, using built-in catalog');
            this.data = {
                sites: [
                    { name: "Faustini Rim A", mission: "Artemis", lat: -85.3, lon: 77.0, Bmag: 0.45, classification: "low/null-field" },
                    { name: "Peak Near Shackleton", mission: "Artemis", lat: -89.7, lon: 166.0, Bmag: 0.82, classification: "low/null-field" },
                    { name: "Connecting Ridge", mission: "Artemis", lat: -88.0, lon: 137.0, Bmag: 0.60, classification: "low/null-field" },
                    { name: "Malapert Massif", mission: "Artemis", lat: -86.0, lon: 0.0, Bmag: 0.55, classification: "low/null-field" },
                    { name: "Leibnitz Beta Plateau", mission: "Artemis", lat: -85.0, lon: 31.0, Bmag: 0.70, classification: "low/null-field" },
                    { name: "Apollo 11", mission: "Apollo", lat: 0.67, lon: 23.47, Bmag: 0.42, classification: "low/null-field" },
                    { name: "Apollo 16", mission: "Apollo", lat: -8.97, lon: 15.50, Bmag: 4.15, classification: "moderate" },
                    { name: "Chang'e 4 (SPA Basin)", mission: "Chang'e", lat: -45.46, lon: 177.60, Bmag: 8.65, classification: "high-field" },
                    { name: "Chandrayaan-3", mission: "Chandrayaan", lat: -69.37, lon: 32.35, Bmag: 0.78, classification: "low/null-field" }
                ],
                grid: null
            };
        }
        
        this.createMarkers();
        this.createMagneticOverlay();
    }
    
    latLonToVector3(lat, lon, radius) {
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (lon + 180) * (Math.PI / 180);
        
        const x = -(radius * Math.sin(phi) * Math.cos(theta));
        const z = (radius * Math.sin(phi) * Math.sin(theta));
        const y = (radius * Math.cos(phi));
        
        return new THREE.Vector3(x, y, z);
    }
    
    createMarkers() {
        if(!this.data || !this.data.sites) return;
        
        this.markerGroup = new THREE.Group();
        this.scene.add(this.markerGroup);
        
        this.data.sites.forEach(site => {
            let geometry;
            if(site.mission === 'Artemis') {
                geometry = new THREE.ConeGeometry(0.018, 0.05, 8);
                geometry.translate(0, 0.025, 0); 
                geometry.rotateX(Math.PI / 2);
            } else if(site.mission === 'Apollo') {
                geometry = new THREE.SphereGeometry(0.016, 12, 12);
            } else {
                geometry = new THREE.OctahedronGeometry(0.018);
            }
            
            const bval = site.Bmag !== undefined ? site.Bmag : site.b_mag;
            const cls = (site.classification || '').toLowerCase();
            
            let color = 0x29b6f6; // blue: low/null
            if(cls.includes('high') || (bval && bval > 5.0)) {
                color = 0xef5350; // red: high
            } else if(cls.includes('mod') || (bval && bval >= 1.0)) {
                color = 0xffa726; // orange: moderate
            }
            
            const material = new THREE.MeshStandardMaterial({ 
                color: color,
                emissive: color,
                emissiveIntensity: 0.4,
                roughness: 0.3
            });
            const mesh = new THREE.Mesh(geometry, material);
            
            const pos = this.latLonToVector3(site.lat, site.lon, this.globeRadius * 1.008);
            mesh.position.copy(pos);
            mesh.lookAt(new THREE.Vector3(0,0,0)); 
            
            mesh.userData = site;
            this.markerGroup.add(mesh);
            this.markers.push(mesh);
        });
    }
    
    createMagneticOverlay() {
        const overlayGeo = new THREE.SphereGeometry(this.globeRadius * 1.004, 128, 64);
        
        const textureLoader = new THREE.TextureLoader();
        const textureUrls = [
            '../assets/img/lunar_mag_texture.png',
            './assets/img/lunar_mag_texture.png',
            '/lunar-magnetic-biology/assets/img/lunar_mag_texture.png'
        ];

        const tryLoadTexture = (index) => {
            if (index >= textureUrls.length) {
                this.createProceduralOverlay(overlayGeo);
                return;
            }
            textureLoader.load(
                textureUrls[index],
                (texture) => {
                    texture.wrapS = THREE.RepeatWrapping;
                    texture.wrapT = THREE.ClampToEdgeWrapping;
                    const overlayMat = new THREE.MeshBasicMaterial({
                        map: texture,
                        transparent: true,
                        opacity: 0.65,
                        blending: THREE.NormalBlending,
                        depthWrite: false
                    });
                    this.overlayMesh = new THREE.Mesh(overlayGeo, overlayMat);
                    this.scene.add(this.overlayMesh);
                },
                undefined,
                () => tryLoadTexture(index + 1)
            );
        };

        tryLoadTexture(0);
    }

    createProceduralOverlay(overlayGeo) {
        const overlayMat = new THREE.ShaderMaterial({
            uniforms: {
                opacity: { value: 0.55 }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform float opacity;
                varying vec2 vUv;
                void main() {
                    float v = sin(vUv.x * 12.0) * sin(vUv.y * 8.0);
                    v = clamp((v + 0.8) / 1.6, 0.0, 1.0);
                    vec3 col = mix(vec3(0.1, 0.2, 0.8), vec3(0.9, 0.1, 0.2), v);
                    gl_FragColor = vec4(col, opacity * v);
                }
            `,
            transparent: true,
            depthWrite: false
        });
        this.overlayMesh = new THREE.Mesh(overlayGeo, overlayMat);
        this.scene.add(this.overlayMesh);
    }
    
    setupControls() {
        const layerSelect = document.getElementById('layer-select');
        if (layerSelect) {
            layerSelect.addEventListener('change', (e) => {
                if(this.overlayMesh) {
                    this.overlayMesh.visible = e.target.value !== 'none';
                }
            });
        }
        
        const toggleMarkers = document.getElementById('toggle-markers');
        if (toggleMarkers) {
            toggleMarkers.addEventListener('change', (e) => {
                if(this.markerGroup) {
                    this.markerGroup.visible = e.target.checked;
                }
            });
        }
    }
    
    onWindowResize() {
        if (!this.container) return;
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight;
        this.camera.aspect = this.width / this.height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.width, this.height);
    }
    
    onMouseMove(event) {
        const rect = this.renderer.domElement.getBoundingClientRect();
        this.mouse.x = ((event.clientX - rect.left) / this.width) * 2 - 1;
        this.mouse.y = -((event.clientY - rect.top) / this.height) * 2 + 1;
        
        this.raycaster.setFromCamera(this.mouse, this.camera);
        
        if(!this.markerGroup || !this.markerGroup.visible) {
            if (this.tooltip) this.tooltip.style.display = 'none';
            return;
        }
        
        const intersects = this.raycaster.intersectObjects(this.markers);
        
        if (intersects.length > 0) {
            const site = intersects[0].object.userData;
            const bVal = site.Bmag !== undefined ? (site.Bmag !== null ? Number(site.Bmag).toFixed(2) : 'N/A') : site.b_mag;
            
            if (this.tooltip) {
                this.tooltip.style.display = 'block';
                this.tooltip.style.left = (event.clientX + 12) + 'px';
                this.tooltip.style.top = (event.clientY + 12) + 'px';
                this.tooltip.innerHTML = `<strong>${site.name}</strong><br>|B|: ${bVal} nT (${site.classification || 'unknown'})`;
            }
            
            if (this.siteInfo) {
                this.siteInfo.innerHTML = `
                    <p><strong>Site:</strong> ${site.name}</p>
                    <p><strong>Mission:</strong> ${site.mission}</p>
                    <p><strong>Coordinates:</strong> ${Number(site.lat).toFixed(2)}° Lat, ${Number(site.lon).toFixed(2)}° Lon</p>
                    <p><strong>|B| Magnetic Field:</strong> ${bVal} nT</p>
                    <p><strong>Classification:</strong> ${site.classification || 'unknown'}</p>
                    ${site.notes ? `<p><small><em>${site.notes}</em></small></p>` : ''}
                `;
            }
            document.body.style.cursor = 'pointer';
        } else {
            if (this.tooltip) this.tooltip.style.display = 'none';
            document.body.style.cursor = 'default';
        }
    }
    
    onClick(event) {
        this.raycaster.setFromCamera(this.mouse, this.camera);
        if(!this.markerGroup || !this.markerGroup.visible) return;
        
        const intersects = this.raycaster.intersectObjects(this.markers);
        if(intersects.length > 0) {
            const mesh = intersects[0].object;
            const targetPos = mesh.position.clone().multiplyScalar(1.6);
            
            this.camera.position.copy(targetPos);
            this.camera.lookAt(new THREE.Vector3(0,0,0));
            this.controls.update();
        }
    }
    
    animate() {
        requestAnimationFrame(this.animate.bind(this));
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new LunarGlobe('globe-container');
});
