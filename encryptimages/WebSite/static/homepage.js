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

    // const url = "http://127.0.0.1:5000/homepage/"
    // fetch(url,{
    //   method: "POST",
    //   headers: {"Content-Type": "application/json"},
    //   body: JSON.stringify(container)
    // }).then(response =>{
    //   if(!response.ok){
    //     throw new Error("Errore")
    //   }
    // })
    // .then(data => {
    //   console.log(data);
    // })
    //.then(console.error(error))

    // container.forEach((object1, index, line) => {
    //   object1.forEach((internal_object, index2, line2) => {
    //     console.log(line[index][index2])
    //   });
    // });
  });

  const form = document.getElementById("form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log('I\'m under submit event')
    const form = event.currentTarget;
    const url = "http://127.0.0.1:5000/homepage/0"      
    try {
      const formData = new FormData(form);
      const responseData = await postFormDataAsJson({ url, formData })
      console.log({ responseData });
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
async function postFormDataAsJson({ url, formData }) {
  console.log('I\'m under postFormDataAsJson function')
  /**
   * We can't pass the `FormData` instance directly to `fetch`
   * as that will cause it to automatically format the request
   * body as "multipart" and set the `Content-Type` request header
   * to `multipart/form-data`. We want to send the request body
   * as JSON, so we're converting it to a plain object and then
   * into a JSON string.
   * 
   * @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries
   * @see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
   */
  //const plainFormData = Object.fromEntries(formData.entries());
  //const formDataJsonString = JSON.stringify(container);
  console.log("JSON FORMAT: \n" + JSON.stringify(container));
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(container),
  }).then(response => {
    if (!response.ok) {
      const errorMessage = response.text();
      throw new Error(errorMessage);
    }
  }).then( response => {
    console.log(response.json())
  })

  return response.json();
}
