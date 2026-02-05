/**
 * Quiz view module
 * Handles the question display and answer submission
 */

import { state } from '../state.js';
import { submitAnswer, fetchNextQuestion } from '../api.js';
import { showResult } from './results.js';

const setupView = document.getElementById('setup-view');
const quizView = document.getElementById('quiz-view');
const questionText = document.getElementById('question-text');
const answerInput = document.getElementById('answer-input');
const questionCounter = document.getElementById('question-counter');
const selectedCategoriesDisplay = document.getElementById('selected-categories-display');
const submitBtn = document.getElementById('submit-btn');
const questionContainer = document.getElementById('question-container');
const resultContainer = document.getElementById('result-container');

/**
 * Display the quiz interface with current question
 */
export function showQuiz() {
  setupView.classList.add('hidden');
  quizView.classList.remove('hidden');
  
  // Reset UI for new question
  resultContainer.classList.add('hidden');
  resultContainer.innerHTML = '';
  questionContainer.classList.remove('hidden');
  submitBtn.textContent = 'Submit Answer (Enter)';
  
  questionText.textContent = state.currentQuestion.text;
  questionCounter.textContent = `Question ${state.questionNumber}`;
  selectedCategoriesDisplay.textContent = state.selectedCategories.join(', ');
  answerInput.value = '';
  answerInput.focus();
}

/**
 * Handle answer submission
 */
async function handleSubmit() {
  if (state.showingResult) {
    // Get next question
    try {
      const data = await fetchNextQuestion(state.selectedCategories);
      
      if (data.complete) {
        alert('Quiz complete! Great job!');
        import('./setup.js').then(({ resetSetup }) => resetSetup());
        return;
      }
      
      state.setQuestion(data.question);
      showQuiz();
    } catch (error) {
      console.error('Error fetching question:', error);
      alert('Failed to load next question. Please try again.');
    }
    return;
  }

  const answer = answerInput.value.trim();
  
  if (!answer) {
    alert('Please enter an answer');
    return;
  }

  try {
    const data = await submitAnswer(
      state.currentQuestion.category,
      state.currentQuestion.seed,
      answer
    );
    
    state.markShowingResult();
    showResult(data);
  } catch (error) {
    console.error('Error submitting answer:', error);
    alert('Failed to submit answer. Please try again.');
  }
}

/**
 * Initialize the quiz view
 */
export function initQuiz() {
  submitBtn.addEventListener('click', handleSubmit);
  
  // Enter key handler for quiz view
  document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !setupView.classList.contains('hidden')) {
      return;
    }
    if (e.key === 'Enter' && !quizView.classList.contains('hidden')) {
      handleSubmit();
    }
  });
}
