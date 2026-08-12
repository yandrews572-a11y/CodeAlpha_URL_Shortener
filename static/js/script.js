const form = document.getElementById("shortenForm");

const urlInput = document.getElementById("url");
const aliasInput = document.getElementById("customAlias");
const expiryInput = document.getElementById("expiry");

const resultBox = document.getElementById("result");
const shortLink = document.getElementById("shortLink");

const errorBox = document.getElementById("error");
const loading = document.getElementById("loading");

const copyButton = document.getElementById("copyButton");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Clear previous messages
    errorBox.style.display = "none";
    resultBox.style.display = "none";

    const url = urlInput.value.trim();
    const customAlias = aliasInput.value.trim();
    const expiry = expiryInput.value.trim();

    // Basic URL validation
    if (!url) {
        showError("Please enter a URL.");
        return;
    }

    try {
        new URL(url);
    } catch {
        showError("Please enter a valid URL.");
        return;
    }

    // Show loading
    loading.style.display = "block";

    // Request data
    const data = {
        url: url
    };

    if (customAlias) {
        data.custom_alias = customAlias;
    }

    if (expiry) {
        data.expires_in_days = Number(expiry);
    }

    try {

        const response = await fetch("/shorten", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        });

        const result = await response.json();

        loading.style.display = "none";

        if (!response.ok) {
            showError(result.error || "Something went wrong.");
            return;
        }

        // Display short URL
        shortLink.href = result.short_url;
        shortLink.textContent = result.short_url;

        resultBox.style.display = "block";

        // Clear form
        urlInput.value = "";

    } catch (error) {

        loading.style.display = "none";

        showError(
            "Unable to connect to server. Make sure Flask is running."
        );

        console.error(error);
    }
});


/* Copy short URL */
copyButton.addEventListener("click", async function () {

    const link = shortLink.textContent;

    try {

        await navigator.clipboard.writeText(link);

        copyButton.textContent = "Copied!";

        setTimeout(() => {
            copyButton.textContent = "Copy";
        }, 1500);

    } catch {

        showError("Unable to copy the link.");
    }
});


/* Error message */
function showError(message) {

    errorBox.textContent = message;

    errorBox.style.display = "block";
}