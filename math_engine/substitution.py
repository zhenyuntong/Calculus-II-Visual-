import sympy as sp


def compute_steps(g_str: str, f_str: str, a: float, b: float) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
        "teal":   "#0891b2",
    }
    try:
        x = sp.Symbol("x")
        u = sp.Symbol("u")

        g = sp.sympify(g_str.replace("^", "**"))
        f = sp.sympify(f_str.replace("^", "**"))

        g_prime = sp.diff(g, x)
        h = f.subs(u, g) * g_prime   # h(x) = f(g(x)) * g'(x)

        # Transformed bounds
        ua = float(g.subs(x, a).evalf())
        ub = float(g.subs(x, b).evalf())

        # Symbolic integrals
        try:
            int_fu = sp.integrate(f, (u, ua, ub))
            int_fu_tex = sp.latex(int_fu)
            int_fu_val = float(int_fu.evalf())
        except Exception:
            int_fu_tex = r"\text{(no closed form)}"
            int_fu_val = None

        try:
            int_hx = sp.integrate(h, (x, a, b))
            int_hx_tex = sp.latex(int_hx)
        except Exception:
            int_hx_tex = r"\approx \text{numerical}"

        g_tex = sp.latex(g)
        gp_tex = sp.latex(g_prime)
        f_tex = sp.latex(f)
        h_tex = sp.latex(sp.simplify(h))

        steps = [
            {
                "color": C["amber"],
                "latex": rf"u = g(x) = {g_tex}",
                "desc":  "Choose the substitution: the inner function",
                "val":   "",
            },
            {
                "color": C["blue"],
                "latex": rf"du = g'(x)\,dx = {gp_tex}\,dx",
                "desc":  "Differentiate u with respect to x",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"h(x) = f(g(x))\cdot g'(x) = {h_tex}",
                "desc":  "Integrand in x-domain (must contain g'(x) for sub to work)",
                "val":   "",
            },
            {
                "color": C["purple"],
                "latex": (
                    rf"x = {a:.3f} \;\Rightarrow\; u = {ua:.4f},"
                    rf"\quad x = {b:.3f} \;\Rightarrow\; u = {ub:.4f}"
                ),
                "desc":  "Transform the bounds of integration via u = g(x)",
                "val":   f"[{ua:.4f}, {ub:.4f}]",
            },
            {
                "color": C["teal"],
                "latex": (
                    rf"\int_{{{a:.3f}}}^{{{b:.3f}}} {h_tex}\,dx"
                    rf"\;=\; \int_{{{ua:.4f}}}^{{{ub:.4f}}} {f_tex}\,du"
                    rf"\;=\; {int_fu_tex}"
                ),
                "desc":  "Substitution transforms x-integral into a simpler u-integral",
                "val":   f"{int_fu_val:.6f}" if int_fu_val is not None else "—",
            },
        ]

        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
