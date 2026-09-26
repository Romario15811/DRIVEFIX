const bookingForm = document.querySelector("#booking-form");

const nameInput = document.querySelector("#client-name");
const phoneInput = document.querySelector("#client-phone");
const carInput = document.querySelector("#client-car");
const serviceInput = document.querySelector("#client-service");

const formMessage = document.querySelector("#form-message");
const submitButton = bookingForm.querySelector('button[type="submit"]');


bookingForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    clearMessage();

    const clientData = {
        name: nameInput.value.trim(),
        phone: phoneInput.value.trim(),
        car: carInput.value.trim(),
        service: serviceInput.value
    };


    // Проверка имени

    if (clientData.name.length < 2) {
        showMessage(
            "Введите корректное имя.",
            "error"
        );

        nameInput.focus();

        return;
    }


    // Проверка телефона

    if (!isValidPhone(clientData.phone)) {
        showMessage(
            "Введите корректный номер телефона.",
            "error"
        );

        phoneInput.focus();

        return;
    }


    // Проверка услуги

    if (clientData.service === "") {
        showMessage(
            "Выберите услугу.",
            "error"
        );

        serviceInput.focus();

        return;
    }


    // Пока вместо сервера смотрим данные в консоли

    submitButton.disabled = true;
    submitButton.textContent = "Отправляем...";

    showMessage(
        "Отправляем заявку. Это может занять несколько секунд...",
        ""
    );

    try {

        const response = await fetch(
            "https://drivefix-api-pwn5.onrender.com/api/booking",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(clientData)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.message || "Ошибка отправки заявки."
            );
        }

        showMessage(
            "Заявка успешно отправлена! Мы свяжемся с вами.",
            "success"
        );

        bookingForm.reset();

    } catch (error) {
        console.error("Ошибка:", error);

        showMessage(
            "Не удалось отправить заявку. Попробуйте ещё раз или свяжитесь с нами по телефону.",
            "error"
        );
    } finally {

        submitButton.disabled = false;
        submitButton.textContent = "Отправить заявку";
    }
});


function isValidPhone(phone) {

    const cleanedPhone = phone.replace(/[\s()-]/g, "");

    const phonePattern = /^\+?\d{10,15}$/;

    return phonePattern.test(cleanedPhone);
}


function showMessage(text, type) {

    formMessage.textContent = text;

    formMessage.className = type;
}


function clearMessage() {

    formMessage.textContent = "";

    formMessage.className = "";
}

const menuButton = document.querySelector("#menu-button");
const nav = document.querySelector("#nav");
const navLinks = document.querySelectorAll("#nav a");


menuButton.addEventListener("click", function() {

    nav.classList.toggle("active");
    menuButton.classList.toggle("active");

});


navLinks.forEach(function(link) {

    link.addEventListener("click", function() {

        nav.classList.remove("active");
        menuButton.classList.remove("active");

    });

});