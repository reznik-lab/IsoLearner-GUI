let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Nucleus
let nucleusGeometry = new THREE.SphereGeometry(5, 32, 32);
let nucleusMaterial = new THREE.MeshBasicMaterial({ color: 0x61dafb });
let nucleus = new THREE.Mesh(nucleusGeometry, nucleusMaterial);
scene.add(nucleus);

// Electrons
let electronGeometry = new THREE.SphereGeometry(1, 32, 32);
let electronMaterial = new THREE.MeshBasicMaterial({ color: 0xe31b6d });

let radii = [10, 15, 20];
let speeds = [0.02, 0.015, 0.01];

radii.forEach((radius, index) => {
    for (let i = 0; i < 8; i++) {
        let electron = new THREE.Mesh(electronGeometry, electronMaterial);
        let angle = (i / 8) * Math.PI * 2;
        electron.position.x = radius * Math.cos(angle);
        electron.position.y = radius * Math.sin(angle);
        electron.userData = { angle: angle, speed: speeds[index], radius: radius };
        scene.add(electron);
    }
});

camera.position.z = 50;

function animate() {
    requestAnimationFrame(animate);

    scene.children.forEach(child => {
        if (child !== nucleus && child instanceof THREE.Mesh) {
            child.userData.angle += child.userData.speed;
            child.position.x = child.userData.radius * Math.cos(child.userData.angle);
            child.position.y = child.userData.radius * Math.sin(child.userData.angle);
        }
    });

    renderer.render(scene, camera);
}

animate();

window.addEventListener('resize', function() {
    let width = window.innerWidth;
    let height = window.innerHeight;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
});
