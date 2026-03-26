/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {

    /* =========================================================
       HELPERS
       ========================================================= */

    /** Read a cookie by name. Returns null if not found. */
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    /** Set a cookie (expires in `days` days, SameSite=Strict). */
    function setCookie(name, value, days = 1) {
        const expires = new Date(Date.now() + days * 86400000).toUTCString();
        document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Strict`;
    }

    /** Get a URL query param. */
    function getParam(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    /** Escape HTML to avoid XSS when injecting user data. */
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = String(str);
        return div.innerHTML;
    }

    /** Show a star string for a numeric rating 1-5. */
    function renderStars(rating) {
        const n = Math.round(Number(rating));
        return '★'.repeat(n) + '☆'.repeat(5 - n);
    }

    /** Show/hide an alert element. */
    function showAlert(id, message) {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = message;
        el.style.display = 'block';
    }

    function hideAlert(id) {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    }

    /* =========================================================
       AUTH HELPERS
       ========================================================= */

    const token = getCookie('token');

    /**
     * Update the header login link:
     * - If logged in: show "Logout" and clear cookie on click.
     * - Otherwise: keep "Login" pointing to login.html.
     */
    function updateAuthLink() {
        const link = document.getElementById('login-link') || document.getElementById('auth-link');
        if (!link) return;
        if (token) {
            link.textContent = 'Logout';
            link.href = '#';
            link.addEventListener('click', (e) => {
                e.preventDefault();
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                window.location.href = 'index.html';
            });
        } else {
            link.textContent = 'Login';
            link.href = 'login.html';
        }
    }

    updateAuthLink();

    /* =========================================================
       TASK 2 — LOGIN PAGE (login.html)
       ========================================================= */

    const loginForm = document.getElementById('login-form');

    if (loginForm) {

        /* If already authenticated, go straight to index */
        if (token) {
            window.location.href = 'index.html';
            return;
        }

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert('login-error');

            const email    = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            const btn      = loginForm.querySelector('button[type="submit"]');

            if (!email || !password) {
                showAlert('login-error', 'Please fill in all fields.');
                return;
            }

            btn.textContent = 'Logging in…';
            btn.disabled    = true;

            try {
                const response = await fetch('/api/v1/auth/login', {
                    method:  'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body:    JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    /* Store JWT token in a cookie — expires in 1 day */
                    setCookie('token', data.access_token, 1);
                    window.location.href = 'index.html';
                } else {
                    const err = await response.json().catch(() => ({}));
                    showAlert('login-error', err.message || 'Invalid credentials. Please try again.');
                    btn.textContent = 'Login';
                    btn.disabled    = false;
                }
            } catch (err) {
                showAlert('login-error', 'Connection error. Please try again.');
                btn.textContent = 'Login';
                btn.disabled    = false;
            }
        });
    }

    /* =========================================================
       TASK 3 — INDEX PAGE (index.html)
       ========================================================= */

    const placesList  = document.getElementById('places-list');
    const priceFilter = document.getElementById('price-filter');

    if (placesList) {

        /* Redirect to login if not authenticated */
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        let allPlaces = [];

        /* Populate price filter options */
        function populatePriceFilter(places) {
            const prices = [...new Set(places.map(p => p.price_by_night ?? p.price))].sort((a, b) => a - b);
            priceFilter.innerHTML = '<option value="all">All prices</option>';
            prices.forEach(price => {
                const opt = document.createElement('option');
                opt.value       = price;
                opt.textContent = `Up to $${price}`;
                priceFilter.appendChild(opt);
            });
        }

        /* Render place cards */
        function renderPlaces(places) {
            placesList.innerHTML = '';

            if (places.length === 0) {
                placesList.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">🏠</div>
                        <h3>No places found</h3>
                        <p>Try adjusting the price filter.</p>
                    </div>`;
                return;
            }

            places.forEach(place => {
                const price = place.price_by_night ?? place.price ?? '—';
                const id    = place.id ?? place._id ?? '';

                const article = document.createElement('article');
                article.className         = 'place-card';
                article.dataset.price     = price;
                article.innerHTML = `
                    <div class="place-card-thumb">
                        <img src="images/logo.png" alt="${escapeHtml(place.name)}">
                    </div>
                    <h3>${escapeHtml(place.name)}</h3>
                    <div class="place-card-icons">
                        <span><img src="images/icon_bed.png" alt="Bedrooms" class="amenity-icon"> ${escapeHtml(String(place.number_rooms ?? place.bedrooms ?? '?'))}</span>
                        <span><img src="images/icon_bath.png" alt="Bathrooms" class="amenity-icon"> ${escapeHtml(String(place.number_bathrooms ?? place.bathrooms ?? '?'))}</span>
                        <span><img src="images/icon_wifi.png" alt="WiFi" class="amenity-icon"> WiFi</span>
                    </div>
                    <p class="price">$${escapeHtml(String(price))} <span>/ night</span></p>
                    <div class="place-card-footer">
                        <a href="place.html?id=${escapeHtml(String(id))}" class="details-button">View Details</a>
                    </div>`;
                placesList.appendChild(article);
            });
        }

        /* Client-side price filter */
        priceFilter.addEventListener('change', function () {
            const selected = this.value;
            if (selected === 'all') {
                renderPlaces(allPlaces);
            } else {
                const max = parseFloat(selected);
                renderPlaces(allPlaces.filter(p => (p.price_by_night ?? p.price) <= max));
            }
        });

        /* Fetch places from API */
        async function fetchPlaces() {
            try {
                const response = await fetch('/api/v1/places/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (!response.ok) throw new Error('Failed to fetch places');

                allPlaces = await response.json();
                populatePriceFilter(allPlaces);
                renderPlaces(allPlaces);

            } catch (err) {
                showAlert('alert-msg', 'Could not load places. Please refresh the page.');
            }
        }

        fetchPlaces();
    }

    /* =========================================================
       TASK 4 — PLACE DETAILS PAGE (place.html)
       ========================================================= */

    const placeDetailsSection = document.getElementById('place-details');
    const reviewsSection      = document.getElementById('reviews');
    const addReviewSection    = document.getElementById('add-review');

    if (placeDetailsSection) {

        const placeId = getParam('id');
        if (!placeId) {
            window.location.href = 'index.html';
            return;
        }

        /* Update breadcrumb back link */
        const addReviewBackLink = document.getElementById('back-to-place');
        if (addReviewBackLink) addReviewBackLink.href = `place.html?id=${placeId}`;

        async function fetchPlaceDetails() {
            try {
                const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
                const response = await fetch(`/api/v1/places/${placeId}`, { headers });

                if (!response.ok) throw new Error('Place not found');

                const place = await response.json();
                renderPlaceDetails(place);
                renderReviews(place.reviews ?? []);
                renderAddReviewArea(placeId);

            } catch (err) {
                placeDetailsSection.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">❌</div>
                        <h3>Place not found</h3>
                        <p>This place may have been removed. <a href="index.html">Go back home</a>.</p>
                    </div>`;
            }
        }

        function renderPlaceDetails(place) {
            document.title = `${place.name} — HBnB`;
            const breadcrumb = document.getElementById('breadcrumb-name');
            if (breadcrumb) breadcrumb.textContent = place.name;

            const price       = place.price_by_night ?? place.price ?? '—';
            const host        = place.host_name ?? place.host ?? '—';
            const description = place.description ?? '';
            const amenities   = place.amenities ?? [];

            placeDetailsSection.innerHTML = `
                <div class="place-details">
                    <div class="place-details-header">
                        <h1>${escapeHtml(place.name)}</h1>
                        <span class="price-badge">$${escapeHtml(String(price))} <small>/ night</small></span>
                    </div>

                    <div class="place-banner">
                        <img src="images/logo.png" alt="${escapeHtml(place.name)}">
                    </div>

                    <div class="place-info">
                        <div class="info-item">
                            <span class="info-label">Host</span>
                            <span class="info-value">${escapeHtml(host)}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Price per night</span>
                            <span class="info-value">$${escapeHtml(String(price))}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Max Guests</span>
                            <span class="info-value">${escapeHtml(String(place.max_guest ?? place.guests ?? '—'))}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label"><img src="images/icon_bed.png" alt="" class="amenity-icon"> Bedrooms</span>
                            <span class="info-value">${escapeHtml(String(place.number_rooms ?? place.bedrooms ?? '—'))}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label"><img src="images/icon_bath.png" alt="" class="amenity-icon"> Bathrooms</span>
                            <span class="info-value">${escapeHtml(String(place.number_bathrooms ?? place.bathrooms ?? '—'))}</span>
                        </div>
                    </div>

                    <p class="place-description-text">${escapeHtml(description)}</p>

                    ${amenities.length > 0 ? `
                    <div>
                        <p class="amenities-title">Amenities</p>
                        <div class="amenities-list">
                            ${amenities.map(a => {
                                const name = escapeHtml(a.name ?? a);
                                const isWifi = (a.name ?? a).toLowerCase().includes('wifi') || (a.name ?? a).toLowerCase().includes('wi-fi');
                                const icon = isWifi ? `<img src="images/icon_wifi.png" alt="" class="amenity-icon"> ` : '';
                                return `<span class="amenity-tag">${icon}${name}</span>`;
                            }).join('')}
                        </div>
                    </div>` : ''}
                </div>`;
        }

        function renderReviews(reviews) {
            reviewsSection.innerHTML = `<h2>Guest Reviews</h2>`;

            if (reviews.length === 0) {
                reviewsSection.innerHTML += `
                    <div class="empty-state">
                        <div class="empty-icon">💬</div>
                        <h3>No reviews yet</h3>
                        <p>Be the first to share your experience!</p>
                    </div>`;
                return;
            }

            reviews.forEach(review => {
                const card = document.createElement('article');
                card.className = 'review-card';
                card.innerHTML = `
                    <div class="review-card-header">
                        <span class="review-author">${escapeHtml(review.user_name ?? review.user ?? 'Guest')}</span>
                        <span class="review-rating" aria-label="Rating: ${review.rating} out of 5">${renderStars(review.rating)}</span>
                    </div>
                    <p class="review-text">${escapeHtml(review.text ?? review.comment ?? '')}</p>`;
                reviewsSection.appendChild(card);
            });
        }

        function renderAddReviewArea(placeId) {
            addReviewSection.innerHTML = '';
            if (!token) return; /* Not authenticated — show nothing */

            /* Show a button to navigate to add_review.html */
            addReviewSection.innerHTML = `
                <h2>Share Your Experience</h2>
                <a href="add_review.html?id=${escapeHtml(placeId)}" class="add-review-btn">
                    ✍️ Write a Review
                </a>`;

            /*
             * OPTIONAL INLINE FORM (uncomment to use instead of the button above):
             *
             * addReviewSection.innerHTML = `
             *     <div class="add-review">
             *         <h2>Add a Review</h2>
             *         <form id="inline-review-form" class="form">
             *             <label for="inline-review">Your Review:</label>
             *             <textarea id="inline-review" name="review" required
             *                       placeholder="Describe your stay…"></textarea>
             *             <label for="inline-rating">Rating:</label>
             *             <select id="inline-rating" name="rating" required>
             *                 <option value="" disabled selected>Select a rating</option>
             *                 <option value="5">⭐⭐⭐⭐⭐ Excellent (5/5)</option>
             *                 <option value="4">⭐⭐⭐⭐ Very Good (4/5)</option>
             *                 <option value="3">⭐⭐⭐ Good (3/5)</option>
             *                 <option value="2">⭐⭐ Fair (2/5)</option>
             *                 <option value="1">⭐ Poor (1/5)</option>
             *             </select>
             *             <button type="submit">Submit Review</button>
             *         </form>
             *     </div>`;
             * setupInlineReviewForm(placeId);
             */
        }

        fetchPlaceDetails();
    }

    /*TASK 5 — ADD REVIEW PAGE (add_review.html)*/

    const reviewForm = document.getElementById('review-form');
    /* Guard: only run on add_review.html (has #review-form but NOT #place-details) */

    if (reviewForm && !placeDetailsSection) {

        /* Redirect to index if not authenticated */
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        const placeId = getParam('id');

        /* Update breadcrumb / back link */
        const backLink = document.getElementById('back-to-place');
        if (backLink && placeId) backLink.href = `place.html?id=${placeId}`;

        /* Show place name in the form if available */
        async function loadPlaceName() {
            if (!placeId) return;
            try {
                const response = await fetch(`/api/v1/places/${placeId}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const place = await response.json();
                    const info  = document.getElementById('review-place-info');
                    if (info) info.textContent = `Reviewing: ${place.name}`;
                }
            } catch (_) { /* silent — place name is cosmetic */ }
        }

        loadPlaceName();

        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert('review-error');
            hideAlert('review-success');

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;
            const btn  = reviewForm.querySelector('button[type="submit"]');

            if (!reviewText) {
                showAlert('review-error', 'Please write a review before submitting.');
                return;
            }
            if (!rating) {
                showAlert('review-error', 'Please select a rating.');
                return;
            }
            if (!placeId) {
                showAlert('review-error', 'No place selected. Please go back and try again.');
                return;
            }

            btn.textContent = 'Submitting…';
            btn.disabled    = true;

            try {
                const response = await fetch(`/api/v1/places/${placeId}/reviews`, {
                    method:  'POST',
                    headers: {
                        'Content-Type':  'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
                });

                if (response.ok || response.status === 201) {
                    showAlert('review-success', '✅ Your review has been submitted! Redirecting…');
                    reviewForm.style.opacity        = '0.5';
                    reviewForm.style.pointerEvents  = 'none';
                    setTimeout(() => {
                        window.location.href = placeId ? `place.html?id=${placeId}` : 'index.html';
                    }, 2000);
                } else {
                    const err = await response.json().catch(() => ({}));
                    showAlert('review-error', err.message || 'Could not submit your review. Please try again.');
                    btn.textContent = 'Submit Review';
                    btn.disabled    = false;
                }
            } catch (err) {
                showAlert('review-error', 'Connection error. Please check your network and try again.');
                btn.textContent = 'Submit Review';
                btn.disabled    = false;
            }
        });
    }

});
