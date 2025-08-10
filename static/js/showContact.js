let contactDisplay = document.querySelector('.showContact'); 

contactDisplay.addEventListener('click', ()=> {
    if (contactDisplay.style.dispaly == 'none'){
        console.log('btnclicked')
        contactDisplay.style.dispaly == 'flex'; 
    }else{
        console.log('btnclicked')
        contactDisplay.style.dispaly == 'none';
    }
})