// Simulated blog data (you can load this from an API in real use)
const blogPosts = [
    {
        image: "/static/images/blog-image0.png",
        category: "Skincare",
        title: "How to Get Clear Skin Fast",
        author: "Dr. Wade Warren",
        date: "Jan 20, 2021",
        excerpt: "Many people find it difficult to get clear skin. The methods for getting clear skin will vary, depending on the person's skin type..."
    },
    {
        image: "/static/images/blog-image1.png",
        category: "Skincare",
        title: "Winter Skincare Essentials",
        author: "Dr. Sarah Johnson",
        date: "Nov 15, 2021",
        excerpt: "Protecting your skin during winter requires special care. Learn which products can help combat dryness and maintain healthy skin..."
    },
    {
        image: "/static/images/blog-image2.png",
        category: "Makeup",
        title: "2023 Makeup Trends to Try",
        author: "Mia Chen",
        date: "Feb 3, 2023",
        excerpt: "Discover the hottest makeup trends of the year and how to incorporate them into your daily routine for a fresh, modern look..."
    },
    // Add more blog objects here as needed
];

let postIndex = 0;
const postsPerLoad = 3;
let loading = false;

window.addEventListener('scroll', () => {
    if (loading) return;
    const scrollTop = window.scrollY;
    const windowHeight = window.innerHeight;
    const fullHeight = document.body.scrollHeight;

    if (scrollTop + windowHeight >= fullHeight - 100) {
        loadMorePosts();
    }
});

function loadMorePosts() {
    if (postIndex >= blogPosts.length) return;

    loading = true;
    const grid = document.querySelector('.blog-grid');

    const slice = blogPosts.slice(postIndex, postIndex + postsPerLoad);
    slice.forEach(post => {
        const article = document.createElement('article');
        article.classList.add('blog-card');
        article.innerHTML = `
            <div class="blog-image">
                <img src="${post.image}" alt="${post.title}">
            </div>
            <div class="blog-content">
                <span class="category">${post.category}</span>
                <h2 class="blog-title">${post.title}</h2>
                <div class="blog-meta">
                    <span class="author">${post.author}</span>
                    <span class="date">${post.date}</span>
                </div>
                <p class="blog-excerpt">${post.excerpt}</p>
                <a href="#" class="read-more">Read More</a>
            </div>
        `;
        grid.appendChild(article);
    });

    postIndex += slice.length;
    loading = false;
}
