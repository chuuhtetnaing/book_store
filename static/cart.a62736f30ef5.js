document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const currency = document.querySelector('#currency').value;
        // request.open('POST', '/store/view_cart');

        // request.onload = () => {

        //     const data = JSON.parse(request.responseText);

        //     if (data.success) {
        //         const contents = `1 USD is equal to ${data.rate} ${currency}.`
        //         document.querySelector('#result').innerHTML = contents;
        //     }
        //     else {
        //         document.querySelector('#result').innerHTML = 'There was an error.';
        //     }
        // }

        // const data = new FormData();
        // data.append('currency', currency);

        // request.send(data);
        return false;
    };

});
