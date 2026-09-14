// Flask API URL 
const API_URL = "https://movie-recommand-system.vercel.app";
// HTML elements 
const movieSelect = document.getElementById("movieSelect");
const recommendBtn = document.getElementById("recommendBtn");
const loading = document.getElementById("loading");
const error = document.getElementById("error");
const result = document.getElementById("result");
const recommendations = document.getElementById("recommendations");
// ----------------------------------- // Load movies // ----------------------------------- 
async function loadMovies() {
    try {
        const response = await fetch(`${API_URL}/movies`);
        if (!response.ok) {
            throw new Error("Failed to load movies");
        }
        const data = await response.json();
        movieSelect.innerHTML = '<option value="">Select a movie</option>';
        data.movies.forEach(movie => {
            const option = document.createElement("option");
            option.value = movie; option.textContent = movie;
            movieSelect.appendChild(option);
        });
    } catch (err) {
        movieSelect.innerHTML = '<option value="">Unable to load movies</option>';
        showError(err.message);
    }
}
// ----------------------------------- // Recommend movies // ----------------------------------- 
async function getRecommendations() {
    const movie = movieSelect.value;
    if (!movie) {
        showError("Please select a movie.");
        return;
    } hideError();
    result.classList.add("hidden");
    loading.classList.remove("hidden");
    recommendBtn.disabled = true;
    try {
        const response = await fetch(`${API_URL}/recommend`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ movie: movie })
            });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Something went wrong");
        }
        displayRecommendations(data.recommendations);
    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add("hidden");
        recommendBtn.disabled = false;
    }
}
// ----------------------------------- // Display recommendations // ----------------------------------- 
function displayRecommendations(movieList) {
    recommendations.innerHTML = "";
    movieList.forEach((movie, index) => {
        const movieElement = document.createElement("div");
        movieElement.className = "movie";
        movieElement.textContent = `${index + 1}. ${movie}`;
        recommendations.appendChild(movieElement);
    });
    result.classList.remove("hidden");
}
// ----------------------------------- // Error handling // ----------------------------------- 
function showError(message) {
    error.textContent = message;
    error.classList.remove("hidden");
} function hideError() {
    error.textContent = ""; error.classList.add("hidden");
}
// ----------------------------------- // Events // ----------------------------------- 
recommendBtn.addEventListener("click", getRecommendations);
// ----------------------------------- // Start application // ----------------------------------- 
loadMovies();