/**
 * Attente du chargement complet du DOM avant d'exécuter le script.
 * Cela garantit que tous les éléments HTML sont accessibles.
 */
document.addEventListener('DOMContentLoaded', () => {

    /*  FONCTIONS OUTILS (HELPERS) --- */

    /**
     * Récupère la valeur d'un cookie par son nom.
     */
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    /**
     * Sécurise les chaînes de caractères pour éviter les failles XSS.
     */
    function escapeHtml(str) {
        if (!str) return "";
        const div = document.createElement('div');
        div.textContent = String(str);
        return div.innerHTML;
    }

    /**
     * Extrait l'identifiant (ID) du lieu depuis les paramètres de l'URL (?id=...).
     */
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    /* LOGIQUE POUR LE FILTRAGE */

    /**
     * Remplit dynamiquement le menu déroulant du filtre de prix sur l'index.
     */
    function populatePriceFilter() {
        const filter = document.getElementById('price-filter');
        if (!filter) return;

        const options = [
            { value: 'all', text: 'All' },
            { value: '10',  text: '$10' },
            { value: '50',  text: '$50' },
            { value: '100', text: '$100' }
        ];

        filter.innerHTML = options.map(opt =>
            `<option value="${opt.value}">${opt.text}</option>`
        ).join('');
    }

    /**
     * Écoute les changements sur le filtre de prix et masque/affiche les cartes.
     */
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
                    card.style.display = cardPrice <= maxPrice ? 'block' : 'none';
                }
            });
        });
    }

    /* LOGIQUE API (FETCH & DISPLAY) */

    /**
     * Récupère la liste de tous les lieux via l'API.
     */
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
            }
        } catch (error) {
            if (container) container.innerHTML = "<p>Impossible de contacter le serveur.</p>";
        }
    }

    /**
     * Génère le HTML pour chaque lieu et l'injecte dans la liste.
     */
    function displayPlaces(places) {
        const container = document.getElementById('places-list');
        if (!container) return;
        container.innerHTML = '';

        places.forEach(place => {
            /* L'API  utilise "name", pas "title" */
            const title = place.name || place.title || "Untitled Place";
            const price = place.price_by_night ?? place.price ?? 0;

            const article = document.createElement('article');
            article.className = 'place-card';
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

    /**
     * Récupère les détails spécifiques d'un lieu (incluant les avis et équipements).
     */
    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(
                `http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });

            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
            }
        } catch (error) {
            console.error("Erreur API Details:", error);
        }
    }

    /**
     * Affiche les informations détaillées, les équipements et les avis d'un lieu.
     */
    function displayPlaceDetails(place) {
        const detailsContainer = document.getElementById('place-details');
        const reviewsContainer = document.getElementById('reviews');
        const breadcrumbName   = document.getElementById('breadcrumb-name');

        /* Mise à jour du fil d'Ariane */
        if (breadcrumbName) breadcrumbName.textContent = place.name || place.title;

        /* Injection des informations principales */
        if (detailsContainer) {
            const price = place.price_by_night ?? place.price ?? 0;
            
            // CORRECTIF ICI : On teste plusieurs noms de clés possibles
            const rooms = place.number_rooms ?? place.rooms ?? place.max_guests ?? '—';
            const bathrooms = place.number_bathrooms ?? place.bathrooms ?? '—';

            detailsContainer.innerHTML = `
                <div class="place-details">
                    <div class="place-details-header">
                        <h1>${escapeHtml(place.name || place.title)}</h1>
                        <span class="price-badge">$${price} <small>/ night</small></span>
                    </div>
                    <div class="place-info">
                        <div class="info-item">
                            <span class="info-label">Host</span>
                            <span class="info-value">${escapeHtml(place.owner?.first_name || '—')}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">
                                <img src="images/icon_bed.png" alt="" class="amenity-icon"> Bedrooms
                            </span>
                            <span class="info-value">${escapeHtml(String(rooms))}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">
                                <img src="images/icon_bath.png" alt="" class="amenity-icon"> Bathrooms
                            </span>
                            <span class="info-value">${escapeHtml(String(bathrooms))}</span>
                        </div>
                    </div>
                    <p class="place-description-text">${escapeHtml(place.description)}</p>
                    <div>
                        <p class="amenities-title">Amenities</p>
                        <div class="amenities-list">
                            ${place.amenities?.length > 0
                                ? place.amenities.map(a => {
                                    const isWifi = a.name?.toLowerCase().includes('wifi') ||
                                                   a.name?.toLowerCase().includes('wi-fi');
                                    const icon = isWifi
                                        ? `<img src="images/icon_wifi.png" alt="" class="amenity-icon"> `
                                        : '';
                                    return `<span class="amenity-tag">${icon}${escapeHtml(a.name)}</span>`;
                                }).join('')
                                : '<span class="amenity-tag">None listed</span>'
                            }
                        </div>
                    </div>
                </div>
            `;
        }

        /* Injection de la liste des avis (Le reste du code est correct) */
        if (reviewsContainer) {
            reviewsContainer.innerHTML = `<h2>Reviews</h2>`;
            if (place.reviews?.length > 0) {
                place.reviews.forEach(r => {
                    const card = document.createElement('article');
                    card.className = 'review-card';
                    card.innerHTML = `
                        <div class="review-card-header">
                            <span class="review-author">${escapeHtml(r.user_name || 'Guest')}</span>
                            <span class="review-rating">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</span>
                        </div>
                        <p class="review-text">${escapeHtml(r.text)}</p>
                    `;
                    reviewsContainer.appendChild(card);
                });
            } else {
                reviewsContainer.innerHTML += '<p>No reviews yet.</p>';
            }
        }
    }
    /*  FONCTIONS POUR ADD REVIEW */

    /**
     * Vérifie l'authentification. Redirige vers index.html si non connecté.
     */
    function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
        }
        return token;
    }

    /**
     * Envoie l'avis à l'API.
     */
    async function submitReview(token, placeId, reviewText, rating) {
        const response = await fetch(
            `http://127.0.0.1:5000/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ text: reviewText, rating: parseInt(rating), place_id: placeId })
        });
        return response;
    }

    /**
     * Gère la réponse de l'API après soumission d'un avis.
     */
    function handleResponse(response, form, placeId) {
        if (response.ok || response.status === 201) {
            alert('Review submitted successfully!');
            form.reset();
            if (placeId) window.location.href = `place.html?id=${placeId}`;
        } else {
            alert('Failed to submit review');
        }
    }

    /* INITIALISATION ET ROUTAGE*/

    /**
     * Fonction principale qui orchestre le comportement selon la page chargée.
     */
    function initialize() {
        const token    = getCookie('token');
        const placeId  = getPlaceIdFromURL();
        const authLink = document.getElementById('login-link');

        /* Gestion dynamique du Header (Login / Logout) */
        if (authLink) {
            if (token) {
                authLink.textContent = "Logout";
                authLink.onclick = (e) => {
                    e.preventDefault();
                    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                    window.location.href = "index.html";
                };
            } else {
                authLink.textContent = "Login";
                authLink.href = "login.html";
            }
        }

        /* Page d'accueil (index.html) */
        if (document.getElementById('places-list')) {

            populatePriceFilter();
            setupPriceFilter();
            fetchPlaces(token);
        }

        /* Formulaire de connexion (login.html) */
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            /* Déjà connecté aller directement à l'index */
            if (token) {
                window.location.href = 'index.html';
                return;
            }

            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email    = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    alert("Invalid credentials");
                }
            });
        }

        /* Page de détails (place.html) */
        if (placeId && document.getElementById('place-details')) {
            fetchPlaceDetails(token, placeId);

            const addReviewSection = document.getElementById('add-review');
            if (addReviewSection) {
                addReviewSection.innerHTML = token
                    ? `<a href="add_review.html?id=${placeId}" class="add-review-btn">
                           ✍️ Add a Review
                       </a>`
                    : `<p><a href="login.html">Login</a> to add a review.</p>`;
            }
        }

        /*  Page de création d'avis (add_review.html) */
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            /* Vérification auth avec la fonction dédiée */
            const reviewToken = checkAuthentication();

            /* Lien de retour vers le lieu */
            const backLink = document.getElementById('back-to-place');
            if (backLink && placeId) backLink.href = `place.html?id=${placeId}`;

            /* Afficher le nom du lieu dans le sous-titre du formulaire */
            if (reviewToken && placeId) {
                fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                    headers: { 'Authorization': `Bearer ${reviewToken}` }
                })
                .then(r => r.ok ? r.json() : null)
                .then(place => {
                    if (!place) return;
                    const info = document.getElementById('review-place-info');
                    if (info) info.textContent = `Reviewing: ${place.name || place.title}`;
                })
                .catch(() => {});
            }

            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();

                const text   = document.getElementById('review').value.trim();
                const rating = document.getElementById('rating').value;

                if (!text || !rating) {
                    alert('Please fill in all fields.');
                    return;
                }

                /* Envoi de l'avis via submitReview() */
                const response = await submitReview(reviewToken, placeId, text, rating);

                /* Gestion de la réponse via handleResponse() */
                handleResponse(response, reviewForm, placeId);
            });
        }
    }

    /* Lancement de la logique applicative */
    initialize();
});
