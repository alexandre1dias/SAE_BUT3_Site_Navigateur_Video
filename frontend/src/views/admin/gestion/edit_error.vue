<script>
export default {
    name: "edit_error",
    props: {
        message: {
            type: String,
            required: true
        }
    }
};
</script>

<template>
    <div class="toast-error">
        <p>{{ message }}</p>
    </div>
</template>

<style scoped>
/* Toast non bloquant */
.toast-error {
    position: fixed;
    top: 10vh;
    right: 0;
    /* haut droite */
    background-color: var(--rouge);
    color: var(--white);
    padding: 20px 30px;
    /* ✅ arrondi seulement à gauche (haut gauche et bas gauche) */
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;

    font-weight: 600;
    font-size: 1.2rem;
    max-width: 400px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
    z-index: 9999;

    /* ne bloque pas les interactions */
    pointer-events: none;

    /* animation d'entrée et sortie */
    animation: slideInRight 0.4s ease-out, fadeOut 1s ease-in 4s forwards;
}

/* texte */
.toast-error p {
    margin: 0;
    line-height: 1.5;
}

/* animation d'entrée depuis la droite */
@keyframes slideInRight {
    from {
        transform: translateX(50px);
        opacity: 0;
    }

    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* animation de disparition (fade out) */
@keyframes fadeOut {
    from {
        opacity: 1;
    }

    to {
        opacity: 0;
    }
}
</style>
