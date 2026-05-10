// TASK 14: Client Authentication Logic
const API_URL = "http://localhost:8080";
let appState = { dbType: 'a', session_id: null, quiz_id: null, user_name: "", user_id: 3, currentQuestion: null };

async function joinGame() {
    const pin = document.getElementById("pin-input").value;
    appState.user_name = document.getElementById("name-input").value;
    
    // Auto-route: Even PINs go to 'a', Odd PINs go to 'b'
    appState.dbType = (parseInt(pin) % 2 === 0) ? 'a' : 'b';

    try {
        const sessionRes = await fetch(`${API_URL}/${appState.dbType}/sessions/pin/${pin}`);
        if (!sessionRes.ok) throw new Error("Game not found");
        const sessionData = await sessionRes.json();
        
        appState.session_id = sessionData.Session_ID;
        appState.quiz_id = sessionData.Quiz_ID;

        // Fetch the quiz questions
        const quizRes = await fetch(`${API_URL}/${appState.dbType}/quizzes/${appState.quiz_id}/full`);
        const questions = await quizRes.json();
        appState.currentQuestion = questions[0]; // Just load the first question for now

        buildGameUI(appState.currentQuestion);
        
        document.getElementById("login-screen").classList.remove("active");
        document.getElementById("game-screen").classList.add("active");
    } catch (err) {
        document.getElementById("error-msg").style.display = "block";
    }
}