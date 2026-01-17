(function() {
  'use strict';

  const STORAGE_KEY = 'theme-preference';
  const THEME_LIGHT = 'light';
  const THEME_DARK = 'dark';

  /**
   * Get the system's preferred color scheme
   * @returns {string} 'dark' or 'light'
   */
  function getSystemPreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? THEME_DARK : THEME_LIGHT;
  }

  /**
   * Get the user's theme preference from localStorage or system preference
   * @returns {string} 'dark' or 'light'
   */
  function getThemePreference() {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored || getSystemPreference();
  }

  /**
   * Apply the theme to the document and update the toggle button
   * @param {string} theme - 'dark' or 'light'
   */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateToggleButton(theme);
  }

  /**
   * Update the toggle button icon and aria-label
   * @param {string} theme - 'dark' or 'light'
   */
  function updateToggleButton(theme) {
    const btn = document.getElementById('theme-toggle-btn');
    const icon = btn?.querySelector('.theme-icon');
    if (icon) {
      // Show sun icon when in dark mode (to switch to light)
      // Show moon icon when in light mode (to switch to dark)
      icon.textContent = theme === THEME_DARK ? '☀️' : '🌙';
      btn.setAttribute('aria-label',
        theme === THEME_DARK ? 'Switch to light theme' : 'Switch to dark theme'
      );
    }
  }

  /**
   * Toggle between light and dark themes
   */
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === THEME_DARK ? THEME_LIGHT : THEME_DARK;
    localStorage.setItem(STORAGE_KEY, next);
    applyTheme(next);
  }

  /**
   * Initialize theme early to prevent flash of unstyled content (FOUC)
   * This runs immediately when the script loads
   */
  function initThemeEarly() {
    // Add preload class to prevent transitions on initial load
    document.documentElement.classList.add('preload');
    const theme = getThemePreference();
    document.documentElement.setAttribute('data-theme', theme);

    // Remove preload class after a short delay to enable transitions
    setTimeout(() => {
      document.documentElement.classList.remove('preload');
    }, 100);
  }

  /**
   * Initialize theme toggle functionality after DOM is ready
   */
  function initTheme() {
    const theme = getThemePreference();
    applyTheme(theme);

    // Add click event listener to toggle button
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);
    }

    // Listen for system theme changes (only applies if user hasn't set manual preference)
    window.matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        // Only update if user hasn't manually set a preference
        if (!localStorage.getItem(STORAGE_KEY)) {
          applyTheme(e.matches ? THEME_DARK : THEME_LIGHT);
        }
      });
  }

  // Run early initialization immediately
  initThemeEarly();

  // Run full initialization when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();
