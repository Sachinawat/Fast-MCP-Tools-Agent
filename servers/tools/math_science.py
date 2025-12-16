import sympy
from servers.config import logger

def execute_math(expression: str):
    logger.info(f"Calculating: {expression}")
    try:
        # Safe evaluation of math expressions
        expr = sympy.sympify(expression)
        result = expr.evalf()
        return {"status": "success", "result": str(result), "latex": sympy.latex(expr)}
    except Exception as e:
        return {"status": "error", "message": str(e)}