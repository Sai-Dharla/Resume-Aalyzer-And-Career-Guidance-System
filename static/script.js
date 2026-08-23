// ==================== GLOBAL SCRIPTS ====================
// This file contains global functionality used across all pages
// Note: Resume upload logic is now in my_resumes.html (embedded JavaScript)

/**
 * Toggle Sidebar Visibility
 * Shows/hides the sidebar on mobile devices
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth < 768) {
        // On mobile: toggle open/close
        sidebar.classList.toggle('open');
    } else {
        // On desktop: toggle collapsed/expanded
        sidebar.classList.toggle('collapsed');
    }
}

/**
 * Initialize Page
 * Runs when the page loads
 */
document.addEventListener('DOMContentLoaded', function() {
    // Global initialization code
    console.log('Page loaded successfully');
});

// ==================== END OF GLOBAL SCRIPTS ====================

