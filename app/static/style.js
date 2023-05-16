// base.html
const currentUrl = window.location.href;
const links = document.querySelectorAll('.navbar a');
links.forEach((link) => {
    if (link.href === currentUrl) {
        link.classList.add('active');
    }
});


// function dropdown() {
//     document.getElementById("dropdown-menu").classList.toggle("show");
// }
// window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//         var dropdowns = document.getElementsByClassName("dropdown-content");
//         var i;
//         for (var i = 0; i < dropdowns.length; i++) {
//             var openDropdown = dropdowns[i];
//             if (openDropdown.classList.contains('show')) {
//                 openDropdown.classList.remove('show');
//             }
//         }
//     }
// }
function dropdown() {
    var dropdownMenu = document.getElementById("dropdown-menu");
    if (dropdownMenu.style.display === "block") {
        dropdownMenu.style.display = "none";
    } else {
        dropdownMenu.style.display = "block";
    }
}

