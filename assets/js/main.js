// EASTER Navigation and Data Loading
// Uses oninput event for all API calls per D7460N architecture

// Cookie management
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function setCookie(name, value, days = 365) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/`;
}

// Data file mapping based on index.json categories
const dataFiles = {
  'introduction': './data/introduction.json',
  'roles': './data/roles.json',
  'basics': './data/basics.json',
  'rehearsal': './data/rehearsal.json',
  'production': './data/production.json'
};

// Load data for selected nav item
function loadCategoryData(categoryId) {
  const url = dataFiles[categoryId];
  if (!url) {
    console.error(`No data file mapped for category: ${categoryId}`);
    return;
  }

  const root = document.querySelector('app-container');
  runPipeline(url, root)
    .then(() => {
      console.log(`Loaded data for: ${categoryId}`);
      setCookie('selectedNav', categoryId);
    })
    .catch(err => {
      console.error('Pipeline error:', err);
    });
}

// Initialize navigation
function initNavigation() {
  const navInputs = document.querySelectorAll('nav input[type="radio"]');
  
  // Set up oninput event for each nav radio button
  navInputs.forEach((input, index) => {
    input.oninput = function() {
      const categoryIds = Object.keys(dataFiles);
      const categoryId = categoryIds[index];
      if (categoryId) {
        loadCategoryData(categoryId);
      }
    };
  });

  // Check for saved nav preference
  const savedNav = getCookie('selectedNav');
  if (savedNav) {
    const categoryIds = Object.keys(dataFiles);
    const index = categoryIds.indexOf(savedNav);
    if (index >= 0 && navInputs[index]) {
      navInputs[index].checked = true;
      loadCategoryData(savedNav);
      return;
    }
  }

  // Default to first nav item
  if (navInputs[0]) {
    navInputs[0].checked = true;
    const firstCategory = Object.keys(dataFiles)[0];
    loadCategoryData(firstCategory);
  }
}

// Run on page load
window.onload = initNavigation;
