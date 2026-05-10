function buildGameUI(questionData) {
    document.getElementById("question-text").innerText = questionData.Question_text;
    const container = document.getElementById("button-container");
    container.innerHTML = "";

    questionData.options.forEach((opt, index) => {
    const btn = createAnswerButton(opt, index);
    container.appendChild(btn);
    });
}

function createAnswerButton(opt, index) {
    const btn = document.createElement("button");

    btn.className = `kahoot-btn btn-${index % 4}`;
    btn.innerText = opt.Option_text;

    btn.onclick = () => submitVote(opt.Option_ID);

    addButtonEffects(btn);

    return btn;
}
function addButtonEffects(btn) {
    btn.addEventListener("click", () => {
        btn.style.opacity = "0.7";
    });
}