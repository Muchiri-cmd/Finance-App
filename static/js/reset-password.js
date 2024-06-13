document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');
    
    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        
        this.textContent = this.textContent === 'SHOW' ? 'HIDE' : 'SHOW';
    });

    togglePassword2.addEventListener('click', function () {
        const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
        password2.setAttribute('type', type);
        
        this.textContent = this.textContent === 'SHOW' ? 'HIDE' : 'SHOW';
    });
});