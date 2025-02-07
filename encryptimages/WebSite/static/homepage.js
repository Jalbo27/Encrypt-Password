var container = [{}];
var index = 0;

window.onload = () => {
  let submit_btn = document.getElementById("liveToastBtn");
  submit_btn.addEventListener("click", function (e) {
  let name_pass = document.getElementsByName("name-control").value;
  let username = document.getElementsByName("username-control")[0].value;
  let password = document.getElementsByName("password-control")[0].value;
  let uri = document.getElementsByName("uri-control")[0].value;
  container[index]['name'] = name_pass;
  container[index]['username'] = username;
  container[index]['password'] = password;
  container[index]['uri'] = uri;
  console.log(name_pass);
  console.log(username);
  console.log(password);
  console.log(uri);
  alert(toString(name_pass) + ' ' + toString(username) + ' ' + toString(password) + ' ' + toString(uri));
  // container.forEach((element) => {
  //     console.log(typeof (element))
  //     if (element === String && element != "")
  //         return true;
  //     else {
  //         alert('Dei campi sono vuoti oppure sono errati');
  //         return false;
  //     }
  // })         
});
}