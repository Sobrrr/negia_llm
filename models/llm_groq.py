from groq import Groq

def chat_with_groq(system_prompt: str, history: list, user_message: str,
                   groq_api_key: str, model_name: str = "llama-3.3-70b-versatile",
                   temperature: float = 0.6):
    """
    history: list of dicts {"role": "user"/"assistant", "content": "..."}
    Returns the assistant text response (str).
    """
    # Build messages for the Groq API
    messages = [{"role": "system", "content": system_prompt}]
    for m in history:
        role = m.get("role")
        content = m.get("content")
        if role and content is not None:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})

    # Instantiate Groq client
    client = Groq(api_key=groq_api_key)

    # Call the API
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature
    )

    # Extract content
    if hasattr(response.choices[0].message, "content"):
        return response.choices[0].message.content
    return str(response)
