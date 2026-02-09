// EASTER Initialization
// Handles initial page load by checking the first nav input

window.onload = () => {
  const firstInput = document.querySelector('nav input[type="radio"]');
  if (firstInput) {
    firstInput.checked = true;
    // Trigger oninput to load data
    if (firstInput.value) {
      runPipeline(firstInput.value, document);
    }
  }
};
