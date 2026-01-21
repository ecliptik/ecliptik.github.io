/**
 * Search Initialization Module
 * Lazy loads search functionality on first focus of search input
 */
(function() {
  'use strict';

  const searchInput = document.getElementById('search-input');
  if (!searchInput) return; // Exit if search input not found

  let searchLoaded = false;

  /**
   * Initialize SimpleJekyllSearch after script loads
   */
  function initSearch() {
    SimpleJekyllSearch({
      searchInput: searchInput,
      resultsContainer: document.getElementById('results-container'),
      json: '/search.json',
      searchResultTemplate: '<li><a href="{url}">{title}</a>  <span class="post-meta">{date}</span></li>',
      limit: 10,
      fuzzy: false,
      debounceTime: 300,
      noResultsText: '<li>No results found</li>'
    });
  }

  /**
   * Lazy load search script on first focus
   */
  searchInput.addEventListener('focus', function() {
    if (!searchLoaded) {
      const script = document.createElement('script');
      script.src = '/assets/js/search-script.js';
      script.onload = initSearch;
      document.head.appendChild(script);
      searchLoaded = true;
    }
  }, { once: true });
})();
