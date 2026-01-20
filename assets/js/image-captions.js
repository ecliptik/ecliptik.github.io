// Add figcaption text as title attribute for image hover tooltips
(function() {
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
            img.setAttribute('title', captionText);
          }
        }
      }
    });
  });
})();
