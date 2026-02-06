/**
 * Theme management module
 * Handles dark/light mode toggle and persistence
 */

const THEME_KEY = 'ezquiz-theme';

/**
 * Get current theme from localStorage or default to light
 * @returns {string} 'light' or 'dark'
 */
function getStoredTheme() {
  return localStorage.getItem(THEME_KEY) || 'light';
}

/**
 * Save theme preference to localStorage
 * @param {string} theme - 'light' or 'dark'
 */
function setStoredTheme(theme) {
  localStorage.setItem(THEME_KEY, theme);
}

/**
 * Apply theme to document
 * @param {string} theme - 'light' or 'dark'
 */
function applyTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  updateThemeIcon(theme);
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
  const currentTheme = getStoredTheme();
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';
  setStoredTheme(newTheme);
  applyTheme(newTheme);
}

/**
 * Update theme toggle button icon
 * @param {string} theme - 'light' or 'dark'
 */
function updateThemeIcon(theme) {
  const sunIcon = document.getElementById('theme-icon-sun');
  const moonIcon = document.getElementById('theme-icon-moon');
  
  if (sunIcon && moonIcon) {
    if (theme === 'dark') {
      sunIcon.classList.remove('hidden');
      moonIcon.classList.add('hidden');
    } else {
      sunIcon.classList.add('hidden');
      moonIcon.classList.remove('hidden');
    }
  }
}

/**
 * Initialize theme system
 */
export function initTheme() {
  // Apply stored theme on load
  const theme = getStoredTheme();
  applyTheme(theme);
  
  // Add event listener to toggle button
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleTheme);
  }
}

/**
 * Get current theme
 * @returns {string} 'light' or 'dark'
 */
export function getCurrentTheme() {
  return getStoredTheme();
}
