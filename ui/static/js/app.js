const API_BASE = '';
const LLM_PREVIEW_REASON_COUNT = 2;
const LLM_EVIDENCE_PREVIEW_LENGTH = 160;

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initDetect();
    initBatchDetect();
    initTrain();
    initFeatures();
    checkApiStatus();
    loadModelInfo();
});

function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(`${tabId}-tab`).classList.add('active');
        });
    });
}

async function checkApiStatus() {
    const statusEl = document.getElementById('apiStatus');
    
    try {
        const response = await fetch('/health');
        if (response.ok) {
            statusEl.classList.remove('connecting');
            statusEl.classList.add('connected');
            statusEl.querySelector('.status-text').textContent = 'Connected';
        } else {
            throw new Error('API returned error');
        }
    } catch (error) {
        statusEl.classList.remove('connecting');
        statusEl.classList.add('disconnected');
        statusEl.querySelector('.status-text').textContent = 'Disconnected';
    }
}

async function loadModelInfo() {
    try {
        const response = await fetch('/model-info');
        const data = await response.json();
        
        const mlStatus = document.getElementById('mlModelStatus');
        const llmStatus = document.getElementById('llmStatus');
        
        if (data.ml_model_loaded) {
            mlStatus.textContent = 'Loaded';
            mlStatus.classList.add('connected');
        } else {
            mlStatus.textContent = 'Not Loaded';
            mlStatus.classList.add('disconnected');
        }
        
        if (data.llm_available) {
            llmStatus.textContent = 'Available';
            llmStatus.classList.add('connected');
        } else {
            llmStatus.textContent = 'Not Available';
            llmStatus.classList.add('disconnected');
        }
    } catch (error) {
        console.error('Error loading model info:', error);
    }
}

function initDetect() {
    const btn = document.getElementById('detectBtn');
    const textInput = document.getElementById('newsText');
    
    btn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to analyze');
            return;
        }

        clearDetectResult();
        setButtonLoading(btn, true);
        
        try {
            const response = await fetch('/detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    use_ml: document.getElementById('useML').checked,
                    use_rules: document.getElementById('useRules').checked,
                    use_llm: document.getElementById('useLLM').checked
                })
            });
            
            const result = await response.json();
            if (!response.ok || result.error || result.detail) {
                throw new Error(result.detail || result.error || 'Detection failed');
            }
            displayDetectResult(result);
        } catch (error) {
            clearDetectResult();
            alert('Error: ' + error.message);
        } finally {
            setButtonLoading(btn, false);
        }
    });
}

function clearDetectResult() {
    const resultCard = document.getElementById('detectResult');
    const verdictBadge = document.getElementById('verdictBadge');
    const confidenceValue = document.getElementById('confidenceValue');
    const mlPrediction = document.getElementById('mlPrediction');
    const ruleVerdict = document.getElementById('ruleVerdict');
    const redFlagsContainer = document.getElementById('redFlags');
    const llmSection = document.getElementById('llmSection');
    const llmToggle = document.getElementById('llmToggle');
    const llmPreview = document.getElementById('llmPreview');
    const llmDetails = document.getElementById('llmDetails');
    const llmVerdict = document.getElementById('llmVerdict');
    const llmConfidence = document.getElementById('llmConfidence');
    const llmReasons = document.getElementById('llmReasons');
    const llmReasonsBlock = document.getElementById('llmReasonsBlock');
    const llmRedFlags = document.getElementById('llmRedFlags');
    const llmRedFlagsBlock = document.getElementById('llmRedFlagsBlock');
    const llmEvidence = document.getElementById('llmEvidence');
    const llmEvidenceBlock = document.getElementById('llmEvidenceBlock');
    const llmRawBlock = document.getElementById('llmRawBlock');
    const llmAnalysis = document.getElementById('llmAnalysis');

    resultCard.style.display = 'none';
    verdictBadge.className = 'verdict';
    verdictBadge.querySelector('.verdict-text').textContent = '';
    confidenceValue.textContent = '0%';
    mlPrediction.textContent = '-';
    ruleVerdict.textContent = '-';
    redFlagsContainer.innerHTML = '';
    llmSection.style.display = 'none';
    llmSection.dataset.expanded = 'false';
    llmToggle.style.display = 'none';
    llmToggle.textContent = 'Show More';
    llmPreview.textContent = '-';
    llmDetails.style.display = 'none';
    llmVerdict.className = 'llm-stat-value llm-verdict';
    llmVerdict.textContent = '-';
    llmConfidence.textContent = '-';
    llmReasons.innerHTML = '';
    llmReasonsBlock.style.display = 'none';
    llmRedFlags.innerHTML = '';
    llmRedFlagsBlock.style.display = 'none';
    llmEvidence.textContent = '-';
    llmEvidenceBlock.style.display = 'none';
    llmRawBlock.style.display = 'none';
    llmAnalysis.textContent = '-';
}

function displayDetectResult(result) {
    const resultCard = document.getElementById('detectResult');
    const verdictBadge = document.getElementById('verdictBadge');
    const confidenceValue = document.getElementById('confidenceValue');
    const mlPrediction = document.getElementById('mlPrediction');
    const ruleVerdict = document.getElementById('ruleVerdict');
    const redFlagsContainer = document.getElementById('redFlags');
    const llmSection = document.getElementById('llmSection');
    const llmToggle = document.getElementById('llmToggle');
    const llmPreview = document.getElementById('llmPreview');
    const llmDetails = document.getElementById('llmDetails');
    const llmVerdict = document.getElementById('llmVerdict');
    const llmConfidence = document.getElementById('llmConfidence');
    const llmReasons = document.getElementById('llmReasons');
    const llmReasonsBlock = document.getElementById('llmReasonsBlock');
    const llmRedFlags = document.getElementById('llmRedFlags');
    const llmRedFlagsBlock = document.getElementById('llmRedFlagsBlock');
    const llmEvidence = document.getElementById('llmEvidence');
    const llmEvidenceBlock = document.getElementById('llmEvidenceBlock');
    const llmRawBlock = document.getElementById('llmRawBlock');
    const llmAnalysis = document.getElementById('llmAnalysis');
    
    resultCard.style.display = 'block';
    
    const verdict = result.final_verdict || 'unable to determine';
    const confidence = Math.round((result.confidence || 0) * 100);
    
    verdictBadge.className = 'verdict ' + verdict;
    verdictBadge.querySelector('.verdict-text').textContent = verdict === 'unable to determine' ? 'Unknown' : verdict.toUpperCase();
    
    confidenceValue.textContent = confidence + '%';
    
    if (result.ml_prediction) {
        mlPrediction.textContent = `${result.ml_prediction} (${Math.round((result.ml_confidence || 0) * 100)}%)`;
    } else {
        mlPrediction.textContent = 'Not available';
    }
    
    if (result.rule_based_result) {
        ruleVerdict.textContent = result.rule_based_result.verdict || '-';
        
        const redFlags = result.rule_based_result.red_flags || [];
        redFlagsContainer.innerHTML = redFlags.map(flag => 
            `<span class="red-flag">${flag}</span>`
        ).join('');
    } else {
        ruleVerdict.textContent = 'Not available';
        redFlagsContainer.innerHTML = '';
    }
    
    renderLlmAnalysis(
        result.llm_analysis,
        {
            llmSection,
            llmToggle,
            llmPreview,
            llmDetails,
            llmVerdict,
            llmConfidence,
            llmReasons,
            llmReasonsBlock,
            llmRedFlags,
            llmRedFlagsBlock,
            llmEvidence,
            llmEvidenceBlock,
            llmRawBlock,
            llmAnalysis
        }
    );
    
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderLlmAnalysis(llmResult, elements) {
    if (!llmResult) {
        elements.llmSection.style.display = 'none';
        return;
    }

    elements.llmSection.style.display = 'block';
    elements.llmSection.dataset.expanded = 'false';

    if (llmResult.error) {
        elements.llmToggle.style.display = 'none';
        elements.llmPreview.textContent = 'LLM analysis failed.';
        elements.llmDetails.style.display = 'block';
        elements.llmVerdict.className = 'llm-stat-value llm-verdict uncertain';
        elements.llmVerdict.textContent = 'Error';
        elements.llmConfidence.textContent = '-';
        elements.llmReasonsBlock.style.display = 'none';
        elements.llmRedFlagsBlock.style.display = 'none';
        elements.llmEvidenceBlock.style.display = 'block';
        elements.llmEvidence.textContent = llmResult.error;
        elements.llmRawBlock.style.display = 'none';
        return;
    }

    const verdict = (llmResult.verdict || 'uncertain').toLowerCase();
    const confidence = typeof llmResult.confidence === 'number'
        ? `${Math.round(llmResult.confidence * 100)}%`
        : '-';
    const reasons = Array.isArray(llmResult.reasons) ? llmResult.reasons : [];
    const redFlags = Array.isArray(llmResult.red_flags) ? llmResult.red_flags : [];
    const evidence = llmResult.supporting_evidence || '';
    const hasStructuredData =
        Object.prototype.hasOwnProperty.call(llmResult, 'verdict') ||
        Object.prototype.hasOwnProperty.call(llmResult, 'confidence') ||
        reasons.length > 0 ||
        redFlags.length > 0 ||
        Boolean(evidence);
    const previewText = buildLlmPreview(verdict, reasons, redFlags, evidence);
    const shouldCollapse = reasons.length > LLM_PREVIEW_REASON_COUNT || evidence.length > LLM_EVIDENCE_PREVIEW_LENGTH || redFlags.length > 0;

    elements.llmVerdict.className = `llm-stat-value llm-verdict ${verdict}`;
    elements.llmVerdict.textContent = formatLabel(verdict);
    elements.llmConfidence.textContent = confidence;
    elements.llmPreview.textContent = previewText;

    elements.llmReasonsBlock.style.display = reasons.length ? 'block' : 'none';
    elements.llmReasons.innerHTML = reasons.map(reason => `<li>${escapeHtml(reason)}</li>`).join('');

    elements.llmRedFlagsBlock.style.display = redFlags.length ? 'block' : 'none';
    elements.llmRedFlags.innerHTML = redFlags.map(flag =>
        `<span class="red-flag">${escapeHtml(flag)}</span>`
    ).join('');

    elements.llmEvidenceBlock.style.display = evidence ? 'block' : 'none';
    elements.llmEvidence.textContent = evidence || '-';

    elements.llmRawBlock.style.display = hasStructuredData ? 'none' : 'block';
    elements.llmAnalysis.textContent = JSON.stringify(llmResult, null, 2);
    elements.llmToggle.style.display = shouldCollapse ? 'inline-flex' : 'none';
    elements.llmToggle.textContent = 'Show More';
    elements.llmDetails.style.display = shouldCollapse ? 'none' : 'block';
    elements.llmToggle.onclick = shouldCollapse
        ? () => toggleLlmDetails(elements.llmSection, elements.llmToggle, elements.llmDetails)
        : null;
}

function toggleLlmDetails(section, toggle, details) {
    const isExpanded = section.dataset.expanded === 'true';
    const nextExpanded = !isExpanded;

    section.dataset.expanded = nextExpanded ? 'true' : 'false';
    details.style.display = nextExpanded ? 'block' : 'none';
    toggle.textContent = nextExpanded ? 'Show Less' : 'Show More';
}

function buildLlmPreview(verdict, reasons, redFlags, evidence) {
    const previewReasons = reasons.slice(0, LLM_PREVIEW_REASON_COUNT);
    const previewParts = [];

    if (previewReasons.length) {
        previewParts.push(previewReasons.join(' '));
    }

    if (redFlags.length) {
        previewParts.push(`${redFlags.length} red flag${redFlags.length > 1 ? 's' : ''} detected.`);
    }

    if (evidence) {
        previewParts.push(truncateText(evidence, LLM_EVIDENCE_PREVIEW_LENGTH));
    }

    if (!previewParts.length) {
        return `${formatLabel(verdict)} analysis available.`;
    }

    return previewParts.join(' ');
}

function truncateText(value, maxLength) {
    if (!value || value.length <= maxLength) {
        return value;
    }

    return `${value.slice(0, maxLength).trimEnd()}...`;
}

function formatLabel(value) {
    if (!value) {
        return '-';
    }

    return value
        .split('_')
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ');
}

function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value;
    return div.innerHTML;
}

function initBatchDetect() {
    const btn = document.getElementById('batchDetectBtn');
    const textInput = document.getElementById('batchText');
    
    btn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to analyze');
            return;
        }
        
        const texts = text.split('\n').filter(t => t.trim());
        if (texts.length === 0) {
            alert('Please enter at least one article');
            return;
        }

        setButtonLoading(btn, true);
        
        try {
            const response = await fetch('/batch-detect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texts })
            });
            
            const result = await response.json();
            if (!response.ok || result.error || result.detail) {
                throw new Error(result.detail || result.error || 'Batch detection failed');
            }
            displayBatchResult(result, texts);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setButtonLoading(btn, false);
        }
    });
}

function displayBatchResult(result, texts) {
    const resultCard = document.getElementById('batchResult');
    const batchCount = document.getElementById('batchCount');
    const batchResults = document.getElementById('batchResults');
    
    resultCard.style.display = 'block';
    batchCount.textContent = result.results ? result.results.length : 0;
    
    if (result.results && result.results.length > 0) {
        const originalTexts = texts;
        batchResults.innerHTML = result.results.map((r, i) => {
            const prediction = r.prediction || 'unknown';
            const confidence = Math.round((r.confidence || 0) * 100);
            return `
                <div class="batch-item ${prediction}">
                    <div class="batch-item-text">${originalTexts[i] || 'Article ' + (i + 1)}</div>
                    <div class="batch-item-result">
                        <span class="batch-item-verdict ${prediction}">${prediction.toUpperCase()}</span>
                        <span class="batch-item-confidence">${confidence}% confidence</span>
                    </div>
                </div>
            `;
        }).join('');
    } else {
        batchResults.innerHTML = '<p>No results available</p>';
    }
    
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function initTrain() {
    const btn = document.getElementById('trainBtn');
    const textInput = document.getElementById('trainText');
    
    btn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter training data');
            return;
        }
        
        const lines = text.split('\n').filter(l => l.trim());
        const texts = [];
        const labels = [];
        
        for (const line of lines) {
            const parts = line.split('|');
            if (parts.length >= 2) {
                texts.push(parts[0].trim());
                labels.push(parts[1].trim().toLowerCase());
            }
        }
        
        if (texts.length < 10) {
            alert('Please provide at least 10 training samples');
            return;
        }

        setButtonLoading(btn, true);
        
        try {
            const response = await fetch('/train', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    texts,
                    labels,
                    algorithm: document.getElementById('algorithm').value
                })
            });
            
            const result = await response.json();
            if (!response.ok || result.error || result.detail) {
                throw new Error(result.detail || result.error || 'Training failed');
            }
            displayTrainResult(result);
            loadModelInfo();
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setButtonLoading(btn, false);
        }
    });
}

function displayTrainResult(result) {
    const resultCard = document.getElementById('trainResult');
    
    if (result.status === 'success' && result.metrics) {
        const m = result.metrics;
        
        document.getElementById('accuracy').textContent = (m.accuracy * 100).toFixed(1) + '%';
        document.getElementById('precision').textContent = (m.precision * 100).toFixed(1) + '%';
        document.getElementById('recall').textContent = (m.recall * 100).toFixed(1) + '%';
        document.getElementById('f1Score').textContent = (m.f1_score * 100).toFixed(1) + '%';
        document.getElementById('cvMean').textContent = (m.cv_accuracy_mean * 100).toFixed(1) + '%';
        document.getElementById('cvStd').textContent = (m.cv_accuracy_std * 100).toFixed(1) + '%';
        
        document.getElementById('classificationReport').textContent = m.classification_report || 'N/A';
    } else {
        alert('Training failed: ' + (result.error || 'Unknown error'));
        return;
    }
    
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function initFeatures() {
    const btn = document.getElementById('extractBtn');
    const textInput = document.getElementById('featureText');
    
    btn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text');
            return;
        }

        setButtonLoading(btn, true);
        
        try {
            const response = await fetch('/extract-features', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            
            const result = await response.json();
            if (!response.ok || result.error || result.detail) {
                throw new Error(result.detail || result.error || 'Feature extraction failed');
            }
            displayFeaturesResult(result);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setButtonLoading(btn, false);
        }
    });
}

function displayFeaturesResult(result) {
    const resultCard = document.getElementById('featureResult');
    const featuresGrid = document.getElementById('featuresGrid');
    
    resultCard.style.display = 'block';
    
    if (result.features) {
        const featureNames = {
            length: 'Text Length',
            word_count: 'Word Count',
            sentence_count: 'Sentence Count',
            avg_word_length: 'Avg Word Length',
            avg_sentence_length: 'Avg Sentence Length',
            capital_ratio: 'Capital Ratio',
            digit_ratio: 'Digit Ratio',
            special_char_ratio: 'Special Char Ratio',
            exclamation_count: 'Exclamation Count',
            question_count: 'Question Count',
            quote_count: 'Quote Count',
            uppercase_word_count: 'Uppercase Words',
            unique_word_ratio: 'Unique Word Ratio',
            punctuation_ratio: 'Punctuation Ratio',
            url_count: 'URL Count',
            mention_count: 'Mention Count',
            hashtag_count: 'Hashtag Count',
            readability_score: 'Readability Score',
            sentiment_polarity: 'Sentiment Polarity',
            entity_density: 'Entity Density'
        };
        
        featuresGrid.innerHTML = Object.entries(result.features).map(([key, value]) => {
            const displayName = featureNames[key] || key;
            const displayValue = typeof value === 'number' ? value.toFixed(3) : value;
            return `
                <div class="feature-item">
                    <div class="feature-name">${displayName}</div>
                    <div class="feature-value">${displayValue}</div>
                </div>
            `;
        }).join('');
    } else {
        featuresGrid.innerHTML = '<p>No features available</p>';
    }
    
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function setButtonLoading(btn, loading) {
    const btnText = btn.querySelector('.btn-text');
    const btnLoading = btn.querySelector('.btn-loading');
    
    if (loading) {
        btn.disabled = true;
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline-flex';
    } else {
        btn.disabled = false;
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
    }
}
