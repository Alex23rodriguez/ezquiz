/**
 * API communication module
 */

/**
 * Fetch the next question from the API
 * @param {string[]} categories - Selected category names
 * @returns {Promise<Object>} Question data or completion status
 */
export async function fetchNextQuestion(categories) {
  const response = await fetch('api/next', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ categories })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

/**
 * Submit an answer to the API
 * @param {string} category - Question category
 * @param {*} seed - Question seed
 * @param {string} answer - User's answer
 * @returns {Promise<Object>} Result with correctness and explanation
 */
export async function submitAnswer(category, seed, answer) {
  const response = await fetch('api/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      category,
      seed,
      answer: answer.trim()
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}
