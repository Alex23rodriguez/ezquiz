/**
 * Setup view module
 * Handles category selection and quiz initialization
 */

import { state } from '../state.js';
import { showQuiz } from './quiz.js';
import { fetchNextQuestion } from '../api.js';

const setupView = document.getElementById('setup-view');
const startBtn = document.getElementById('start-btn');

/**
 * Get selected categories from checkboxes
 * @param {string} selector - Checkbox selector
 * @returns {string[]} Selected category values
 */
function getSelectedCategories(selector) {
  const checkboxes = document.querySelectorAll(selector);
  return Array.from(checkboxes).map(cb => cb.value);
}

/**
 * Sync sidebar checkboxes with current state
 */
function syncSidebarCategories() {
  document.querySelectorAll('.sidebar-category-checkbox').forEach(cb => {
    cb.checked = state.selectedCategories.includes(cb.value);
  });
}

/**
 * Load and display the first question
 */
async function loadFirstQuestion() {
  try {
    const data = await fetchNextQuestion(state.selectedCategories);
    
    if (data.complete) {
      alert('Quiz complete! Great job!');
      resetSetup();
      return;
    }
    
    state.setQuestion(data.question);
    showQuiz();
  } catch (error) {
    console.error('Error fetching question:', error);
    alert('Failed to load question. Please try again.');
  }
}

/**
 * Reset the setup view
 */
function resetSetup() {
  setupView.classList.remove('hidden');
  document.getElementById('quiz-view').classList.add('hidden');
  
  document.querySelectorAll('.category-checkbox, .sidebar-category-checkbox').forEach(cb => {
    cb.checked = false;
  });
  
  state.reset();
}

/**
 * Initialize the setup view
 */
export function initSetup() {
  startBtn.addEventListener('click', async () => {
    const categories = getSelectedCategories('.category-checkbox:checked');
    
    if (categories.length === 0) {
      alert('Please select at least one category');
      return;
    }
    
    state.selectCategories(categories);
    syncSidebarCategories();
    await loadFirstQuestion();
  });
}

export { resetSetup, getSelectedCategories };
