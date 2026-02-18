// Load category data from JSON file
export async function loadCategory(categoryName) {
	try {
		const response = await fetch(`./assets/data/${categoryName}.json`);
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error loading category:', error);
		return null;
	}
}
