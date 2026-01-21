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
   * Initialize theme toggle functionality
   * Early theme setting is now handled by inline script in HTML head
   */
  function initTheme() {
    const theme = getThemePreference();
    applyTheme(theme);

    // Add click event listener to toggle button
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleTheme);

      // Add tooltip on hover (using shared Tooltip module)
      toggleBtn.addEventListener('mouseenter', function(e) {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const tooltipText = currentTheme === THEME_DARK
          ? 'Switch to Light Mode'
          : 'Switch to Dark Mode';
        const themeClass = currentTheme === THEME_DARK
          ? 'theme-light'
          : 'theme-dark';
        Tooltip.show(e, tooltipText, { themeClass });
      });

      toggleBtn.addEventListener('mouseleave', Tooltip.hide);
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

  // Initialize when DOM is ready (script is deferred, so DOM is already parsed)
  initTheme();
})();
