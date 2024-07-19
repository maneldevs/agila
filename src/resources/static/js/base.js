async function showErrorMessage(response) {
    let message = 'Some error happened';
    const toastEl = document.getElementById('errorToast');
    const toast = new bootstrap.Toast(toastEl);
    toastMessageEl = document.getElementById('errorToastMessage');
    const error = await response.json() 
    if (response.status == 422) {
        message = (error.detail[0].loc[1] + ": " + error.detail[0].msg);
    } else {
        if (error.message) {
            message = error.message;
        }
    }
    toastMessageEl.textContent = message;
    toast.show();
}