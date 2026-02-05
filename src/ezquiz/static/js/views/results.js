/**
 * Results view module
 * Handles display of answer feedback and explanations
 */

import { renderTextDiff } from '../diff.js';
import { state } from '../state.js';

const submitBtn = document.getElementById('submit-btn');
const questionContainer = document.getElementById('question-container');
const resultContainer = document.getElementById('result-container');

/**
 * Display the result of an answer submission
 * @param {Object} data - Result data from API
 * @param {boolean} data.correct - Whether answer was correct
 * @param {string} data.submitted_answer - User's answer
 * @param {string} data.correct_answer - Correct answer
 * @param {string} data.explanation - Explanation or "{textdiff}"
 */
export function showResult(data) {
  questionContainer.classList.add('hidden');
  resultContainer.classList.remove('hidden');
  submitBtn.textContent = 'Next Question (Enter)';
  
  const isCorrect = data.correct;
  const bgColor = isCorrect ? 'bg-green-100' : 'bg-red-100';
  const textColor = isCorrect ? 'text-green-800' : 'text-red-800';
  const icon = isCorrect ? '✓' : '✗';
  const message = isCorrect ? 'Correct!' : 'Incorrect';
  
  // Check if explanation is textdiff placeholder
  const isTextDiff = data.explanation === "{textdiff}";
  
  let explanationHtml = '';
  if (!isCorrect && isTextDiff) {
    explanationHtml = `
      <div class="bg-gray-50 border-l-4 border-gray-400 p-4">
        ${renderTextDiff(data.submitted_answer, data.correct_answer)}
      </div>
    `;
  } else if (!isCorrect && data.explanation) {
    explanationHtml = `<div class="bg-blue-50 border-l-4 border-blue-500 p-4"><p class="text-gray-700"><strong>Explanation:</strong> ${data.explanation}</p></div>`;
  }
  
  resultContainer.innerHTML = `
    <div class="${bgColor} border-l-4 ${isCorrect ? 'border-green-500' : 'border-red-500'} p-4 mb-4">
      <div class="flex items-center">
        <span class="text-2xl mr-3">${icon}</span>
        <div>
          <p class="font-bold ${textColor} text-lg">${message}</p>
          <p class="text-gray-600 mt-1">Your answer: <span class="font-semibold">${data.submitted_answer}</span></p>
          ${!isCorrect && !isTextDiff ? `<p class="text-gray-600 mt-1">Correct answer: <span class="font-semibold">${data.correct_answer}</span></p>` : ''}
        </div>
      </div>
    </div>
    ${explanationHtml}
    <div class="mt-4 text-sm text-gray-500 text-center">Press Enter to continue</div>
  `;
  
  // Blur focus to prevent double submission
  if (document.activeElement) {
    document.activeElement.blur();
  }
}
