function updateSubcategories() {
  const category = document.getElementById("category-filter").value;
  const subcategoryFilter = document.getElementById("subcategory-filter");

  subcategoryFilter.disabled = false;
  subcategoryFilter.innerHTML =
    '<option value="" selected disabled>-- Choisissez une option --</option>';

  if (category in categoryData) {
    categoryData[category].forEach((subcat) => {
      const option = document.createElement("option");
      option.value = subcat.toLowerCase();
      option.textContent = subcat;
      subcategoryFilter.appendChild(option);
    });
  }
}

function filterVideos() {
  const category = document.getElementById("category-filter").value;
  const subcategory = document
    .getElementById("subcategory-filter")
    .value.toLowerCase();

  document
    .querySelectorAll("#questionIndiv-section .video-card")
    .forEach((card) => {
      let matches = false;
      if (category === "artist") {
        const artists = card.dataset.artists.toLowerCase().split(",");
        matches = artists.includes(subcategory);
      } else if (category === "theme") {
        const themes = card.dataset.themes.toLowerCase().split(",");
        console.log(subcategory);
        console.log(themes);
        matches = themes.includes(subcategory);
      } else if (category === "author") {
        const author = card.dataset.author.toLowerCase();
        matches = author === subcategory;
      }

      card.style.display = matches ? "block" : "none";
    });
}

function resetFilters() {
  document.getElementById("category-filter").value = "";
  document.getElementById("subcategory-filter").value = "";
  document.getElementById("subcategory-filter").disabled = true;
  console.log(document.getElementById("subcategory-filter"));

  document
    .querySelectorAll("#questionIndiv-section .video-card")
    .forEach((card) => {
      card.style.display = "block";
    });
}
