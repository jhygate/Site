function updateLineNumbers(text, lineNumbersElement) {
    const lines = text.split('\n');
    const lineNumberContent = lines.map((_, index) => `${index + 1}`).join('\n');
    lineNumbersElement.textContent = lineNumberContent;
}

document.getElementById('inputText').addEventListener('input', () => {
    const inputText = document.getElementById('inputText');
    const inputLineNumbers = document.getElementById('inputLineNumbers');
    updateLineNumbers(inputText.value, inputLineNumbers);
});

document.getElementById('convertButton').addEventListener('click', () => {
    const inputText = document.getElementById('inputText').value;
    const logList = document.getElementById('logList');
    const outputLineNumbers = document.getElementById('outputLineNumbers');
    const outputTextElement = document.getElementById('outputText');

    logList.innerHTML = ''; // Clear previous log entries

    // Define regex replacements
    const replacements = [
        { find: /foo/g, replace: 'bar' }, // Example: replace 'foo' with 'bar'
        { find: /hello/g, replace: 'hi' }, // Example: replace 'hello' with 'hi'
        { find: /\.((-|—)+)/g, replace: "." },
        // Add more replacements here
    ];

    let convertedText = inputText;
    const lines = inputText.split('\n'); // Split input into lines

    // Apply replacements line by line
    const outputLines = lines.map((line, index) => {
        let updatedLine = line;

        replacements.forEach(({ find, replace }) => {
            const matches = [...updatedLine.matchAll(find)];
            if (matches.length > 0) {
                matches.forEach(match => {
                    // Add to log with line number
                    const logItem = document.createElement('li');
                    logItem.textContent = `Line ${index + 1}: Replaced "${match[0]}" with "${replace}"`;
                    logList.appendChild(logItem);
                });
            }
            // Replace text in the current line
            updatedLine = updatedLine.replace(find, replace);
        });

        return updatedLine;
    });

    // Update the output text and line numbers
    const outputText = outputLines.join('\n');
    outputTextElement.value = outputText;
    updateLineNumbers(outputText, outputLineNumbers);
});
