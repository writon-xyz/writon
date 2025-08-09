"""
Writon CLI - AI-powered text formatter
"""

import os
from datetime import datetime
from formatter.text_formatter import format_text, format_text_with_params
from formatter.case_converter import convert_case


def safe_input(prompt):
    """
    Handles user input safely, exiting gracefully on Ctrl+C or Ctrl+D.
    """
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\n\nGoodbye!")
        exit(0)


def main():
    # ANSI escape codes for colors
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    ENDC = "\033[0m"
    RED = "\033[91m"

    # Display the professional logo and introduction
    print()
    print(
        "░██       ░██          ░██   ░██                               ░██████  ░██         ░██████    ░██████    ░████    ░██████  ░████████ "
    )
    print(
        "░██       ░██                ░██                              ░██   ░██ ░██           ░██     ░██   ░██  ░██ ░██  ░██   ░██ ░██       "
    )
    print(
        "░██  ░██  ░██ ░██░████ ░██░████████  ░███████  ░████████     ░██        ░██           ░██           ░██ ░██ ░████       ░██ ░███████  "
    )
    print(
        "░██ ░████ ░██ ░███     ░██   ░██    ░██    ░██ ░██    ░██    ░██        ░██           ░██       ░█████  ░██░██░██   ░█████        ░██ "
    )
    print(
        "░██░██ ░██░██ ░██      ░██   ░██    ░██    ░██ ░██    ░██    ░██        ░██           ░██      ░██      ░████ ░██  ░██      ░██   ░██ "
    )
    print(
        "░████   ░████ ░██      ░██   ░██    ░██    ░██ ░██    ░██     ░██   ░██ ░██           ░██     ░██        ░██ ░██  ░██       ░██   ░██ "
    )
    print(
        "░███     ░███ ░██      ░██    ░████  ░███████  ░██    ░██      ░██████  ░██████████ ░██████   ░████████   ░████   ░████████  ░██████  "
    )

    print(
        f"\n{BLUE}Writon is a free and open-source AI-powered text processor available as both a command-line tool and a web application, and an api.{ENDC}"
    )
    print(
        f"{BLUE}It's a clean, fast, and reliable tool that transforms your text while preserving your intent and applying consistent case formatting.{ENDC}"
    )

    print("\n" + "How to use Writon:")
    print(f"1. {YELLOW}Enter your text when prompted.{ENDC}")
    print(f"2. {YELLOW}Select a processing mode and case style.{ENDC}")
    print(f"3. {YELLOW}Confirm to process the text with AI.{ENDC}")
    print(f"4. {YELLOW}Optionally save the result to a file.{ENDC}")
    print(f"\n{BLUE}To exit at any time, press Ctrl+C or Ctrl+D.{ENDC}")

    # Input validation
    while True:
        raw_text = safe_input("\n" + f"{GREEN}> Enter your text:{ENDC} ").strip()
        if raw_text:
            break
        print(f"{RED}Please enter some text to process.{ENDC}")

    # Mode selection with validation
    while True:
        print("\n" + f"{BLUE}Select mode:{ENDC}")
        print(f"1. {YELLOW}Fix Grammar{ENDC}")
        print(f"2. {YELLOW}Translate{ENDC}")
        print(f"3. {YELLOW}Summarize{ENDC}")

        mode_input = safe_input("> ").strip()
        mode_map = {"1": "grammar", "2": "translate", "3": "summarize"}

        if mode_input in mode_map:
            selected_mode = mode_map[mode_input]
            break
        print(f"{RED}Please select a valid option (1, 2, or 3).{ENDC}")

    # Get target language for translation
    target_language = None
    if selected_mode == "translate":
        while True:
            print("\n" + f"{BLUE}Select target language:{ENDC}")
            print(f"1. {YELLOW}Spanish{ENDC}")
            print(f"2. {YELLOW}French{ENDC}")
            print(f"3. {YELLOW}German{ENDC}")
            print(f"4. {YELLOW}Italian{ENDC}")
            print(f"5. {YELLOW}Portuguese{ENDC}")
            print(f"6. {YELLOW}Custom (enter manually){ENDC}")

            lang_input = safe_input("> ").strip()
            lang_map = {
                "1": "Spanish",
                "2": "French",
                "3": "German",
                "4": "Italian",
                "5": "Portuguese",
            }

            if lang_input in lang_map:
                target_language = lang_map[lang_input]
                break
            elif lang_input == "6":
                while True:
                    custom_lang = safe_input(
                        f"{GREEN}> Enter target language:{ENDC} "
                    ).strip()
                    if custom_lang:
                        target_language = custom_lang
                        break
                    print(f"{RED}Please enter a language name.{ENDC}")
                break
            else:
                print(f"{RED}Please select a valid option (1-6).{ENDC}")

    # Case selection
    while True:
        print("\n" + f"{BLUE}Select case style:{ENDC}")
        print(f"1. {YELLOW}lowercase{ENDC}")
        print(f"2. {YELLOW}Sentence case{ENDC}")
        print(f"3. {YELLOW}Title Case{ENDC}")
        print(f"4. {YELLOW}UPPERCASE{ENDC}")

        case_input = safe_input("> ").strip()
        case_map = {"1": "lower", "2": "sentence", "3": "title", "4": "upper"}

        if case_input in case_map:
            case_style = case_map[case_input]
            break
        print(f"{RED}Please select a valid option (1, 2, 3, or 4).{ENDC}")

    # Show selections and confirm
    mode_names = {
        "grammar": "Fix Grammar",
        "translate": "Translate",
        "summarize": "Summarize",
    }
    case_names = {
        "lower": "lowercase",
        "sentence": "Sentence case",
        "title": "Title Case",
        "upper": "UPPERCASE",
    }

    print(f"\n{BLUE}Processing Summary:{ENDC}")
    print(f"   {YELLOW}Mode:{ENDC} {mode_names[selected_mode]}")
    if target_language:
        print(f"   {YELLOW}Target:{ENDC} {target_language}")
    print(f"   {YELLOW}Case:{ENDC} {case_names[case_style]}")

    confirm = safe_input(f"\n{GREEN}> Proceed? (y/n):{ENDC} ").strip().lower()
    if confirm not in ["y", "yes"]:
        print(f"{RED}Processing cancelled.{ENDC}")
        return

    # Process with AI
    print("\n" + f"{BLUE}Processing with AI...{ENDC}")
    try:
        if selected_mode == "translate" and target_language:
            formatted = format_text_with_params(
                raw_text, selected_mode, {"target_language": target_language}
            )
        else:
            formatted = format_text(raw_text, selected_mode)

        if (
            formatted.startswith("[") and formatted.endswith("]")
        ) or "error" in formatted.lower():
            if (
                "HTTPSConnectionPool" in formatted
                or "NewConnectionError" in formatted
                or "Name or service not known" in formatted
            ):
                print(
                    f"{RED}Error: No internet connection. Please check your network and try again.{ENDC}"
                )
            elif "API key" in formatted.lower() or "unauthorized" in formatted.lower():
                print(
                    f"{RED}Error: Invalid API key. Please check your .env file.{ENDC}"
                )
            elif "Rate limit" in formatted or "429" in formatted:
                print(
                    f"{RED}Error: API rate limit exceeded. Please wait and try again.{ENDC}"
                )
            elif formatted.startswith("[") and formatted.endswith("]"):
                print(f"{RED}Error: {formatted}{ENDC}")
            else:
                print(f"{RED}Error: Unable to process text. Please try again.{ENDC}")
            return

        final_output = convert_case(formatted, case_style)

        print("\n" + f"{GREEN}Formatted text:{ENDC}")
        print(final_output)

        # Ask if user wants to save to file
        save = safe_input(f"\n{GREEN}> Save to file? (y/n):{ENDC} ").strip().lower()
        if save in ["y", "yes"]:
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Auto-generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_short = {"grammar": "gram", "translate": "trans", "summarize": "summ"}

            if selected_mode == "translate" and target_language:
                clean_target = target_language.lower().replace(" ", "_")
                filename = f"{mode_short[selected_mode]}_{clean_target}_{timestamp}.txt"
            else:
                filename = f"{mode_short[selected_mode]}_{timestamp}.txt"

            filepath = os.path.join(output_dir, filename)

            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(final_output)
                print(f"{GREEN}Saved to {filepath}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to save file: {e}{ENDC}")

    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{ENDC}")
        print(f"{RED}Please check your API key and internet connection.{ENDC}")


if __name__ == "__main__":
    main()
