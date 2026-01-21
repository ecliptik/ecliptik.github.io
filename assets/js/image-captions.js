// Add figcaption text as custom tooltip for image hover
// Uses shared Tooltip module
(function() {
  'use strict';

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
              // Apply theme class based on current theme (show opposite theme colors)
              const currentTheme = document.documentElement.getAttribute('data-theme');
              const themeClass = currentTheme === 'dark' ? 'theme-light' : 'theme-dark';

              // Show tooltip at center of image
              Tooltip.show(e, captionText, { themeClass, position: 'center' });
            });

            img.addEventListener('mouseleave', Tooltip.hide);
          }
        }
      }
    });
  });
})();
