document.getElementById('inputText').addEventListener('input', () => {
    const inputText = document.getElementById('inputText');
    const inputLineNumbers = document.getElementById('inputLineNumbers');
    updateLineNumbers(inputText.value, inputLineNumbers);
});

document.getElementById('convertButton').addEventListener('click', async () => {
    const inputText = document.getElementById('inputText').value;
    const logList = document.getElementById('logList');
    const outputLineNumbers = document.getElementById('outputLineNumbers');
    const outputTextElement = document.getElementById('outputText');

    logList.innerHTML = ''; // Clear previous log entries

    // Fetch and parse the rules from rules.txt
    const response = await fetch('rules.txt');
    const rulesText = await response.text();
    const rules = parseRules(rulesText);

    let convertedText = inputText;

    // Apply replacements
    rules.forEach(({ name, find, replace }) => {
        const matches = [...convertedText.matchAll(find)];
        if (matches.length > 0) {
            matches.forEach(match => {
                // Add to log with line number and rule name
                const logItem = document.createElement('li');
                logItem.textContent = `Rule "${name}": Replaced "${match[0]}" with "${replace}"`;
                logList.appendChild(logItem);
            });
        }
        // Replace text in the entire input
        convertedText = convertedText.replace(find, replace);
    });

    // Update the output text and line numbers
    outputTextElement.value = convertedText;
});

function parseRules(rulesText) {
    const rules = [];
    const ruleBlocks = rulesText.split('[NEW_RULE]');
    ruleBlocks.forEach(block => {
        const parts = block.split('[SEPARATOR]');
        if (parts.length >= 3) {
            const name = parts[0].trim();
            const pattern = parts[1].trim().slice(1, -2);
            const flags = parts[1].trim().slice(-1);
            const find = new RegExp(pattern, flags.includes('g') ? flags : flags + 'g'); // Ensure 'g' flag is included
            const replace = parts[2].trim();
            rules.push({ name, find, replace });
        }
    });
    return rules;
}