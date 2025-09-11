import pytest
from core.writon import WritonCore

@pytest.fixture
def core():
    """Returns a WritonCore instance."""
    return WritonCore()

def test_process_text_grammar_sentence_case(core, mocker):
    """Tests the process_text method for grammar mode and sentence case."""
    mock_call_ai = mocker.patch.object(core, '_call_ai', return_value="this is a test sentence.")
    
    result = core.process_text(
        text="this is a test.",
        mode="grammar",
        case_style="sentence"
    )
    
    # Verify that the AI was called correctly
    mock_call_ai.assert_called_once()
    
    # Verify that the output is correctly cased
    assert result == "This is a test sentence."

def test_process_text_translation_with_params(core, mocker):
    """Tests that target_language is correctly passed for translation."""
    mocker.patch('builtins.open', mocker.mock_open(read_data='{"template": "Translate to {{target_language}}: {{text}}"}'))
    mock_call_ai = mocker.patch.object(core, '_call_ai', return_value="hola mundo")

    core.process_text(
        text="hello world",
        mode="translate",
        case_style="lower",
        target_language="Spanish"
    )

    # Check if the prompt sent to the AI was generated with the target_language
    call_args = mock_call_ai.call_args[0][0]
    assert "Translate to Spanish: hello world" in call_args['user']

def test_error_handling_in_process_text(core, mocker):
    """Tests that an exception from the AI call is raised as a ValueError."""
    # Mock _call_ai to raise an exception instead of returning an error message
    mocker.patch.object(core, '_call_ai', side_effect=Exception("AI service unavailable"))
    
    with pytest.raises(ValueError, match="Error processing text: AI service unavailable"):
        core.process_text(
            text="some text",
            mode="grammar",
            case_style="sentence"
        )