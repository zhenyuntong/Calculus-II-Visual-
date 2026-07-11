import sympy as sp


def compute_steps(u_str: str, vp_str: str, a: float, b: float) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
    }
    try:
        x = sp.Symbol("x")
        u_expr = sp.sympify(u_str.replace("^", "**"))
        vp_expr = sp.sympify(vp_str.replace("^", "**"))

        u_prime = sp.diff(u_expr, x)
        v_expr = sp.integrate(vp_expr, x)

        u_tex = sp.latex(u_expr)
        vp_tex = sp.latex(vp_expr)
        up_tex = sp.latex(sp.simplify(u_prime))
        v_tex = sp.latex(sp.simplify(v_expr))

        # [u·v] evaluated at a and b
        uv_b = (u_expr * v_expr).subs(x, b).evalf()
        uv_a = (u_expr * v_expr).subs(x, a).evalf()
        boundary = float(uv_b - uv_a)

        # Remainder ∫v·u' dx
        remainder_sym = sp.integrate(v_expr * u_prime, (x, a, b))
        try:
            remainder = float(remainder_sym.evalf())
            rem_tex = sp.latex(remainder_sym)
        except Exception:
            remainder = None
            rem_tex = r"\approx \text{numerical}"

        # Original integral ∫u·v' dx
        orig_sym = sp.integrate(u_expr * vp_expr, (x, a, b))
        try:
            orig = float(orig_sym.evalf())
            orig_tex = sp.latex(orig_sym)
        except Exception:
            orig = None
            orig_tex = r"\approx \text{numerical}"

        steps = [
            {
                "color": C["blue"],
                "latex": rf"u = {u_tex}, \quad dv = {vp_tex}\,dx",
                "desc":  "Choose u and dv (LIATE: Log, Inverse-trig, Algebraic, Trig, Exp)",
                "val":   "",
            },
            {
                "color": C["amber"],
                "latex": rf"u' = {up_tex}, \quad v = \int {vp_tex}\,dx = {v_tex}",
                "desc":  "Differentiate u and integrate v' to get v",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"\int u\,dv = \bigl[u\cdot v\bigr]_a^b - \int_a^b v\cdot u'\,dx",
                "desc":  "Integration by parts formula (product rule rearranged)",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": (
                    rf"\bigl[{u_tex}\cdot({v_tex})\bigr]_{{{a:.3f}}}^{{{b:.3f}}}"
                    rf" = {boundary:.5f}"
                ),
                "desc":  f"Boundary term [u·v] evaluated at endpoints",
                "val":   f"{boundary:.5f}",
            },
            {
                "color": C["purple"],
                "latex": (
                    rf"-\int_{{{a:.3f}}}^{{{b:.3f}}} ({v_tex})\cdot({up_tex})\,dx"
                    rf" = {rem_tex}"
                ),
                "desc":  "Remainder integral −∫v·u' dx",
                "val":   f"{-remainder:.5f}" if remainder is not None else "—",
            },
            {
                "color": C["blue"],
                "latex": (
                    rf"\int_{{{a:.3f}}}^{{{b:.3f}}} {u_tex}\cdot {vp_tex}\,dx"
                    rf" = {orig_tex}"
                ),
                "desc":  "Result = boundary − remainder",
                "val":   f"{orig:.5f}" if orig is not None else "—",
            },
        ]
        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
