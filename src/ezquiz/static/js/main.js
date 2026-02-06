/**
 * Main entry point
 * Initializes all view modules
 */

import { initSetup } from './views/setup.js';
import { initQuiz } from './views/quiz.js';
import { initSidebar } from './views/sidebar.js';
import { initTheme } from './theme.js';

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSetup();
  initSidebar();
  initQuiz();
});
