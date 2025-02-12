let container = {};

window.onload = () => {
/**
 * CONTROLLO LATO BACKEND DEI DATI INSERITI DALL'UTENTE E AGGIUNTA IN TABELLA DEI NUOVI CAMPI
 */
  const form = document.getElementById("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const myModal = document.getElementById('submitModal');
    const myInput = document.getElementById('submitBtn');
    const name_pass = document.getElementsByName("name-control")[0].value;
    const username = document.getElementsByName("username-control")[0].value;
    const password = document.getElementsByName("password-control")[0].value;
    const uri = document.getElementsByName("uri-control")[0].value;
    container = {
      id: 0,
      name: name_pass,
      username: username,
      password: password,
      uri: uri
    }

    console.log('name: ' + container.name);
    console.log('username: ' + container.username);
    console.log('password: ' + container.password);
    console.log('uri: ' + container.uri);
    console.log(container);
    console.log('I\'m under submit event')    
    try {
      if(name_pass != '' && username != '' && password != '' && uri != ''){
        const url = "http://127.0.0.1:5000/homepage/";
        let responseData = await postFormDataAsJson({ url });
        console.log(responseData);
        addNewPassword(responseData);
        name_pass.value = '';
        username.value = '';
        password.value = '';
        uri.value = '';

        myModal.addEventListener('shown.bs.modal', () => {
          myInput.focus()
        })
      }
      else{  
        console.log('error'); 
        myModal.addEventListener('shown.bs.modal', () => {
          myInput.focus()
        })
      }
    } catch (error) {
      console.error(error);
    }
  });
}

/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {Object} options
 * @param {string} options.url - URL to POST data to
 * @param {FormData} options.formData - `FormData` instance
 * @return {Object} - Response body from URL that was POSTed to
 */
async function postFormDataAsJson({ url }) {
  console.log('I\'m under postFormDataAsJson function')
  /**
   * 
   * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
   * 
  */
  console.log("JSON FORMAT: \n" + JSON.stringify(container));
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(container)
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else{
      return response.json().then(value => {
        return value;
      });
    }
  });

  return response;
}

function addNewPassword(data){
  let table = document.getElementById("table-body");

  /* CREATE OF FIELD AND NEW LINE INSIDE OF TABLE FOR NEW PASSWORDS */
  let line = document.createElement('tr');
  let delBtn = document.createElement('button');
  let editBtn = document.createElement('button');
  let pwdBtn = document.createElement('button');
  let link_uri = document.createElement('a');
  pwdBtn.style = "border:none;background:none;"
  link_uri.href = data['uri'];
  link_uri.target = "_blank";
  link_uri.textContent = data['uri'];
  pwdBtn.textContent = "•••••••••••";
  delBtn.classList.add("btn", "btn-danger");
  delBtn.textContent = "DELETE";
  editBtn.classList.add("btn", "btn-primary")
  editBtn.textContent = "EDIT";


  /* ADD OF NEW LINE INSIDE OF THE TABLE */
  for (i = 0; i < 7; i++){
    let field = document.createElement('th');
    field.scope = 'col';
    line.appendChild(field);
  }

  console.log(line);
  line.childNodes[0].textContent = data['id'];
  line.childNodes[0].classList.add("col-1");
  line.childNodes[5].classList.add("col-1");
  line.childNodes[6].classList.add("col-1");
  line.childNodes[1].textContent = data['name'];
  line.childNodes[2].textContent = data['username'];
  line.childNodes[3].appendChild(pwdBtn);
  line.childNodes[4].appendChild(link_uri);
  line.childNodes[5].appendChild(editBtn);
  line.childNodes[6].appendChild(delBtn);
  console.log('line: ' + line);

  table.appendChild(line);
}