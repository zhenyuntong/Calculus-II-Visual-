from flask import Flask, render_template, request, jsonify
from math_engine import riemann, substitution, integration_by_parts, partial_derivatives, lagrange, linear_ode, leibniz

app = Flask(__name__)

# ── Page routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/riemann-sum")
def riemann_sum():
    return render_template("riemann_sum.html")

@app.route("/substitution")
def substitution_page():
    return render_template("substitution.html")

@app.route("/integration-by-parts")
def integration_by_parts_page():
    return render_template("integration_by_parts.html")

@app.route("/partial-derivatives")
def partial_derivatives_page():
    return render_template("partial_derivatives.html")

@app.route("/lagrange-multipliers")
def lagrange_multipliers():
    return render_template("lagrange_multipliers.html")

@app.route("/linear-ode")
def linear_ode_page():
    return render_template("linear_ode.html")

@app.route("/leibniz")
def leibniz_page():
    return render_template("leibniz.html")

# ── API routes ────────────────────────────────────────────────────────────────

@app.route("/api/riemann", methods=["POST"])
def api_riemann():
    data = request.get_json(force=True)
    steps = riemann.compute_steps(
        data.get("f", "sin(x)"),
        float(data.get("a", 0)),
        float(data.get("b", 3.14159)),
        int(data.get("n", 8)),
        data.get("method", "left"),
    )
    return jsonify({"steps": steps})

@app.route("/api/substitution", methods=["POST"])
def api_substitution():
    data = request.get_json(force=True)
    steps = substitution.compute_steps(
        data.get("g", "x**2"),
        data.get("f", "cos(u)"),
        float(data.get("a", 0)),
        float(data.get("b", 1.5)),
    )
    return jsonify({"steps": steps})

@app.route("/api/ibp", methods=["POST"])
def api_ibp():
    data = request.get_json(force=True)
    steps = integration_by_parts.compute_steps(
        data.get("u", "x"),
        data.get("vp", "cos(x)"),
        float(data.get("a", 0)),
        float(data.get("b", 3.14159)),
    )
    return jsonify({"steps": steps})

@app.route("/api/partial", methods=["POST"])
def api_partial():
    data = request.get_json(force=True)
    steps = partial_derivatives.compute_steps(
        data.get("f", "sin(x)*cos(y)"),
        float(data.get("x0", 0.8)),
        float(data.get("y0", 0.5)),
    )
    return jsonify({"steps": steps})

@app.route("/api/lagrange", methods=["POST"])
def api_lagrange():
    data = request.get_json(force=True)
    steps = lagrange.compute_steps(
        data.get("f", "x**2 + y**2"),
        data.get("g", "x + y"),
        float(data.get("c", 1)),
    )
    return jsonify({"steps": steps})

@app.route("/api/ode", methods=["POST"])
def api_ode():
    data = request.get_json(force=True)
    steps = linear_ode.compute_steps(
        data.get("P", "1"),
        data.get("Q", "sin(x)"),
        float(data.get("x0", 0)),
        float(data.get("y0", 1)),
    )
    return jsonify({"steps": steps})

@app.route("/api/leibniz", methods=["POST"])
def api_leibniz():
    data = request.get_json(force=True)
    steps = leibniz.compute_steps(
        data.get("f", "x*t"),
        data.get("a_t", "0"),
        data.get("b_t", "t"),
        float(data.get("t0", 1)),
    )
    return jsonify({"steps": steps})


if __name__ == "__main__":
    app.run(debug=True, port=5050)
