console.log('js loaded');

const sessionCheckbox = document.querySelector('#session');
const loginBtn        = document.querySelector('#loginBtn')

sessionCheckbox.onchange = _ => {
    if (sessionCheckbox.checked) {
        loginBtn.disabled = false;
    } else {
        loginBtn.disabled = true;
    }
}

loginBtn.disabled = true;