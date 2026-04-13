let questions = [];
let currentIndex = 0;



async function loadQuestions() {
  try {
    const response = await fetch('./data/benchmark_answers_complete.json');
    const data = await response.json();

    questions = data;

    console.log("Questions loaded:", questions);
    console.log("First question:", questions[0]);

    renderQuestion();

  } catch (error) {
    console.error("Error loading questions:", error);
  }
}

function renderQuestion() {
  if (questions.length === 0) return;

  const current = questions[currentIndex];

  document.getElementById("question-box").textContent = current.question;
  document.getElementById("rlm-answer").textContent = current.RLM_answer;
  document.getElementById("rag-answer").textContent = current.intouch_answer;
}

document.getElementById("next-btn").addEventListener("click", () => {
  if (currentIndex < questions.length - 1) {
    currentIndex++;
    renderQuestion();
  } else {
    alert("No more questions");
  }
});

loadQuestions(); 