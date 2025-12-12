from langchain_groq.chat_models import  ChatGroq
def chat_with_groq(system_prompt: str, history: list, user_message: str,
                   groq_api_key: str, model_name: str = "llama-3.3-70b-versatile",
                   temperature: float = 0.6):
    """
    history: list of dicts {"role": "user"/"assistant", "content": "..."}
    Returns the assistant text response (str).
    """
    # Build messages consumable par ChatGroq: list of tuples (role, content) or dicts
    messages = [("system", system_prompt)]
    for m in history:
        role = m.get("role")
        content = m.get("content")
        if role and content is not None:
            messages.append((role, content))
    # Append current user message
    messages.append(("user", user_message))

    llm =  ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model_name,
        temperature=temperature
    )

    # Invoke - api may return an object with .content or .text; we follow previous pattern
    response = llm.invoke(messages)
    # response may be object; try to return common attributes
    if hasattr(response, "content"):
        return response.content
    if isinstance(response, dict) and "content" in response:
        return response["content"]
    # fallback to string
    return str(response)
