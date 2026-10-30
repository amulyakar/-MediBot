
async function askMediBot() {

    // Get the question entered by the user
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();

    // Get the website elements
    const askButton = document.getElementById("askButton");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const answer = document.getElementById("answer");
    const disclaimer = document.getElementById("disclaimer");
    const error = document.getElementById("error");

    // Check whether the user entered a question
    if (question.length < 3) {
        error.textContent = "Please enter a question with at least 3 characters.";
        error.classList.remove("hidden");
        result.classList.add("hidden");
        return;
    }

    // Show loading message
    loading.classList.remove("hidden");

    // Hide previous results and errors
    result.classList.add("hidden");
    error.classList.add("hidden");

    // Disable button while MediBot processes the question
    askButton.disabled = true;
    askButton.textContent = "Processing...";

    try {

        // Send the question to the FastAPI backend
        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        // Convert the response into JSON
        const data = await response.json();

        // Check whether the request was successful
        if (!response.ok) {
            throw new Error(
                data.detail || "Something went wrong. Please try again."
            );
        }

        // Display MediBot's answer
        answer.textContent = data.answer;

        // Display the medical disclaimer
        disclaimer.textContent = data.disclaimer;

        // Show the result section
        result.classList.remove("hidden");

    }

    catch (err) {

        // Display an error message
        error.textContent = "Error: " + err.message;

        error.classList.remove("hidden");

    }

    finally {

        // Hide loading message
        loading.classList.add("hidden");

        // Enable the button again
        askButton.disabled = false;
        askButton.textContent = "Ask MediBot";

    }

}
