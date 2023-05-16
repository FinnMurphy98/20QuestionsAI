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
var currentPage = {{ current_page }};
var totalPageCount = {{ total_pages }};

function changePage(direction) {
    if (direction === 'prev' && currentPage > 1) {
        currentPage--;
    } else if (direction === 'next' && currentPage < totalPageCount) {
        currentPage++;
    }
    updatePageInfo();
}

function jumpToPage() {
    var jumpInput = document.getElementById('jump-input');
    var jumpPage = parseInt(jumpInput.value);
    if (!isNaN(jumpPage) && jumpPage >= 1 && jumpPage <= totalPageCount) {
        currentPage = jumpPage;
        updatePageInfo();
    }
    jumpInput.value = '';
}

function updatePageInfo() {
    document.getElementById('current-page').textContent = currentPage;
}