document.onload = () => {
    let form = document.getElementById("form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            let username = document.getElementById("username-control");
            let password = document.getElementById("password-control");
            const url = "http://127.0.0.1:5000/login/";
            if (username != '' && password != '')
                response = await sendForm({url}, username, password);
                if(response["login"] == "failed")
                    alert('Login failed');
        } catch (error) {
            console.log(error);
        }
    });
}

async function sendForm({url}, username, password) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body: JSON.stringify(username, password)
    }).then(response => {
        if (!response.ok) {
            const errorMessage = response.text();
            throw new Error(errorMessage);
        }
        else {
            return response.json().then(value => {
                return value;
            });
        }
    });
    return response;
}