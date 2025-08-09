def generate_prompt(text, config, params=None):
    """Generate structured prompt from config and user text"""
    template = config["template"]

    # Replace text placeholder
    template = template.replace("{{text}}", text.strip())

    # Replace parameter placeholders if provided
    if params:
        for key, value in params.items():
            template = template.replace("{{" + key + "}}", str(value))

    prompt = {"user": template}

    if "system" in config:
        prompt["system"] = config["system"]

    return prompt
