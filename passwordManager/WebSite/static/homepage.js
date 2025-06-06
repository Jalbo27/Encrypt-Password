let container = {};
let url = window.location.href;
let url_login = window.location.origin + '/login';

window.onload = () => {
  /**
   * CONTROLLO DELLA LOGIN ESEGUITA DALL'UTENTE
   */
  if (document.getElementById("form-login") != null) {
    const form_login = document.getElementById("form-login");
    form_login.addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        const username = document.getElementById("user-control").value;
        const password = document.getElementById("password-control").value;
        if (username != '' && password != '') {
          const account = {
            username: username,
            password: password
          }
          await sendLogin(account);
        }
      } catch (error) {
        console.log(error);
      }
    });
  }

  /**
   * CHECK IF THE FORM IS CORRECTLY FORMATTED AND SEND THE DATA TO THE BACKEND
   */
  const form_element = document.getElementById("form-element");
  form_element.addEventListener("submit", async (event) => {
    event.preventDefault();
    let name_pass = document.getElementsByName("name-control")[0].value;
    let username = document.getElementsByName("username-control")[0].value;
    let password = document.getElementsByName("password-control")[0].value;
    let uri = document.getElementsByName("uri-control")[0].value;
    let number;
    /**
     * GET LAST ID OF PASSSWORD TO UPDATE THE DATABASE AND FRONTEND
     */
    if (document.getElementById('table-body').childNodes.length >= 2) {
      let table = document.getElementById('table-body');
      let last_line = table.getElementsByTagName('tr');
      let lenght = last_line.length - 1
      number = parseInt(last_line.item(lenght).firstElementChild.textContent);
    }
    else
      number = -1;

    container = {
      action: 'submit',
      id: number,
      name: name_pass,
      username: username,
      password: password,
      uri: uri
    };

    try {
      if (name_pass != '' && username != '' && password != '' && uri != '') {
        let responseData = await sendForm();
        if (responseData['code'] == 200) {
          addNewPassword(responseData['id']);
        }
        else if (responseData['code'] == 401){
          alert(responseData['message'])
        }
      }
      else {
        console.log('error');
      }
    } catch (error) {
      console.error(error);
    }
  });

  /**
    * ADD THE EVENT TO THE ALL BUTTONS TO DELETE OR EDIT
    */
  let editbtns = document.getElementsByClassName('btn btn-warning');
  let delbtns = document.getElementsByClassName('btn btn-danger');
  Array.prototype.map.call(editbtns, element => { element.addEventListener("click", modifyElement) });
  Array.prototype.map.call(delbtns, element => { element.addEventListener("click", modifyElement) });

  /**
   * ADD THE EVENT TO THE EYE VIEW PASSWORD TOGGLE
   */
  document.querySelectorAll('.togglePassword').forEach(el => {
    el.addEventListener('click', e => {
      let password = el.parentElement.getElementsByClassName('form-control')[0];
      const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
      password.setAttribute('type', type);
      e.target.classList.toggle('fa-eye-slash');
    });
  });


  /**
   * GENERATE RANDOM PASSWORD
   */
  let dice_generator = document.getElementById('button-addon1-control');
  dice_generator.addEventListener('click', () =>{
    document.getElementsByName("password-control")[0].value = Math.random().toString(36).substring(2,20); 
  });

  // /**
  //  * PASSWORD TOGGLE VIEW
  //  */
  // let eye_toggle = document.getElementsByName("eye-pwd-control");
  // Array.prototype.map.call(eye_toggle, element => { element.addEventListener("click", () => {
  //   let password = element.parentElement.childNodes[1];
  //   let hiddenpwd = document.getElementsByClassName("password-value")[0].value;
  //   console.log(password);
  //   console.log(hiddenpwd);
  //   const type = document.getElementById('eye-toggle').className === 'bi-eye-slash' ? 'bi-eye' : 'bi-eye-slash';
  //   console.log(type);
  //   if (type == 'bi-eye-slash'){
  //     document.getElementById('eye-toggle').className.replace("bi-eye-slash", "bi-eye");
  //     password.textContent = hiddenpwd;
  //   }
  //   else{
  //     document.getElementById('eye-toggle').className.replace("bi-eye", "bi-eye-slash");
  //     password.textContent = "•••••••••••";  
  //   }
  // });});


  /**
   * ADD THE EVENT TO THE EYE VIEW PASSWORD TOGGLE TO THE TABLE
   */
  document.getElementsByName("eye-pwd-control").forEach(el => {
    el.addEventListener('click', e => {
      let password = el.parentElement.getElementsByTagName('input')[0];
      //let password = el.parentElement.getElementsByClassName('password-control')[0];
      const type = el.firstChild.className === 'bi bi-eye-slash' ? 'bi bi-eye' : 'bi bi-eye-slash';
      if (type == 'bi bi-eye-slash'){
        password.setAttribute("type", "text");
        type.replace("bi bi-eye-slash", "bi bi-eye");
      }
      else{
        password.setAttribute("type", "password");
        type.replace("bi bi-eye", "bi bi-eye-slash");
      }
    });
  });
}


/**
 * Helper function for POSTing data as JSON with fetch.
 *
 * @param {FormData} options.formData - `FormData` instance
 * @return {Object} - Response body from URL that was POSTed to
 */
async function sendLogin(account) {
  const response = await fetch(url_login, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    credentials: 'same-origin',
    body: JSON.stringify(account),
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else if(response.ok && response.status == 200){
      window.location.href = window.location.origin + `/homepage/${account['username']}`;
    }
    else{
      alert("Impossibile effettuare il login");
    }
  });
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
  /**
   * 
   * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
   * 
  */
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "X-CSRF-TOKEN": (document.cookie.split(';')?.find(row => row.startsWith('csrf_access_token='))).replace("csrf_access_token=", ""),
    },
    credentials:'same-origin',
    body: JSON.stringify(container)
  }).then(async response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else if(response.ok){
      const value = await response.json();
      return value;
    }
  });

  return response;
}

/**
 * @param {HTMLElement} e 
 * @return {Object} 
 */
async function modifyElement(e) {
  e.preventDefault();
  let btnId = e.target.getAttribute('id');
  requestAction = {
    action: e.target.dataset.action,
    id: btnId,
  };
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept-Post": "application/json",
      "X-CSRF-TOKEN": (document.cookie.split(';')?.find(row => row.startsWith('csrf_access_token='))).replace("csrf_access_token=", ""),
    },
    credentials: "same-origin",
    body: JSON.stringify(requestAction)
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
    else {
      return response.json().then(value => {
        if(value['code'] == 200)
        {
          if (value['message'].includes("deleted")){
            let column = e.target.parentElement;
            let row = e.target.parentElement.parentElement;
            let table = document.getElementById("table-body");
            let table_rows = table.getElementsByTagName("tr")
            column.removeChild(e.target)
            row.removeChild(column);
            table.removeChild(row);
            Array.prototype.map.call(table_rows, element => {
              let row_cur_id = parseInt(element.childNodes[0].textContent);
              if(row_cur_id > parseInt(btnId)){
                element.childNodes[0].textContent = String(row_cur_id - 1);
                element.childNodes[6].firstElementChild.setAttribute("id", String(row_cur_id - 1)); 
              }
            });
          }
        }else if (value['message'].includes("edited")){
          e.target.textContent = value['new'];
        }else
          return ;
      });
    }
  })
}

/**
 * ADD A NEW LINE TO THE TABLE WITH THE PASSWORD INSERTED BY USER
 */
function addNewPassword(id) {
  let table = document.getElementById("table-body");

  /* CREATE OF FIELD AND NEW LINE INSIDE OF TABLE FOR NEW PASSWORDS */
  let line = document.createElement('tr');
  let delBtn = document.createElement('button');
  let editBtn = document.createElement('button');
  let pwdBtn = document.createElement('button');
  let link_uri = document.createElement('a');
  let eyeBtn = document.createElement('button');
  let svgImg = document.createElement('i');
  eyeBtn.classList.add("btn", "btn-outline-secondary");
  eyeBtn.setAttribute("type", "button");
  eyeBtn.setAttribute("id", "eye-toggle");
  eyeBtn.setAttribute("name", "eye-pwd-control");
  eyeBtn.style.border = "none";
  svgImg.classList.add("bi", "bi-eye-slash");
  eyeBtn.appendChild(svgImg);
  pwdBtn.setAttribute("id", "password-btn");
  pwdBtn.classList.add("form-control");
  pwdBtn.textContent = "•••••••••••";
  pwdBtn.addEventListener('click', () => { navigator.clipboard.writeText(container.password) });
  eyeBtn.addEventListener('click', () => {
    if(svgImg.classList.contains("bi-eye-slash")){
      pwdBtn.textContent = container.password;
      svgImg.classList.replace("bi-eye-slash", "bi-eye");
    }else{
      pwdBtn.textContent = "•••••••••••";
      svgImg.classList.replace("bi-eye", "bi-eye-slash");
    }
  });
  link_uri.href = container.uri;

  link_uri.target = "_blank";
  link_uri.textContent = container.uri;
  delBtn.classList.add("btn", "btn-danger");
  delBtn.textContent = "DELETE";
  delBtn.setAttribute("id", `${id}`);
  delBtn.setAttribute("type", "button");
  delBtn.setAttribute("data-action", "delete");
  delBtn.addEventListener('click', modifyElement);
  editBtn.classList.add("btn", "btn-warning");
  editBtn.textContent = "EDIT";
  editBtn.setAttribute("id", `${id}`);
  editBtn.setAttribute("data-action", "edit");
  editBtn.setAttribute("type", "button");
  editBtn.addEventListener('click', modifyElement);

  /* ADD OF NEW LINE INSIDE OF THE TABLE */
  for (i = 0; i < 7; i++) {
    let field = document.createElement('th');
    field.scope = 'col';
    line.appendChild(field);
  }

  /**
   * ADD OF CONTENT SENT BY BACKEND TO THE FIELDS OF THE NEW LIÌNE
   */
  line.childNodes[0].textContent = id;
  line.childNodes[0].classList.add("col-1");
  line.childNodes[5].classList.add("col-1");
  line.childNodes[6].classList.add("col-1");
  line.childNodes[1].textContent = container.name;
  line.childNodes[2].textContent = container.username;
  line.childNodes[3].appendChild(pwdBtn);
  line.childNodes[3].appendChild(eyeBtn);
  line.childNodes[4].appendChild(link_uri);
  line.childNodes[5].appendChild(editBtn);
  line.childNodes[6].appendChild(delBtn);

  table.appendChild(line);
}
