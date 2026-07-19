(function () {
  'use strict';

  const LESSONS = {
    '/riemann-sum': {
      name: 'Area, one strip at a time',
      stages: [
        { targets: ['header'], title: 'From curved area to a repeatable pattern', copy: 'A definite integral is signed area. We cannot tile a curved roof exactly with simple shapes, so we start with rectangles and make them thinner.', math: String.raw`\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^n f(x_i^*)\,\Delta x` },
        { targets: ['.panel .field', '.bounds-grid'], title: 'Choose the curve and the interval', copy: 'The function sets each strip height. The limits a and b set the floor we divide. Try the built-in sine example first; the picture and every equation will update together.' },
        { targets: ['.method-row', '.n-row'], title: 'Change the sampling rule', copy: 'Left, right, and midpoint choose different points on each strip. Trapezoids connect both edges. Increase n and watch the gaps between the shapes and curve collapse.' },
        { targets: ['.canvas-wrap'], title: 'Read the geometry before the number', copy: 'Each colored shape has width Δx and a height sampled from the curve. The total colored area is the sum. Hover the plot to inspect a strip, then compare the visible gaps.' },
        { targets: ['.steps-panel'], title: 'Now build the equation', copy: 'Use Next step to reveal the partition, sample point, first strips, and sum in order. The final value stays hidden until the preceding manipulations are visible.' }
      ]
    },
    '/substitution': {
      name: 'Watch a strip change coordinates',
      stages: [
        { targets: ['header'], title: 'Substitution is a coordinate change', copy: 'The area does not change. We only measure the same thin strip using u instead of x.', math: String.raw`u=g(x),\qquad du=g'(x)\,dx` },
        { targets: ['.panel'], title: 'Spot the inner function and its derivative', copy: 'Choose u=g(x). The extra factor g′(x) is not decoration: it converts the strip width dx into du.' },
        { targets: ['.plots-row .canvas-wrap'], title: 'One strip, two coordinate systems', copy: 'The highlighted strip is the same contribution in both plots. Its width stretches or shrinks, while its height compensates so signed area is preserved.' },
        { targets: ['.ctrl-row'], title: 'Scrub the mapping yourself', copy: 'Move the strip slowly. Notice that equal x-steps usually do not become equal u-steps. That geometric stretching is exactly what g′(x) measures.' },
        { targets: ['.steps-panel'], title: 'Transform every symbol in order', copy: 'Reveal u, then du, then the new bounds, and only then the transformed integral. This prevents the common mistake of changing the integrand but leaving old bounds.' }
      ]
    },
    '/integration-by-parts': {
      name: 'Split a rectangle into two areas',
      stages: [
        { targets: ['header'], title: 'The product rule, seen as area', copy: 'As u and v grow together, the boundary rectangle uv is filled by two swept regions. Rearranging that split gives integration by parts.', math: String.raw`d(uv)=u\,dv+v\,du` },
        { targets: ['.panel'], title: 'Choose which factor changes gently', copy: 'Pick u so differentiating simplifies it, and dv so integrating it is manageable. The LIATE hint is a heuristic, not a law.' },
        { targets: ['.canvas-wrap'], title: 'See the rectangle tile itself', copy: 'The two colored regions complement each other inside the uv boundary rectangle. The original integral is one sweep; the remainder is the other.' },
        { targets: ['.ctrl-row'], title: 'Switch viewpoints', copy: 'Use the view controls to connect the uv-plane geometry to the familiar x-domain curves. Pause on any position and trace the matching boundary values.' },
        { targets: ['.steps-panel'], title: 'Reverse the product rule line by line', copy: 'Reveal du and v, substitute them into [uv]−∫vdu, evaluate the boundary, and only then simplify the remainder.' }
      ]
    },
    '/partial-derivatives': {
      name: 'Slice a surface to measure slope',
      stages: [
        { targets: ['header'], title: 'A surface has more than one slope', copy: 'At one point, moving east can feel different from moving north. Partial derivatives measure those axis-aligned slopes.', math: String.raw`\nabla f=(f_x,f_y)` },
        { targets: ['.panel'], title: 'Plant the probe', copy: 'Choose a surface and a point (x₀,y₀). The point stays fixed while we compare the two perpendicular slices through it.' },
        { targets: ['.canvas-wrap'], title: 'Read the tangent geometry', copy: 'The slice slopes become two components of one arrow. That gradient arrow points across the surface in the steepest uphill direction.' },
        { targets: ['.ctrl-row'], title: 'Rotate and compare views', copy: 'Switch between the surface and the top-down gradient map. The same local information appears as a tangent plane in 3D and an arrow in 2D.' },
        { targets: ['.steps-panel'], title: 'Hold one variable constant', copy: 'Reveal fₓ first, then fᵧ, combine them into ∇f, and finally substitute the probe point. The numeric slope is the last step, not the first.' }
      ]
    },
    '/lagrange-multipliers': {
      name: 'Find where two curves just touch',
      stages: [
        { targets: ['header'], title: 'The best allowed point is a tangency', copy: 'You may climb the objective only while staying on the constraint. At an optimum, the objective contour and constraint share a tangent.', math: String.raw`\nabla f=\lambda\nabla g` },
        { targets: ['.panel'], title: 'Separate goal from restriction', copy: 'f is what you optimize. g=c is the path you are allowed to follow. Keeping those roles distinct makes the geometry much easier to read.' },
        { targets: ['.canvas-wrap'], title: 'Look for parallel normals', copy: 'Gradients are perpendicular to level curves. Where the two curves touch, their normal arrows must be parallel; λ records their relative length and direction.' },
        { targets: ['.ctrl-row'], title: 'Remove layers to test the idea', copy: 'Toggle contours, the constraint, and gradients. The solution points should remain exactly where a contour kisses the constraint.' },
        { targets: ['.steps-panel'], title: 'Turn tangency into a system', copy: 'Build both gradients, equate their components with λ, append g=c, and solve the three equations together.' }
      ]
    },
    '/linear-ode': {
      name: 'Make the left side collapse',
      stages: [
        { targets: ['header'], title: 'An integrating factor creates a product derivative', copy: 'Multiplying by μ makes two separate terms lock into the product rule pattern.', math: String.raw`\mu y'+\mu Py=(\mu y)'` },
        { targets: ['.panel'], title: 'Identify P and Q', copy: 'First put the equation in standard form y′+P(x)y=Q(x). The method only works cleanly after the coefficient of y′ is 1.' },
        { targets: ['.canvas-wrap'], title: 'See a family flow through a slope field', copy: 'Every short stroke shows the slope required at that location. The highlighted curve is the unique family member passing through the initial point.' },
        { targets: ['.ctrl-row'], title: 'Compare solution and μ', copy: 'Switch views and toggle the layers. μ rescales the equation so the left side becomes one derivative; it is a mechanism, not just a memorized formula.' },
        { targets: ['.steps-panel'], title: 'Create the product rule before integrating', copy: 'Reveal ∫P, then μ, then the collapsed derivative (μy)′. Only after that do we integrate and apply the initial condition.' }
      ]
    },
    '/leibniz': {
      name: 'Track three sources of area change',
      stages: [
        { targets: ['header'], title: 'An integral can change in three ways', copy: 'Its right edge can move, its left edge can move, and the roof itself can deform. Leibniz’s rule simply adds those effects.' },
        { targets: ['.panel'], title: 'Define the roof and both moving walls', copy: 'f(x,t) controls the roof. a(t) and b(t) control the walls. A fixed wall has derivative zero, so its contribution vanishes.' },
        { targets: ['.canvas-wrap'], title: 'Read swept strips at the edges', copy: 'Boundary speed times boundary height gives the thin area swept per unit time. The lower wall subtracts area; the upper wall adds it.' },
        { targets: ['.breakdown'], title: 'Add edge motion and roof deformation', copy: 'The three rows are geometric rates. Their signed sum is dI/dt. Move t and watch which mechanism dominates.' },
        { targets: ['.steps-panel'], title: 'Differentiate the mechanisms separately', copy: 'Build the upper term, lower term, and interior partial derivative one at a time, then combine them in the final line.' }
      ]
    }
  };

  function firstVisible(selector) {
    return Array.from(document.querySelectorAll(selector)).find(el => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    });
  }

  function setupTour() {
    const lesson = LESSONS[location.pathname];
    if (!lesson) return;
    const header = document.querySelector('body > header');
    if (!header) return;

    const launch = document.createElement('button');
    launch.className = 'lesson-launch';
    launch.type = 'button';
    launch.innerHTML = '<span class="lesson-launch-icon" aria-hidden="true">▶</span><span>Start guided lesson</span>';
    launch.setAttribute('aria-label', 'Start guided lesson: ' + lesson.name);
    header.appendChild(launch);

    let index = 0;
    let activeTargets = [];
    let backdrop, card;

    function clearTargets() {
      activeTargets.forEach(el => el.classList.remove('tour-focus'));
      activeTargets = [];
    }

    function close() {
      clearTargets();
      backdrop?.remove();
      card?.remove();
      backdrop = card = null;
      launch.focus();
      document.body.style.overflow = '';
    }

    function renderStage() {
      const stage = lesson.stages[index];
      clearTargets();
      activeTargets = (stage.targets || []).map(firstVisible).filter(Boolean);
      activeTargets.forEach(el => el.classList.add('tour-focus'));
      activeTargets[0]?.scrollIntoView({ behavior: 'smooth', block: 'center' });

      card.querySelector('.tour-kicker').textContent = lesson.name;
      card.querySelector('.tour-count').textContent = `${index + 1} / ${lesson.stages.length}`;
      card.querySelector('.tour-title').textContent = stage.title;
      card.querySelector('.tour-copy').textContent = stage.copy;
      const math = card.querySelector('.tour-math');
      if (stage.math) {
        math.hidden = false;
        try { katex.render(stage.math, math, { throwOnError: false, displayMode: false }); }
        catch (_) { math.textContent = stage.math; }
      } else {
        math.hidden = true;
        math.textContent = '';
      }
      card.querySelector('.tour-progress').innerHTML = lesson.stages.map((_, i) => `<span class="tour-dot${i <= index ? ' is-done' : ''}"></span>`).join('');
      card.querySelector('[data-tour="back"]').disabled = index === 0;
      card.querySelector('[data-tour="next"]').textContent = index === lesson.stages.length - 1 ? 'Finish lesson' : 'Continue';
    }

    function open() {
      index = 0;
      backdrop = document.createElement('div');
      backdrop.className = 'tour-backdrop';
      backdrop.setAttribute('aria-hidden', 'true');
      card = document.createElement('section');
      card.className = 'tour-card';
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', lesson.name);
      card.innerHTML = `
        <div class="tour-topline"><span class="tour-kicker"></span><span class="tour-count"></span></div>
        <h2 class="tour-title"></h2><p class="tour-copy"></p><div class="tour-math"></div>
        <div class="tour-progress" aria-hidden="true"></div>
        <div class="tour-actions">
          <button class="tour-btn" type="button" data-tour="quit">Quit</button>
          <button class="tour-btn" type="button" data-tour="back">← Back</button>
          <button class="tour-btn tour-btn-primary" type="button" data-tour="next">Continue</button>
        </div>`;
      document.body.append(backdrop, card);
      document.body.style.overflow = 'hidden';
      card.addEventListener('click', e => {
        const action = e.target.closest('[data-tour]')?.dataset.tour;
        if (action === 'quit') close();
        if (action === 'back' && index > 0) { index -= 1; renderStage(); }
        if (action === 'next') {
          if (index >= lesson.stages.length - 1) close();
          else { index += 1; renderStage(); }
        }
      });
      requestAnimationFrame(() => { backdrop.classList.add('is-open'); card.classList.add('is-open'); });
      renderStage();
      card.querySelector('[data-tour="next"]').focus();
    }

    launch.addEventListener('click', open);
    document.addEventListener('keydown', e => {
      if (!card) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft' && index > 0) { index -= 1; renderStage(); }
      if (e.key === 'ArrowRight') {
        if (index < lesson.stages.length - 1) { index += 1; renderStage(); }
        else close();
      }
    });
  }

  function whyText(item, index, total) {
    if (index === 0) return 'Start by translating the given problem into the method’s notation.';
    if (index === total - 1) return 'Every required transformation is now in place, so the result can be stated.';
    return 'This line changes one ingredient only; the next line will build directly on it.';
  }

  function setupEquationPlayer(panel) {
    if (panel.dataset.playerReady) return;
    const list = panel.querySelector('.steps-list');
    const head = panel.querySelector('.steps-head');
    if (!list || !head || !list.children.length) return;
    panel.dataset.playerReady = '1';
    panel.classList.add('is-sequential');

    const controls = document.createElement('div');
    controls.className = 'equation-player';
    controls.innerHTML = '<button type="button" class="eq-prev">← Previous</button><span class="equation-player-status"></span><button type="button" class="eq-all">Show all</button><button type="button" class="eq-next">Next step →</button>';
    head.appendChild(controls);
    let current = 0;

    function items() { return Array.from(list.querySelectorAll('.step-item')); }
    function paint(shouldScroll) {
      const all = items();
      current = Math.max(0, Math.min(current, all.length - 1));
      all.forEach((item, i) => {
        item.classList.toggle('is-revealed', i <= current);
        item.classList.toggle('is-current', i === current);
        if (!item.querySelector('.step-why')) {
          const why = document.createElement('div');
          why.className = 'step-why';
          why.textContent = whyText(item, i, all.length);
          item.appendChild(why);
        }
      });
      controls.querySelector('.equation-player-status').textContent = `Step ${current + 1} of ${all.length}`;
      controls.querySelector('.eq-prev').disabled = current === 0;
      controls.querySelector('.eq-next').disabled = current === all.length - 1;
      if (shouldScroll) all[current]?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    controls.querySelector('.eq-prev').addEventListener('click', () => { current -= 1; paint(true); });
    controls.querySelector('.eq-next').addEventListener('click', () => { current += 1; paint(true); });
    controls.querySelector('.eq-all').addEventListener('click', () => { current = items().length - 1; paint(true); });
    paint(false);
  }

  function observeSteps() {
    document.querySelectorAll('.steps-panel').forEach(panel => {
      const list = panel.querySelector('.steps-list');
      if (!list) return;
      const observer = new MutationObserver(() => {
        if (list.children.length) {
          panel.dataset.playerReady = '';
          panel.querySelector('.equation-player')?.remove();
          setupEquationPlayer(panel);
        }
      });
      observer.observe(list, { childList: true });
      setupEquationPlayer(panel);
    });
  }

  function addGeometryBadges() {
    const labels = {
      '/riemann-sum': 'Geometric lens: tiled area',
      '/substitution': 'Geometric lens: matching strips',
      '/integration-by-parts': 'Geometric lens: complementary areas',
      '/partial-derivatives': 'Geometric lens: surface slices',
      '/lagrange-multipliers': 'Geometric lens: tangency',
      '/linear-ode': 'Geometric lens: slope flow',
      '/leibniz': 'Geometric lens: swept area'
    };
    const label = labels[location.pathname];
    if (!label) return;
    document.querySelectorAll('.canvas-wrap').forEach(wrap => {
      const badge = document.createElement('div');
      badge.className = 'geometry-badge';
      badge.textContent = label;
      wrap.appendChild(badge);
    });
  }

  function init() {
    setupTour();
    observeSteps();
    addGeometryBadges();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
