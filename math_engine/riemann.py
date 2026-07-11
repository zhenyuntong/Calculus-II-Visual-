import sympy as sp


def _parse(expr_str: str, var: str = "x"):
    sym = sp.Symbol(var)
    return sp.sympify(expr_str.replace("^", "**")), sym


def _safe_float(expr, subs_dict):
    try:
        v = float(expr.subs(subs_dict).evalf())
        return v if sp.sympify(v).is_finite else None
    except Exception:
        return None


def compute_steps(f_str: str, a: float, b: float, n: int, method: str) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
        "teal":   "#0891b2",
    }

    method = {"midpoint": "mid", "trapezoid": "trap", "trapezoidal": "trap"}.get(method, method)
    method_names = {
        "left":  "Left Endpoint",
        "right": "Right Endpoint",
        "mid":   "Midpoint",
        "trap":  "Trapezoid",
    }
    method_name = method_names.get(method, method)

    try:
        f, x = _parse(f_str)
        dx = (b - a) / n
        f_tex = sp.latex(f)

        # ── Exact integral ───────────────────────────────────────────────────
        try:
            exact_sym = sp.integrate(f, (x, a, b))
            exact = float(exact_sym.evalf())
            exact_tex = sp.latex(exact_sym)
        except Exception:
            exact = None
            exact_tex = r"\text{(no closed form)}"

        # ── Numerical approximation + collect first 3 strips ─────────────────
        approx = 0.0
        strip_details = []   # list of dicts per strip

        for i in range(1, n + 1):
            if method == "left":
                xi = a + (i - 1) * dx
                yi = _safe_float(f, {x: xi})
                if yi is None:
                    continue
                area = yi * dx
                approx += area
                if i <= 3:
                    strip_details.append({"i": i, "xi": xi, "yi": yi, "area": area})

            elif method == "right":
                xi = a + i * dx
                yi = _safe_float(f, {x: xi})
                if yi is None:
                    continue
                area = yi * dx
                approx += area
                if i <= 3:
                    strip_details.append({"i": i, "xi": xi, "yi": yi, "area": area})

            elif method == "mid":
                xi = a + (i - 0.5) * dx
                yi = _safe_float(f, {x: xi})
                if yi is None:
                    continue
                area = yi * dx
                approx += area
                if i <= 3:
                    strip_details.append({"i": i, "xi": xi, "yi": yi, "area": area})

            else:  # trap
                x0 = a + (i - 1) * dx
                x1 = a + i * dx
                y0 = _safe_float(f, {x: x0})
                y1 = _safe_float(f, {x: x1})
                if y0 is None or y1 is None:
                    continue
                area = (y0 + y1) * 0.5 * dx
                approx += area
                if i <= 3:
                    strip_details.append({"i": i, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "area": area})

        steps = []

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 1 — Setup
        # ═══════════════════════════════════════════════════════════════════════
        steps.append({
            "color": C["amber"],
            "title": "Goal",
            "latex": (
                rf"\int_{{{a:.4g}}}^{{{b:.4g}}} \!\left({f_tex}\right)dx"
                rf"\;\approx\; \text{{{method_name} sum}},\quad n = {n}"
            ),
            "desc": (
                f"Approximate ∫f(x)dx on [{a:.4g}, {b:.4g}] by cutting the interval "
                f"into {n} equal-width strips and sampling each with the {method_name} rule."
            ),
            "val": "",
        })

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 2 — Partition: compute Δx
        # ═══════════════════════════════════════════════════════════════════════
        steps.append({
            "color": C["blue"],
            "title": "Partition",
            "latex": (
                rf"\Delta x = \frac{{b - a}}{{n}}"
                rf"= \frac{{{b:.4g} - ({a:.4g})}}{{{n}}}"
                rf"= \frac{{{b - a:.4g}}}{{{n}}}"
                rf"= {dx:.6f}"
            ),
            "desc": (
                f"Divide [{a:.4g}, {b:.4g}] into {n} strips of equal width Δx. "
                "This is the horizontal width of every rectangle (or trapezoid)."
            ),
            "val": f"Δx = {dx:.6f}",
        })

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 3 — Sample point rule (method-specific)
        # ═══════════════════════════════════════════════════════════════════════
        if method == "left":
            rule_tex = (
                rf"x_i^* = a + (i-1)\,\Delta x"
                rf"\;=\; {a:.4g} + (i-1)\cdot{dx:.4f}"
            )
            rule_desc = (
                "Left Endpoint rule: sample at the LEFT edge of each strip (i starts at 1). "
                "Strip i spans [a+(i−1)Δx, a+iΔx] — we use the left boundary as the height. "
                "This OVERESTIMATES for increasing f and UNDERESTIMATES for decreasing f."
            )
        elif method == "right":
            rule_tex = (
                rf"x_i^* = a + i\,\Delta x"
                rf"\;=\; {a:.4g} + i\cdot{dx:.4f}"
            )
            rule_desc = (
                "Right Endpoint rule: sample at the RIGHT edge of each strip. "
                "Strip i spans [a+(i−1)Δx, a+iΔx] — we use the right boundary. "
                "This UNDERESTIMATES for increasing f and OVERESTIMATES for decreasing f."
            )
        elif method == "mid":
            rule_tex = (
                rf"x_i^* = a + \!\left(i - \tfrac{{1}}{{2}}\right)\!\Delta x"
                rf"\;=\; {a:.4g} + \!\left(i - \tfrac{{1}}{{2}}\right)\!\cdot{dx:.4f}"
            )
            rule_desc = (
                "Midpoint rule: sample at the CENTER of each strip. "
                "This cancels the over/under-estimation from left and right edges, "
                "giving error that shrinks as 1/n² (much faster than left or right)."
            )
        else:  # trap
            rule_tex = (
                rf"\text{{Height}}_i = \frac{{f(x_{{i-1}}) + f(x_i)}}{2}"
                rf",\quad x_{{i-1}} = {a:.4g}+(i-1)\cdot{dx:.4f},\; x_i = {a:.4g}+i\cdot{dx:.4f}"
            )
            rule_desc = (
                "Trapezoid rule: instead of a rectangle, fit a TRAPEZOID between the two edges. "
                "The height is the average of f at both edges. "
                "Like Midpoint, error shrinks as 1/n² — exact for linear functions."
            )

        steps.append({
            "color": C["teal"],
            "title": "Sample Point Rule",
            "latex": rule_tex,
            "desc": rule_desc,
            "val": "",
        })

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 4 — First few strips worked out explicitly
        # ═══════════════════════════════════════════════════════════════════════
        if strip_details:
            lines = []
            for s in strip_details:
                i_ = s["i"]
                if method != "trap":
                    xi_v, yi_v, area_v = s["xi"], s["yi"], s["area"]
                    lines.append(
                        rf"i={i_}:&\quad x_{i_}^* = {xi_v:.5f},\;"
                        rf"f({xi_v:.5f}) = {yi_v:.5f},\;"
                        rf"\text{{area}} = {yi_v:.5f} \times {dx:.5f} = {area_v:.6f}"
                    )
                else:
                    x0v, x1v, y0v, y1v, av = s["x0"], s["x1"], s["y0"], s["y1"], s["area"]
                    lines.append(
                        rf"i={i_}:&\quad \tfrac{{{y0v:.4f}+{y1v:.4f}}}{2}"
                        rf"\times{dx:.5f} = {av:.6f}"
                    )

            shown = len(strip_details)
            if shown < n:
                lines.append(rf"\vdots&\quad ({n - shown}\text{{ more strips}}\ldots)")

            steps.append({
                "color": C["purple"],
                "title": f"First {shown} Strip{'s' if shown > 1 else ''}",
                "latex": r"\begin{aligned}" + r"\\" .join(lines) + r"\end{aligned}",
                "desc": (
                    f"Compute the first {shown} strip{'s' if shown > 1 else ''} explicitly "
                    "to see the pattern. Each area = height × Δx."
                ),
                "val": "",
            })

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 5 — Full sum = approximation
        # ═══════════════════════════════════════════════════════════════════════
        xi_sym_map = {
            "left":  rf"a+(i-1)\Delta x",
            "right": rf"a+i\,\Delta x",
            "mid":   rf"a+(i-\tfrac{{1}}{{2}})\Delta x",
        }
        if method != "trap":
            sum_tex = (
                rf"\sum_{{i=1}}^{{{n}}} f\!\left({xi_sym_map[method]}\right)\cdot\Delta x"
                rf"\;=\; {approx:.6f}"
            )
        else:
            sum_tex = (
                rf"\sum_{{i=1}}^{{{n}}} \tfrac{{f(x_{{i-1}})+f(x_i)}}{2}\,\Delta x"
                rf"\;=\; {approx:.6f}"
            )

        steps.append({
            "color": C["green"],
            "title": "Total Sum",
            "latex": sum_tex,
            "desc": (
                f"Sum all {n} strip areas. Each term is height × Δx. "
                f"As n → ∞ this sum converges to the exact integral."
            ),
            "val": f"≈ {approx:.6f}",
        })

        # ═══════════════════════════════════════════════════════════════════════
        # STEP 6 — Exact integral (SymPy antiderivative)
        # ═══════════════════════════════════════════════════════════════════════
        if exact is not None:
            # Try to show antiderivative symbolically
            try:
                antideriv = sp.integrate(f, x)
                anti_tex = sp.latex(antideriv)
                exact_step_tex = (
                    rf"\int_{{{a:.4g}}}^{{{b:.4g}}} \!\left({f_tex}\right)dx"
                    rf"= \Bigl[{anti_tex}\Bigr]_{{{a:.4g}}}^{{{b:.4g}}}"
                    rf"= {exact_tex} = {exact:.6f}"
                )
                exact_desc = (
                    "Symbolic integration (SymPy finds the antiderivative, then applies "
                    "the Fundamental Theorem: F(b) − F(a)). This is the TRUE value."
                )
            except Exception:
                exact_step_tex = (
                    rf"\int_{{{a:.4g}}}^{{{b:.4g}}} \!\left({f_tex}\right)dx"
                    rf"= {exact_tex} = {exact:.6f}"
                )
                exact_desc = "Exact value via SymPy symbolic integration."

            steps.append({
                "color": C["blue"],
                "title": "Exact Integral (FTC)",
                "latex": exact_step_tex,
                "desc": exact_desc,
                "val": f"{exact:.6f}",
            })

            # ═══════════════════════════════════════════════════════════════════
            # STEP 7 — Error & convergence rate
            # ═══════════════════════════════════════════════════════════════════
            error = abs(approx - exact)
            rel = error / abs(exact) if exact != 0 else float("nan")
            is_quadratic = method in ("mid", "trap")
            rate_tex  = r"O(n^{-2})" if is_quadratic else r"O(n^{-1})"
            rate_desc = "1/n² — quadratic convergence" if is_quadratic else "1/n — linear convergence"
            halving_err = error / 4 if is_quadratic else error / 2

            steps.append({
                "color": C["red"],
                "title": "Error & Convergence",
                "latex": (
                    rf"\left|\text{{Approx}} - \text{{Exact}}\right|"
                    rf"= \left|{approx:.6f} - {exact:.6f}\right|"
                    rf"= {error:.2e}"
                    rf"\approx {rel*100:.4f}\%"
                ),
                "desc": (
                    f"{method_name} converges at rate {rate_desc}. "
                    f"Doubling n (→ {2*n}) shrinks error from {error:.2e} to ≈ {halving_err:.2e}. "
                    f"Try it with the slider!"
                ),
                "val": f"{rel*100:.4f}%",
            })

        return steps

    except Exception as e:
        return [{
            "color": "#ef4444",
            "latex": rf"\text{{Error: {str(e)}}}",
            "desc": "Could not parse expression",
            "val": "",
        }]
