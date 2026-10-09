const menuButton = document.getElementById("menuButton");
const nav = document.getElementById("nav");


// Mobile menu

menuButton.addEventListener("click", () => {
    nav.classList.toggle("active");
});


// Contact form

const contactForm = document.getElementById("contactForm");
const formMessage = document.getElementById("formMessage");


contactForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;


    formMessage.textContent = "Sending...";


    try {

        const response = await fetch(
            "https://minimalist-demo.onrender.com",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    message: message
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }


        formMessage.textContent =
            "Message sent successfully!";


        contactForm.reset();


    } catch (error) {

        console.error(error);

        formMessage.textContent =
            "Failed to send message. Please try again.";

    }

});
