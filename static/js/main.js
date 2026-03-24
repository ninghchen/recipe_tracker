// ── INGREDIENTS ──
function addIngredient() {
  const container = document.getElementById('ingredients-container');
  if (!container) return;
  const row = document.createElement('div');
  row.className = 'ingredient-row';
  row.innerHTML = `
    <input type="text" name="ing_name[]" class="form-control" placeholder="e.g. Banana">
    <input type="text" name="ing_amount[]" class="form-control" placeholder="e.g. 1">
    <input type="text" name="ing_unit[]" class="form-control" placeholder="e.g. cup">
    <button type="button" class="remove-ing" onclick="removeIngredient(this)" title="Remove">✕</button>
  `;
  container.appendChild(row);
  row.querySelector('input').focus();
}

function removeIngredient(btn) {
  const container = document.getElementById('ingredients-container');
  if (container.children.length > 1) {
    btn.closest('.ingredient-row').remove();
  }
}

// ── STEPS ──
function addStep() {
  const container = document.getElementById('steps-container');
  if (!container) return;
  const num = container.children.length + 1;
  const row = document.createElement('div');
  row.className = 'step-row';
  row.innerHTML = `
    <div class="step-drag">⠿</div>
    <div class="step-num">${num}</div>
    <div class="step-fields">
      <input type="text" name="step_title[]" class="form-control step-title-input"
             placeholder="Step title (optional) — e.g. Brown the meat">
      <textarea name="step_desc[]" class="form-control" rows="3"
                placeholder="Describe what to do in this step…"></textarea>
    </div>
    <button type="button" class="remove-step" onclick="removeStep(this)" title="Remove step">✕</button>
  `;
  container.appendChild(row);
  row.querySelector('input').focus();
  row.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function removeStep(btn) {
  const container = document.getElementById('steps-container');
  if (container.children.length > 1) {
    btn.closest('.step-row').remove();
    renumberSteps();
  }
}

function renumberSteps() {
  const container = document.getElementById('steps-container');
  if (!container) return;
  Array.from(container.querySelectorAll('.step-num')).forEach((el, i) => {
    el.textContent = i + 1;
  });
}

// ── IMAGE PREVIEW ──
function previewImage(input) {
  const preview = document.getElementById('image-preview');
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
  }
}

// ── DRAG-AND-DROP STEP REORDERING ──
function initStepDragDrop() {
  const container = document.getElementById('steps-container');
  if (!container) return;

  let dragEl = null;

  container.addEventListener('dragstart', e => {
    dragEl = e.target.closest('.step-row');
    if (dragEl) {
      dragEl.style.opacity = '0.5';
      e.dataTransfer.effectAllowed = 'move';
    }
  });

  container.addEventListener('dragend', e => {
    if (dragEl) {
      dragEl.style.opacity = '';
      dragEl = null;
      renumberSteps();
    }
  });

  container.addEventListener('dragover', e => {
    e.preventDefault();
    const target = e.target.closest('.step-row');
    if (target && target !== dragEl) {
      const rect = target.getBoundingClientRect();
      const midY = rect.top + rect.height / 2;
      if (e.clientY < midY) {
        container.insertBefore(dragEl, target);
      } else {
        container.insertBefore(dragEl, target.nextSibling);
      }
    }
  });
}

// ── DRAG UPLOAD ──
function initImageDrop() {
  const area = document.getElementById('upload-area');
  if (!area) return;
  area.addEventListener('dragover', e => { e.preventDefault(); area.style.borderColor = 'var(--sky)'; area.style.background = 'rgba(74,144,164,0.06)'; });
  area.addEventListener('dragleave', () => { area.style.borderColor = ''; area.style.background = ''; });
  area.addEventListener('drop', () => { area.style.borderColor = ''; area.style.background = ''; });
}

// ── COOKING MODE ──
function initCookingMode() {
  const steps = document.querySelectorAll('.step-card');
  if (!steps.length) return;

  let activeStep = 0;

  // Add "Mark done" button to each step card on recipe page
  steps.forEach((card, i) => {
    const btn = document.createElement('button');
    btn.className = 'step-done-btn';
    btn.textContent = i === 0 ? '✓ Mark done' : '✓ Mark done';
    btn.onclick = () => {
      card.classList.toggle('step-done');
      btn.textContent = card.classList.contains('step-done') ? '↩ Undo' : '✓ Mark done';
    };
    card.appendChild(btn);
  });
}

// ── INIT ──
document.addEventListener('DOMContentLoaded', () => {
  initStepDragDrop();
  initImageDrop();
  initCookingMode();

  // Animate elements into view
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.animationPlayState = 'running';
      }
    });
  }, { threshold: 0.05 });

  document.querySelectorAll('.step-card, .recipe-card, .category-card, .form-card, .info-card').forEach(el => {
    observer.observe(el);
  });
});

// Close categories dropdown when clicking outside
document.addEventListener('click', function(e) {
  const dropdown = document.querySelector('.nav-dropdown');
  if (dropdown && !dropdown.contains(e.target)) {
    dropdown.classList.remove('open');
  }
});
