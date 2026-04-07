document.addEventListener('DOMContentLoaded', () => {

    /* HELPERS */

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

    /* AUTHENTIFICATION  */

    const token = getCookie('token');

    function checkAuthentication() {
        const loginLink = document.getElementById('login-link');
        if (!loginLink) return;

        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    /* RÉCUPÉRATION DES DONNÉES  */

    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
            } else {
                console.error("Erreur lors de la récupération des lieux");
            }
        } catch (error) {
            console.error("Erreur de connexion à l'API :", error);
        }
    }

    /* AFFICHAGE DYNAMIQUE */

    function displayPlaces(places) {
        const container = document.getElementById('places-list');
        if (!container) return;

        container.innerHTML = ''; 

        if (places.length === 0) {
            container.innerHTML = '<p class="no-places">No places available at the moment.</p>';
            return;
        }

        places.forEach(place => {
            // AJUSTEMENT ICI : On gère 'title' ou 'name' pour le titre, et on s'assure du prix
            const displayTitle = place.title || place.name || "Untitled Place";
            const displayPrice = place.price_by_night ?? place.price ?? 0;
            
            const article = document.createElement('article');
            article.className = 'place-card';
            article.setAttribute('data-price', displayPrice);

            article.innerHTML = `
                <div class="place-info">
                    <h3>${escapeHtml(displayTitle)}</h3>
                    <p>${escapeHtml(place.description)}</p>
                    <p><strong>Price :</strong> $${displayPrice} / night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                </div>
            `;
            container.appendChild(article);
        });
    }

    /* FILTRAGE CÔTÉ CLIENT  */

    const priceFilter = document.getElementById('price-filter');
    
    if (priceFilter) {
        const filterOptions = ['all', '10', '50', '100'];
        priceFilter.innerHTML = '';
        
        filterOptions.forEach(val => {
            const opt = document.createElement('option');
            opt.value = val;
            opt.textContent = (val === 'all') ? 'All' : `$${val}`;
            priceFilter.appendChild(opt);
        });

        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const cards = document.querySelectorAll('.place-card');

            cards.forEach(card => {
                const cardPrice = parseFloat(card.getAttribute('data-price'));
                if (selectedPrice === 'all' || cardPrice <= parseFloat(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    /* --- GESTION DU FORMULAIRE DE CONNEXION --- */

    const loginForm = document.getElementById('login-form');

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
                } else {
                    errorMsg.textContent = "Login failed: Check your email or password.";
                    errorMsg.style.display = 'block';
                }
            } catch (error) {
                console.error("Erreur lors de la connexion :", error);
            }
        });
    }

    checkAuthentication();
});
