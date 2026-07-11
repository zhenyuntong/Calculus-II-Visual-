import sympy as sp


def compute_steps(f_str: str, g_str: str, c: float) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
        "teal":   "#0891b2",
    }
    try:
        x, y, lam = sp.symbols("x y lambda")
        f = sp.sympify(f_str.replace("^", "**"))
        g = sp.sympify(g_str.replace("^", "**"))

        # Gradients
        grad_f = (sp.diff(f, x), sp.diff(f, y))
        grad_g = (sp.diff(g, x), sp.diff(g, y))

        grad_f_simplified = tuple(sp.simplify(d) for d in grad_f)
        grad_g_simplified = tuple(sp.simplify(d) for d in grad_g)

        f_tex    = sp.latex(f)
        g_tex    = sp.latex(g)
        gfx_tex  = sp.latex(grad_f_simplified[0])
        gfy_tex  = sp.latex(grad_f_simplified[1])
        ggx_tex  = sp.latex(grad_g_simplified[0])
        ggy_tex  = sp.latex(grad_g_simplified[1])

        # Try to solve the system
        eq1 = sp.Eq(grad_f[0], lam * grad_g[0])
        eq2 = sp.Eq(grad_f[1], lam * grad_g[1])
        eq3 = sp.Eq(g, c)
        sol_info = ""
        sol_tex = r"\text{(solving\ldots)}"
        try:
            sols = sp.solve([eq1, eq2, eq3], [x, y, lam], dict=True)
            if sols:
                parts = []
                for s in sols[:3]:
                    xs = sp.nsimplify(s.get(x, "?"), rational=False)
                    ys = sp.nsimplify(s.get(y, "?"), rational=False)
                    ls = sp.nsimplify(s.get(lam, "?"), rational=False)
                    fv = f.subs([(x, xs), (y, ys)]).evalf()
                    parts.append(
                        rf"({sp.latex(xs)},\,{sp.latex(ys)}),\;\lambda={sp.latex(ls)},\;f={sp.latex(sp.nsimplify(fv))}"
                    )
                sol_tex = r";\quad".join(parts)
                sol_info = f"{len(sols)} critical point(s) found"
            else:
                sol_tex = r"\text{No symbolic solution found}"
                sol_info = "Try numerical methods for complex constraints"
        except Exception:
            sol_tex = r"\text{Symbolic solve timed out — system is complex}"
            sol_info = "Check if constraint intersects the feasible region"

        steps = [
            {
                "color": C["amber"],
                "latex": rf"\text{{Optimize }} f(x,y) = {f_tex}",
                "desc":  "Objective function to maximize / minimize",
                "val":   "",
            },
            {
                "color": C["blue"],
                "latex": rf"\text{{Subject to }} g(x,y) = {g_tex} = {c:.3f}",
                "desc":  "Constraint curve — search only on this level set",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"\nabla f = ({gfx_tex},\; {gfy_tex})",
                "desc":  "Gradient of f — direction of fastest increase",
                "val":   "",
            },
            {
                "color": C["purple"],
                "latex": rf"\nabla g = ({ggx_tex},\; {ggy_tex})",
                "desc":  "Gradient of g — normal to the constraint curve",
                "val":   "",
            },
            {
                "color": C["red"],
                "latex": (
                    rf"\nabla f = \lambda\,\nabla g \;\Leftrightarrow\;"
                    rf"{gfx_tex} = \lambda\cdot{ggx_tex},\quad"
                    rf"{gfy_tex} = \lambda\cdot{ggy_tex}"
                ),
                "desc":  "At the optimum, ∇f and ∇g must be parallel — both perpendicular to g = c",
                "val":   "",
            },
            {
                "color": C["teal"],
                "latex": sol_tex,
                "desc":  sol_info,
                "val":   "",
            },
        ]
        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
