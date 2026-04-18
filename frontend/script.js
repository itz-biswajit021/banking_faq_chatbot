const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const input = document.getElementById("messageInput");
const chatBox = document.getElementById("chat-box");
const clearBtn = document.getElementById("clearBtn");

// Toggle for audio icon
let audioIconEnabled = true; // Change to false to disable by default

// Create chat bubble
function addMessage(msg, sender = "bot", animate = false) {
  const wrapper = document.createElement("div");
  wrapper.className = `message-wrapper ${sender}`;

  // Avatar
  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = sender === "user" ? "assets/OIP.jpeg" : "assets/bot.png";
  wrapper.appendChild(avatar);

  // Message bubble
  const bubble = document.createElement("div");
  bubble.className = "message";
  wrapper.appendChild(bubble);

  if (animate) {
    typeWriterEffect(bubble, msg, () => {
      if (sender === "bot" && audioIconEnabled) showAudioIcon(wrapper, msg);
    });
  } else {
    bubble.innerText = msg;
    if (sender === "bot" && audioIconEnabled) showAudioIcon(wrapper, msg);
  }

  chatBox.appendChild(wrapper);

  anime({
    targets: bubble,
    opacity: [0, 1],
    translateY: [10, 0],
    duration: 400,
    easing: "easeOutQuad"
  });

  chatBox.scrollTop = chatBox.scrollHeight;
}

// Show audio icon after typing is done
function showAudioIcon(wrapper, msg) {
  const ttsBtn = document.createElement("img");
  ttsBtn.src = "assets/audio-svgrepo-com (1).svg";
  ttsBtn.className = "audio-icon";
  ttsBtn.title = "Play message";
  ttsBtn.style.opacity = "0";
  ttsBtn.style.transform = "translateX(-10px)";

  ttsBtn.addEventListener("click", () => {
    const utterance = new SpeechSynthesisUtterance(msg);
    utterance.rate = 0.9;
    utterance.lang = "en-IN";
    speechSynthesis.speak(utterance);
  });

  wrapper.appendChild(ttsBtn);

  // Play pop sound
  const popSound = new Audio("assets/pop.mp3"); // Add pop.mp3 to assets folder
  popSound.volume = 0.4;

  // Slide in animation + pop sound
  setTimeout(() => {
    popSound.play();
    ttsBtn.style.transition = "all 0.3s ease";
    ttsBtn.style.opacity = "1";
    ttsBtn.style.transform = "translateX(0)";
  }, 100);
}

// Typewriter effect with callback
function typeWriterEffect(element, text, onComplete, delay = 30) {
  let index = 0;
  element.innerHTML = "";
  function type() {
    if (index < text.length) {
      element.innerHTML += text.charAt(index);
      index++;
      setTimeout(type, delay);
    } else if (onComplete) {
      onComplete();
    }
  }
  type();
}

// Typing indicator
function addTypingIndicator() {
  const typingWrapper = document.createElement("div");
  typingWrapper.className = "message-wrapper bot typing";

  const avatar = document.createElement("img");
  avatar.className = "avatar";
  avatar.src = "assets/bot.png";

  const bubble = document.createElement("div");
  bubble.className = "message typing-bubble";
  bubble.innerHTML = `<span></span><span></span><span></span>`;

  typingWrapper.appendChild(avatar);
  typingWrapper.appendChild(bubble);
  chatBox.appendChild(typingWrapper);
  chatBox.scrollTop = chatBox.scrollHeight;

  return typingWrapper;
}

// Send message
sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
clearBtn.addEventListener("click", () => {
  chatBox.innerHTML = "";
});

// Toggle button for TTS
document.getElementById("toggleTTS")?.addEventListener("click", () => {
  audioIconEnabled = !audioIconEnabled;
  alert(`Audio icon is now ${audioIconEnabled ? "enabled" : "disabled"}.`);
});

function sendMessage() {
  const msg = input.value.trim();
  if (!msg) return;

  addMessage(msg, "user");
  input.value = "";

  const typingIndicator = addTypingIndicator();

  fetch("http://127.0.0.1:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  })
    .then(res => res.json())
    .then(data => {
      setTimeout(() => {
        typingIndicator.remove();
        addMessage(data.reply, "bot", true);
        showSuggestions(data.intent);   // 👈 new line
      }, 1000);
    })
    .catch(err => {
      typingIndicator.remove();
      addMessage("Sorry, something went wrong.", "bot");
      console.error(err);
    });
}

// Voice input
micBtn.addEventListener("click", () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-IN";
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    input.value = event.results[0][0].transcript;
  };

  recognition.start();
});


// Suggested follow-up messages based on intent
const suggestionsByIntent = {
  security: [
    "How to reset my password?",
    "What if my card is stolen?"
  ],
  accounts: [
    "How to check my balance?",
    "How to get my account statement?"
  ],
  loans: [
    "What is the interest rate on personal loan?",
    "How can I prepay my loan?"
  ],
  fundstransfer: [
    "What is NEFT?",
    "What is RTGS transfer?"
  ],
  // default suggestions if intent not mapped
  _default: [
    "Tell me about account opening",
    "I want to know about credit cards"
  ]
};


function showSuggestions(intent) {
  // Remove old suggestions if any
  const old = document.querySelector(".suggestions-row");
  if (old) old.remove();

  // Pick suggestions list for this intent
  const suggestions =
    suggestionsByIntent[intent] || suggestionsByIntent._default;

  if (!suggestions || suggestions.length === 0) return;

  // Create a container
  const row = document.createElement("div");
  row.className = "suggestions-row";

  suggestions.forEach(text => {
    const chip = document.createElement("button");
    chip.className = "suggestion-chip";
    chip.innerText = text;

    chip.addEventListener("click", () => {
      // When user clicks, send this text as next message
      input.value = text;
      sendMessage();  // reuses existing sendMessage()
    });

    row.appendChild(chip);
  });

  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
}
