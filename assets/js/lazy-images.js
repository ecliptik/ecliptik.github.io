/**
 * Lazy Loading Images
 * Add loading="lazy" attribute to all images for better performance
 */
(function() {
  'use strict';

  // Add lazy loading to all images
  document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');

    images.forEach(function(img) {
      // Add loading="lazy" if not already set
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
    });
  });
})();
