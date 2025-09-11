
// DOM Elements
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
const fileUploadInput = document.getElementById('fileUpload');
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
const fabSettingsToggle = document.getElementById('fab-settings-toggle');
const settingsPanel = document.querySelector('.settings-panel');

// Key links
const keyLinks = {
    'groq': document.getElementById('groq-link'),
    'openai': document.getElementById('openai-link'),
    'google': document.getElementById('google-link'),
    'anthropic': document.getElementById('anthropic-link')
};

export {
    providerSelect, apiKeyInput, modelInput, inputTextArea, charCountSpan, wordCountSpan, sentenceCountSpan,
    modeSelect, caseStyleSelect, targetLanguageSelect, customLanguageInput, languageGroup, processBtn,
    resultsSection, originalTextDiv, processedTextDiv, copyBtn, downloadBtn, shareBtn, processAgainBtn,
    statusMessage, loadingOverlay, mobileNavToggle, mobileNavOverlay, mobileNavClose, toggleApiKeyBtn,
    clearTextBtn, pasteTextBtn, fileUploadInput, apiStatus, statusIndicator, statusText, usedMode,
    usedProvider, usedCase, usedLanguage, usedLanguageMeta, processingTime, timeValue, originalStats,
    wordDiffStat, charDiffStat, fabSettingsToggle, settingsPanel, keyLinks
};

import { setupCustomSelects, updateTextStats, updateKeyLinks, setupAccessibilityFeatures } from './ui.js';
import { loadStoredConfig, loadSavedText, addCustomLanguageOption } from './config.js';
import { setupEventListeners } from './events.js';

document.addEventListener('DOMContentLoaded', function () {
    setupCustomSelects();
    loadStoredConfig();
    setupEventListeners();
    updateTextStats();
    updateKeyLinks();
    loadSavedText();
    addCustomLanguageOption();
    setupAccessibilityFeatures();
});
