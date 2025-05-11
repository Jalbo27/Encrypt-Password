window.onload = () => {
  /**
 * CONTROLLO LATO BACKEND DEI DATI INSERITI DALL'UTENTE E AGGIUNTA IN TABELLA DEI NUOVI CAMPI
 */
  const form = document.getElementById("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const username = document.getElementById("user-control").value;
      const password = document.getElementById("password-control").value;
      console.log("username: " + username + "\npassword: " + password);
      if (username != '' && password != '') {
        const account = {
          username: username,
          password: password
        }
        const url = window.location.href;
        await sendForm(url, account);
      }
    } catch (error) {
      console.log(error);
    }
  });
}

/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {FormData} options.formData - `FormData` instance
 * @return {Object} - Response body from URL that was POSTed to
 */
async function sendForm(url, account) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "X-CSRF-TOKEN": (document.cookie.split(';')?.find(row => row.startsWith('csrf_access_token='))).replace("csrf_access_token=", "")
    },
    credentials: 'same-origin',
    body: JSON.stringify(account),
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else {
      if(response.ok){
        response.json().then(value =>{
          if(value["code"] == 200)
            window.location.href = window.location.origin + `/homepage/${account['username']}`;
          else
            alert(value["message"]); 
        });
      }else if(response.status != 200){
        alert("Impossibile registrarsi")
      }
    }
  });
  return response;
}