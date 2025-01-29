const elementos = document.querySelectorAll('.animacion');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('animacion-visible');
            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 1
});

elementos.forEach(el => observer.observe(el));

const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
