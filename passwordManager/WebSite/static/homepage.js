let container = {};
let url = window.location.href;
let url_login = window.location.href.replace('/homepage/', '/login')

window.onload = () => {
  /**
   * CONTROLLO DELLA LOGIN ESEGUITA DALL'UTENTE
   */
  if (document.getElementById("form-login") != null)
  {
    const form_login = document.getElementById("form-login");
    form_login.addEventListener("submit", async (event) =>{
      console.log("I\'m inside the addEventListener function!");
      event.preventDefault();
      try {
        const username = document.getElementById("user-control").value;
        const password = document.getElementById("password-control").value;
        if (username != '' && password != '') {
          console.log("I\'m sending data to backend!");
          console.log(url_login)
          const account = {
            username: username,
            password: password
          }
          let response = await sendLogin( account);
          if (response['code'] == 200){
            console.log(response['url'])
            window.location = url_login.replace('/login', response['url'])
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
   * CONTROLLO LATO BACKEND DEI DATI INSERITI DALL'UTENTE E AGGIUNTA IN TABELLA DEI NUOVI CAMPI
   */
  const form_element = document.getElementById("form-element");
  form_element.addEventListener("submit", async (event) => {
    event.preventDefault();
    let name_pass = document.getElementsByName("name-control")[0].value;
    let username = document.getElementsByName("username-control")[0].value;
    let password = document.getElementsByName("password-control")[0].value;
    let uri = document.getElementsByName("uri-control")[0].value;
    let number;
    if (document.getElementById('table-body').childNodes.length >= 2)
      number = parseInt(document.getElementById('table-body').lastChild.childNodes[0].textContent);
    else
      number = -1;

    container = {
      action: 'submit',
      id: number,
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
    console.log('I\'m under submit event');

    try {
      if (name_pass != '' && username != '' && password != '' && uri != '') {
        let responseData = await sendForm();
        //console.log(responseData);
        if (responseData['status'] == 'Ok') {
          addNewPassword(responseData);
        }
        else {
        }
      }
      else {
        console.log('error');
      }
    } catch (error) {
      console.error(error);
    }
  });
}

/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {FormData} formData - `FormData` instance
 * @return {Object} - Response body from URL that was POSTed to
 */
async function sendLogin( account) {
  console.log("I\'m inside sendLogin function");
  console.log(JSON.stringify(account));
  console.log(typeof(url_login));
  const response = await fetch(url_login, {
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

/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {object}
 * @param {String} options.url
 * @param {FormData} options 
 * @return {Object} - Response body from URL that was POSTed to
 */
async function sendForm() {
  console.log('I\'m under sendForm function');
  /**
   * 
   * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
   * 
  */
  console.log("JSON FORMAT: \n" + JSON.stringify(container));
  console.log(url)
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-Post": "application/json"
    },
    body: JSON.stringify(container)
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else {
      return response.json().then(value => {
        //console.log(value)
        return value;
      });
    }
  });

  return response;
}

/**
 * 
 */
async function manageElement(event, id, action) {
  event.preventDefault();
  requestAction = {
    action: action,
    id: id
  }
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-Post": "application/json"
    },
    body: JSON.stringify(requestAction)
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else {
      return response.json().then(value => {
        console.log(value)
        return value;
      });
    }
  });
}

function addNewPassword(data) {
  let table = document.getElementById("table-body");

  /* CREATE OF FIELD AND NEW LINE INSIDE OF TABLE FOR NEW PASSWORDS */
  let line = document.createElement('tr');
  let delBtn = document.createElement('button');
  let editBtn = document.createElement('button');
  let pwdBtn = document.createElement('button');
  let link_uri = document.createElement('a');
  pwdBtn.style = "border:none;background:none;";
  link_uri.href = data['uri'];
  link_uri.target = "_blank";
  link_uri.textContent = data['uri'];
  pwdBtn.textContent = "•••••••••••";
  delBtn.classList.add("btn", "btn-danger");
  delBtn.textContent = "DELETE";
  delBtn.setAttribute("id", `delete-${data["id"]}`);
  delBtn.addEventListener('click', manageElement(event, data["id"], "delete"));
  editBtn.classList.add("btn", "btn-primary");
  editBtn.textContent = "EDIT";
  editBtn.setAttribute("id", `edit-${data["id"]}`);
  editBtn.addEventListener('click', manageElement(event, data["id"], "edit"));


  /* ADD OF NEW LINE INSIDE OF THE TABLE */
  for (i = 0; i < 7; i++) {
    let field = document.createElement('th');
    field.scope = 'col';
    line.appendChild(field);
  }

  /**
   * ADD OF CONTENT SENT BY BACKEND TO THE FIELDS OF THE NEW LIÌNE
   */
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

  table.appendChild(line);
}