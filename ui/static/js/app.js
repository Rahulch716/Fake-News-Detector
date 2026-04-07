const API_BASE = '';

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
            displayDetectResult(result);
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            setButtonLoading(btn, false);
        }
    });
}

function displayDetectResult(result) {
    const resultCard = document.getElementById('detectResult');
    const verdictBadge = document.getElementById('verdictBadge');
    const confidenceValue = document.getElementById('confidenceValue');
    const mlPrediction = document.getElementById('mlPrediction');
    const ruleVerdict = document.getElementById('ruleVerdict');
    const redFlagsContainer = document.getElementById('redFlags');
    const llmSection = document.getElementById('llmSection');
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
    
    if (result.llm_analysis && result.llm_analysis.available) {
        llmSection.style.display = 'block';
        llmAnalysis.textContent = JSON.stringify(result.llm_analysis, null, 2);
    } else {
        llmSection.style.display = 'none';
    }
    
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
