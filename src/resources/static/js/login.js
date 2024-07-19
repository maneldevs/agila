window.addEventListener('DOMContentLoaded', (event) => {
    let loginBtn = document.getElementById("login-btn");
    loginBtn.addEventListener("click", performLogin);
});

async function performLogin(event) {
    event.preventDefault()
    const usernameIpt = document.getElementById("login-username")
    const passwordIpt = document.getElementById("login-password")
    // const options = {
    //     method: 'POST',
    //     mode: 'cors',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({ // TODO pasar como form data
    //         username: usernameIpt.value,
    //         password: passwordIpt.value
    //     })
    // }
    let formData = new FormData()
    formData.append('username', usernameIpt.value)
    formData.append('password', passwordIpt.value)
    const options = {
        method: 'POST',
        mode: 'cors',
        body: formData
    }
    let response = await fetch(window.urlBase + 'auth/login', options);
    if (response && response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token)
        window.location.href = window.urlBase + 'admin/home'
    } else {
        showErrorMessage(response)
    }
}
