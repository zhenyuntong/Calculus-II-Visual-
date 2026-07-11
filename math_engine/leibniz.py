import sympy as sp


def compute_steps(f_str: str, a_str: str, b_str: str, t0: float) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
        "teal":   "#0891b2",
    }
    try:
        x, t = sp.symbols("x t")

        f = sp.sympify(f_str.replace("^", "**"))
        a_t = sp.sympify(a_str.replace("^", "**"))
        b_t = sp.sympify(b_str.replace("^", "**"))

        a_prime = sp.diff(a_t, t)
        b_prime = sp.diff(b_t, t)

        # Partial derivative of f w.r.t. t
        df_dt = sp.diff(f, t)

        # Three components of Leibniz rule
        term_upper = f.subs(x, b_t) * b_prime
        term_lower = f.subs(x, a_t) * a_prime
        # ∫ ∂f/∂t dx (symbolic)
        try:
            int_dft = sp.integrate(df_dt, x)
            int_dft_tex = sp.latex(sp.simplify(int_dft))
        except Exception:
            int_dft_tex = rf"\int_{{a(t)}}^{{b(t)}} {sp.latex(sp.simplify(df_dt))}\,dx"

        # Evaluate all at t = t0
        t0_upper = float(term_upper.subs(t, t0).evalf())
        t0_lower = float(term_lower.subs(t, t0).evalf())

        # Full derivative d/dt I(t)
        try:
            int_dft_val_sym = sp.integrate(df_dt, (x, a_t, b_t))
            dIdt = sp.simplify(term_upper - term_lower + int_dft_val_sym)
            dIdt_at_t0 = float(dIdt.subs(t, t0).evalf())
            dIdt_tex = sp.latex(sp.simplify(dIdt))
        except Exception:
            dIdt_tex = r"\text{(numerical)}"
            dIdt_at_t0 = None

        f_tex  = sp.latex(f)
        at_tex = sp.latex(a_t)
        bt_tex = sp.latex(b_t)
        apt_tex = sp.latex(sp.simplify(a_prime))
        bpt_tex = sp.latex(sp.simplify(b_prime))
        dft_tex = sp.latex(sp.simplify(df_dt))
        tu_tex  = sp.latex(sp.simplify(term_upper))
        tl_tex  = sp.latex(sp.simplify(term_lower))

        steps = [
            {
                "color": C["amber"],
                "latex": (
                    rf"I(t) = \int_{{a(t)}}^{{b(t)}} f(x,t)\,dx"
                    rf" = \int_{{{at_tex}}}^{{{bt_tex}}} {f_tex}\,dx"
                ),
                "desc":  "The parameterized integral — bounds and integrand may depend on t",
                "val":   "",
            },
            {
                "color": C["blue"],
                "latex": (
                    rf"\frac{{d}}{{dt}}I(t) = f(b(t),t)\,b'(t) - f(a(t),t)\,a'(t)"
                    rf" + \int_{{a(t)}}^{{b(t)}}\frac{{\partial f}}{{\partial t}}\,dx"
                ),
                "desc":  "Leibniz rule: three components — upper bound, lower bound, interior derivative",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"f(b(t),t)\cdot b'(t) = {tu_tex}",
                "desc":  f"Upper-bound term (evaluated at t={t0}): {t0_upper:.5f}",
                "val":   f"{t0_upper:.5f}",
            },
            {
                "color": C["red"],
                "latex": rf"-f(a(t),t)\cdot a'(t) = -{tl_tex}",
                "desc":  f"Lower-bound term (subtracted, t={t0}): {-t0_lower:.5f}",
                "val":   f"{-t0_lower:.5f}",
            },
            {
                "color": C["purple"],
                "latex": rf"\frac{{\partial f}}{{\partial t}} = {dft_tex}",
                "desc":  "Interior term — partial of f w.r.t. t, then integrate over x",
                "val":   "",
            },
            {
                "color": C["teal"],
                "latex": rf"\frac{{d}}{{dt}}I(t) = {dIdt_tex}",
                "desc":  (
                    f"Full derivative at t={t0}: {dIdt_at_t0:.5f}"
                    if dIdt_at_t0 is not None else "Symbolic derivative of I(t)"
                ),
                "val":   f"{dIdt_at_t0:.5f}" if dIdt_at_t0 is not None else "",
            },
        ]
        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
