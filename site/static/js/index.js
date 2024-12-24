// links/buttons starts
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button');
      buttons.forEach(button => {
          button.addEventListener('click', event => {
              window.open('https://discord.com/channels/1307354161737629696/1307362255532200086', '_blank');
          });
      });
    });
  
    // links/buttons ends
    document.querySelectorAll('.faq-question').forEach(question => {
      question.addEventListener('click', () => {
          const faqItem = question.parentNode;
  
          // Fecha outras FAQs abertas
          document.querySelectorAll('.faq-item').forEach(item => {
              if (item !== faqItem) {
                  item.classList.remove('active');
              }
          });
  
          // Alterna a classe 'active' para a FAQ clicada
          faqItem.classList.toggle('active');
      });
  });
  //logout
  document.getElementById("logout-btn").addEventListener("click", () => {
    logout();
  })
  
  function logout() {
      const resposta = confirm("Tens a certeza que queres sair?");
      if (resposta) {
          alert("A sair...");
          window.location.href = "/logout";
      } else {
          alert("Cancelaste esta operação");
      }
  }
  // Alterna o menu no mobile
  const toggleButton = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');
  
  toggleButton.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      toggleButton.classList.toggle('active');
  });
  
  // Adiciona efeito ao rolar
  window.addEventListener('scroll', () => {
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 50) {
          navbar.classList.add('scrolled');
      } else {
          navbar.classList.remove('scrolled');
      }
  });
  
  // smooth scroll starts
  function smoothScrollTo(target) {
      const startPosition = window.scrollY;
      const targetPosition = target.getBoundingClientRect().top + startPosition;
      const distance = targetPosition - startPosition;
      const duration = 800;
      const startTime = performance.now();
  
      function animation(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        const ease = easeInOutCubic(progress);
        window.scrollTo(0, startPosition + distance * ease);
  
        if (progress < 1) {
          requestAnimationFrame(animation);
        }
      }
  
      function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      }
  
      requestAnimationFrame(animation);
    }
  
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        smoothScrollTo(target);
      });
    });
    // smooth scroll ends
    //comprar starts
    document.getElementById("btn-sell-1").addEventListener("click", async () => {
      try {
          const response = await fetch("/comprar", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
          });
          const data = await response.json();
          if (data.success) {
              alert("Verifique sua mensagem no Discord.");
          } else {
              alert(`Erro: ${data.message}`);
          }
      } catch (error) {
          console.error("Erro na requisição:", error);
          alert("Ocorreu um erro ao processar sua compra.");
      }
  });
  
  document.getElementById("btn-sell-2").addEventListener("click", async () => {
    try {
        const response = await fetch("/comprar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        if (data.success) {
            alert("Verifique sua mensagem no Discord.");
        } else {
            alert(`Erro: ${data.message}`);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Ocorreu um erro ao processar sua compra.");
    }
  });
  
  document.getElementById("btn-sell-3").addEventListener("click", async () => {
    try {
        const response = await fetch("/comprar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        });
        const data = await response.json();
        if (data.success) {
            alert("Verifique sua mensagem no Discord.");
        } else {
            alert(`Erro: ${data.message}`);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Ocorreu um erro ao processar sua compra.");
    }
  });
  //comprar ends