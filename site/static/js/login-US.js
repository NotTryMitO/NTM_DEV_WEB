// FAQ's starts
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const faqItem = question.parentNode;
  
        document.querySelectorAll('.faq-item').forEach(item => {
            if (item !== faqItem) {
                item.classList.remove('active');
            }
        });
  
        faqItem.classList.toggle('active');
    });
  });
  // FAQ's ends
  
  // hamburguer starts
  const toggleButton = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  toggleButton.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      toggleButton.classList.toggle('active');
  });
  // hamburger ends
  
  //login discord
  document.getElementById("logar-dc").onclick = function() {
    window.location.href = "/discord/login";
  };
  
  function btnalert() {
    const response = confirm("You need to log in! Do you want to continue?");
    if (response) {
      alert("Redirecting to the login page...");
      window.location.href = "/discord/login";
    } else {
      alert("Operation canceled.");
    }
  }
  
  function translatorbtn() {
    window.location.href = "/site/templates/login-PT.html";
  }