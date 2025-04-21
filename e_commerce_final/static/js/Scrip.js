
      let slideIndex = 0;
      const slides = document.querySelectorAll(".slide");
      const dots = document.querySelectorAll(".dot");
      const wrapper = document.querySelector(".slideshow-wrapper");

      function showSlide(n) {
        if (n >= slides.length) slideIndex = 0;
        if (n < 0) slideIndex = slides.length - 1;

        wrapper.style.transform = `translateX(-${slideIndex * 100}%)`;

        dots.forEach((dot, i) => {
          dot.classList.toggle("active", i === slideIndex);
        });
      }

      function moveSlide(n) {
        showSlide((slideIndex += n));
      }

      function currentSlide(n) {
        showSlide((slideIndex = n));
      }

      // Auto slide
      let slideInterval = setInterval(() => moveSlide(1), 3000);

      // Pause on hover
      const slideshow = document.querySelector(".hero-slider");
      slideshow.addEventListener("mouseenter", () =>
        clearInterval(slideInterval)
      );
      slideshow.addEventListener("mouseleave", () => {
        slideInterval = setInterval(() => moveSlide(1), 3000);
      });

      // Initialize
      showSlide(slideIndex);

// Slider functionality for both Best Sellers and New In
function setupSlider(sliderId) {
  const slider = document.getElementById(sliderId);
  const productGrid = slider.querySelector('.product-grid');
  const cards = productGrid.querySelectorAll('.product-card');
  const cardWidth = cards[0].offsetWidth + 24; // card width + gap
  const visibleCards = 4;
  let currentIndex = 0;
  const totalCards = cards.length;

  function scrollSlider(direction) {
    currentIndex += direction;
    
    // Handle wrapping around
    if (currentIndex >= totalCards - visibleCards + 1) {
      currentIndex = 0;
    } else if (currentIndex < 0) {
      currentIndex = totalCards - visibleCards;
    }

    productGrid.style.transition = 'transform 0.5s ease';
    productGrid.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
  }

  return scrollSlider;
}

const scrollProducts = setupSlider('productSlider');
const scrollNewProducts = setupSlider('newProductSlider');

// Make sliders responsive
window.addEventListener('resize', function() {
  // Reset sliders on resize
  document.querySelectorAll('.product-grid').forEach(grid => {
    grid.style.transition = 'none';
    grid.style.transform = 'translateX(0)';
    // Force reflow
    void grid.offsetWidth;
    grid.style.transition = 'transform 0.5s ease';
  });
});

      // Newsletter form submission
      const newsletterForm = document.querySelector(".newsletter-form");
      newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const emailInput = this.querySelector('input[type="email"]');
        alert(`Thank you for subscribing with ${emailInput.value}!`);
        emailInput.value = "";
      });
