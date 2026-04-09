console.log('JS loaded');

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {
                await loginUser(email, password);
            } catch (error) {
                displayError(error.message);
            }
      });
    }
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review-text').value.trim();
            if (!reviewText) {
                alert('Please ! Enter a review.');
                return;
            }
            await submitReview(token, placeId, reviewText, reviewForm);
        });
    }

    checkAuthentication();
    const priceFilter = document.getElementById('price-filter');
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        filterPlacesByPrice(selectedPrice);
    });

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    function checkAuthenticationIndex() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
        } else {
            if (loginLink) loginLink.style.display = 'none';
        }
        fetchPlaces(token);
    }

    function checkAuthenticationPlaceDetails(placeId) {
        const token = getCookie('token');
        const addReviewSection = document.getElementById('add-review');
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
            fetchPlaceDetails(token, placeId);
        }
    }

    function checkAuthenticationIndexReview() {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
        }
        return token;
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('id');
    }

    async function fetchPlaces(token) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const placesData = await response.json();
                displayPlaces(placesData);
            } else {
                console.error('Error fetchPlaces:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetchPlaces:', error);
        }
    }

    function displayPlaces(places) {
        const container = document.getElementById('places-list');
        container.innerHTML = '';
        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.dataset.price = place.price;
            card.innerHTML = `
                <h3>${place.name}</h3>
                <p>Price per night: $${place.price}</p>
                <p>${place.description || ''}</p>
                <button class="details-button" onclick="window.location.href='place.html?id=${place.id}'">View Details</button>
            `;
            container.appendChild(card);
        })
    }

    async function fetchPlaceDetails(token, placeId) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/${placeId}', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token ? `Bearer ${token}` : ''
                }
            });
            if (response.ok) {
                const data = await response.json();
                displayPlaceDetails(data);
            } else {
                console.error('Error fetchPlaceDetails:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetchPlaceDetails:', error);
        }
    }

    function displayPlaceDetails(place) {
        const container = document.getElementById('place-details');
        container.innerHTML = '';
        const detailsHTML = `
            <h2>${place.name}</h2>
            <p>Price per night: $${place.price}</p>
            <p>${place.description || ''}</p>
            <h3>Amenities:</h3>
            <ul>
                ${place.amenities.map(a => `<li>${a}</li>`).join('')}
            </ul>
            <h3>Reviews:</h3>
            <ul>
                ${place.reviews.map(r => `<li><strong>${r.user}:</strong> ${r.text}</li>`).join('')}
            </ul>
        `;
        container.innerHTML = detailsHTML;
    }

    function filterPlacesByPrice(selectedPrice) {
        const cards = document.querySelectorAll('.place-card');
        cards.forEach(card => {
            const price = Number(card.dataset.price);
            if (selectedPrice === 'all') {
                card.style.display = 'block';
            } else if (price === Number(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    }

    async function submitReview(token, placeId, reviewText, form) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/${placeId}/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application-json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ review: reviewText, place_id: placeId })
            });
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occured while submitting your review.');
        }
    }

    async function loginUser(email, password) {
        const response = await fetch('http://127.0.0.1/5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed: ' + response.statusText);
        }
    }

    function handleResponse(response, form) {
        if (response.ok) {
            alert('Review submitted successfully!');
            form.reset();
        } else {
            alert ('Failed to submit review.');
        }
    }
});
