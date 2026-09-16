let focusInterval;
let focusSeconds = 0;

// Elements
const stateIcon = document.getElementById('state-icon');
const stateName = document.getElementById('state-name');
const focusScore = document.getElementById('focus-score');
const currentActivity = document.getElementById('current-activity');
const focusDurationEl = document.getElementById('focus-duration');
const decisionFeed = document.getElementById('decision-feed');
const learningList = document.getElementById('learning-list');

// Init
async function init() {
    await fetchState();
    await fetchLearning();
    startTimer();
}

// Fetch current state from backend
async function fetchState() {
    try {
        const res = await fetch('/api/state');
        const data = await res.json();
        updateDashboard(data);
    } catch (e) {
        console.error("Failed to fetch state", e);
    }
}

// Fetch learning preferences
async function fetchLearning() {
    try {
        const res = await fetch('/api/learning');
        const data = await res.json();
        updateLearningUI(data);
    } catch (e) {
        console.error("Failed to fetch learning", e);
    }
}

function updateDashboard(data) {
    stateName.textContent = data.state.name;
    focusScore.textContent = `Focus Threshold: ${data.state.threshold}%`;
    
    // Update icon color based on state
    if (data.state.name.includes('🟢')) stateIcon.textContent = '🟢';
    else if (data.state.name.includes('🟡')) stateIcon.textContent = '🟡';
    else if (data.state.name.includes('🔴')) stateIcon.textContent = '🔴';
    else if (data.state.name.includes('🟣')) stateIcon.textContent = '🟣';

    focusSeconds = Math.floor(data.duration_mins * 60);
    updateTimerDisplay();
}

function updateLearningUI(data) {
    learningList.innerHTML = '';
    const keys = Object.keys(data);
    
    if (keys.length === 0) {
        learningList.innerHTML = `
            <div class="learning-item">
                <span class="learning-desc">No preferences learned yet. Simulate overrides to train the agent.</span>
            </div>
        `;
        return;
    }
    
    for (const key of keys) {
        const [source, sender] = key.split('::');
        const score = data[key];
        let action = score > 0 ? "Usually allowed" : "Usually blocked";
        let color = score > 0 ? "var(--color-available)" : "var(--color-deep)";
        
        learningList.innerHTML += `
            <div class="learning-item">
                <span class="learning-rule">${source} from ${sender}</span>
                <span class="learning-desc" style="color: ${color}">Preference Score: ${score > 0 ? '+' : ''}${score} (${action})</span>
            </div>
        `;
    }
}

// Timer
function startTimer() {
    clearInterval(focusInterval);
    focusInterval = setInterval(() => {
        focusSeconds++;
        updateTimerDisplay();
        if (focusSeconds % 60 === 0) {
            fetchState(); // refresh state every minute
        }
    }, 1000);
}

function updateTimerDisplay() {
    const h = String(Math.floor(focusSeconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((focusSeconds % 3600) / 60)).padStart(2, '0');
    const s = String(focusSeconds % 60).padStart(2, '0');
    focusDurationEl.textContent = `${h}:${m}:${s}`;
}

// Controls
document.getElementById('btn-start-focus').addEventListener('click', async () => {
    await fetch('/api/set_state', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ override: 'DEEP_FOCUS', reset_timer: false })
    });
    fetchState();
});

document.getElementById('btn-reset-state').addEventListener('click', async () => {
    await fetch('/api/set_state', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ override: 'AVAILABLE', reset_timer: true })
    });
    fetchState();
});

document.getElementById('btn-reset-learning').addEventListener('click', async () => {
    await fetch('/api/reset_learning', { method: 'POST' });
    fetchLearning();
});

// Simulate Events
const SCENARIOS = {
    instagram: {
        source: 'instagram',
        sender_name: 'Random User',
        sender_type: 'unknown',
        content: 'Liked your photo',
        icon: '<i class="fa-brands fa-instagram"></i>'
    },
    whatsapp: {
        source: 'whatsapp',
        sender_name: 'Project Group',
        sender_type: 'project_group',
        content: 'Meeting link is ready',
        icon: '<i class="fa-brands fa-whatsapp"></i>'
    },
    calendar: {
        source: 'calendar',
        sender_name: 'System',
        sender_type: 'system',
        content: 'Team Meeting in 10 mins',
        icon: '<i class="fa-regular fa-calendar"></i>'
    },
    emergency: {
        source: 'phone_call',
        sender_name: 'Mom',
        sender_type: 'family',
        content: 'Emergency',
        icon: '<i class="fa-solid fa-phone"></i>'
    }
};

async function simulateEvent(type) {
    const scenario = SCENARIOS[type];
    
    const res = await fetch('/api/event', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(scenario)
    });
    
    const data = await res.json();
    addFeedItem(scenario, data);
}

function addFeedItem(scenario, result) {
    const item = document.createElement('div');
    const decisionClass = result.decision.toLowerCase();
    item.className = `feed-item ${decisionClass}`;
    
    let actionsHtml = '';
    if (result.decision === 'BLOCK' || result.decision === 'DELAY') {
        actionsHtml = `<button class="btn-small" onclick="overrideDecision('${scenario.source}', '${scenario.sender_name}', 'ALLOW', '${result.decision}')">Override: Allow</button>`;
    } else if (result.decision === 'ALLOW') {
        actionsHtml = `<button class="btn-small" onclick="overrideDecision('${scenario.source}', '${scenario.sender_name}', 'DISMISS', '${result.decision}')">Override: Block/Dismiss</button>`;
    }

    item.innerHTML = `
        <div class="feed-header">
            <span class="feed-title">${scenario.icon} ${scenario.source} — ${scenario.sender_name}</span>
            <span class="feed-decision">${result.decision}</span>
        </div>
        <span class="feed-importance">Importance: ${result.importance_score}/100 (Threshold: ${result.threshold})</span>
        <span class="feed-desc">"${scenario.content}"</span>
        <div class="feed-actions">
            ${actionsHtml}
        </div>
    `;
    
    decisionFeed.prepend(item);
}

async function overrideDecision(source, senderName, userAction, agentDecision) {
    await fetch('/api/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            source: source,
            sender_name: senderName,
            user_action: userAction,
            agent_decision: agentDecision
        })
    });
    fetchLearning();
}

// Start
init();
