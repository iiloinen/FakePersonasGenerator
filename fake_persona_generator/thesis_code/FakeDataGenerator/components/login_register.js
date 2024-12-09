const popup = document.getElementById('popup');
const closePopupBtn = document.getElementById('closePopup');
const openLoginPopupBtn = document.getElementById('login-button');
const openRegisterPopupBtn = document.getElementById('register-button');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

function CheckForUserInSession(){
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
      const [key, value] = cookie.split("=");
      if (key === "user_id") {
        return true;
      }
    }
    return false;
}


openLoginPopupBtn.addEventListener('click', () => {
    document.getElementById("login_register_error").style.display = 'none';
    if (CheckForUserInSession())
    {
        document.getElementById("login-button").textContent = "Zaloguj się";
        document.cookie = `user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`
        return;
    }

    popup.style.display = 'flex';
    loginForm.style.display = 'block';
    loginForm.classList.add('active');
    registerForm.classList.remove('active');
});

openRegisterPopupBtn.addEventListener('click', () => {
    popup.style.display = 'flex';
    document.getElementById("login_register_error").style.display = 'none';
    registerForm.style.display = 'block';
    registerForm.classList.add('active');
    loginForm.classList.remove('active');
});

closePopupBtn.addEventListener('click', () => {
    popup.style.display = 'none';
    loginForm.style.display = 'none';
    registerForm.style.display = 'none';
    loginForm.classList.remove('active');
    registerForm.classList.remove('active');
});

window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
        loginForm.style.display = 'none';
        registerForm.style.display = 'none'
        loginForm.classList.remove('active');
        registerForm.classList.remove('active');
    }
});


loginForm.addEventListener('submit', (event) => {
  event.preventDefault();
  ExecuteLogin(document.getElementById("loginUsername").value,
               document.getElementById("loginPassword").value);
});

registerForm.addEventListener('submit', (event) => {
    event.preventDefault();
    ExecuteRegister(document.getElementById("registerUsername").value,
                    document.getElementById("registerPassword").value);
});

const registerUrl = "http://127.0.0.1:5000/register";
const loginUrl = "http://127.0.0.1:5000/login";

async function ExecuteLogin(login, password){
    var session_id = ""
    var error_text = document.getElementById("login_register_error");
    var loginData = {
        "user_name" : login,
        "password": password
    };
    await fetch( loginUrl,{
        method: 'POST',
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify(loginData)
    })
    .then(Response => Response.json())
    .then(responseData => {
           session_id = responseData["received_data"]["session_id"];
           const date = new Date();
           date.setTime(date.getTime() + 7 * 24 * 60 * 60 * 1000);
           openLoginPopupBtn.textContent = "Wyloguj się";
           document.cookie = 'user_id=${session_id}; expires=${date.toUTCString()}; path=/';
           error_text.textContent = "";
           error_text.style.display = 'none';
    })
    .catch(error => {

        error_text.textContent = "Niepoprawne dane logowania";
        error_text.style.display = 'block';
    })

    if(error_text.textContent != ""){
        return;
    }
    else{
        popup.style.display = 'none';
        loginForm.style.display = 'none';
        loginForm.classList.remove('active');
    }
    }



async function ExecuteRegister(login, password){
    var error_text = document.getElementById("login_register_error");
    var registerData = {
        "user_name" : login,
        "password": password
    };
    await fetch( registerUrl,
        {
        method: 'POST',
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify(registerData)
    })
    .then(Response => {
        if (!Response.ok){
            error_text = document.getElementById("login_register_error");
            error_text.textContent = "Nazwa użytkownika zajęta";
            error_text.style.display = 'block';
        }
    })
    .catch(error => {
        error_text = document.getElementById("login_register_error");
        error_text.textContent = "Nazwa użytkownika zajęta";
        error_text.style.display = 'block';
    })


    
    if(error_text.textContent != ""){
        return;
    }
    else{
        popup.style.display = 'none';
        registerForm.style.display = 'none';
        registerForm.classList.remove('active');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM is fully loaded and parsed!");
    if (CheckForUserInSession()){
        document.getElementById("login-button").textContent = "Wyloguj się";
    }
    else{
        document.getElementById("login-button").textContent = "Zaloguj się";
    }
  });
  