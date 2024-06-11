const togglePassword = document.getElementById('togglePassword');
const usernameInput = document.getElementById('username');
const emailInput = document.getElementById('email')
const feedback = document.querySelector('.feedback');
const emailFeedback = document.querySelector('.email-feedback');

togglePassword.addEventListener('click', function (e) {
    const password = document.getElementById('password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.textContent = this.textContent === 'SHOW' ? 'HIDE' : 'SHOW';
});

usernameInput.addEventListener('keyup',(e) => {
    const username= e.target.value
    //console.log(username)

    usernameInput.classList.remove('is-invalid');
    feedback.innerHTML=``
    feedback.style.display='none'

    if (username!==''){
         //make API call
        fetch('/users/validate-username',{
            body: JSON.stringify({
                'username':username,
            }),
            method: "POST",
        }).then((res)=>res.json())
        .then((data) =>{
            //console.log('data',data);
            if (data.error){
                usernameInput.classList.add('is-invalid');
                feedback.innerHTML=`<p>${data.error}</p>`
                feedback.style.display='block'
            } 
        });
    }
})

emailInput.addEventListener('keyup', (e)=> {
    const email = e.target.value;

    emailInput.classList.remove('is-invalid')
    emailFeedback.innerHTML=``
    emailFeedback.style.display = 'none';

    if (email!==''){
        //make API call
        fetch('/users/validate-email',{
            body:JSON.stringify({
                'email':email
            }),
            method:"POST",
        }). then ((res) => res.json())
        .then((data)=>{
            if (data.error){
                emailInput.classList.add('is-invalid');
                emailFeedback.innerHTML = `<p>${data.error}</p>`
                emailFeedback.style.display='block';
            }
        })
    }
})