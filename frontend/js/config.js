import { providerSelect, apiKeyInput, modelInput, modeSelect, caseStyleSelect, targetLanguageSelect, customLanguageInput, inputTextArea } from './main.js';
import { toggleLanguageOptions, toggleCustomLanguage, updateModelPlaceholder, updateTextStats } from './ui.js';
import { checkApiKeyStatus } from './api.js';

function saveConfig() {
    const config = {
        provider: providerSelect.value,
        apiKey: apiKeyInput.value,
        model: modelInput.value,
        mode: modeSelect.value,
        caseStyle: caseStyleSelect.value,
        targetLanguage: targetLanguageSelect.value,
        customLanguage: customLanguageInput.value
    };
    localStorage.setItem('writon-config', JSON.stringify(config));
}

function loadStoredConfig() {
    const stored = localStorage.getItem('writon-config');
    if (stored) {
        try {
            const config = JSON.parse(stored);
            providerSelect.value = config.provider || 'groq';
            apiKeyInput.value = config.apiKey || '';
            modelInput.value = config.model || '';
            modeSelect.value = config.mode || 'grammar';
            caseStyleSelect.value = config.caseStyle || 'sentence';
            targetLanguageSelect.value = config.targetLanguage || 'Spanish';
            customLanguageInput.value = config.customLanguage || '';

            document.querySelectorAll('.custom-select-wrapper').forEach(wrapper => {
                const select = wrapper.querySelector('select');
                const selectedDisplay = wrapper.querySelector('.select-selected');
                if (select && selectedDisplay) {
                    selectedDisplay.textContent = select.options[select.selectedIndex].textContent;
                }
            });

            toggleLanguageOptions();
            toggleCustomLanguage();
            updateModelPlaceholder();
            checkApiKeyStatus();
        } catch (e) {
            console.warn('Error loading stored config:', e);
        }
    }
}

const debouncedSave = debounce(() => {
    if (inputTextArea.value.trim()) {
        localStorage.setItem('writon-current-text', inputTextArea.value);
    }
}, 1000);

function loadSavedText() {
    const savedText = localStorage.getItem('writon-current-text');
    if (savedText && !inputTextArea.value) {
        inputTextArea.value = savedText;
        updateTextStats();
    }
}

function addCustomLanguageOption() {
    if (!Array.from(targetLanguageSelect.options).some(opt => opt.value === 'Custom')) {
        const option = document.createElement('option');
        option.value = 'Custom';
        option.textContent = 'Custom Language...';
        targetLanguageSelect.appendChild(option);
    }
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

export { saveConfig, loadStoredConfig, loadSavedText, addCustomLanguageOption, debouncedSave, debounce };