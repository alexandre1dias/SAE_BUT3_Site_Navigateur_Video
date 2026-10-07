// === Gestion du défilement (Navbar) ===
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => navbar.classList.toggle('scrolled', window.scrollY > 50));

// === Logique de la fenêtre Modale ===
const modal = document.getElementById('video-modal');

function ouvrirModal(titre, imageUrl, description, format, lieu, colorHex, genreText, relatedString) {
    document.getElementById('modal-title').textContent = titre;
    document.getElementById('modal-desc').textContent = description;
    document.getElementById('modal-bg').style.backgroundImage = `url('${imageUrl}')`;
    
    document.getElementById('modal-location').textContent = `📍 ${lieu}`;
    document.getElementById('modal-color-badge').style.background = colorHex;
    document.getElementById('modal-genre-text').textContent = genreText;

    const badge = document.getElementById('modal-format-badge');
    document.getElementById('modal-meta-type').textContent = format === 'interview' ? 'Interview Intégrale' : 'Extrait / Réponse spécifique';
    
    if (format === 'interview') {
        badge.textContent = "Interview Intégrale"; 
        badge.className = "format-badge interview";
    } else {
        badge.textContent = "Extrait (Question)"; 
        badge.className = "format-badge question";
    }

    const linksContainer = document.getElementById('modal-related-links');
    linksContainer.innerHTML = "";
    
    if (relatedString) {
        // On sépare chaque bouton par le symbole "|"
        relatedString.split('|').forEach(linkData => {
            // On sépare l'ID cible et le texte du bouton grâce au symbole ":::"
            const parts = linkData.split(':::');
            
            if(parts.length === 2) {
                const targetId = parts[0];
                const linkText = parts[1];

                const btn = document.createElement('button');
                btn.className = 'btn-related';
                btn.textContent = linkText;
                
                // Au clic, on déclenche l'ouverture de l'autre vidéo
                btn.onclick = () => {
                    const targetCard = document.getElementById(targetId);
                    if(targetCard) {
                        targetCard.click(); // Simule un clic sur la carte correspondante
                        document.querySelector('.modal-content').scrollTop = 0; // Remonte la modale tout en haut
                    }
                };
                linksContainer.appendChild(btn);
            }
        });
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function fermerModal() { 
    modal.classList.remove('active'); 
    document.body.style.overflow = 'auto'; 
}

modal.addEventListener('click', e => { 
    if (e.target === modal) fermerModal(); 
});

function lancerVideo() {
    const lecteur = document.getElementById('player-source').value;
    alert(`Lancement du lecteur vidéo via l'API : ${lecteur.toUpperCase()}`);
}

// === Logique des filtres croisés de la base de données ===
const filterGenre = document.getElementById('filter-genre');
const filterLieu = document.getElementById('filter-lieu');
const filterArtiste = document.getElementById('filter-artiste');
const allCards = document.querySelectorAll('.card');

function filtrerVidéos() {
    const selectedGenre = filterGenre.value;
    const selectedLieu = filterLieu.value;
    const selectedArtiste = filterArtiste.value;

    allCards.forEach(card => {
        const cardGenre = card.getAttribute('data-genre');
        const cardLieu = card.getAttribute('data-lieu');
        const cardArtiste = card.getAttribute('data-artiste');

        const matchGenre = (selectedGenre === "" || cardGenre === selectedGenre);
        const matchLieu = (selectedLieu === "" || cardLieu === selectedLieu);
        const matchArtiste = (selectedArtiste === "" || cardArtiste === selectedArtiste);

        if (matchGenre && matchLieu && matchArtiste) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

filterGenre.addEventListener('change', filtrerVidéos);
filterLieu.addEventListener('change', filtrerVidéos);
filterArtiste.addEventListener('change', filtrerVidéos);