import sympy as sp


def compute_steps(f_str: str, x0: float, y0: float) -> list[dict]:
    C = {
        "amber":  "#d97706",
        "blue":   "#3b82f6",
        "green":  "#10a37f",
        "purple": "#7c3aed",
        "red":    "#ef4444",
        "teal":   "#0891b2",
    }
    try:
        x, y = sp.symbols("x y")
        f = sp.sympify(f_str.replace("^", "**"))

        dfx = sp.diff(f, x)
        dfy = sp.diff(f, y)
        dfx_simplified = sp.simplify(dfx)
        dfy_simplified = sp.simplify(dfy)

        # Evaluate at probe point
        f_val  = float(f.subs([(x, x0), (y, y0)]).evalf())
        dfx_val = float(dfx.subs([(x, x0), (y, y0)]).evalf())
        dfy_val = float(dfy.subs([(x, x0), (y, y0)]).evalf())
        grad_mag = (dfx_val**2 + dfy_val**2) ** 0.5

        f_tex   = sp.latex(f)
        dfx_tex = sp.latex(dfx_simplified)
        dfy_tex = sp.latex(dfy_simplified)

        steps = [
            {
                "color": C["amber"],
                "latex": rf"f(x, y) = {f_tex}",
                "desc":  "The surface function to differentiate",
                "val":   "",
            },
            {
                "color": C["blue"],
                "latex": rf"\frac{{\partial f}}{{\partial x}} = {dfx_tex}",
                "desc":  "Partial w.r.t. x — treat y as constant, differentiate in x",
                "val":   "",
            },
            {
                "color": C["red"],
                "latex": rf"\frac{{\partial f}}{{\partial y}} = {dfy_tex}",
                "desc":  "Partial w.r.t. y — treat x as constant, differentiate in y",
                "val":   "",
            },
            {
                "color": C["green"],
                "latex": rf"\nabla f = \left({dfx_tex},\; {dfy_tex}\right)",
                "desc":  "Gradient vector — points in the direction of steepest ascent",
                "val":   "",
            },
            {
                "color": C["purple"],
                "latex": (
                    rf"\text{{At }} (x_0, y_0) = ({x0:.3f}, {y0:.3f}):"
                    rf"\quad \nabla f = ({dfx_val:.4f},\; {dfy_val:.4f})"
                ),
                "desc":  f"Gradient magnitude |∇f| = {grad_mag:.4f} — steepness at probe",
                "val":   f"|∇f| = {grad_mag:.4f}",
            },
            {
                "color": C["teal"],
                "latex": (
                    rf"f({x0:.3f}, {y0:.3f}) = {f_val:.4f},\quad"
                    rf"|\nabla f| = {grad_mag:.4f}"
                ),
                "desc":  "f-value and gradient magnitude at the probe point",
                "val":   f"f = {f_val:.4f}",
            },
        ]
        return steps

    except Exception as e:
        return [{"color": "#ef4444", "latex": rf"\text{{Error: {str(e)}}}", "desc": "Could not parse", "val": ""}]
