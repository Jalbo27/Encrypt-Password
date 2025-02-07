let container = [];
let index = 0;

window.onload = () => {
  let submit_btn = document.getElementById("liveToastBtn");
  submit_btn.addEventListener("click", function (e) {
    /*const name_pass = */ console.log(document.getElementsByName("name-control")[0].value);
    const username = document.getElementsByName("username-control")[0].value;
    const password = document.getElementsByName("password-control")[0].value;
    const uri = document.getElementsByName("uri-control")[0].value;
    container.push(
      {
        //'name': name_pass, 
        'username': username,
        'password': password,
        'uri': uri
      });
    //console.log(name_pass)
    console.log('name: ' + container[index].name);
    console.log('username: ' + container[index].username);
    console.log('password: ' + container[index].password);
    console.log('uri: ' + container[index].uri);
    console.log(container);
  
  // container.forEach((object1, index, line) => {
  //   object1.forEach((internal_object, index2, line2) => {
  //     console.log(line[index][index2])
  //   });
  // });
  });
}