class Login {
    constructor(form, fields) {
        this.form = form;
        this.fields = fields;
        this.validateOnSubmit();
    }

    validateOnSubmit() {
        let self = this;

        this.form.addEventListener("submit", (e) => {
            e.preventDefault();
            var error = 0;
            self.fields.forEach((field) => {
                const input = document.querySelector(`#${field}`);
                //console.log(input.value);
                if (self.validateFields(input) == false){
                    error++;
                }
            });

            let newUserData = new FormData();
            //console.log("fields: ", self.fields);
            self.fields.forEach((field) => {
                const input = document.querySelector(`#${field}`);
                console.log(field, input.value);
                newUserData.append(field, input.value);
            });
            //console.log("newUserData: ", newUserData)

            //newUserData.append('username', document.querySelector(self.fields[0]).value);
            //newUserData.append('password', self.fields[1]);

            if (error == 0) {
                // do login
                //localStorage.setItem("auth", 1)
                //this.form.submit();
                //console.log("Sending data: ", newUserData);
                fetch('http://localhost:8000/logging', {
                    method: 'post',
                    /*headers: {
                        //'Content-Type': 'application/json'
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },*/
                    //body: JSON.stringify('username={username}&password={password}'),
                    body: newUserData
                })
                  //.then(response => response.json())
                  .then ((response) => {
                    if(!response.ok) {
                        console.log('There was a problem');
                        return;
                    }
                    let responseData = response.json();
                    let cookie_value = document.cookie;
                    console.log('Cookie', cookie_value);
                    //console.log(responseData);
                    //console.log(document.cookie)
                    //console.log(newUserData.get('username'));
                    //window.location = 'user.html?username=' + newUserData.get('username');
                    var divElement = document.getElementById('buttonsClass');
                    divElement.style.visibility='visible';
                    var divForm = document.getElementById('loginForm');
                    divForm.style.visibility='hidden';
                  })
                  .then ((data) => {
                    console.log('Success:', data);
                  })
                  .catch ((error) => {
                    console.error('Error:', error);
                  });
            } else {
                console.log("Error Getting data");
            }
        });
    }

    validateFields(field) {
        if (field.value.trim() == "") {
            this.setStatus(
                field,
                `${field.previousElementSibling.innerText} cannot be blank`,
                "error"
            );
            return false;
        } else {
            if (field.type == "password") {
                if (field.value.length < 1) {
                    this.setStatus(
                        field,
                        `${field.previousElementSibling.innerText} must be at least 1 characters`,
                        "error"
                    );
                } else {
                    this.setStatus(field, null, "success")
                    return true;
                }
            } else {
                this.setStatus(field, null, "success")
                return true;
            }
        }
    }

    setStatus(field, message, status) {
        const errorMessage = field.parentElement.querySelector(".error-message");

        if (status == "success") {
            if (errorMessage) {
                errorMessage.innerText = "";
            }
            field.classList.remove("input-error");

        }

        if (status == "error") {
            errorMessage.innerText = message;
            field.classList.add("input-error");
        }
    }
};

const form = document.querySelector(".loginForm");
if (form) {
    const fields = ["username", "password"];
    const validator = new Login(form, fields);

}
