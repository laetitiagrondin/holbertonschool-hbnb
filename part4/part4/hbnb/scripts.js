/**
 * Attente du chargement complet du DOM avant d'exécuter le script.
 * Cela garantit que tous les éléments HTML sont accessibles.
 */
document.addEventListener('DOMContentLoaded', () => {

    /* --- 1. FONCTIONS OUTILS (HELPERS) --- */

    /**
     * Récupère la valeur d'un cookie par son nom.
     * Utile pour extraire le jeton JWT stocké lors du login.
     */
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    /**
     * Sécurise les chaînes de caractères pour éviter les failles XSS.
     * Remplace les caractères spéciaux par leurs entités HTML.
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

    /* --- 2. LOGIQUE POUR LE FILTRAGE --- */

    /**
     * Remplit dynamiquement le menu déroulant du filtre de prix sur l'index.
     */
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
                    // Logique : afficher si le prix de la carte <= prix maximum choisi
                    card.style.display = cardPrice <= maxPrice ? 'block' : 'none';
                }
            });
        });
    }

    /* --- 3. LOGIQUE API (FETCH & DISPLAY) --- */

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
            const title = place.title || place.name || "Untitled Place";
            const price = place.price_by_night ?? place.price ?? 0;
            const article = document.createElement('article');
            article.className = 'place-card';
            // On stocke le prix en attribut de données pour le filtrage JS
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
        const breadcrumbName = document.getElementById('breadcrumb-name');

        // Mise à jour du fil d'Ariane
        if (breadcrumbName) breadcrumbName.textContent = place.title || place.name;

        // Injection des informations principales
        if (detailsContainer) {
            const price = place.price_by_night ?? place.price ?? 0;
            detailsContainer.innerHTML = `
                <div class="place-header">
                    <h1>${escapeHtml(place.title || place.name)}</h1>
                    <p class="price-tag"><strong>$${price}</strong> per night</p>
                </div>
                <div class="place-content">
                    <p class="description">${escapeHtml(place.description)}</p>
                    <h3>Amenities</h3>
                    <ul class="amenities-list">
                        ${place.amenities?.map(a => `<li>${escapeHtml(a.name)}</li>`).join('') || '<li>None</li>'}
                    </ul>
                </div>
            `;
        }

        // Injection de la liste des avis
        if (reviewsContainer) {
            reviewsContainer.innerHTML = `<h2>Reviews</h2>` + 
                (place.reviews?.length > 0 
                ? place.reviews.map(r => `
                    <div class="review-card">
                        <p>"${escapeHtml(r.text)}"</p>
                        <p><strong>— ${escapeHtml(r.user_name || "Guest")}</strong></p>
                    </div>`).join('')
                : '<p>No reviews yet.</p>');
        }
    }

    /* --- 4. INITIALISATION ET ROUTAGE --- */

    /**
     * Fonction principale qui orchestre le comportement du site selon la page chargée.
     */
    function initialize() {
        const token = getCookie('token');
        const placeId = getPlaceIdFromURL();
        const authLink = document.getElementById('login-link');

        // A. Gestion dynamique du Header (Bouton Login/Logout)
        if (authLink) {
            if (token) {
                authLink.textContent = "Logout";
                authLink.onclick = (e) => {
                    e.preventDefault();
                    // Suppression du cookie en le faisant expirer immédiatement
                    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                    window.location.href = "index.html";
                };
            } else {
                authLink.textContent = "Login";
                authLink.href = "login.html";
            }
        }

        // B. Configuration de la page d'accueil (index.html)
                if (document.getElementById('places-list')) {
            /* Redirection si non connecté */
            if (!token) {
                window.location.href = 'login.html';
                return;
            }
            populatePriceFilter();
            setupPriceFilter();
            fetchPlaces(token);
        }

        // C. Gestion du formulaire de connexion (login.html)
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stockage du token dans un cookie sécurisé pour 24h
                    document.cookie = `token=${data.access_token}; path=/; max-age=86400; SameSite=Strict`;
                    document.cookie = `user_id=${data.user_id}; path=/; max-age=86400; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    alert("Invalid credentials");
                }
            });
        }

        // D. Configuration de la page de détails (place.html)
        if (placeId && document.getElementById('place-details')) {
            fetchPlaceDetails(token, placeId);
            const addReviewSection = document.getElementById('add-review');
            if (addReviewSection) {
                // N'affiche le bouton "Add Review" que si l'utilisateur est connecté
                addReviewSection.innerHTML = token 
                    ? `<a href="add_review.html?id=${placeId}" class="add-review-button">Add a Review</a>`
                    : `<p><a href="login.html">Login</a> to add a review.</p>`;
            }
        }

        // E. Gestion de la page de création d'avis (add_review.html)
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            // Sécurité : redirection si accès direct sans être connecté
            if (!token) {
                window.location.href = 'index.html';
                return;
            }

            // Lien de retour dynamique vers le lieu consulté
            const backLink = document.getElementById('back-to-place');
            if (backLink) backLink.href = `place.html?id=${placeId}`;

            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                
                // --- ON RÉCUPÈRE LES DONNÉES ICI ---
                const text = document.getElementById('review').value;
                const rating = document.getElementById('rating').value;
                const userId = getCookie('user_id'); // On récupère l'ID depuis le cookie ici !

                const response = await fetch('http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: text,
                        rating: parseInt(rating)
                    })
                });

                if (response.ok) {
                    alert('Review submitted!');
                    window.location.href = `place.html?id=${placeId}`;
                } else {
                    const errorData = await response.json();
                    alert('Erreur ' + response.status + ' : ' + (errorData.message || 'Action interdite'));
                    console.error('Détails du refus serveur:', errorData);
                }
            }); // Fermeture correcte de l'EventListener
        }
    }

    // Lancement de la logique applicative
    initialize();
});
