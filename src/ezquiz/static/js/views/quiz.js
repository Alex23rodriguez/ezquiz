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
const contextContainer = document.getElementById('context-container');
const questionContext = document.getElementById('question-context');

/**
 * Display the quiz interface with current question
 * Supports both "simple" and "fill" question types
 */
export function showQuiz() {
  setupView.classList.add('hidden');
  quizView.classList.remove('hidden');
  
  // Reset UI for new question
  resultContainer.classList.add('hidden');
  resultContainer.innerHTML = '';
  questionContainer.classList.remove('hidden');
  submitBtn.textContent = 'Submit Answer (Enter)';
  
  questionCounter.textContent = `Question ${state.questionNumber}`;
  selectedCategoriesDisplay.textContent = state.selectedCategories.join(', ');
  
  const question = state.currentQuestion;
  
  // Display context if present
  if (question.context) {
    questionContext.textContent = question.context;
    contextContainer.classList.remove('hidden');
  } else {
    contextContainer.classList.add('hidden');
    questionContext.textContent = '';
  }
  
  if (question.type === 'fill') {
    renderFillQuestion(question);
  } else {
    renderSimpleQuestion(question);
  }
}

/**
 * Render a simple question with text and input field below
 * @param {Object} question - Question object with text
 */
function renderSimpleQuestion(question) {
  questionContainer.innerHTML = `
    <p id="question-text" class="text-xl text-gray-800 dark:text-gray-100 mb-4">${escapeHtml(question.text)}</p>
    <input type="text" id="answer-input" 
           class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-gray-100 dark:placeholder-gray-400"
           placeholder="Your answer...">
  `;
  
  const input = document.getElementById('answer-input');
  if (input) {
    input.focus();
  }
}

/**
 * Render a fill-in-the-blank question with inline input
 * @param {Object} question - Question object with text containing [...]
 */
function renderFillQuestion(question) {
  const parts = question.text.split('[...]');
  
  if (parts.length !== 2) {
    // Fallback to simple if [...] not found or appears multiple times
    renderSimpleQuestion(question);
    return;
  }
  
  questionContainer.innerHTML = `
    <div class="fill-container text-xl text-gray-800 dark:text-gray-100">
      <span>${escapeHtml(parts[0])}</span>
      <input type="text" id="answer-input" 
             class="inline-input"
             placeholder="">
      <span>${escapeHtml(parts[1])}</span>
    </div>
  `;
  
  const input = document.getElementById('answer-input');
  if (input) {
    input.focus();
  }
}

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Get the current answer from the input field
 * @returns {string} The answer value
 */
function getAnswer() {
  const input = document.getElementById('answer-input');
  return input ? input.value : '';
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

  const answer = getAnswer();

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
