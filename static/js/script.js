document.getElementById("translate-btn").addEventListener("click", async () => {
    const inputText = document.getElementById("input-text").value;
    const spinner = document.getElementById("loading-spinner");
    const outputText = document.getElementById("output-text");

    if (!inputText.trim()) {
        alert("Please enter some text to translate.");
        return;
    }

    let formData = new FormData();
    formData.append("text", inputText);

    // Show spinner
    spinner.style.display = "block";
    outputText.value = ""; // Clear previous output

    try {
        const response = await fetch("/translate", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (data.translated) {
            outputText.value = data.translated;
        } else {
            alert(data.error || "An error occurred.");
        }
    } catch (error) {
        console.error("Error translating text:", error);
        alert("Failed to communicate with the server.");
    } finally {
        // Hide spinner after request is complete
        spinner.style.display = "none";
    }
});

