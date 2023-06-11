let valorInput = document.getElementById('valor')
let btn = document.getElementById('button')

valorInput.addEventListener('input', () => {
    if(valorInput.value === '' || valorInput.value <= 0){
        btn.disabled = true
     }else{
        btn.disabled = false
    }
})