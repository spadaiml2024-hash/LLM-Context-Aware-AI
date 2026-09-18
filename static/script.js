async function analyzeText() {

const textBox = document.getElementById("userText");
const chatBox = document.getElementById("chatBox");

const text = textBox.value.trim();

if (text === "") {
    return;
}

// Show user's message
const userMessage = document.createElement("div");

userMessage.className = "user-message";
userMessage.innerText = text;

chatBox.appendChild(userMessage);

// Clear textbox
textBox.value = "";

// Show loading message
const aiMessage = document.createElement("div");

aiMessage.className = "ai-message loading";
aiMessage.innerText = "AI is thinking...";

chatBox.appendChild(aiMessage);

try {

    const response = await fetch("/analyze", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            text: text
        })
    });

    const data = await response.json();

    // Remove loading animation
    aiMessage.classList.remove("loading");

    // Show AI response
    aiMessage.innerText = data.result;

    // Update memory
    updateMemory(data.memory);

} catch (error) {

    aiMessage.classList.remove("loading");

    aiMessage.innerText =
        "Unable to connect to the AI server.";
}

// Scroll to latest message
chatBox.scrollTop = chatBox.scrollHeight;

}

// Update Memory Panel
function updateMemory(memory) {

const memoryText = document.getElementById("memoryText");

let content = "";

if (memory.name) {
    content += `👤 Name: ${memory.name}<br>`;
}

if (memory.learning_topic) {
    content += `📚 Learning: ${memory.learning_topic}<br>`;
}

if (memory.favorite_subject) {
    content += `⭐ Favorite Subject: ${memory.favorite_subject}<br>`;
}

if (memory.career_goal) {
    content += `🎯 Career Goal: ${memory.career_goal}<br>`;
}

if (memory.skill) {
    content += `💻 Skill: ${memory.skill}<br>`;
}

if (content === "") {
    content = "No information remembered yet.";
}

memoryText.innerHTML = content;

}

// Clear Memory
async function clearMemory() {

try {

    const response = await fetch("/clear-memory", {
        method: "POST"
    });

    const data = await response.json();

    // Clear chat
    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = "";

    // Clear memory
    const memoryText = document.getElementById("memoryText");

    memoryText.innerText =
        "No information remembered yet.";

    // Show confirmation
    const message = document.createElement("div");

    message.className = "ai-message";
    message.innerText = data.result;

    chatBox.appendChild(message);

} catch (error) {

    alert("Unable to clear memory.");
}

}

// Dark Mode
function toggleDarkMode() {

document.body.classList.toggle("dark-mode");

}

// Download Chat History
function downloadChat() {

const chatBox = document.getElementById("chatBox");

const chatText = chatBox.innerText;

if (chatText.trim() === "") {

    alert("No chat history to download.");

    return;
}

const file = new Blob(
    [chatText],
    { type: "text/plain" }
);

const link = document.createElement("a");

link.href = URL.createObjectURL(file);

link.download = "context-aware-ai-chat.txt";

link.click();

URL.revokeObjectURL(link.href);

}

// Enter key to send
document.getElementById("userText").addEventListener("keydown", function(event) {

if (event.key === "Enter" && !event.shiftKey) {

    event.preventDefault();

    analyzeText();
}

});