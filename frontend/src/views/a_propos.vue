<script>
export default {
    name: "page_propos",
};
</script>

<template>
    <h1 class="vert-neon">À propos de nous</h1>
    <div class="local-flex row">
        <div class="spacy">
            <p>HERE</p>
        </div>
        <div class="spacy">
            <p>HERE</p>
        </div>
    </div>
    <div class="local-flex row">
        <div class="spacy">
            <p>HERE</p>
        </div>
        <div class="local-flex">
            <div class="local-flex">
                <a href="https://youtube.com" target="_blank">
                    <img src="/imgs/youtube.svg" alt="youtube" class="logo">
                </a>
                <a href="https://vimeo.com" target="_blank">
                    <img src="/imgs/vimeo.svg" alt="vimeo" class="logo">
                </a>
                <a href="https://www.linkedin.com/" target="_blank">
                    <img src="/imgs/linkedin.svg" alt="linkedin" class="logo">
                </a>
                <a href="https://www.instagram.com/" target="_blank">
                    <img src="/imgs/instagram.svg" alt="instagram" class="logo">
                </a>
                <a href="https://www.facebook.com" target="_blank">
                    <img src="/imgs/facebook.svg" alt="facebook" class="logo">
                </a>
            </div>
            <a href="https://rec117.wixsite.com/rec117/contact">
                <img src="/imgs/favicon/android-chrome-192x192.png" alt="logo chaine contact.png">
            </a>
        </div>
    </div>
    <div class="spacy" style="justify-self: center; width: 80%;">
        <p>HERE</p>
        <p>HERE</p>
        <p>HERE</p>
        <p>HERE</p>
    </div>
</template>

<style scoped>
.local-flex {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    flex: 1 1 200px;
}

.spacy {
    border-radius: 20px;
    width: 500px;
    height: 500px;
    background-color: var(--gris-moyen);
}

.logo {
    max-width: 100px;
}
</style>