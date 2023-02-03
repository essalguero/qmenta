function getUserData() {
    //const input = document.querySelector(`#username`);
    let newUserData = new FormData();
    newUserData.append('username', 'username');

    var urlencoded = new URLSearchParams();
    urlencoded.append("username", "johndoe@mail.com");

    fetch('http://localhost:8000/patient_data?username=johndoe@mail.com', {
        method: 'get',
    })
    .then ((response) => {
        if(!response.ok) {
            console.log('There was a problem');
            return;
        }
        let responseData = response.json();
        console.log(responseData);
        console.log(document.cookie)
        return responseData;
    })
    .then ((data) => {
        console.log('Success:', data);
    })
    .catch ((error) => {
        console.error('Error:', error);
    });
}

function getUserImage() {
    fetch('http://localhost:8000/patient_image?username=johndoe@mail.com', {
        method: 'get'
    })
    .then ((response) => {
        if(!response.ok) {
            console.log('There was a problem');
            return;
        }
        let responseData = response.blob();
        console.log(responseData);
        console.log(document.cookie);
        return responseData;
    })
    .then ((data) => {

        let objectURL = URL.createObjectURL(data);
        window.open(objectURL,'Image','width=largeImage.stylewidth,height=largeImage.style.height,resizable=1');
        console.log('Success:', data);
    })
    .catch ((error) => {
        console.error('Error:', error);
    });
}
