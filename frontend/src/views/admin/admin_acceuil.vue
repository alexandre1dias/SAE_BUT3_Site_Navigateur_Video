<script>
export default {
  name: "page_admin_acceuil",

};


</script>

<template>

  <h1 class="text-center">Admin</h1>
  <nav>
    <ul class="blocchoix">
      <li>
        <RouterLink class="card" to="/admin/extraits/">
          <h2 class="text-center">Question-Extrait</h2>
          <div class="text-center align-middle">
            <img src="/imgs/video.svg" alt="Video logo" class="card-icon">
          </div>
        </RouterLink>
      </li>
      <li>
        <RouterLink class="card" to="/admin/interview">
          <h2 class="text-center">Interview-Playlist</h2>
          <div class="text-center">
            <img src="/imgs/playlist.svg" alt="playlist logo" class="card-icon">
          </div>
        </RouterLink>
      </li>
      <li>
        <RouterLink class="card" to="/admin/users">
          <h2 class="text-center">User</h2>
          <div class="text-center">
            <img src="/imgs/adminlogo.svg" alt="admin logo" class="card-icon">
          </div>
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.card {
  background-color: var(--gris-moyen);
  filter: drop-shadow(20px 13px 4px var(--noir));
  padding: 2rem;
  margin: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-decoration: none;
  color: inherit;
  border-radius: 8px;
  transition: all 0.4s ease;
  min-height: 553px;
  flex: 1;
  max-width: 470px;
}


.card:hover {
  transform: translateY(-15px) scale(1.05);
  filter: drop-shadow(25px 20px 10px var(--noir));
  background-color: var(--gris-taupe);
}

.card:hover .card-icon {
  transform: scale(1.15) rotate(5deg);
}

.card h2 {
  margin-bottom: 2rem;
  transition: color 0.3s ease;
}

.card:hover h2 {
  color: white;
}

.card-icon {
  width: 311px;
  height: 311px;
  transition: transform 0.4s ease;
}

.blocchoix {
  display: flex;
  list-style-type: none;
  justify-content: center;
  align-items: stretch;
  gap: 1rem;
  padding: 1rem;
  margin: 0;
  flex-wrap: wrap;
}

.blocchoix li {
  display: flex;
  flex: 1;
  min-width: 300px;
  max-width: 470px;
}


@media (max-width: 1200px) {
  .card-icon {
    width: 280px;
    height: 280px;
  }

  .card {
    min-height: 500px;
  }
}

@media (max-width: 768px) {
  .blocchoix {
    flex-direction: column;
    align-items: center;
  }

  .blocchoix li {
    width: 100%;
    max-width: 400px;
  }

  .card {
    min-height: 450px;
  }

  .card-icon {
    width: 250px;
    height: 250px;
  }
}
</style>
