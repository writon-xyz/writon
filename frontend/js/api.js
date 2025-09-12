const API_URL = window.location.origin; // Use the current domain (writon.xyz)

import { showLoadingOverlay, hideLoadingOverlay, showStatus, updateApiStatus, updateTextStats, validateApiKey } from './ui.js';
import { providerSelect, apiKeyInput, modelInput, modeSelect, caseStyleSelect, targetLanguageSelect, customLanguageInput, inputTextArea } from './main.js';

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    showLoadingOverlay();
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Failed to upload file.' }));
            throw new Error(errorData.detail);
        }

        const result = await response.json();
        inputTextArea.value = result.content;
        updateTextStats();
        showStatus(`Successfully uploaded ${result.filename}`, 'success');
    } catch (error) {
        console.error('File upload error:', error);
        showStatus(error.message || 'Failed to upload file.', 'error');
    } finally {
        hideLoadingOverlay();
        // Reset the file input so the user can upload the same file again
        event.target.value = null;
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
        [`x-${provider}-key`]: apiKey
    };
    if (model) {
        headers[`x-${provider}-model`] = model;
    }

    const body = { text: text, case_style: caseStyle };
    if (mode === 'translate') {
        body.target_language = targetLanguageSelect.value === 'Custom' ? customLanguageInput.value.trim() : targetLanguageSelect.value;
    }

    const endpoint = mode === 'grammar' ? '/grammar' : mode === 'translate' ? '/translate' : mode === 'summarize' ? '/summarize' : '/process';

    const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || errorData.detail || `HTTP ${response.status}`);
    }
    return await response.json();
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
        const response = await fetch(`${API_URL}/health`, {
            method: 'GET',
            headers: {
                'X-Provider': provider,
                [`x-${provider}-key`]: apiKey
            }
        });
        updateApiStatus(response.ok ? 'connected' : 'error', 'Key invalid');
    } catch (error) {
        updateApiStatus('error', 'Check failed');
    }
}

export { handleFileUpload, callAPI, checkApiKeyStatus };