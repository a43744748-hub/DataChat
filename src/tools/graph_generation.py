from src.llm_instance import LLM_INSTANCES
# Load the prompt content once
with open("./src/prompts/graph_generation_prompt.txt", "r") as f:
    RAW_GRAPH_GENERATION_PROMPT = f.read()


def generate_graph(final_result: str, intermediate_steps: str) -> str:
    """
    Calls the LLM to generate Python code for a chart visualization.


    Args:
        final_result: The final human-readable answer from the SQL agent.
        intermediate_steps: The structured output of the intermediate steps (SQL query, raw data, etc.)
                            which the LLM will use for context.


    Returns:
        The generated Python code snippet as a string.
    """
    # 1. Format the complete prompt
    try:
        formatted_prompt = RAW_GRAPH_GENERATION_PROMPT.format(
            final_result=final_result,
            intermediate_steps=intermediate_steps
        )
    except KeyError as e:
        # Handle case where prompt placeholders might be missing or wrong
        return f"print('Error: Prompt formatting failed for key {e}')"

    # 2. Invoke the LLM
    try:
        model = LLM_INSTANCES["GPT_4_1"]["MODEL"]
       
        # The prompt is the user input for the code generation
        result = model.invoke(formatted_prompt)

        print(result)

        # Depending on your LLM framework (LangChain/LlamaIndex), result might be an object
        # We assume it's a simple result object with a .content attribute or a string.
        if hasattr(result, 'content'):
            return result.content
        return str(result)


    except Exception as e:
        return f"print('LLM invocation error during graph generation: {e}')"

