window.onload = () => {
  /**
 * CONTROLLO LATO BACKEND DEI DATI INSERITI DALL'UTENTE E AGGIUNTA IN TABELLA DEI NUOVI CAMPI
 */
  const form = document.getElementById("form");
  form.addEventListener("submit", async (event) => {
    console.log("I\'m inside the addEventListener function!");
    event.preventDefault();
    try {
      const username = document.getElementById("user-control").value;
      const password = document.getElementById("password-control").value;
      console.log("username: " + username + "\npassword: " + password);
      if (username != '' && password != '') {
        console.log("I\'m sending data to backend!");
        const account = {
          username: username,
          password: password
        }
        const url = window.location.href;
        let response = await sendForm(url, account);
        if (response['code'] == 200){
          console.log(response['url'])
          window.location = url.replace('/login', response['url'])
        }
        else{
          alert('Utente inesistente')
        }
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
  console.log("I\'m inside sendForm function");
  console.log(JSON.stringify(account));
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(account),
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else {
      return response.json().then(value => {
        console.log(value);
        return value;
      });
    }
  });
  return response;
}