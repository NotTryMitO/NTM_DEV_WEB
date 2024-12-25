document.addEventListener("DOMContentLoaded", () => {
    const resources = {
        en: {
            translation: {
                "titulo-pag": "NTM DEV | Quality Bots",
                "nav-inicio": "Home",
                "nav-bots": "Bots",
                "nav-avaliacoes": "Reviews",
                "faq": "FAQ",
                "title-1": "By the creators of NTM DEV",
                "title-2": "Get your BOT<br> in record time.",
                "title-3": "Discord bots skillfully designed and crafted by NTM DEV creators. The perfect team to develop your BOT.",
                "price-title": "Discover our BOTs",
                "price-description": "Below you can see our plans and choose the one that best suits your needs.",
                "nome-price-1": "SUGGESTION",
                "price-price-1": "1€ <span>/month *</span>",
                "description-price-1": "Ideal for efficiently managing suggestions and facilitating decision-making.",
                "plan-1": "Automatic notifications of new suggestions",
                "plan-2": "Integration with Discord channels for direct management",
                "plan-3": "Receive and store suggestions in real time",
                "botao-sell": "Buy",
                "popular": "Most Popular",
                "nome-price-2": "CUSTOM COMMANDS",
                "price-price-2": "3€ <span>/month *</span>",
                "description-price-2": "For those who want to create exclusive custom commands, offering more control and flexibility.",
                "plan-4": "Automatic response with dynamic content",
                "plan-5": "Integration with variables for advanced customization",
                "plan-6": "Permission control for different roles",
                "nome-price-3": "ANTI-LINKS",
                "price-price-3": "2€ <span>/month *</span>",
                "description-price-3": "Protect your server from unwanted and potentially dangerous links, maintaining security and integrity.",
                "plan-7": "Automatic blocking of malicious links",
                "plan-8": "Admin notification of removed links",
                "plan-9": "Integration with logs for full auditing",
                "review-title": "See our reviews",
                "review-description": "Below you can check the reviews of some of our customers.",
                "review-1": "I have no words to express my satisfaction with the work done! I thank you immensely for the excellent service provided. Exceptional quality and top-notch service!",
                "review-2": "The bot developed exceeded all my expectations! It responds quickly and was created with all the desired features. Exceptional service!",
                "review-3": "The bot is excellent, with impeccable setup and clean design. Attentive and helpful service. Highly recommend!",
                "review-4": "The result is impeccable. You can buy without fear!",
                "faq-title": "Do you have a question?",
                "faq-description": "Below, you can see the most frequently asked questions.",
                "faq-1": "How can I buy a bot for Discord?",
                "faq-des-1": "Purchases can be made directly through our Discord. Just select the desired bot, open a TICKET, provide your request, and follow the instructions!",
                "faq-2": "Is it possible to request a refund after purchase?",
                "faq-des-2": "We do not offer refunds after purchase, but we guarantee full support to resolve any issues you may encounter.",
                "faq-3": "Can I resell or distribute the purchased bots?",
                "faq-des-3": "Reselling or distributing the purchased bots is not allowed, according to the agreed terms of use.",
                "faq-4": "What is the time frame for maintaining the budget and the amount paid?",
                "faq-des-4": "The budget and the amount paid remain valid for 7 working days from the approval date.",
                "faq-5": "What are the copyright rights to the purchased bots?",
                "faq-des-5": "Copyrights are reserved for the developer, but you will have full usage rights as per the contract terms."
            }
        },
        pt: {
            translation: {
                
            }
        }
    };

    // Inicializa o i18next
    i18next.init({
        lng: "pt",
        resources
    }, (err, t) => {
        if (err) return console.error(err);
        translateContent();
    });

    // Função para traduzir os elementos da página
    function translateContent() {
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            el.innerHTML = i18next.t(key);
        });
    }

    // Listener para troca de idioma
    document.querySelectorAll("[data-lang]").forEach(btn => {
        btn.addEventListener("click", () => {
            const lang = btn.getAttribute("data-lang");
            i18next.changeLanguage(lang, translateContent);
        });
    });
});
