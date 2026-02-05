/**
 * State management module
 * Encapsulates all application state
 */

class State {
  constructor() {
    this.selectedCategories = [];
    this.currentQuestion = null;
    this.questionNumber = 0;
    this.showingResult = false;
  }

  selectCategories(categories) {
    this.selectedCategories = [...categories];
  }

  setQuestion(question) {
    this.currentQuestion = question;
    this.questionNumber++;
    this.showingResult = false;
  }

  markShowingResult() {
    this.showingResult = true;
  }

  reset() {
    this.selectedCategories = [];
    this.currentQuestion = null;
    this.questionNumber = 0;
    this.showingResult = false;
  }
}

export const state = new State();
