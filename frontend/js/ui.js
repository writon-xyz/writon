import { providerSelect, apiKeyInput, modelInput, inputTextArea, charCountSpan, wordCountSpan, sentenceCountSpan, modeSelect, caseStyleSelect, targetLanguageSelect, customLanguageInput, languageGroup, processBtn, resultsSection, originalTextDiv, processedTextDiv, copyBtn, downloadBtn, shareBtn, processAgainBtn, statusMessage, loadingOverlay, mobileNavToggle, mobileNavOverlay, mobileNavClose, toggleApiKeyBtn, clearTextBtn, pasteTextBtn, fileUploadInput, apiStatus, statusIndicator, statusText, usedMode, usedProvider, usedCase, usedLanguage, usedLanguageMeta, processingTime, timeValue, originalStats, wordDiffStat, charDiffStat, fabSettingsToggle, settingsPanel, keyLinks } from './main.js';
import { debouncedSave } from './config.js';
import { debouncedApiCheck, processingStartTime } from './events.js';

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

function updateTextStats() {
    if (!inputTextArea || !charCountSpan) return;
    
    const text = inputTextArea.value;
    const charCount = text.length;
    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    const sentenceCount = text.trim() ? (text.match(/[.!?]+/g) || []).length : 0;

    charCountSpan.textContent = `${charCount.toLocaleString()} characters`;
    if (charCount > 10000) {
        charCountSpan.style.color = 'var(--system-red)';
    } else if (charCount > 8000) {
        charCountSpan.style.color = '#656d76'; /* fg.muted */
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
    if (providerSelect && modelInput) {
        const provider = providerSelect.value;
        const placeholders = {
            'groq': 'llama-3.1-70b-versatile',
            'openai': 'gpt-4o',
            'google': 'gemini-1.5-flash',
            'anthropic': 'claude-3-haiku-20240307'
        };

        modelInput.placeholder = placeholders[provider] || 'Default model';
    }
}

function toggleLanguageOptions() {
    if (modeSelect && languageGroup) {
        if (modeSelect.value === 'translate') {
            languageGroup.classList.remove('hidden');
        } else {
            languageGroup.classList.add('hidden');
        }
    }
}

function toggleCustomLanguage() {
    if (targetLanguageSelect && customLanguageInput) {
        if (targetLanguageSelect.value === 'Custom') {
            customLanguageInput.classList.remove('hidden');
            customLanguageInput.required = true;
        } else {
            customLanguageInput.classList.add('hidden');
            customLanguageInput.required = false;
        }
    }
}

function updateApiStatus(status, message = '') {
    if (!statusIndicator || !statusText) return;
    
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

function showLoadingOverlay() {
    loadingOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Animate progress bar
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.width = '30%';
        }, 200);
        setTimeout(() => {
            progressBar.style.width = '60%';
        }, 1000);
        setTimeout(() => {
            progressBar.style.width = '90%';
        }, 2000);
    }
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

function displayResults(result) {
    const processingDuration = Date.now() - processingStartTime;
    
    // Animate results appearance
    resultsSection.classList.remove('hidden');
    resultsSection.style.opacity = '0';
    resultsSection.style.transform = 'translateY(30px)';
    
    // Update content
    originalTextDiv.textContent = result.original_text;
    processedTextDiv.textContent = result.processed_text;
    

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

    // Animate in
    setTimeout(() => {
        resultsSection.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        resultsSection.style.opacity = '1';
        resultsSection.style.transform = 'translateY(0)';
    }, 100);

    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    resetCopyButton();
    
    // Add success animation to process button
    processBtn.classList.add('success');
    setTimeout(() => processBtn.classList.remove('success'), 600);
    
    // Return the processed text for sharing
    return result.processed_text;
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
    const originalText = inputTextArea.value;
    const processedText = processedTextDiv.textContent;
    const mode = modeSelect.value;
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    let filename = `writon-${mode}-${timestamp}.txt`;
    if (mode === 'translate' && usedLanguage.textContent) {
        filename = `writon-translate-${usedLanguage.textContent.toLowerCase().replace(/\s+/g, '-')}-${timestamp}.txt`;
    }

    const originalWords = originalText.trim() ? originalText.trim().split(/\s+/).length : 0;
    const processedWords = processedText.trim() ? processedText.trim().split(/\s+/).length : 0;
    const originalChars = originalText.length;
    const processedChars = processedText.length;

    const stats = `--- Original Text ---
${originalText}

--- Processed Text ---
${processedText}

--- Stats ---
Mode: ${modeSelect.options[modeSelect.selectedIndex].text}
Case Style: ${caseStyleSelect.options[caseStyleSelect.selectedIndex].text}
AI Provider: ${providerSelect.options[providerSelect.selectedIndex].text}
Original Character Count: ${originalChars}
Processed Character Count: ${processedChars}
Original Word Count: ${originalWords}
Processed Word Count: ${processedWords}
`;

    const blob = new Blob([stats], { type: 'text/plain;charset=utf-8' });
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

async function shareResult(text) {
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
    document.getElementById('processing-section').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
    setTimeout(() => {
        inputTextArea.focus();
        inputTextArea.setSelectionRange(inputTextArea.value.length, inputTextArea.value.length);
    }, 500);
    showStatus('Ready to process again!', 'info', 2000);
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
        apiKeyInput.classList.add('error');
        apiKeyInput.style.borderColor = 'var(--system-red)';
        apiKeyInput.title = 'API key format appears incorrect';
        showStatus('Invalid API key format', 'error', 3000);
    } else {
        apiKeyInput.classList.remove('error');
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

export { setupCustomSelects, updateTextStats, updateCharCount, toggleApiKeyVisibility, clearText, pasteFromClipboard, updateKeyLinks, updateModelPlaceholder, toggleLanguageOptions, toggleCustomLanguage, updateApiStatus, showLoadingOverlay, hideLoadingOverlay, showStatus, displayResults, updateResultStats, copyResult, resetCopyButton, downloadResult, shareResult, fallbackShare, processAgain, validateApiKey, validateApiKeyFormat, setupAccessibilityFeatures };