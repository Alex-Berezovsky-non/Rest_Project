document.addEventListener('DOMContentLoaded', function() {
    // Инициализация Fancybox
    Fancybox.bind("[data-fancybox]", {
        Thumbs: {
            autoStart: true,
        },
        Toolbar: {
            display: {
                left: [],
                middle: [],
                right: ["close"],
            },
        },
    });
    
    // Ленивая загрузка изображений
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => {
        img.dataset.src = img.src;
        img.src = '';
        observer.observe(img);
    });
});