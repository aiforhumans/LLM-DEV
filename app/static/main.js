const API_BASE = 'http://127.0.0.1:8000/api';

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    checkHealth();
    loadModels();
    setupChat();
    setupABTest();
    setupTools();
    setupTemplates();
});

function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
        });
    });
}

async function checkHealth() {
    const statusEl = document.getElementById('server-status');
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        if (data.status === 'online') {
            statusEl.textContent = '🟢 LM Studio Connected';
            statusEl.style.color = '#4caf50';
        } else {
            console.warn("Health check returned offline:", data);
            statusEl.textContent = '🔴 LM Studio Offline';
            statusEl.style.color = '#f44336';
            if (data.message) {
                statusEl.title = data.message; // Show error on hover
            }
        }
    } catch (e) {
        console.error("Health check error:", e);
        statusEl.textContent = '🔴 Backend Error';
        statusEl.style.color = '#f44336';
    }
}

async function loadModels() {
    try {
        const res = await fetch(`${API_BASE}/models`);
        const data = await res.json();
        const select = document.getElementById('model-select');
        const ab1 = document.getElementById('ab-model-1');
        const ab2 = document.getElementById('ab-model-2');
        
        [select, ab1, ab2].forEach(el => el.innerHTML = '');
        
        data.data.forEach(model => {
            const option = new Option(model.id, model.id);
            select.add(option.cloneNode(true));
            ab1.add(option.cloneNode(true));
            ab2.add(option.cloneNode(true));
        });
    } catch (e) {
        console.error('Failed to load models', e);
    }
}

function setupChat() {
    const sendBtn = document.getElementById('send-btn');
    const input = document.getElementById('chat-input');
    const history = document.getElementById('chat-history');
    const clearBtn = document.getElementById('clear-chat-btn');
    
    // Clear Chat
    clearBtn.addEventListener('click', () => {
        history.innerHTML = '';
    });

    // Update temp value display
    const tempSlider = document.getElementById('temp-slider');
    const tempValue = document.getElementById('temp-value');
    tempSlider.addEventListener('input', (e) => tempValue.textContent = e.target.value);
    
    let lastResponseId = null;

    sendBtn.addEventListener('click', async () => {
        const text = input.value.trim();
        if (!text) return;
        
        // Add user message
        appendMessage('user', text);
        input.value = '';
        
        const model = document.getElementById('model-select').value;
        const temp = parseFloat(tempSlider.value);
        const systemPrompt = document.getElementById('system-prompt').value.trim();
        const reasoningEffort = document.getElementById('reasoning-effort').value;
        
        // Build messages array (Legacy support)
        const messages = [];
        if (systemPrompt) {
            messages.push({role: 'system', content: systemPrompt});
        }
        messages.push({role: 'user', content: text});

        // Create assistant message placeholder
        const assistantMsgDiv = appendMessage('assistant', '...');
        
        try {
            // Prepare payload - prefer new API if reasoning is used or just default to it
            const payload = {
                model: model,
                temperature: temp,
                stream: true
            };

            // Use new API structure
            payload.input = text;
            if (lastResponseId) {
                payload.previous_response_id = lastResponseId;
            }
            if (reasoningEffort) {
                payload.reasoning_effort = reasoningEffort;
            }
            // Fallback for legacy endpoint if needed (backend handles it)
            payload.messages = messages;

            const res = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            // Handle Streaming
            const reader = res.body.getReader();
            const decoder = new TextDecoder();
            let fullText = '';
            assistantMsgDiv.innerHTML = ''; // Clear loading dots

            while (true) {
                const {done, value} = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');
                
                for (const line of lines) {
                    if (line.startsWith('event: ')) {
                        // Handle specific events if needed
                        const eventType = line.slice(7).trim();
                        // We might want to handle 'response.created' to get the ID
                    }
                    else if (line.startsWith('data: ')) {
                        try {
                            const rawData = line.slice(6);
                            // Check if it's a JSON object or raw string
                            let data;
                            try {
                                data = JSON.parse(rawData);
                            } catch {
                                data = rawData;
                            }

                            // Handle new API format
                            if (data.delta) {
                                // response.output_text.delta
                                fullText += data.delta;
                                assistantMsgDiv.innerHTML = marked.parse(fullText);
                            } 
                            else if (data.id) {
                                // response.created or completed
                                lastResponseId = data.id;
                            }
                            // Handle legacy format
                            else if (data.data) {
                                fullText += data.data;
                                assistantMsgDiv.innerHTML = marked.parse(fullText);
                            }
                            
                            history.scrollTop = history.scrollHeight;
                        } catch (e) {
                            console.error('Error parsing SSE chunk', e);
                        }
                    }
                }
            }
            
        } catch (e) {
            assistantMsgDiv.textContent = 'Error: ' + e.message;
        }
    });
}

function appendMessage(role, text) {
    const history = document.getElementById('chat-history');
    const div = document.createElement('div');
    div.className = `message ${role}-msg`;
    // Use innerHTML for assistant to support markdown, textContent for user for safety
    if (role === 'assistant') {
        div.innerHTML = marked.parse(text);
    } else {
        div.textContent = text;
    }
    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
    return div;
}

function setupABTest() {
    document.getElementById('run-ab-test-btn').addEventListener('click', async () => {
        const prompt = document.getElementById('ab-prompt').value;
        const m1 = document.getElementById('ab-model-1').value;
        const m2 = document.getElementById('ab-model-2').value;
        const resultsDiv = document.getElementById('ab-results');
        
        resultsDiv.innerHTML = 'Running tests...';
        
        const res = await fetch(`${API_BASE}/ab-test`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                prompt: prompt,
                models: [m1, m2]
            })
        });
        
        const data = await res.json();
        resultsDiv.innerHTML = '';
        
        data.results.forEach(r => {
            const card = document.createElement('div');
            card.className = 'ab-result-card';
            card.innerHTML = `<h3>${r.model}</h3><p>${r.response || r.error}</p>`;
            resultsDiv.appendChild(card);
        });
    });
}

function setupTools() {
    // Basic listing
    loadTools();
    
    document.getElementById('save-tool-btn').addEventListener('click', async () => {
        const tool = {
            name: document.getElementById('tool-name').value,
            description: document.getElementById('tool-desc').value,
            endpoint: document.getElementById('tool-endpoint').value,
            enabled: true
        };
        
        await fetch(`${API_BASE}/tools`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(tool)
        });
        loadTools();
    });
}

async function loadTools() {
    const res = await fetch(`${API_BASE}/tools`);
    const tools = await res.json();
    const list = document.getElementById('tools-list-ul');
    list.innerHTML = '';
    tools.forEach(t => {
        const li = document.createElement('li');
        li.textContent = t.name;
        list.appendChild(li);
    });
}

function setupTemplates() {
    // Similar to tools
}
