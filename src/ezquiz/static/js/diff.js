/**
 * Text diff visualization module
 * Implements Levenshtein distance algorithm for string alignment
 */

/**
 * Escape special characters for HTML display
 * @param {string} c - Character to escape
 * @returns {string} Escaped character
 */
function escapeChar(c) {
  return c === "_" ? "&nbsp;" : c;
}

/**
 * Align two strings using dynamic programming (Levenshtein distance)
 * @param {string} a - First string
 * @param {string} b - Second string
 * @returns {{aAlign: string, bAlign: string}} Aligned strings
 */
function alignStrings(a, b) {
  a = a || "";
  b = b || "";

  const dp = Array.from({ length: a.length + 1 }, () =>
    Array(b.length + 1).fill(0),
  );

  for (let i = 0; i <= a.length; i++) dp[i][0] = i;
  for (let j = 0; j <= b.length; j++) dp[0][j] = j;

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      dp[i][j] =
        a[i - 1] === b[j - 1]
          ? dp[i - 1][j - 1]
          : 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
    }
  }

  let i = a.length,
    j = b.length;
  let aAlign = "",
    bAlign = "";

  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && a[i - 1] === b[j - 1]) {
      aAlign = a[i - 1] + aAlign;
      bAlign = b[j - 1] + bAlign;
      i--;
      j--;
    } else if (i > 0 && j > 0 && dp[i][j] === dp[i - 1][j - 1] + 1) {
      aAlign = a[i - 1] + aAlign;
      bAlign = b[j - 1] + bAlign;
      i--;
      j--;
    } else if (i > 0 && dp[i][j] === dp[i - 1][j] + 1) {
      aAlign = a[i - 1] + aAlign;
      bAlign = " " + bAlign;
      i--;
    } else {
      aAlign = " " + aAlign;
      bAlign = b[j - 1] + bAlign;
      j--;
    }
  }

  return { aAlign, bAlign };
}

/**
 * Render a visual diff between two strings
 * @param {string} userAnswer - User's submitted answer
 * @param {string} correctAnswer - Correct answer
 * @returns {string} HTML string with visual diff
 */
export function renderTextDiff(userAnswer, correctAnswer) {
  userAnswer = String(userAnswer || "");
  correctAnswer = String(correctAnswer || "");

  const { aAlign, bAlign } = alignStrings(userAnswer, correctAnswer);

  let top = "";
  let bottom = "";

  for (let i = 0; i < aAlign.length; i++) {
    const a = aAlign[i];
    const b = bAlign[i];

    // TOP ROW (user input)
    if (a === " " && b !== " ") {
      top += `<span class="diff-grey">-</span>`;
    } else if (a === b) {
      top += `<span class="diff-green">${escapeChar(a)}</span>`;
    } else if (a !== " ") {
      top += `<span class="diff-red">${escapeChar(a)}</span>`;
    }

    // BOTTOM ROW (reference)
    if (b === " ") {
      bottom += `<span class="diff-grey">${"_"}</span>`;
    } else if (a === b) {
      bottom += `<span class="diff-green">${escapeChar(b)}</span>`;
    } else {
      bottom += `<span class="diff-grey">${escapeChar(b)}</span>`;
    }
  }

  return `<div class="diff"><div class="diff-row">${top}</div><div class="diff-row">${bottom}</div></div>`;
}
