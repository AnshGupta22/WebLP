'''Main code of the Linear Programming Solver App.'''
from flask import Flask, render_template, request
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve_lp', methods=['POST'])
def solve_lp():
    if request.method == 'POST':
        # Get form data
        problem_type = request.form['problem_type']
        obj_coefficients = list(map(float, filter(None, request.form['obj_coefficients'].replace('\r\n', '').split(','))))
        if problem_type == 'max':
            # If it's a maximization problem, multiply the coefficients by -1
            obj_coefficients = [-1*coef for coef in obj_coefficients]
        try:
            lhs_coefficients = [list(map(float, filter(None, row.split(',')))) for row in request.form['lhs_coefficients'].replace('\r\n', '').split(';')]
        except ValueError:
            return "Error: lhs_coefficients must be a semicolon-separated list of comma-separated numeric values."

        # Check that lhs_coefficients is a 2-D list
        if not all(isinstance(row, list) for row in lhs_coefficients):
            return "Error: lhs_coefficients must be a 2-D list."

        # Check that all values in lhs_coefficients are numeric
        if not all(all(isinstance(val, (int, float)) for val in row) for row in lhs_coefficients):
            return "Error: All values in lhs_coefficients must be numeric."

        rhs_values = list(map(float, filter(None, request.form['rhs_values'].replace('\r\n', '').split(','))))

        # Solve LP problem with non-negativity constraints
        result = linprog(c=obj_coefficients, A_ub=lhs_coefficients, b_ub=rhs_values, bounds=(0, None))

        # Prepare the result for display
        if result.success:
            optimal_value = result.fun
            if problem_type == 'max':
                optimal_value *= -1
            result_text = f"Optimal value: {optimal_value}, Optimal point: {result.x}"
        else:
            result_text = "LP problem is infeasible or unbounded."

        return render_template('result.html', result=result_text)

if __name__ == '__main__':
    app.run(debug=True)
