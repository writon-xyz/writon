import { providerSelect, apiKeyInput, modelInput, inputTextArea, modeSelect, caseStyleSelect, targetLanguageSelect, customLanguageInput, processBtn, toggleApiKeyBtn, clearTextBtn, pasteTextBtn, fileUploadInput, copyBtn, downloadBtn, shareBtn, processAgainBtn, fabSettingsToggle, settingsPanel, mobileNavToggle, mobileNavOverlay, mobileNavClose } from './main.js';
import * as UI from './ui.js';
import { handleFileUpload, callAPI, checkApiKeyStatus } from './api.js';
import { saveConfig, debouncedSave, debounce } from './config.js';

let processingStartTime = 0;
let currentProcessedText = '';

    const debouncedApiCheck = debounce(checkApiKeyStatus, 1500);

function setupEventListeners() {
    if (mobileNavToggle && mobileNavOverlay && mobileNavClose) {
        mobileNavToggle.addEventListener('click', () => {
            mobileNavOverlay.classList.remove('hidden');
        });

        mobileNavClose.addEventListener('click', () => {
            mobileNavOverlay.classList.add('hidden');
        });

        mobileNavOverlay.addEventListener('click', (e) => {
            if (e.target === mobileNavOverlay) {
                mobileNavOverlay.classList.add('hidden');
            }
        });
        
        // Handle mobile nav link clicks separately
        const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
        mobileNavLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileNavOverlay.classList.add('hidden');
            });
        });
    }

    // Only add event listeners if elements exist (for main page)
    if (providerSelect) {
        providerSelect.addEventListener('change', function () {
            UI.updateKeyLinks();
            saveConfig();
            UI.updateModelPlaceholder();
        });
    }

    if (apiKeyInput) {
        apiKeyInput.addEventListener('input', function () {
            saveConfig();
            UI.validateApiKeyFormat();
        });
    }

    if (modelInput) {
        modelInput.addEventListener('input', saveConfig);
    }

    if (inputTextArea) {
        inputTextArea.addEventListener('input', function () {
            UI.updateTextStats();
            debouncedSave();
        });
    }

    if (modeSelect) {
        modeSelect.addEventListener('change', function () {
            UI.toggleLanguageOptions();
            saveConfig();
        });
    }

    if (caseStyleSelect) {
        caseStyleSelect.addEventListener('change', saveConfig);
    }

    if (targetLanguageSelect) {
        targetLanguageSelect.addEventListener('change', function () {
            UI.toggleCustomLanguage();
            saveConfig();
        });
    }

    if (customLanguageInput) {
        customLanguageInput.addEventListener('input', saveConfig);
    }

    if (processBtn) {
        processBtn.addEventListener('click', processText);
    }

    if (inputTextArea) {
        inputTextArea.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                processText();
            }
        });
    }

    toggleApiKeyBtn?.addEventListener('click', UI.toggleApiKeyVisibility);
    clearTextBtn?.addEventListener('click', UI.clearText);
    pasteTextBtn?.addEventListener('click', UI.pasteFromClipboard);
    fileUploadInput?.addEventListener('change', handleFileUpload);

    if (copyBtn) copyBtn.addEventListener('click', UI.copyResult);
    if (downloadBtn) downloadBtn.addEventListener('click', UI.downloadResult);
    if (shareBtn) shareBtn.addEventListener('click', () => UI.shareResult(currentProcessedText));
    if (processAgainBtn) processAgainBtn.addEventListener('click', UI.processAgain);

    if (fabSettingsToggle) {
        fabSettingsToggle.addEventListener('click', () => {
            if (settingsPanel) settingsPanel.classList.toggle('visible');
        });
    }

    if (settingsPanel) {
        settingsPanel.addEventListener('click', (e) => {
            if (e.target === settingsPanel) {
                settingsPanel.classList.remove('visible');
            }
        });
    }


    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function () {
            const feature = this.dataset.feature;
            if (feature) {
                // Remove previous selection to handle rapid clicks
                document.querySelectorAll('.feature-card').forEach(c => c.classList.remove('selected'));
                
                // Add selection to clicked card
                this.classList.add('selected');
                
                // Deselect after feedback duration
                setTimeout(() => {
                    this.classList.remove('selected');
                }, 2000);

                modeSelect.value = feature;
                const modeCustomSelect = modeSelect.closest('.custom-select-wrapper').querySelector('.select-selected');
                if (modeCustomSelect) modeCustomSelect.textContent = modeSelect.options[modeSelect.selectedIndex].textContent;

                UI.toggleLanguageOptions();
                saveConfig();
                document.getElementById('processing-section').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Show success feedback
                UI.showStatus(`${feature.charAt(0).toUpperCase() + feature.slice(1)} mode selected`, 'success', 2000);
            }
        });
    });

}

async function processText() {
    if (!inputTextArea.value.trim()) return UI.showStatus('Please enter some text to process', 'error');
    if (!apiKeyInput.value.trim()) return UI.showStatus('Please enter your API key', 'error');
    if (inputTextArea.value.length > 10000) return UI.showStatus('Text is too long. Maximum 10,000 characters allowed.', 'error');
    if (modeSelect.value === 'translate') {
        const targetLang = targetLanguageSelect.value === 'Custom' ? customLanguageInput.value.trim() : targetLanguageSelect.value;
        if (!targetLang) return UI.showStatus('Please specify a target language for translation', 'error');
    }

    processingStartTime = Date.now();
    processBtn.disabled = true;
    processBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    console.log('Calling UI.showLoadingOverlay()');
    UI.showLoadingOverlay();

    try {
        const result = await callAPI();
        console.log('callAPI() returned result:', result);
        currentProcessedText = UI.displayResults(result);
        UI.showStatus('Text processed successfully!', 'success');
    } catch (error) {
        console.error('Processing error:', error);
        console.error('Error object details:', JSON.stringify(error, Object.getOwnPropertyNames(error)));
        UI.showStatus(error.message || 'Failed to process text', 'error');
    } finally {
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-magic"></i> Process Text';
        console.log('Calling UI.hideLoadingOverlay()');
        UI.hideLoadingOverlay();
    }
}

export { setupEventListeners, processingStartTime, currentProcessedText, debouncedApiCheck };