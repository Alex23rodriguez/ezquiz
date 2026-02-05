/**
 * Sidebar view module
 * Handles category updates during quiz
 */

import { state } from '../state.js';
import { fetchNextQuestion } from '../api.js';
import { showQuiz } from './quiz.js';

const updateCategoriesBtn = document.getElementById('update-categories-btn');

/**
 * Get selected categories from sidebar checkboxes
 * @returns {string[]} Selected category values
 */
function getSidebarCategories() {
  const checkboxes = document.querySelectorAll('.sidebar-category-checkbox:checked');
  return Array.from(checkboxes).map(cb => cb.value);
}

/**
 * Update categories and load next question
 */
async function handleUpdateCategories() {
  const categories = getSidebarCategories();
  
  if (categories.length === 0) {
    alert('Please select at least one category');
    return;
  }
  
  state.selectCategories(categories);
  
  try {
    const data = await fetchNextQuestion(state.selectedCategories);
    
    if (data.complete) {
      alert('Quiz complete! Great job!');
      const { resetSetup } = await import('./setup.js');
      resetSetup();
      return;
    }
    
    state.setQuestion(data.question);
    showQuiz();
  } catch (error) {
    console.error('Error fetching question:', error);
    alert('Failed to update categories. Please try again.');
  }
}

/**
 * Initialize the sidebar
 */
export function initSidebar() {
  updateCategoriesBtn.addEventListener('click', handleUpdateCategories);
}
