let container = {};

window.onload = () => {
  let submit_btn = document.getElementById("liveToastBtn");
  submit_btn.addEventListener("click", function (e) 
  {
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
    
    const url = "/homepage/upload/"
    fetch(url,{ 
      "method": "POST",
      "headers": {"Content-Type": "application/json"},
      "body": JSON.stringify(container)
    }).then(response =>{
      if(!response.ok){
        throw new Error("Errore")
      }
    })
    .then(data => {
      console.log(data);
    })
    .then(console.error(error))
  
  // container.forEach((object1, index, line) => {
  //   object1.forEach((internal_object, index2, line2) => {
  //     console.log(line[index][index2])
  //   });
  // });
  });
}