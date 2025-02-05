var container = [{}];
var index = 0;

window.onload = () => {
    var submit_btn = document.getElementById("liveToastBtn");
    console.log(document.getElementsByName("name-control"));
    submit_btn.addEventListener("click", function (e) {
        //alert('ciao' + 'ciao');
        let name_pass = document.getElementsByName("name-control").firstChild.textContent;
        let username = document.getElementsByName("username-control").firstChild.textContent;
        let password = document.getElementsByName("password-control").firstChild.textContent;
        let uri = document.getElementsByName("uri-control").firstChild.textContent;
        container[index]['name'] = name_pass[0].innerHTML;
        container[index]['username'] = username[0].innerHTML;
        container[index]['password'] = password[0].innerHTML;
        container[index]['uri'] = uri[0].innerHTML;
        console.log(document.getElementsByName("name-control").firstChild.textContent);
        console.log(document.getElementsByName("username-control").firstChild.textContent);
        console.log(document.getElementsByName("password-control").firstChild.textContent);
        console.log(document.getElementsByName("uri-control").firstChild.textContent);
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

