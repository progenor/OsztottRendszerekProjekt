// TASK 12: Form Result Handling
async function submitVote(option_id) {
    const payload = {
        session_id: appState.session_id,
        user_id: appState.user_id, // Hardcoded player ID from seed.sql for demo
        question_id: appState.currentQuestion.Question_ID,
        option_id: option_id,
        user_name: appState.user_name
    };

    await fetch(`${API_URL}/${appState.dbType}/vote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    document.getElementById("game-screen").classList.remove("active");
    document.getElementById("result-screen").classList.add("active");
}