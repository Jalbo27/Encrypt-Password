let container = {};

window.onload = () => {
  let submit_btn = document.getElementById("liveToastBtn");
  submit_btn.addEventListener("click", function (e) {
    const name_pass = document.getElementsByName("name-control")[0].value;
    const username = document.getElementsByName("username-control")[0].value;
    const password = document.getElementsByName("password-control")[0].value;
    const uri = document.getElementsByName("uri-control")[0].value;
    container = {
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
  });

  const form = document.getElementById("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log('I\'m under submit event')
    const url = "http://127.0.0.1:5000/homepage/"      
    try {
      let responseData = await postFormDataAsJson({ url })
      console.log(responseData);
      addNewPassword(responseData);
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
  // table.firstElementChild.childNodes[3].textContent = data['name'];
  // table.firstElementChild.childNodes[5].textContent = data['username'];
  // table.firstElementChild.childNodes[7].textContent = data['password'];
  // table.firstElementChild.childNodes[9].textContent = data['uri'];

  /* CREATE OF FIELD AND NEW LINE INSIDE OF TABLE FOR NEW PASSWORDS */
  let line = document.createElement('tr');
  let field = document.createElement('th');
  field.scope = 'col';
  console.log(field)
  // let field_id = document.createElement('th');
  // let field_name = document.createElement('th');
  // let field_username = document.createElement('th');
  // let field_password = document.createElement('th');
  // let field_uri = document.createElement('th');
  let delBtn = document.createElement('button');
  let editBtn = document.createElement('button');

  /* ADD OF NEW LINE INSIDE OF THE TABLE */
  for (i = 0; i < 7; i++)
    line.append(field);

  console.log(line);
  line.childNodes[0].textContent = 0;
  line.childNodes[0].classList.add("col-1");
  line.childNodes[5].classList.add("col-1");
  line.childNodes[6].classList.add("col-1");
  line.childNodes[1].textContent = data['name'];
  line.childNodes[2].textContent = data['username'];
  line.childNodes[3].textContent = data['password'];
  line.childNodes[4].textContent = data['uri'];
  line.childNodes[5].appendChild(editBtn.classList.add("btn btn-primary"));
  line.childNodes[6].appendChild(delBtn.classList.add("btn btn-danger"));
  console.log('line: ' + line);

  table.appendChild(line);
}