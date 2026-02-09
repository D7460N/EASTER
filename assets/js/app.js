// EASTER App Entry Point
// Adapted from D7460N starter template
// Note: This project uses combined non-module approach
// The original starter uses ES6 modules: import { runPipeline } from './pipeline/14-run-pipeline.js';

// This implementation is handled by main.js which provides:
// - Navigation setup with oninput events
// - Cookie-based persistence
// - Category data loading via runPipeline

// For reference, the original starter pattern was:
// document
//   .querySelectorAll('input')
//   .forEach(input => {
//     input.oninput = () => runPipeline(input.value, document);
//   });

// In EASTER, we've extended this pattern in main.js to:
// - Map navigation inputs to specific data files
// - Save/restore navigation state with cookies
// - Initialize with first nav item on fresh load
// - Use category-specific data URLs instead of input.value

console.log('EASTER app.js loaded - navigation handled by main.js');
