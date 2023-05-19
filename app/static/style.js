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

var modal = document.getElementById("error-modal");
    var span = document.getElementsByClassName("close")[0];
    
    if (modal) {
        modal.style.display = "block";
    }
    
    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }

document.addEventListener('DOMContentLoaded', function() {
    var descriptions = document.querySelectorAll('.index-description p');
    for (var i = 0; i < descriptions.length; i++) {
        descriptions[i].classList.add('fade-in');
    }
});

