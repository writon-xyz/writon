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
            // Only set values if elements exist (for main page)
            if (providerSelect) providerSelect.value = config.provider || 'groq';
            if (apiKeyInput) apiKeyInput.value = config.apiKey || '';
            if (modelInput) modelInput.value = config.model || '';
            if (modeSelect) modeSelect.value = config.mode || 'grammar';
            if (caseStyleSelect) caseStyleSelect.value = config.caseStyle || 'sentence';
            if (targetLanguageSelect) targetLanguageSelect.value = config.targetLanguage || 'Spanish';
            if (customLanguageInput) customLanguageInput.value = config.customLanguage || '';

            document.querySelectorAll('.custom-select-wrapper').forEach(wrapper => {
                const select = wrapper.querySelector('select');
                const selectedDisplay = wrapper.querySelector('.select-selected');
                if (select && selectedDisplay) {
                    selectedDisplay.textContent = select.options[select.selectedIndex].textContent;
                }
            });

            // Only call functions if we're on the main page
            if (typeof toggleLanguageOptions === 'function') toggleLanguageOptions();
            if (typeof toggleCustomLanguage === 'function') toggleCustomLanguage();
            if (typeof updateModelPlaceholder === 'function') updateModelPlaceholder();
            if (typeof checkApiKeyStatus === 'function') checkApiKeyStatus();
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
    if (!inputTextArea) return;
    
    const savedText = localStorage.getItem('writon-current-text');
    if (savedText && !inputTextArea.value) {
        inputTextArea.value = savedText;
        updateTextStats();
    }
}

function addCustomLanguageOption() {
    if (!targetLanguageSelect) return;
    
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