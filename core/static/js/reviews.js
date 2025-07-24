document.addEventListener('DOMContentLoaded', () => {
    const starRating = document.querySelector('.star-rating');
    if (!starRating) return;

    const stars = starRating.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating-input');
    if (!stars.length || !ratingInput) return;

    // Функции для работы с состоянием
    const setRating = (value) => {
        ratingInput.value = value;
        updateStars();
    };

    const updateStars = () => {
        const currentValue = parseInt(ratingInput.value) || 0;
        stars.forEach(star => {
            const starValue = parseInt(star.getAttribute('data-value'));
            star.classList.toggle('active', starValue <= currentValue);
            star.classList.remove('hover');
        });
    };

    // Обработчики событий
    stars.forEach(star => {
        star.addEventListener('click', (e) => {
            e.preventDefault();
            setRating(parseInt(star.getAttribute('data-value')));
        });

        star.addEventListener('mouseover', () => {
            const hoverValue = parseInt(star.getAttribute('data-value'));
            stars.forEach(s => {
                const sValue = parseInt(s.getAttribute('data-value'));
                s.classList.toggle('hover', sValue <= hoverValue);
            });
        });
    });

    starRating.addEventListener('mouseleave', updateStars);

    // Инициализация
    if (ratingInput.value > 0) {
        updateStars();
    }

    // Для доступности
    starRating.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            const star = e.target.closest('.star');
            if (star) star.click();
        }
    });
});