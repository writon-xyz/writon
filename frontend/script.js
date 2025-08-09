// Writon JavaScript
const providerSelect = document.getElementById('provider');
const apiKeyInput = document.getElementById('apiKey');
const modelInput = document.getElementById('model');
const inputTextArea = document.getElementById('inputText');
const charCountSpan = document.getElementById('charCount');
const wordCountSpan = document.getElementById('wordCount');
const sentenceCountSpan = document.getElementById('sentenceCount');
const modeSelect = document.getElementById('mode');
const caseStyleSelect = document.getElementById('caseStyle');
const targetLanguageSelect = document.getElementById('targetLanguage');
const customLanguageInput = document.getElementById('customLanguage');
const languageGroup = document.getElementById('languageGroup');
const processBtn = document.getElementById('processBtn');
const resultsSection = document.getElementById('resultsSection');
const originalTextDiv = document.getElementById('originalText');
const processedTextDiv = document.getElementById('processedText');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const shareBtn = document.getElementById('shareBtn');
const processAgainBtn = document.getElementById('processAgainBtn');
const statusMessage = document.getElementById('statusMessage');
const loadingOverlay = document.getElementById('loadingOverlay');
const mobileNavToggle = document.querySelector('.nav-mobile-toggle');
const mobileNavOverlay = document.getElementById('mobileNavOverlay');
const mobileNavClose = document.getElementById('mobileNavClose');
const toggleApiKeyBtn = document.getElementById('toggleApiKey');
const clearTextBtn = document.getElementById('clearTextBtn');
const pasteTextBtn = document.getElementById('pasteTextBtn');
const learnMoreBtn = document.getElementById('learnMoreBtn');
const apiStatus = document.getElementById('apiStatus');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const usedMode = document.getElementById('usedMode');
const usedProvider = document.getElementById('usedProvider');
const usedCase = document.getElementById('usedCase');
const usedLanguage = document.getElementById('usedLanguage');
const usedLanguageMeta = document.getElementById('usedLanguageMeta');
const processingTime = document.getElementById('processingTime');
const timeValue = document.getElementById('timeValue');
const originalStats = document.getElementById('originalStats');
const wordDiffStat = document.getElementById('wordDiffStat');
const charDiffStat = document.getElementById('charDiffStat');
const animationToggle = document.getElementById('animationToggle');

// Key links
const keyLinks = {
    'groq': document.getElementById('groq-link'),
    'openai': document.getElementById('openai-link'),
    'google': document.getElementById('google-link'),
    'anthropic': document.getElementById('anthropic-link')
};

// Configuration
const API_BASE = 'http://localhost:8000';
let processingStartTime = 0;
let currentProcessedText = '';

document.addEventListener('DOMContentLoaded', function () {
    setupCustomSelects();
    loadStoredConfig();
    setupEventListeners();
    updateTextStats();
    updateKeyLinks();
    loadSavedText();
    addCustomLanguageOption();
    setupAccessibilityFeatures();
    initializeAnimationSettings();
});

function setupCustomSelects() {
    document.querySelectorAll('.custom-select-wrapper').forEach(wrapper => {
        const selectElement = wrapper.querySelector('select');
        if (wrapper.querySelector('.custom-select')) return;

        const customSelect = document.createElement('div');
        customSelect.className = 'custom-select';

        const selectedDisplay = document.createElement('div');
        selectedDisplay.className = 'select-selected';
        selectedDisplay.textContent = selectElement.options[selectElement.selectedIndex].textContent;
        customSelect.appendChild(selectedDisplay);

        const optionsList = document.createElement('div');
        optionsList.className = 'select-items hidden';

        Array.from(selectElement.options).forEach((option) => {
            const optionDiv = document.createElement('div');
            optionDiv.textContent = option.textContent;
            optionDiv.dataset.value = option.value;

            optionDiv.addEventListener('click', function () {
                selectedDisplay.textContent = this.textContent;
                selectElement.value = this.dataset.value;
                selectElement.dispatchEvent(new Event('change'));
                optionsList.classList.add('hidden');
                selectedDisplay.classList.remove('select-arrow-active');
            });
            optionsList.appendChild(optionDiv);
        });

        customSelect.appendChild(optionsList);
        wrapper.appendChild(customSelect);

        selectedDisplay.addEventListener('click', (e) => {
            e.stopPropagation();
            closeAllSelects(selectedDisplay);
            const rect = selectedDisplay.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            if (spaceBelow < 200 && rect.top > spaceBelow) {
                optionsList.classList.add('select-up');
            } else {
                optionsList.classList.remove('select-up');
            }
            optionsList.classList.toggle('hidden');
            selectedDisplay.classList.toggle('select-arrow-active');
        });
    });

    document.addEventListener('click', closeAllSelects);
}

function closeAllSelects(exceptThisOne) {
    document.querySelectorAll('.select-items').forEach(items => {
        if (items.previousSibling !== exceptThisOne) {
            items.classList.add('hidden');
            items.previousSibling.classList.remove('select-arrow-active');
        }
    });
}


function setupEventListeners() {
    if (mobileNavToggle && mobileNavOverlay && mobileNavClose) {
        mobileNavToggle.addEventListener('click', () => {
            mobileNavOverlay.classList.remove('hidden');
        });

        mobileNavClose.addEventListener('click', () => {
            mobileNavOverlay.classList.add('hidden');
        });

        mobileNavOverlay.addEventListener('click', (e) => {
            if (e.target === mobileNavOverlay || e.target.closest('.mobile-nav-link')) {
                mobileNavOverlay.classList.add('hidden');
            }
        });
    }

    providerSelect.addEventListener('change', function () {
        updateKeyLinks();
        saveConfig();
        updateModelPlaceholder();
    });

    apiKeyInput.addEventListener('input', function () {
        saveConfig();
        validateApiKeyFormat();
    });

    modelInput.addEventListener('input', saveConfig);

    inputTextArea.addEventListener('input', function () {
        updateTextStats();
        debouncedSave();
    });

    modeSelect.addEventListener('change', function () {
        toggleLanguageOptions();
        saveConfig();
    });

    caseStyleSelect.addEventListener('change', saveConfig);

    targetLanguageSelect.addEventListener('change', function () {
        toggleCustomLanguage();
        saveConfig();
    });

    customLanguageInput.addEventListener('input', saveConfig);

    processBtn.addEventListener('click', processText);

    inputTextArea.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            processText();
        }
    });

    toggleApiKeyBtn?.addEventListener('click', toggleApiKeyVisibility);
    clearTextBtn?.addEventListener('click', clearText);
    pasteTextBtn?.addEventListener('click', pasteFromClipboard);
    learnMoreBtn?.addEventListener('click', scrollToFeatures);

    copyBtn.addEventListener('click', copyResult);
    downloadBtn.addEventListener('click', downloadResult);
    shareBtn?.addEventListener('click', shareResult);
    processAgainBtn?.addEventListener('click', processAgain);

    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function () {
            const feature = this.dataset.feature;
            if (feature) {
                modeSelect.value = feature;
                const modeCustomSelect = modeSelect.closest('.custom-select-wrapper').querySelector('.select-selected');
                if (modeCustomSelect) modeCustomSelect.textContent = modeSelect.options[modeSelect.selectedIndex].textContent;

                toggleLanguageOptions();
                saveConfig();
                scrollToProcessor();
            }
        });
    });

    animationToggle.addEventListener('change', (e) => {
        setAnimationState(e.target.checked);
    });
}

function updateTextStats() {
    const text = inputTextArea.value;
    const charCount = text.length;
    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    const sentenceCount = text.trim() ? (text.match(/[.!?]+/g) || []).length : 0;

    charCountSpan.textContent = `${charCount.toLocaleString()} characters`;
    if (charCount > 10000) {
        charCountSpan.style.color = 'var(--system-red)';
    } else if (charCount > 8000) {
        charCountSpan.style.color = 'var(--system-orange)';
    } else {
        charCountSpan.style.color = 'var(--text-tertiary)';
    }

    if (wordCountSpan) wordCountSpan.textContent = `${wordCount} words`;
    if (sentenceCountSpan) sentenceCountSpan.textContent = `${sentenceCount} sentences`;
}

function updateCharCount() {
    updateTextStats();
}

function toggleApiKeyVisibility() {
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
        toggleApiKeyBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        apiKeyInput.type = 'password';
        toggleApiKeyBtn.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

function clearText() {
    if (inputTextArea.value.trim()) {
        if (confirm('Are you sure you want to clear all text?')) {
            inputTextArea.value = '';
            updateTextStats();
            localStorage.removeItem('writon-current-text');
            inputTextArea.focus();
            showStatus('Text cleared', 'info', 2000);
        }
    }
}

async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        if (text) {
            inputTextArea.value = text;
            updateTextStats();
            debouncedSave();
            showStatus('Text pasted from clipboard', 'success', 2000);
        }
    } catch (error) {
        showStatus('Unable to access clipboard. Please paste manually.', 'error');
        inputTextArea.focus();
    }
}

function scrollToFeatures() {
    document.querySelector('.features').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

function scrollToProcessor() {
    document.getElementById('processing-section').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

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

function updateKeyLinks() {
    const provider = providerSelect.value;
    Object.values(keyLinks).forEach(link => {
        link.classList.add('hidden');
    });

    if (keyLinks[provider]) {
        keyLinks[provider].classList.remove('hidden');
    }

    updateApiStatus('disconnected');
}

function updateModelPlaceholder() {
    const provider = providerSelect.value;
    const placeholders = {
        'groq': 'llama-3.1-70b-versatile',
        'openai': 'gpt-4o',
        'google': 'gemini-1.5-flash',
        'anthropic': 'claude-3-haiku-20240307'
    };

    modelInput.placeholder = placeholders[provider] || 'Default model';
}

function toggleLanguageOptions() {
    if (modeSelect.value === 'translate') {
        languageGroup.classList.remove('hidden');
    } else {
        languageGroup.classList.add('hidden');
    }
}

function toggleCustomLanguage() {
    if (targetLanguageSelect.value === 'Custom') {
        customLanguageInput.classList.remove('hidden');
        customLanguageInput.required = true;
    } else {
        customLanguageInput.classList.add('hidden');
        customLanguageInput.required = false;
    }
}

function updateApiStatus(status, message = '') {
    statusIndicator.className = 'status-indicator';
    statusText.className = 'status-text';

    switch (status) {
        case 'connected':
            statusIndicator.classList.add('connected');
            statusText.classList.add('connected');
            statusText.textContent = 'Connected';
            break;
        case 'error':
            statusIndicator.classList.add('error');
            statusText.classList.add('error');
            statusText.textContent = message || 'Invalid key';
            break;
        case 'checking':
            statusIndicator.classList.add('checking');
            statusText.classList.add('checking');
            statusText.textContent = 'Checking...';
            break;
        default:
            statusText.textContent = 'Not connected';
    }
}

async function checkApiKeyStatus() {
    const provider = providerSelect.value;
    const apiKey = apiKeyInput.value.trim();

    if (!apiKey) {
        updateApiStatus('disconnected');
        return;
    }
    if (!validateApiKey(provider, apiKey)) {
        updateApiStatus('error', 'Invalid format');
        return;
    }

    updateApiStatus('checking');

    try {
        const response = await fetch(`${API_BASE}/health`, {
            method: 'GET',
            headers: {
                'X-Provider': provider,
                [`X-${provider.charAt(0).toUpperCase() + provider.slice(1)}-Key`]: apiKey
            }
        });
        updateApiStatus(response.ok ? 'connected' : 'error', 'Key invalid');
    } catch (error) {
        updateApiStatus('error', 'Check failed');
    }
}

const debouncedApiCheck = debounce(checkApiKeyStatus, 1500);

function showLoadingOverlay() {
    loadingOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function hideLoadingOverlay() {
    loadingOverlay.classList.add('hidden');
    document.body.style.overflow = '';
}

function showStatus(message, type = 'info', duration = 5000) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, duration);
}

async function processText() {
    if (!inputTextArea.value.trim()) return showStatus('Please enter some text to process', 'error');
    if (!apiKeyInput.value.trim()) return showStatus('Please enter your API key', 'error');
    if (inputTextArea.value.length > 10000) return showStatus('Text is too long. Maximum 10,000 characters allowed.', 'error');
    if (modeSelect.value === 'translate') {
        const targetLang = targetLanguageSelect.value === 'Custom' ? customLanguageInput.value.trim() : targetLanguageSelect.value;
        if (!targetLang) return showStatus('Please specify a target language for translation', 'error');
    }

    processingStartTime = Date.now();
    processBtn.disabled = true;
    processBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    showLoadingOverlay();

    try {
        const result = await callAPI();
        displayResults(result);
        showStatus('Text processed successfully!', 'success');
    } catch (error) {
        console.error('Processing error:', error);
        showStatus(error.message || 'Failed to process text', 'error');
    } finally {
        processBtn.disabled = false;
        processBtn.innerHTML = '<i class="fas fa-magic"></i> Process Text';
        hideLoadingOverlay();
    }
}

async function callAPI() {
    const provider = providerSelect.value;
    const apiKey = apiKeyInput.value.trim();
    const model = modelInput.value.trim();
    const mode = modeSelect.value;
    const text = inputTextArea.value.trim();
    const caseStyle = caseStyleSelect.value;

    const headers = {
        'Content-Type': 'application/json',
        'X-Provider': provider,
        [`X-${provider.charAt(0).toUpperCase() + provider.slice(1)}-Key`]: apiKey
    };
    if (model) {
        headers[`X-${provider.charAt(0).toUpperCase() + provider.slice(1)}-Model`] = model;
    }

    const body = { text: text, case_style: caseStyle };
    if (mode === 'translate') {
        body.target_language = targetLanguageSelect.value === 'Custom' ? customLanguageInput.value.trim() : targetLanguageSelect.value;
    }

    const endpoint = mode === 'grammar' ? '/grammar' : mode === 'translate' ? '/translate' : mode === 'summarize' ? '/summarize' : '/process';

    const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}`);
    }
    return await response.json();
}

function displayResults(result) {
    const processingDuration = Date.now() - processingStartTime;
    originalTextDiv.textContent = result.original_text;
    processedTextDiv.textContent = result.processed_text;
    currentProcessedText = result.processed_text;

    usedMode.textContent = result.mode.charAt(0).toUpperCase() + result.mode.slice(1);
    usedProvider.textContent = result.provider.charAt(0).toUpperCase() + result.provider.slice(1);
    usedCase.textContent = result.case_style.charAt(0).toUpperCase() + result.case_style.slice(1);

    if (timeValue) {
        timeValue.textContent = `${(processingDuration / 1000).toFixed(1)}s`;
        processingTime.classList.remove('hidden');
    }

    usedLanguageMeta.classList.toggle('hidden', !result.target_language);
    if (result.target_language) {
        usedLanguage.textContent = result.target_language;
    }

    updateResultStats(result.original_text, result.processed_text);

    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    resetCopyButton();
}

function updateResultStats(originalText, processedText) {
    const originalWords = originalText.trim() ? originalText.trim().split(/\s+/).length : 0;
    const processedWords = processedText.trim() ? processedText.trim().split(/\s+/).length : 0;
    const originalChars = originalText.length;
    const processedChars = processedText.length;

    if (originalStats) {
        originalStats.textContent = `${originalWords} words, ${originalChars} chars`;
    }

    const wordDiff = processedWords - originalWords;
    const charDiff = processedChars - originalChars;
    const wordPercent = originalWords > 0 ? (wordDiff / originalWords * 100) : 0;
    const charPercent = originalChars > 0 ? (charDiff / originalChars * 100) : 0;

    if (wordDiffStat) {
        wordDiffStat.textContent = `Words: ${wordDiff > 0 ? '+' : ''}${wordDiff} (${wordPercent.toFixed(0)}%)`;
        wordDiffStat.style.color = wordDiff > 0 ? 'var(--system-green)' : wordDiff < 0 ? 'var(--system-red)' : '';
    }

    if (charDiffStat) {
        charDiffStat.textContent = `Chars: ${charDiff > 0 ? '+' : ''}${charDiff} (${charPercent.toFixed(0)}%)`;
        charDiffStat.style.color = charDiff > 0 ? 'var(--system-green)' : charDiff < 0 ? 'var(--system-red)' : '';
    }
}


async function copyResult() {
    try {
        await navigator.clipboard.writeText(processedTextDiv.textContent);
        copyBtn.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
        copyBtn.classList.add('success');
        showStatus('Text copied to clipboard!', 'success', 2000);
        setTimeout(resetCopyButton, 2000);
    } catch (error) {
        console.error('Copy failed:', error);
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(processedTextDiv);
        selection.removeAllRanges();
        selection.addRange(range);
        showStatus('Text selected. Press Ctrl+C to copy.', 'info');
    }
}

function resetCopyButton() {
    copyBtn.innerHTML = '<i class="fas fa-copy"></i><span>Copy to Clipboard</span>';
    copyBtn.classList.remove('success');
}

function downloadResult() {
    const text = processedTextDiv.textContent;
    const mode = modeSelect.value;
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    let filename = `writon-${mode}-${timestamp}.txt`;
    if (mode === 'translate' && usedLanguage.textContent) {
        filename = `writon-translate-${usedLanguage.textContent.toLowerCase().replace(/\s+/g, '-')}-${timestamp}.txt`;
    }
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showStatus(`File downloaded: ${filename}`, 'success');
}

async function shareResult() {
    const text = currentProcessedText;
    if (navigator.share) {
        try {
            await navigator.share({
                title: `Writon Processed Result`,
                text: text
            });
            showStatus('Shared successfully!', 'success');
        } catch (error) {
            if (error.name !== 'AbortError') {
                fallbackShare(text);
            }
        }
    } else {
        fallbackShare(text);
    }
}

function fallbackShare(text) {
    navigator.clipboard.writeText(text).then(() => {
        showStatus('Share not supported. Text copied to clipboard instead!', 'info');
    }).catch(() => {
        showStatus('Share and copy not supported. Please copy manually.', 'error');
    });
}

function processAgain() {
    scrollToProcessor();
    setTimeout(() => {
        inputTextArea.focus();
        inputTextArea.setSelectionRange(inputTextArea.value.length, inputTextArea.value.length);
    }, 500);
    showStatus('Ready to process again!', 'info', 2000);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
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

function validateApiKey(provider, key) {
    const patterns = {
        'openai': /^sk-[a-zA-Z0-9_-]{32,}$/,
        'groq': /^gsk_[a-zA-Z0-9_-]{32,}$/,
        'google': /^AI[a-zA-Z0-9_-]{32,}$/,
        'anthropic': /^sk-ant-[a-zA-Z0-9_-]{32,}$/
    };
    return patterns[provider] ? patterns[provider].test(key) : key.length > 10;
}

function validateApiKeyFormat() {
    const provider = providerSelect.value;
    const key = apiKeyInput.value.trim();
    if (key && !validateApiKey(provider, key)) {
        apiKeyInput.style.borderColor = 'var(--system-red)';
        apiKeyInput.title = 'API key format appears incorrect';
    } else {
        apiKeyInput.style.borderColor = '';
        apiKeyInput.title = '';
    }
    if (key) {
        debouncedApiCheck();
    } else {
        updateApiStatus('disconnected');
    }
}

function setupAccessibilityFeatures() {
    inputTextArea.setAttribute('aria-describedby', 'charCount wordCount sentenceCount');
    apiKeyInput.setAttribute('aria-describedby', 'apiStatus');

    processBtn.addEventListener('click', function () {
        if (this.disabled) return;

        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.textContent = 'Processing text, please wait...';
        document.body.appendChild(announcement);

        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    });
}

document.addEventListener('DOMContentLoaded', setupAccessibilityFeatures);

let autoSaveTimeout;
function autoSave() {
    clearTimeout(autoSaveTimeout);
    autoSaveTimeout = setTimeout(() => {
        const currentText = inputTextArea.value;
        if (currentText.trim()) {
            localStorage.setItem('writon-current-text', currentText);

            const charCount = document.querySelector('.char-count');
            if (charCount) {
                charCount.style.backgroundColor = 'var(--system-green)';
                charCount.style.color = 'white';
                setTimeout(() => {
                    charCount.style.backgroundColor = '';
                    charCount.style.color = '';
                }, 200);
            }
        }
    }, 2000);
}

inputTextArea.addEventListener('input', function () {
    updateTextStats();
    autoSave();
});

function initializeAdvancedFeatures() {
    document.querySelectorAll('.tooltip').forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function () {
            if (!this.hasAttribute('data-initialized')) {
                this.setAttribute('data-initialized', 'true');
            }
        });
    });
}

window.addEventListener('load', initializeAdvancedFeatures);

function exportConfig() {
    const config = {
        provider: providerSelect.value,
        model: modelInput.value,
        mode: modeSelect.value,
        caseStyle: caseStyleSelect.value,
        targetLanguage: targetLanguageSelect.value,
        customLanguage: customLanguageInput.value,
        version: '2.0',
        exported: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.href = url;
    link.download = `writon-config-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showStatus('Configuration exported successfully!', 'success');
}

function importConfig(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const config = JSON.parse(e.target.result);

            if (config.version && config.provider) {
                providerSelect.value = config.provider;
                modelInput.value = config.model || '';
                modeSelect.value = config.mode || 'grammar';
                caseStyleSelect.value = config.caseStyle || 'sentence';
                targetLanguageSelect.value = config.targetLanguage || 'Spanish';
                customLanguageInput.value = config.customLanguage || '';

                saveConfig();
                updateKeyLinks();
                toggleLanguageOptions();
                toggleCustomLanguage();
                updateModelPlaceholder();

                showStatus('Configuration imported successfully!', 'success');
            } else {
                throw new Error('Invalid configuration file');
            }
        } catch (error) {
            showStatus('Failed to import configuration: ' + error.message, 'error');
        }
    };
    reader.readAsText(file);
}

// Performance Optimization
function initializeAnimationSettings() {
    const savedState = localStorage.getItem('writon-animations-enabled');
    // Default to 'true' (enabled) if no setting is found
    const animationsEnabled = savedState !== 'false';
    animationToggle.checked = animationsEnabled;
    setAnimationState(animationsEnabled);
}

function setAnimationState(enabled) {
    if (enabled) {
        document.body.classList.remove('animations-disabled');
    } else {
        document.body.classList.add('animations-disabled');
    }
    localStorage.setItem('writon-animations-enabled', enabled);
}
