const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item => {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

// Sidebar toggle işlemi
if (menuBar && sidebar) {
    menuBar.addEventListener('click', function () {
        sidebar.classList.toggle('hide');
    });
}

// Sayfa yüklendiğinde ve boyut değişimlerinde sidebar durumunu ayarlama
function adjustSidebar() {
    if (sidebar) {
        if (window.innerWidth <= 576) {
            sidebar.classList.add('hide');  // 576px ve altı için sidebar gizli
            sidebar.classList.remove('show');
        } else {
            sidebar.classList.remove('hide');  // 576px'den büyükse sidebar görünür
            sidebar.classList.add('show');
        }
    }
}

// Sayfa yüklendiğinde ve pencere boyutu değiştiğinde sidebar durumunu ayarlama
window.addEventListener('load', adjustSidebar);
window.addEventListener('resize', adjustSidebar);

// Arama butonunu toggle etme
const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

if (searchButton && searchButtonIcon && searchForm) {
    searchButton.addEventListener('click', function (e) {
        if (window.innerWidth < 768) {
            e.preventDefault();
            searchForm.classList.toggle('show');
            if (searchForm.classList.contains('show')) {
                searchButtonIcon.classList.replace('bx-search', 'bx-x');
            } else {
                searchButtonIcon.classList.replace('bx-x', 'bx-search');
            }
        }
    })
}

// Dark mode configuration is handled inline in base.html to prevent flash and avoid script caching issues.

// Notification Menu Toggle
const notificationBtn = document.querySelector('.notification');
const notificationMenu = document.querySelector('.notification-menu');
const profileMenu = document.querySelector('.profile-menu');

if (notificationBtn && notificationMenu) {
    notificationBtn.addEventListener('click', function () {
        notificationMenu.classList.toggle('show');
        if (profileMenu) {
            profileMenu.classList.remove('show'); // Close profile menu if open
        }
    });
}

// Profile Menu Toggle
const profileBtn = document.querySelector('.profile');

if (profileBtn && profileMenu) {
    profileBtn.addEventListener('click', function () {
        profileMenu.classList.toggle('show');
        if (notificationMenu) {
            notificationMenu.classList.remove('show'); // Close notification menu if open
        }
    });
}

// Close menus if clicked outside
window.addEventListener('click', function (e) {
    if ((!profileBtn || !e.target.closest('.profile')) && (!notificationBtn || !e.target.closest('.notification'))) {
        if (notificationMenu) notificationMenu.classList.remove('show');
        if (profileMenu) profileMenu.classList.remove('show');
    }
});

// Menülerin açılıp kapanması için fonksiyon
function toggleMenu(menuId) {
    var menu = document.getElementById(menuId);
    var allMenus = document.querySelectorAll('.menu');

    if (menu) {
        // Diğer tüm menüleri kapat
        allMenus.forEach(function (m) {
            if (m !== menu) {
                m.style.display = 'none';
            }
        });

        // Tıklanan menü varsa aç, yoksa kapat
        if (menu.style.display === 'none' || menu.style.display === '') {
            menu.style.display = 'block';
        } else {
            menu.style.display = 'none';
        }
    }
}

// Başlangıçta tüm menüleri kapalı tut
document.addEventListener("DOMContentLoaded", function () {
    var allMenus = document.querySelectorAll('.menu');
    allMenus.forEach(function (menu) {
        menu.style.display = 'none';
    });
});