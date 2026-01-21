/**
 * Shared Tooltip Module
 * Provides reusable tooltip functionality for theme toggle and image captions
 */
(function(global) {
  'use strict';

  let tooltip = null;

  /**
   * Create tooltip element and append to body
   */
  function createTooltip() {
    tooltip = document.createElement('div');
    tooltip.className = 'image-tooltip';
    document.body.appendChild(tooltip);
  }

  /**
   * Show tooltip with custom text and optional theme class
   * @param {MouseEvent} e - Mouse event for positioning
   * @param {string} text - Tooltip text content
   * @param {Object} options - Configuration options
   * @param {string} options.themeClass - Optional CSS class for theming
   * @param {string} options.position - 'below' (default) or 'center'
   */
  function showTooltip(e, text, options = {}) {
    if (!tooltip) createTooltip();

    const { themeClass, position = 'below' } = options;

    tooltip.textContent = text;
    tooltip.className = 'image-tooltip visible';
    if (themeClass) {
      tooltip.classList.add(themeClass);
    }

    const targetRect = e.target.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    let left, top;

    if (position === 'center') {
      // Position tooltip at center of target element
      left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);
      top = targetRect.top + (targetRect.height / 2) - (tooltipRect.height / 2);
    } else {
      // Position tooltip below target element
      left = targetRect.left + (targetRect.width / 2) - (tooltipRect.width / 2);
      top = targetRect.bottom + 8;
    }

    // Keep tooltip within viewport horizontally
    if (left < 5) left = 5;
    if (left + tooltipRect.width > window.innerWidth - 5) {
      left = window.innerWidth - tooltipRect.width - 5;
    }

    tooltip.style.left = left + window.scrollX + 'px';
    tooltip.style.top = top + window.scrollY + 'px';
  }

  /**
   * Hide tooltip
   */
  function hideTooltip() {
    if (tooltip) {
      tooltip.classList.remove('visible');
    }
  }

  // Export to global namespace
  global.Tooltip = {
    show: showTooltip,
    hide: hideTooltip
  };

})(window);
