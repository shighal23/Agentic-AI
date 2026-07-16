from .calculator import calculator
from .time_tool import execute as time_tool
from .weather import execute as weather

# Register all tools here
TOOLS = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather,
}


def execute_tool(tool_name: str, arguments: dict):
    """
    Execute a tool by its name.
    """

    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    return tool(arguments)


def list_tools():
    """
    Return the list of available tools.
    """
    return list(TOOLS.keys())


if __name__ == "__main__":

    print("Registered Tools")
    print("----------------")

    print(list_tools())

    print("\nCalculator")
    print(
        execute_tool(
            "calculator",
            {
                "expression": "25*10"
            }
        )
    )

    print("\nTime")
    print(
        execute_tool(
            "time",
            {}
        )
    )

    print("\nWeather")
    print(
        execute_tool(
            "weather",
            {
                "city": "Delhi"
            }
        )
    )