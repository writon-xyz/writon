"""
Writon CLI - AI-powered text formatter
"""

import os
from datetime import datetime
from core.writon import WritonCore
import argparse
import sys


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
    print("███          █████   ███   █████            ███   █████                             █████████  █████       █████")
    print("░░░███       ░░███   ░███  ░░███            ░░░   ░░███                             ███░░░░░███░░███       ░░███")
    print("  ░░░███      ░███   ░███   ░███  ████████  ████  ███████    ██████  ████████      ███     ░░░  ░███        ░███")
    print("    ░░░███    ░███   ░███   ░███ ░░███░░███░░███ ░░░███░    ███░░███░░███░░███    ░███          ░███        ░███")
    print("     ███░     ░░███  █████  ███   ░███ ░░░  ░███   ░███    ░███ ░███ ░███ ░███    ░███          ░███        ░███")
    print("   ███░        ░░░█████░█████░    ░███      ░███   ░███ ███░███ ░███ ░███ ░███    ░░███     ███ ░███      █ ░███")
    print(" ███░            ░░███ ░░███      █████     █████  ░░█████ ░░██████  ████ █████    ░░█████████  ███████████ █████")
    print("░░░               ░░░   ░░░      ░░░░░     ░░░░░    ░░░░░   ░░░░░░  ░░░░ ░░░░░      ░░░░░░░░░  ░░░░░░░░░░░ ░░░░░")

    print(
        f"\n{BLUE}Writon is a free and open-source AI-powered text processor available as both a command-line tool and a web application, and an api.{ENDC}"
    )
    print(
        f"{BLUE}It's a clean, fast, and reliable tool that transforms your text while preserving your intent and applying consistent case formatting.{ENDC}"
    )

    # --- New argument parsing logic ---
    parser = argparse.ArgumentParser(description="Writon CLI - AI-powered text processor")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s 0.1.0" # Use the version from pyproject.toml
    )
    args = parser.parse_args() # Use parse_args() directly as we want it to exit if version is requested

    # --- End of new argument parsing logic ---

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
            print(f"1. {YELLOW}Hindi{ENDC}")
            print(f"2. {YELLOW}Maori{ENDC}")
            print(f"3. {YELLOW}Arabic{ENDC}")
            print(f"4. {YELLOW}French{ENDC}")
            print(f"5. {YELLOW}German{ENDC}")
            print(f"6. {YELLOW}Swahili{ENDC}")
            print(f"7. {YELLOW}English{ENDC}")
            print(f"8. {YELLOW}Spanish{ENDC}")
            print(f"9. {YELLOW}Tok Pisin{ENDC}")
            print(f"10. {YELLOW}Portuguese{ENDC}")
            print(f"11. {YELLOW}Mandarin Chinese{ENDC}")
            print(f"12. {YELLOW}Custom (enter manually){ENDC}")

            lang_input = safe_input("> ").strip()
            lang_map = {
                "1": "Hindi",
                "2": "Maori",
                "3": "Arabic",
                "4": "French",
                "5": "German",
                "6": "Swahili",
                "7": "English",
                "8": "Spanish",
                "9": "Tok Pisin",
                "10": "Portuguese",
                "11": "Mandarin Chinese",
            }

            if lang_input in lang_map:
                target_language = lang_map[lang_input]
                break
            elif lang_input == "12":
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
                print(f"{RED}Please select a valid option (1-12).{ENDC}")

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
    core = WritonCore()
    try:
        final_output = core.process_text(
            text=raw_text,
            mode=selected_mode,
            case_style=case_style,
            target_language=target_language,
        )

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
                    provider = os.getenv("API_PROVIDER", "not_configured")
                    stats = f"""--- Original Text ---\n{raw_text}\n\n--- Processed Text ---\n{final_output}\n\n--- Stats ---\nMode: {selected_mode}\nCase Style: {case_style}\nAI Provider: {provider}\nOriginal Character Count: {len(raw_text)}
Processed Character Count: {len(final_output)}
Original Word Count: {len(raw_text.split())}\nProcessed Word Count: {len(final_output.split())}"""
                    f.write(stats)
                print(f"{GREEN}Saved to {filepath}{ENDC}")
            except Exception as e:
                print(f"{RED}Failed to save file: {e}{ENDC}")

    except ValueError as e:
        print(f"\n{RED}Error: {e}{ENDC}")
    except Exception as e:
        print(f"\n{RED}An unexpected error occurred: {e}{ENDC}")


if __name__ == "__main__":
    main()
