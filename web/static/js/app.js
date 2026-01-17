const cnfInput = document.querySelector('#cnfInput');
const outputPanel = document.querySelector('#output');
const statusChip = document.querySelector('#statusChip');
const generateBtn = document.querySelector('#generateBtn');
const solveBtn = document.querySelector('#solveBtn');

const sampleCNF = `c Example 3-SAT
p cnf 3 3
1 -2 0
2 3 0
3 -1 0

excpected output:
SAT: 001
`;

function parseIntOrNull(value) {
    const trimmed = String(value ?? '').trim();
    if (!trimmed) return null;
    const num = parseInt(trimmed, 10);
    return Number.isNaN(num) ? null : num;
}

function collectOptions() {
    return {
        num_vars: parseIntOrNull(document.querySelector('#vars').value) ?? 50,
        num_clauses: parseIntOrNull(document.querySelector('#clauses').value) ?? 200,
        min_clause_length: parseIntOrNull(document.querySelector('#minClause').value) ?? 2,
        max_clause_length: parseIntOrNull(document.querySelector('#maxClause').value) ?? 4,
        seed: parseIntOrNull(document.querySelector('#seed').value),
    };
}

function setStatus(text, tone = 'neutral') {
    statusChip.textContent = text;
    statusChip.dataset.tone = tone;
}

async function generateFormula() {
    const options = collectOptions();

    setStatus('Generating…', 'working');
    generateBtn.disabled = true;

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ options }),
        });
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || 'Generation failed');
        }

        cnfInput.value = data.cnf;
        setStatus('Generated', 'success');
    } catch (err) {
        console.error(err);
        setStatus(err.message, 'error');
    } finally {
        generateBtn.disabled = false;
    }
}

async function solveFormula() {
    const cnf = cnfInput.value.trim();
    if (!cnf) {
        setStatus('Add or generate a formula first', 'error');
        return;
    }

    setStatus('Solving…', 'working');
    solveBtn.disabled = true;
    outputPanel.textContent = 'Running tinydpll…';

    try {
        const res = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cnf }),
        });
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || 'Solver failed');
        }

        const lines = [];
        if (typeof data.output === 'string' && data.output.trim()) {
            lines.push(data.output.trim());
        }
        if (typeof data.error === 'string' && data.error.trim()) {
            lines.push('stderr:\n' + data.error.trim());
        }
        outputPanel.textContent = lines.join('\n\n') || 'No output received.';
        setStatus('Solved', 'success');
    } catch (err) {
        console.error(err);
        outputPanel.textContent = err.message;
        setStatus(err.message, 'error');
    } finally {
        solveBtn.disabled = false;
    }
}

function attachEvents() {
    document.querySelector('#fillSample').addEventListener('click', () => {
        cnfInput.value = sampleCNF;
        setStatus('Loaded sample', 'neutral');
    });
    generateBtn.addEventListener('click', generateFormula);
    solveBtn.addEventListener('click', solveFormula);
}

function init() {
    attachEvents();
    setStatus('Ready');
}

init();


async function solveFormula() {
    const cnf = cnfInput.value.trim();
    if (!cnf) {
        setStatus('Add or generate a formula first', 'error');
        return;
    }

    setStatus('Solving…', 'working');
    solveBtn.disabled = true;
    outputPanel.textContent = 'Running tinydpll…';

    try {
        const res = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cnf }),
        });
        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || 'Solver failed');
        }

        const lines = [];
        if (typeof data.output === 'string' && data.output.trim()) {
            lines.push(data.output.trim());
        }
        if (typeof data.error === 'string' && data.error.trim()) {
            lines.push('stderr:\n' + data.error.trim());
        }
        outputPanel.textContent = lines.join('\n\n') || 'No output received.';
        setStatus('Solved', 'success');
    } catch (err) {
        console.error(err);
        outputPanel.textContent = err.message;
        setStatus(err.message, 'error');
    } finally {
        solveBtn.disabled = false;
    }
}

function attachEvents() {
    document.querySelector('#fillSample').addEventListener('click', () => {
        cnfInput.value = sampleCNF;
        setStatus('Loaded sample', 'neutral');
    });
    generateBtn.addEventListener('click', generateFormula);
    solveBtn.addEventListener('click', solveFormula);
}

function init() {
    attachEvents();
    setStatus('Ready');
}

init();
