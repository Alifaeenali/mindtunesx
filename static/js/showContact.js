let contactDisplay = document.querySelector('.showContact'); 
let contactPage = document.querySelector('.Contact'); 

contactDisplay.addEventListener('click', ()=> {
    if (contactDisplay.style.dispaly == 'none'){
        console.log('btnclicked')
        contactPage.style.dispaly == 'flex'; 
    }else{
        console.log('btnclicked')
        contactPage.style.dispaly == 'none';
    }
})