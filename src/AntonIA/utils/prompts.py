

def build_prompt_from_template(prompt_template: str, tags: dict[str, str]) -> str:
    """
    Fills in a prompt template with the provided tags.

    Args:
        prompt_template: The template string with placeholders for tags.
        tags: A dictionary of tag names and their corresponding values.
    Returns:
        The filled-in prompt string.
    """
    for key, value in tags.items():
        placeholder = "{{" + key + "}}"
        prompt_template = prompt_template.replace(placeholder, value)

    if "{{" in prompt_template:
        raise ValueError(f"Unreplaced placeholders found in template: {prompt_template}")
    
    return prompt_template
