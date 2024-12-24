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
    //login discord
    document.getElementById("logar-dc").onclick = function() {
      window.location.href = "/discord/login";
    };
    //login discord
    document.getElementById("btn-sell-1").onclick = function () {
      exibirAlerta();
    };

    document.getElementById("btn-sell-2").onclick = function () {
      exibirAlerta();
    };

    document.getElementById("btn-sell-3").onclick = function () {
      exibirAlerta();
    };

    function exibirAlerta() {
      const resposta = confirm("Tens que fazer login! Desejas continuar?");
      if (resposta) {
        alert("Redirecionando para a página de login...");
        window.location.href = "/discord/login";
      } else {
        alert("Operação cancelada.");
      }
    }
