// Clean up URL
const disableEmptyInputs = (form) => {
    let controls = form.elements;
    for (let i=0; i< controls.length; i++) {
        if (controls[i].value == '') {
            controls[i].disabled = true
        }
    }
}



