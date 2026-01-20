// Add figcaption text as custom tooltip for image hover
(function() {
  let tooltip = null;

  function createTooltip() {
    tooltip = document.createElement('div');
    tooltip.className = 'image-tooltip';
    document.body.appendChild(tooltip);
  }

  function showTooltip(e, text) {
    if (!tooltip) createTooltip();

    tooltip.textContent = text;

    // Apply theme class based on current theme (show opposite theme colors)
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const themeClass = currentTheme === 'dark' ? 'theme-light' : 'theme-dark';
    tooltip.className = 'image-tooltip visible ' + themeClass;

    // Position tooltip at center of the image
    const imgRect = e.target.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    let left = imgRect.left + (imgRect.width / 2) - (tooltipRect.width / 2);
    let top = imgRect.top + (imgRect.height / 2) - (tooltipRect.height / 2);

    // Keep tooltip within viewport horizontally
    if (left < 5) left = 5;
    if (left + tooltipRect.width > window.innerWidth - 5) {
      left = window.innerWidth - tooltipRect.width - 5;
    }

    tooltip.style.left = left + window.scrollX + 'px';
    tooltip.style.top = top + window.scrollY + 'px';
  }

  function hideTooltip() {
    if (tooltip) {
      tooltip.classList.remove('visible');
    }
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Find all paragraphs that contain images and are followed by figure elements
    const paragraphsWithImages = document.querySelectorAll('p:has(img)');

    paragraphsWithImages.forEach(function(p) {
      const nextElement = p.nextElementSibling;

      // Check if next element is a figure with a figcaption
      if (nextElement && nextElement.tagName === 'FIGURE') {
        const figcaption = nextElement.querySelector('figcaption');

        if (figcaption) {
          const captionText = figcaption.textContent.trim();

          // Find the image in the paragraph (might be wrapped in <a>)
          const img = p.querySelector('img');

          if (img && captionText) {
            img.addEventListener('mouseenter', function(e) {
              showTooltip(e, captionText);
            });

            img.addEventListener('mouseleave', hideTooltip);
          }
        }
      }
    });
  });
})();
