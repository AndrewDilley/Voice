document.getElementById("translate-btn").addEventListener("click", async () => {
    const inputText = document.getElementById("input-text").value;

    if (!inputText.trim()) {
        alert("Please enter some text to translate.");
        return;
    }

    let formData = new FormData();
    formData.append("text", inputText);

    try {
        const response = await fetch("/translate", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (data.translated) {
            document.getElementById("output-text").value = data.translated;
        } else {
            alert(data.error || "An error occurred.");
        }
    } catch (error) {
        console.error("Error translating text:", error);
        alert("Failed to communicate with the server.");
    }
});

document.getElementById("copy-btn").addEventListener("click", async () => {
    const outputText = document.getElementById("output-text").value;

    if (outputText.trim() === "") {
        alert("There's no text to copy!");
        return;
    }

    try {
        await navigator.clipboard.writeText(outputText);
        alert("Text copied to clipboard!");
    } catch (error) {
        console.error("Failed to copy text:", error);
        alert("Failed to copy text. Please copy manually.");
    }
});
