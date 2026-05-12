const aeroColors = ["aero-red", "aero-blue", "aero-yellow", "aero-green"];

function buildGameUI(questionData) {
    appState.currentQuestionId = questionData.Question_ID;
    document.getElementById("question-text").innerText = questionData.Question_text;
    const container = document.getElementById("button-container");
    container.innerHTML = "";


    questionData.options.forEach((opt, index) => {
    const btn = createAnswerButton(opt, index);
    container.appendChild(btn);
    });

    startTimer(questionData.Time_limit || 15);
}

function createAnswerButton(opt, index) {
    const btn = document.createElement("button");

    const colorClass = aeroColors[index % aeroColors.length];

    btn.className = `vote-option ${colorClass}`;
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

let countdownInterval;

function startTimer(seconds) {
    let timeLeft = seconds;
    document.getElementById("time-left").innerText = timeLeft;
    document.getElementById("timer-display").style.display = "block";
    document.getElementById("results-chart").style.display = "none"; // Hide graph initially

    clearInterval(countdownInterval); // Clear any old timers
    countdownInterval = setInterval(() => {
        timeLeft--;
        document.getElementById("time-left").innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            document.getElementById("game-screen").classList.remove("active")
            document.getElementById("result-screen").classList.add("active");
            showResultsGraph(); 
        }
    }, 1000); // Runs every 1000 milliseconds (1 second)
}

let myChart = null; // Global variable to store the chart instance

function renderChart(labels, votes) {
    const canvas = document.getElementById("results-chart");
    if (!canvas) {
        console.error("Could not find canvas with ID 'results-chart'");
        return;
    }
    
    canvas.style.display = "block";

    // 1. IMPORTANT: Destroy the old chart if it exists
    if (myChart) {
        myChart.destroy();
    }

    // 2. Create the new chart
    myChart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: votes,
                backgroundColor: ['#e21b3c', '#1368ce', '#ffa602', '#26890c']
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 1 } }
            }
        }
    });
}

async function showResultsGraph() {
    document.getElementById("timer-display").style.display = "none"; // Hide "Time Left"
    const container = document.getElementById("button-container");
    if(container) container.style.display = "none";
    
    // Ensure we are using the correct API URL and State
    const url = `${API_URL}/${appState.dbType}/sessions/${appState.session_id}/questions/${appState.currentQuestionId}/stats`;
    
    try {
        const response = await fetch(url);
        const stats = await response.json();

        // Map the database response to Chart.js format
        const labels = stats.map(s => s.Option_text);
        const votes = stats.map(s => s.VoteCount);

        renderChart(labels, votes); 
    } catch (err) {
        console.error("Failed to fetch stats:", err);
    }
}