document.getElementById("translate-btn").addEventListener("click", async () => {
    const inputText = document.getElementById("input-text").value;
    const fileInput = document.getElementById("file-upload").files[0];

    let formData = new FormData();
    if (fileInput) {
        formData.append("file", fileInput);
    } else {
        formData.append("text", inputText);
    }

    const response = await fetch("/translate", {
        method: "POST",
        body: formData,
    });

    const data = await response.json();

    if (data.file_content) {
        // Display uploaded file content in the input text area
        document.getElementById("input-text").value = data.file_content;
    } else if (data.translated) {
        // Display translated text in the output text area
        document.getElementById("output-text").value = data.translated;
    } else {
        alert(data.error || "An error occurred.");
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
    } catch (error) {
        console.error("Failed to copy text:", error);
        alert("Failed to copy text. Please copy manually.");
    }
});
