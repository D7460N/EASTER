// D7460N Architecture - Data transport only, no UI logic
// All UI state management is handled by CSS

// Initialize navigation on page load
document.addEventListener('DOMContentLoaded', () => {
	// Load initial category (Introduction is checked by default)
	const checkedNav = document.querySelector('nav input[type="radio"]:checked');
	if (checkedNav) {
		loadCategory(checkedNav.value);
	}

	// Listen for navigation changes
	document.querySelectorAll('nav input[type="radio"]').forEach(input => {
		input.oninput = () => {
			loadCategory(input.value);
		};
	});

	// Listen for document clicks in the list
	document.addEventListener('click', (event) => {
		const listItem = event.target.closest('app-document-list li');
		if (listItem) {
			const documentId = listItem.getAttribute('data-id');
			if (documentId) {
				displayDocumentDetail(documentId);
			}
		}
	});
});

// Store current category data for detail lookup
let currentCategoryData = null;

// Load a category by name
async function loadCategory(categoryName) {
	try {
		const response = await fetch(`./assets/data/${categoryName}.json`);
		const data = await response.json();
		
		currentCategoryData = data;
		
		// Inject category info
		injectCategoryInfo(data);
		
		// Inject document list
		injectDocumentList(data.documents);
		
		// Clear document detail
		clearDocumentDetail();
	} catch (error) {
		console.error('Error loading category:', error);
	}
}

// Inject category information
function injectCategoryInfo(data) {
	const iconEl = document.querySelector('app-category-icon');
	const nameEl = document.querySelector('app-category-name');
	const descEl = document.querySelector('app-category-description');
	
	if (iconEl) iconEl.textContent = data.icon || '';
	if (nameEl) nameEl.textContent = data.name || '';
	if (descEl) descEl.textContent = data.description || '';
}

// Inject document list
function injectDocumentList(documents) {
	const listContainer = document.querySelector('app-document-list ol');
	if (!listContainer) return;
	
	// Clear existing content
	listContainer.replaceChildren();
	
	// Add each document
	documents.forEach(doc => {
		const li = document.createElement('li');
		li.setAttribute('data-id', doc.id);
		
		const title = document.createElement('document-title');
		title.textContent = doc.title;
		
		const summary = document.createElement('document-summary');
		summary.textContent = doc.summary;
		
		const tags = document.createElement('document-tags');
		(doc.tags || []).forEach(tag => {
			const tagEl = document.createElement('document-tag');
			tagEl.textContent = tag;
			tags.appendChild(tagEl);
		});
		
		li.appendChild(title);
		li.appendChild(summary);
		li.appendChild(tags);
		
		listContainer.appendChild(li);
	});
}

// Display document detail in aside
function displayDocumentDetail(documentId) {
	if (!currentCategoryData) return;
	
	const doc = currentCategoryData.documents.find(d => d.id === documentId);
	if (!doc) return;
	
	const titleEl = document.querySelector('app-document-title');
	const categoryEl = document.querySelector('app-document-category');
	const summaryEl = document.querySelector('app-document-summary');
	const contentEl = document.querySelector('app-document-content');
	const tagsContainer = document.querySelector('app-document-tags ol');
	const audienceContainer = document.querySelector('app-document-audience ol');
	
	if (titleEl) titleEl.textContent = doc.title;
	if (categoryEl) categoryEl.textContent = doc.category || currentCategoryData.name;
	if (summaryEl) summaryEl.textContent = doc.summary;
	if (contentEl) contentEl.innerHTML = doc.content || '';
	
	// Tags
	if (tagsContainer) {
		tagsContainer.replaceChildren();
		(doc.tags || []).forEach(tag => {
			const li = document.createElement('li');
			li.textContent = tag;
			tagsContainer.appendChild(li);
		});
	}
	
	// Audience
	if (audienceContainer) {
		audienceContainer.replaceChildren();
		(doc.audience || []).forEach(aud => {
			const li = document.createElement('li');
			li.textContent = aud;
			audienceContainer.appendChild(li);
		});
	}
}

// Clear document detail
function clearDocumentDetail() {
	const titleEl = document.querySelector('app-document-title');
	const categoryEl = document.querySelector('app-document-category');
	const summaryEl = document.querySelector('app-document-summary');
	const contentEl = document.querySelector('app-document-content');
	const tagsContainer = document.querySelector('app-document-tags ol');
	const audienceContainer = document.querySelector('app-document-audience ol');
	
	if (titleEl) titleEl.textContent = '';
	if (categoryEl) categoryEl.textContent = '';
	if (summaryEl) summaryEl.textContent = '';
	if (contentEl) contentEl.innerHTML = '';
	if (tagsContainer) tagsContainer.replaceChildren();
	if (audienceContainer) audienceContainer.replaceChildren();
}
