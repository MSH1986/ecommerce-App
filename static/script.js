const addCategoryWindow = document.querySelector('.add-Category-Window');
const closeAddCategoryWindow = document.querySelector('.close-Add-Category-Window');
const openCategoryWindow = document.querySelector('.add-category');
const modalOverlay = document.getElementById('modalOverlay'); // The dark background overlay


if(closeAddCategoryWindow != null){
    closeAddCategoryWindow.addEventListener('click', ()=> {
        addCategoryWindow.style.display = 'none'
        modalOverlay.style.display = 'none'; // Hide the overlay
    })
}

if(openCategoryWindow != null){
    openCategoryWindow.addEventListener('click', ()=> {
        addCategoryWindow.style.display = 'block'
        modalOverlay.style.display = 'block'; // Show the overlay to darken the screen
    })
}

if(modalOverlay != null){
    modalOverlay.addEventListener('click', () => {
        addCategoryWindow.style.display = 'none';
        modalOverlay.style.display = 'none';
    });
}




