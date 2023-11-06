import fetch from 'node-fetch';

const apiUrl = "http://127.0.0.1:8000/login"; // Замените на ваш URL

const userData = {
    username: "user123",
    password: "123",
};

const requestOptions = {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
};

fetch(apiUrl, requestOptions)
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        if (data.message === "Пользователь авторизовался успешно.") {
            // Авторизация прошла успешно
        } else {
            console.error("Ошибка авторизации:", data.detail);
        }
    })
    .catch((error) => {
        console.error("Ошибка при выполнении запроса:", error);
    });
