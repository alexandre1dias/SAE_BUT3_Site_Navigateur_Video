<script>
export default {
    name: "comp_footerbar",
};
</script>

<template>
    <footer class="bg-dark text-white py-3 mt-auto">
        <div class="text-center mb-2">
            <div class="d-flex justify-content-center gap-3 mb-2">
                <a href="https://youtube.com" target="_blank">
                    <img src="/imgs/youtube.svg" alt="youtube" style="width:32px; height:32px;">
                </a>
                <a href="https://vimeo.com" target="_blank">
                    <img src="/imgs/vimeo.svg" alt="vimeo" style="width:32px; height:32px;">
                </a>
                <a href="https://www.linkedin.com/" target="_blank">
                    <img src="/imgs/linkedin.svg" alt="linkedin" style="width:32px; height:32px;">
                </a>
                <a href="https://www.instagram.com/" target="_blank">
                    <img src="/imgs/instagram.svg" alt="instagram" style="width:32px; height:32px;">
                </a>
                <a href="https://www.facebook.com" target="_blank">
                    <img src="/imgs/facebook.svg" alt="facebook" style="width:32px; height:32px;">
                </a>
            </div>
            <div class="d-flex justify-content-center gap-3 mb-2">
                <RouterLink class="text-white mx-2 text-decoration-none" to="/">Accueil</RouterLink>
                <!--<RouterLink class="text-white mx-2 text-decoration-none" to="/propos">À propos de nous</RouterLink>-->
                <!--<RouterLink class="text-white mx-2 text-decoration-none" to="/conditiongeneral">Conditions générales d'utilisation </RouterLink>-->
            </div>
        </div>
    </footer>
</template>

<style scoped>
footer {
    background-color: var(--gris-moyen);
    width: 100%;
}
</style>