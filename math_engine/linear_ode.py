import sympy as sp


def compute_steps(P_str: str, Q_str: str, x0: float, y0: float) -> list[dict]:
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
        P = sp.sympify(P_str.replace("^", "**"))
        Q = sp.sympify(Q_str.replace("^", "**"))

        # Integrating factor μ = e^(∫P dx)
        int_P = sp.integrate(P, x)
        mu = sp.exp(int_P)
        mu_simplified = sp.simplify(mu)

        # μ·Q
        muQ = sp.simplify(mu * Q)

        # ∫μ·Q dx
        try:
            int_muQ = sp.integrate(muQ, x)
            int_muQ_s = sp.simplify(int_muQ)
            int_muQ_tex = sp.latex(int_muQ_s)
        except Exception:
            int_muQ_tex = r"\text{(no closed form — numerical)}"
            int_muQ_s = None

        # General solution y = (1/μ)(∫μQ dx + C)
        C_sym = sp.Symbol("C")
        if int_muQ_s is not None:
            y_gen = sp.simplify((int_muQ_s + C_sym) / mu)
            y_gen_tex = sp.latex(y_gen)
        else:
            y_gen_tex = rf"\frac{{1}}{{{sp.latex(mu_simplified)}}}\!\left(\int {sp.latex(muQ)}\,dx + C\right)"

        # Particular solution with y(x0) = y0
        part_info = ""
        y_part_tex = ""
        if int_muQ_s is not None:
            try:
                C_val = sp.solve(
                    sp.Eq(y_gen.subs(x, x0), y0), C_sym
                )
                if C_val:
                    y_part = y_gen.subs(C_sym, C_val[0])
                    y_part_s = sp.simplify(y_part)
                    y_part_tex = sp.latex(y_part_s)
                    part_info = f"y(x) satisfying y({x0}) = {y0}"
            except Exception:
                part_info = "Particular solution requires numerical constant"

        P_tex  = sp.latex(P)
        Q_tex  = sp.latex(Q)
        intP_tex = sp.latex(sp.simplify(int_P))
        mu_tex = sp.latex(mu_simplified)
        muQ_tex = sp.latex(muQ)

        steps = [
            {
                "color": C["amber"],
                "latex": rf"y' + P(x)\,y = Q(x) \;\Rightarrow\; y' + ({P_tex})\,y = {Q_tex}",
                "desc":  "Standard form: identify P(x) and Q(x)",
                "val":   "",
            },
            {
                "color": C["blue"],
                "latex": rf"\int P(x)\,dx = \int {P_tex}\,dx = {intP_tex}",
                "desc":  "Step 1 — Integrate P(x) to build the exponent",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"\mu(x) = e^{{\int P\,dx}} = {mu_tex}",
                "desc":  "Step 2 — Integrating factor μ(x): multiplying by this makes the LHS a perfect derivative",
                "val":   "",
            },
            {
                "color": C["purple"],
                "latex": rf"\frac{{d}}{{dx}}\!\bigl[\mu\,y\bigr] = \mu\,Q = {muQ_tex}",
                "desc":  "Step 3 — After multiplying by μ, left side collapses to d/dx[μy]",
                "val":   "",
            },
            {
                "color": C["teal"],
                "latex": rf"y = \frac{{1}}{{\mu}}\!\left(\int \mu Q\,dx + C\right) = {y_gen_tex}",
                "desc":  "Step 4 — Integrate both sides and solve for y",
                "val":   "",
            },
        ]

        if y_part_tex:
            steps.append({
                "color": C["red"],
                "latex": rf"y({x0}) = {y0} \;\Rightarrow\; y(x) = {y_part_tex}",
                "desc":  part_info,
                "val":   f"y({x0}) = {y0}",
            })

        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
