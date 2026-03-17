function generateGSD() {
  if (gsdSelected.size < 2) {
    alert('Please select at least 2 frequencies to generate your symbol.');
    return;
  }

  const template = document.querySelector('input[name="gsd-template"]:checked').value;
  const canvas = document.getElementById('gsd-canvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const cx = W / 2, cy = H / 2;

  // Clear
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#050508';
  ctx.fillRect(0, 0, W, H);

  const selectedFreqs = GSD_FREQS.filter(f => gsdSelected.has(f.hz));
  const maxR = Math.min(W, H) * 0.41;

  // ── STEP 1: Base template (dim background layer) ──
  ctx.save();
  ctx.globalAlpha = 0.22;
  switch (template) {
    case 'flower':       drawFlowerOfLife(ctx, cx, cy, maxR * 0.33); break;
    case 'seed':         drawSeedOfLife(ctx, cx, cy, maxR * 0.38); break;
    case 'phi':          drawPhiSpiral(ctx, cx, cy, maxR); break;
    case 'torus':        drawTorusField(ctx, cx, cy, maxR); break;
    case 'vesica':       drawVesicaPiscis(ctx, cx, cy, maxR * 0.6); break;
    case 'quasicrystal': drawQuasicrystal(ctx, cx, cy, maxR); break;
  }
  ctx.restore();

  // ── STEP 2: Phi-ratio concentric guide rings ──
  ctx.save();
  ctx.globalAlpha = 0.08;
  ctx.strokeStyle = 'rgba(212,175,55,0.6)';
  ctx.lineWidth = 0.4;
  let guideR = maxR;
  for (let i = 0; i < 8; i++) {
    ctx.beginPath(); ctx.arc(cx, cy, guideR, 0, GSD_TAU); ctx.stroke();
    guideR /= GSD_PHI;
    if (guideR < 8) break;
  }
  ctx.restore();

  // ── STEP 3: Radial symmetry lines ──
  const sorted = [...selectedFreqs].sort((a, b) => a.hz - b.hz);
  // Symmetry fold is determined by the template, not the number of frequencies
  const templateSymmetry = {
    flower: 6, seed: 6, phi: 4, torus: 8, vesica: 2, quasicrystal: 10
  };
  const symmetryFold = templateSymmetry[template] || 6;
  ctx.save();
  ctx.globalAlpha = 0.06;
  ctx.strokeStyle = 'rgba(212,175,55,0.8)';
  ctx.lineWidth = 0.4;
  for (let i = 0; i < symmetryFold; i++) {
    const angle = i * GSD_TAU / symmetryFold;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + maxR * 1.05 * Math.cos(angle), cy + maxR * 1.05 * Math.sin(angle));
    ctx.stroke();
  }
  ctx.restore();

  // ── STEP 4: Frequency layers (Structural Node Placement) ──
  // Shapes are placed at the actual mathematical intersection nodes of the chosen template
  // rather than just stacked concentrically in the center.
  
  // Calculate node positions based on the selected template
  const nodes = [];
  
  if (template === 'flower' || template === 'seed') {
    // 6-fold petal intersections
    const r = template === 'flower' ? maxR * 0.33 : maxR * 0.38;
    for (let i = 0; i < 6; i++) {
      const angle = i * GSD_TAU / 6;
      nodes.push({ x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), angle });
    }
  } else if (template === 'phi') {
    // Points along the golden spiral arms
    const a = maxR * 0.04;
    const b = Math.log(GSD_PHI) / Math.PI;
    for (let i = 0; i < 4; i++) { // 4 mirrored arms
      const t = GSD_TAU * 1.5; // Midpoint of spiral
      const rad = a * Math.exp(b * t);
      const angle = (i * GSD_TAU / 4) + t;
      nodes.push({ x: cx + rad * Math.cos(angle), y: cy + rad * Math.sin(angle), angle });
    }
  } else if (template === 'torus') {
    // Points along the major radius (center of the tube)
    const R = maxR * 0.6;
    for (let i = 0; i < 8; i++) {
      const angle = i * GSD_TAU / 8;
      nodes.push({ x: cx + R * Math.cos(angle), y: cy + R * Math.sin(angle), angle });
    }
  } else if (template === 'vesica') {
    // The two circle centers and the top/bottom lens intersections
    const r = maxR * 0.6;
    const h = r * Math.sqrt(3) / 2;
    nodes.push({ x: cx - r/2, y: cy, angle: Math.PI }); // Left center
    nodes.push({ x: cx + r/2, y: cy, angle: 0 }); // Right center
    nodes.push({ x: cx, y: cy - h, angle: -Math.PI/2 }); // Top intersection
    nodes.push({ x: cx, y: cy + h, angle: Math.PI/2 }); // Bottom intersection
  } else if (template === 'quasicrystal') {
    // 10-fold vertices of the inner decagon
    const r = maxR * 0.5;
    for (let i = 0; i < 10; i++) {
      const angle = i * GSD_TAU / 10 - Math.PI / 10;
      nodes.push({ x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle), angle });
    }
  }

  // Draw the frequencies
  sorted.forEach((freq, i) => {
    // The lowest frequency (foundation) goes in the center
    if (i === 0) {
      const layerR = maxR * 0.45;
      drawShape(ctx, freq.shape, cx, cy, layerR, freq.color, 0.8, 0, freq.sides || 0);
    } 
    // The highest frequency (apex) goes on the outer boundary
    else if (i === sorted.length - 1 && sorted.length > 2) {
      const layerR = maxR * 0.85;
      drawShape(ctx, freq.shape, cx, cy, layerR, freq.color, 0.6, Math.PI / sorted.length, freq.sides || 0);
    }
    // Middle frequencies are distributed across the template's structural nodes
    else {
      const shapeR = maxR * 0.18; // Smaller radius for node shapes
      const alpha = 0.7;
      
      // If we have nodes, place this frequency's shape at every node
      if (nodes.length > 0) {
        nodes.forEach(node => {
          // Rotate the shape to point outward from the center
          const rotation = node.angle + Math.PI / 2;
          drawShape(ctx, freq.shape, node.x, node.y, shapeR, freq.color, alpha, rotation, freq.sides || 0);
        });
      } else {
        // Fallback if no nodes (shouldn't happen)
        const layerR = maxR * Math.pow(1 / GSD_PHI, i * 0.55);
        drawShape(ctx, freq.shape, cx, cy, layerR, freq.color, alpha, 0, freq.sides || 0);
      }
    }
  });

  // ── STEP 5: Connecting lines between adjacent layers ──
  ctx.save();
  ctx.globalAlpha = 0.12;
  ctx.strokeStyle = 'rgba(212,175,55,0.5)';
  ctx.lineWidth = 0.5;
  for (let i = 0; i < sorted.length - 1; i++) {
    const r1 = maxR * Math.pow(1 / GSD_PHI, i * 0.55);
    const r2 = maxR * Math.pow(1 / GSD_PHI, (i + 1) * 0.55);
    // Draw connecting arc
    ctx.beginPath(); ctx.arc(cx, cy, (r1 + r2) / 2, 0, GSD_TAU); ctx.stroke();
  }
  ctx.restore();

  // ── STEP 6: Central point (anchor) ──
  const gradient = ctx.createRadialGradient(cx, cy, 0, cx, cy, 18);
  gradient.addColorStop(0, 'rgba(255,255,255,0.95)');
  gradient.addColorStop(0.35, 'rgba(212,175,55,0.7)');
  gradient.addColorStop(1, 'rgba(212,175,55,0)');
  ctx.fillStyle = gradient;
  ctx.beginPath(); ctx.arc(cx, cy, 18, 0, GSD_TAU); ctx.fill();

  // ── STEP 7: Outer boundary ring ──
  ctx.save();
  ctx.globalAlpha = 0.45;
  ctx.strokeStyle = 'rgba(212,175,55,0.5)';
  ctx.lineWidth = 1;
  ctx.beginPath(); ctx.arc(cx, cy, maxR * 1.04, 0, GSD_TAU); ctx.stroke();
  ctx.globalAlpha = 0.2;
  ctx.beginPath(); ctx.arc(cx, cy, maxR * 1.08, 0, GSD_TAU); ctx.stroke();
  ctx.restore();

  // ── Show output ──
  const output = document.getElementById('gsd-output');
  output.style.display = 'block';
  output.scrollIntoView({ behavior: 'smooth', block: 'start' });

  const meta = document.getElementById('gsd-output-meta');
  const templateNames = {
    flower: 'Flower of Life', seed: 'Seed of Life', phi: 'Phi Spiral',
    torus: 'Torus Field', vesica: 'Vesica Piscis', quasicrystal: 'Quasicrystal'
  };
  meta.innerHTML = `
    <strong style="color:var(--gold-mid);">Symbol Generated</strong><br>
    <span>Frequencies: ${sorted.map(f => f.hz + ' Hz').join(' . ')}</span><br>
    <span>Base: ${templateNames[template] || template} . Layers: ${sorted.length} . Symmetry: ${symmetryFold}-fold</span><br>
    <span style="font-size:0.75rem;opacity:0.6;">432 Hz scale . Golden Ratio proportions (phi = 1.618)</span>
  `;

  document.getElementById('gsd-reading-box').style.display = 'none';
  document.getElementById('gsd-reading-text').textContent = '';
}

function downloadGSD() {
  const canvas = document.getElementById('gsd-canvas');
  const link = document.createElement('a');
  link.download = 'taylored-harmony-symbol.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}

async function requestGSDReading() {
  const btn = document.getElementById('gsd-reading-btn');
  const box = document.getElementById('gsd-reading-box');
  const text = document.getElementById('gsd-reading-text');

  btn.disabled = true;
  btn.textContent = 'Generating reading...';
  box.style.display = 'block';
  document.getElementById('gsd-loading-state').style.display = 'block';
  document.getElementById('gsd-result-state').style.display = 'none';
  text.textContent = '';
  let gsdProgress=0;const gsdProgressBar=document.getElementById('gsd-progress-bar');const gsdProgressInterval=setInterval(function(){gsdProgress=Math.min(gsdProgress+(Math.random()*3+0.5),90);gsdProgressBar.style.width=gsdProgress+'%';},600);

  const selectedFreqs = GSD_FREQS.filter(f => gsdSelected.has(f.hz));
  const template = document.querySelector('input[name="gsd-template"]:checked').value;
  const freqSummary = selectedFreqs.map(f => `${f.hz} Hz (${f.name}  -  ${f.desc})`).join(', ');

  try {
    const response = await fetch('https://taylored-harmony.tayloredharmony.workers.dev/gsd-reading', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ frequencies: freqSummary, template })
    });
    const data = await response.json();
    clearInterval(gsdProgressInterval);
    document.getElementById('gsd-progress-bar').style.width = '100%';
    setTimeout(function() {
      document.getElementById('gsd-loading-state').style.display = 'none';
      document.getElementById('gsd-result-state').style.display = 'block';
      text.textContent = data.reading || 'Unable to generate reading at this time.';
    }, 400);
  } catch(e) {
    clearInterval(gsdProgressInterval);
    document.getElementById('gsd-loading-state').style.display = 'none';
    document.getElementById('gsd-result-state').style.display = 'block';
    text.textContent = 'Unable to generate reading at this time. Please try again in a moment.';
  }
  btn.disabled = false;
  btn.textContent = '✦ Geometry Analysis';
}

// Init on load
document.addEventListener('DOMContentLoaded', initGSD);


// Navigation toggle