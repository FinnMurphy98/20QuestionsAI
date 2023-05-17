// base.html
const currentUrl = window.location.href;
const links = document.querySelectorAll('.navbar a');
links.forEach((link) => {
    if (link.href === currentUrl) {
        link.classList.add('active');
    }
});


function dropdown() {
    var dropdownMenu = document.getElementById("dropdown-menu");
    if (dropdownMenu.style.display === "block") {
        dropdownMenu.style.display = "none";
    } else {
        dropdownMenu.style.display = "block";
    }
}


// history
// function of change the page 
function changePage(direction) {
    var currentPage = parseInt(document.getElementById("current-page").textContent);
    var totalPages = parseInt(document.getElementById("total-pages").textContent);
    var jumpInput = document.getElementById("jump-input");
    
    if (direction === "prev" && currentPage > 1) {
        window.location.href = "{{ url_for('app.history') }}?page=" + (currentPage - 1);
    } else if (direction === "next" && currentPage < totalPages) {
        window.location.href = "{{ url_for('app.history') }}?page=" + (currentPage + 1);
    }
}

// function of jumping to page by input 
function jumpToPage() {
    var jumpInput = document.getElementById("jump-input");
    var page = parseInt(jumpInput.value);
    
    if (!isNaN(page) && page >= 1 && page <= {{ games.pages }}) {
            window.location.href = "{{ url_for('app.history') }}?page=" + page;
    }
}
