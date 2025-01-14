// Template Rendering Utility
class TemplateRenderer {
    constructor(metadataPath) {
        this.metadataPath = metadataPath;
        this.metadata = null;
    }

    // Fetch metadata from JSON file
    async loadMetadata() {
        try {
            const response = await fetch(this.metadataPath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.metadata = await response.json();
        } catch (error) {
            console.error("Failed to fetch metadata:", error);
        }
    }

    // Generate HTML for a single template card
    createTemplateCard(templateData) {
        const card = document.createElement('div');
        card.className = 'template-card';

        const title = document.createElement('h3');
        title.className = 'template-title';
        title.textContent = templateData.title;

        const description = document.createElement('p');
        description.className = 'template-description';
        description.textContent = templateData.summary || 'No description provided';

        const footer = document.createElement('div');
        footer.className = 'template-footer';

        const keywords = document.createElement('span');
        keywords.className = 'template-keywords';
        keywords.textContent = templateData.tags ? templateData.tags.join(', ') : 'No keywords';

        const downloadLink = document.createElement('a');
        downloadLink.className = 'download-link';
        downloadLink.href = `/templates/${templateData.id}/template.md`;
        downloadLink.textContent = 'Download';

        footer.appendChild(keywords);
        footer.appendChild(downloadLink);

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(footer);

        // Add images with descriptive alt text
        if (templateData.content_files && templateData.content_files.length > 0) {
            templateData.content_files.forEach(file => {
                if (/\.(png|jpg|jpeg|gif|webp)$/i.test(file)) {
                    const image = document.createElement('img');
                    image.src = file;
                    image.alt = `Preview of ${templateData.title} template`; // Descriptive alt text
                    image.loading = 'lazy'; // Improve performance
                    card.appendChild(image);
                }
            });
        }

        return card;
    }

    // Render all templates in a grid
    renderTemplateGrid(containerId) {
        if (!this.metadata) {
            console.error('Metadata not loaded');
            return;
        }

        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID ${containerId} not found`);
            return;
        }

        // Clear existing content
        container.innerHTML = '';

        // Group templates by category
        const templatesByCategory = this.groupTemplatesByCategory();

        // Create category tabs if multiple categories exist
        if (Object.keys(templatesByCategory).length > 1) {
            this.createCategoryTabs(container, templatesByCategory);
        } else {
            // If only one category, directly render templates
            const categoryName = Object.keys(templatesByCategory)[0];
            this.renderTemplatesInCategory(container, templatesByCategory[categoryName]);
        }
    }

    // Group templates by category
    groupTemplatesByCategory() {
        const templatesByCategory = {};
        
        Object.values(this.metadata.knowledge_blocks).forEach(template => {
            if (!templatesByCategory[template.category]) {
                templatesByCategory[template.category] = [];
            }
            templatesByCategory[template.category].push(template);
        });

        return templatesByCategory;
    }

    // Create category tabs
    createCategoryTabs(container, templatesByCategory) {
        const tabContainer = document.createElement('div');
        tabContainer.className = 'template-tabs';

        // Create tab buttons
        const tabButtonsContainer = document.createElement('ul');
        tabButtonsContainer.className = 'tab-buttons';

        // Create tab contents container
        const tabContentsContainer = document.createElement('div');
        tabContentsContainer.className = 'tab-contents';

        let isFirstTab = true;
        Object.entries(templatesByCategory).forEach(([categoryName, templates]) => {
            // Create tab button
            const tabButton = document.createElement('li');
            tabButton.className = `tab-button ${isFirstTab ? 'active' : ''}`;
            tabButton.textContent = categoryName;
            tabButton.setAttribute('data-tab', categoryName.replace(/\s+/g, '-'));
            tabButtonsContainer.appendChild(tabButton);

            // Create tab content
            const tabContent = document.createElement('div');
            tabContent.className = `tab-content ${isFirstTab ? 'active' : ''}`;
            tabContent.setAttribute('data-tab-content', categoryName.replace(/\s+/g, '-'));

            // Render templates in this category
            const gridContainer = document.createElement('div');
            gridContainer.className = 'template-grid';
            
            templates.forEach(template => {
                gridContainer.appendChild(this.createTemplateCard(template));
            });

            tabContent.appendChild(gridContainer);
            tabContentsContainer.appendChild(tabContent);

            isFirstTab = false;
        });

        tabContainer.appendChild(tabButtonsContainer);
        tabContainer.appendChild(tabContentsContainer);
        container.appendChild(tabContainer);

        // Add tab switching functionality
        this.setupTabSwitching(tabContainer);
    }

    // Render templates directly in a single category
    renderTemplatesInCategory(container, templates) {
        const gridContainer = document.createElement('div');
        gridContainer.className = 'template-grid';
        
        templates.forEach(template => {
            gridContainer.appendChild(this.createTemplateCard(template));
        });

        container.appendChild(gridContainer);
    }

    // Tab switching functionality
    setupTabSwitching(tabContainer) {
        const tabButtons = tabContainer.querySelectorAll('.tab-button');
        const tabContents = tabContainer.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tab = button.getAttribute('data-tab');

                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // Add active class to clicked button and corresponding content
                button.classList.add('active');
                tabContainer.querySelector(`[data-tab-content="${tab}"]`).classList.add('active');
            });
        });
    }
}

// Export for use in other modules
export default TemplateRenderer;
