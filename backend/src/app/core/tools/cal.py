import math

from pydantic_ai import Tool

from pydantic import BaseModel
from typing import Literal


class CalculationInput(BaseModel):
    operation: Literal["add", "subtract", "multiply", "divide", "sqrt", "pow"]
    a: float
    b: float | None = None  # Not needed for unary ops like sqrt

def calculate(input: CalculationInput) -> str:
    """Performs a calculation based on the specified operation and operands."""
    match input.operation:
        case "add":       result = input.a + input.b
        case "subtract":  result = input.a - input.b
        case "multiply":  result = input.a * input.b
        case "divide":    result = input.a / input.b if input.b != 0 else "Error: Division by zero"
        case "sqrt":      result = math.sqrt(input.a)
        case "pow":       result = math.pow(input.a, input.b)
        case _:           return "Unknown operation"
    return f"Result: {result}"

calculate_tool = Tool(calculate)