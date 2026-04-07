/**
 * Attente du chargement complet du DOM avant d'exécuter le script
 */
document.addEventListener('DOMContentLoaded', () => {

    /* --- 1. FONCTIONS OUTILS (HELPERS) --- */

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function escapeHtml(str) {
        if (!str) return "";
        const div = document.createElement('div');
        div.textContent = String(str);
        return div.innerHTML;
    }

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    const token = getCookie('token');

    /* --- 2. LOGIQUE POUR LE FILTRAGE (NOUVEAU) --- */

    // Remplit le menu déroulant avec les options demandées
    function populatePriceFilter() {
        const filter = document.getElementById('price-filter');
        if (!filter) return;

        const options = [
            { value: 'all', text: 'All' },
            { value: '10', text: '$10' },
            { value: '50', text: '$50' },
            { value: '100', text: '$100' }
        ];

        filter.innerHTML = options.map(opt => 
            `<option value="${opt.value}">${opt.text}</option>`
        ).join('');
    }

    // Gère l'affichage des cartes en fonction du prix sélectionné
    function setupPriceFilter() {
        const priceFilter = document.getElementById('price-filter');
        if (!priceFilter) return;

        priceFilter.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
            const cards = document.querySelectorAll('.place-card');

            cards.forEach(card => {
                const cardPrice = parseFloat(card.getAttribute('data-price'));

                if (selectedValue === 'all') {
                    card.style.display = 'block';
                } else {
                    const maxPrice = parseFloat(selectedValue);
                    // Affiche si le prix est inférieur ou égal au filtre choisi
                    card.style.display = cardPrice <= maxPrice ? 'block' : 'none';
                }
            });
        });
    }

    /* --- 3. LOGIQUE POUR LA PAGE D'ACCUEIL (INDEX.HTML) --- */

    async function fetchPlaces(token) {
        const container = document.getElementById('places-list');
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: headers
            });

            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                if (container) container.innerHTML = `<p>Erreur serveur (${response.status}).</p>`;
            }
        } catch (error) {
            if (container) container.innerHTML = "<p>Impossible de contacter le serveur.</p>";
        }
    }

    function displayPlaces(places) {
        const container = document.getElementById('places-list');
        if (!container) return;

        container.innerHTML = ''; 
        if (places.length === 0) {
            container.innerHTML = '<p class="no-places">No places available at the moment.</p>';
            return;
        }

        places.forEach(place => {
            const title = place.title || place.name || "Untitled Place";
            const price = place.price_by_night ?? place.price ?? 0;
            
            const article = document.createElement('article');
            article.className = 'place-card';
            // IMPORTANT : On stocke le prix pour que le filtre puisse le lire
            article.setAttribute('data-price', price);

            article.innerHTML = `
                <div class="place-info">
                    <h3>${escapeHtml(title)}</h3>
                    <p>${escapeHtml(place.description)}</p>
                    <p><strong>Price :</strong> $${price} / night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                </div>
            `;
            container.appendChild(article);
        });
    }

    /* --- 4. LOGIQUE POUR LA PAGE DÉTAILS (PLACE.HTML) --- */
    // (Tes fonctions fetchPlaceDetails et displayPlaceDetails restent identiques...)
    async function fetchPlaceDetails(token, placeId) {
        const container = document.getElementById('place-details');
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
            } else if (container) {
                container.innerHTML = "<p>Lieu introuvable.</p>";
            }
        } catch (error) {
            console.error("Erreur API Details:", error);
        }
    }

    function displayPlaceDetails(place) {
        const detailsContainer = document.getElementById('place-details');
        const reviewsContainer = document.getElementById('reviews');
        const breadcrumbName = document.getElementById('breadcrumb-name');

        if (!detailsContainer) return;

        const title = place.title || place.name || "Détails du lieu";
        const price = place.price_by_night ?? place.price ?? 0;

        if (breadcrumbName) breadcrumbName.textContent = title;

        detailsContainer.innerHTML = `
            <div class="place-header">
                <h1>${escapeHtml(title)}</h1>
                <p class="price-tag"><strong>$${price}</strong> per night</p>
            </div>
            <div class="place-content">
                <p class="description">${escapeHtml(place.description)}</p>
                <div class="amenities-section">
                    <h3>Amenities</h3>
                    <ul class="amenities-list">
                        ${place.amenities && place.amenities.length > 0 
                            ? place.amenities.map(a => `<li>${escapeHtml(a.name)}</li>`).join('') 
                            : '<li>No amenities available</li>'}
                    </ul>
                </div>
            </div>
        `;

        if (reviewsContainer) {
            reviewsContainer.innerHTML = `
                <h2>Reviews</h2>
                <div class="reviews-list">
                    ${place.reviews && place.reviews.length > 0
                        ? place.reviews.map(r => `
                            <div class="review-card">
                                <p class="review-text">"${escapeHtml(r.text)}"</p>
                                <p class="review-author"><strong>— ${escapeHtml(r.user_name || "Guest")}</strong></p>
                            </div>
                        `).join('')
                        : '<p>No reviews yet for this place.</p>'}
                </div>
            `;
        }
    }

    /* --- 5. INITIALISATION ET ROUTAGE --- */

    /* --- 5. INITIALISATION ET ROUTAGE --- */

    function initialize() {
        const token = getCookie('token');
        const authLink = document.getElementById('login-link');
        const placesListElement = document.getElementById('places-list');
        const loginForm = document.getElementById('login-form');
        const placeId = getPlaceIdFromURL();

        // A. Gestion du bouton Login/Logout (Header)
        if (authLink) {
            if (token) {
                authLink.textContent = "Logout";
                authLink.href = "#";
                authLink.onclick = function(e) {
                    e.preventDefault();
                    // On efface le cookie
                    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                    // On force le retour à l'accueil
                    window.location.href = "index.html";
                };
            } else {
                authLink.textContent = "Login";
                authLink.href = "login.html";
                authLink.onclick = null;
            }
        }

        // B. Si on est sur la page d'accueil (index.html)
        if (placesListElement) {
            populatePriceFilter();
            setupPriceFilter();
            fetchPlaces(token);
        }

        // C. Si on est sur la page de Login (login.html)
        if (loginForm) {
            loginForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                const errorMsg = document.getElementById('login-error');

                try {
                    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, password })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Strict`;
                        window.location.href = 'index.html'; 
                    } else if (errorMsg) {
                        errorMsg.textContent = "Login failed: Invalid email or password.";
                        errorMsg.style.display = 'block';
                    }
                } catch (error) { 
                    console.error("Erreur login:", error); 
                }
            });
        }

        // D. Si on est sur la page de détails (place.html)
        if (placeId && document.getElementById('place-details')) {
            fetchPlaceDetails(token, placeId);
            const addReviewSection = document.getElementById('add-review');
            if (addReviewSection) {
                addReviewSection.innerHTML = token 
                    ? `<a href="add_review.html?id=${placeId}" class="add-review-button">Add a Review</a>`
                    : `<p><a href="login.html">Login</a> to add a review.</p>`;
            }
        }
    }

    // On lance enfin toute la logique
    initialize();
});
