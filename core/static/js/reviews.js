// E:\Rest_Project\core\static\js\reviews.js
document.addEventListener('DOMContentLoaded', function() {
    // Основной класс для управления рейтингом
    class StarRating {
        constructor(container) {
            this.container = container;
            this.stars = this.container.querySelectorAll('.star');
            this.ratingInput = this.container.querySelector('input[type="hidden"]') || 
                              document.getElementById('id_rating');
            
            if (!this.stars.length || !this.ratingInput) return;
            
            this.init();
        }
        
        init() {
            // Инициализация текущего значения
            if (this.ratingInput.value > 0) {
                this.updateStars();
            }
            
            this.setupEventListeners();
        }
        
        setupEventListeners() {
            this.stars.forEach(star => {
                // Клик по звезде
                star.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.setRating(parseInt(star.getAttribute('data-value')));
                });
                
                // Наведение на звезду
                star.addEventListener('mouseover', () => {
                    const hoverValue = parseInt(star.getAttribute('data-value'));
                    this.highlightStars(hoverValue);
                });
                
                // Клавиатурные события для доступности
                star.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.setRating(parseInt(star.getAttribute('data-value')));
                    }
                });
            });
            
            // Сброс подсветки при уходе мыши
            this.container.addEventListener('mouseleave', () => {
                this.updateStars();
            });
        }
        
        setRating(value) {
            this.ratingInput.value = value;
            this.updateStars();
            
        }
        
        highlightStars(upToValue) {
            this.stars.forEach(star => {
                const starValue = parseInt(star.getAttribute('data-value'));
                star.classList.toggle('hover', starValue <= upToValue);
            });
        }
        
        updateStars() {
            const currentValue = parseInt(this.ratingInput.value) || 0;
            this.stars.forEach(star => {
                const starValue = parseInt(star.getAttribute('data-value'));
                star.classList.toggle('active', starValue <= currentValue);
                star.classList.remove('hover');
            });
        }
    }
    
    // Инициализация всех компонентов рейтинга на странице
    function initAllStarRatings() {
        const ratingContainers = document.querySelectorAll('.star-rating');
        if (!ratingContainers.length) return;
        
        ratingContainers.forEach(container => {
            new StarRating(container);
        });
    }
    
    // Инициализация при загрузке страницы
    initAllStarRatings();
    
    function setupReviewDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.delete-review');
        if (!deleteButtons.length) return;
        
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    setupReviewDeleteButtons();
});