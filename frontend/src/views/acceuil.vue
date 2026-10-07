<script>
import { videoStore } from "@model/videoStore.js";
import comp_mindmap from "@components/acceuil/mindmap.vue";
import comp_recent from "@components/acceuil/home_recent.vue";
import iframe_lecture_video from "@components/lecteur_video/iframe_lecture_video.vue";

export default {
    name: "page_accueil",
    components: {
        comp_mindmap,
        comp_recent,
        iframe_lecture_video
    },
    setup() {
        return { videoStore };
    },

    data() {
        return {
            isDragging: false,
            offsetX: 0,
            offsetY: 0,
        };
    },
    methods: {
        picture_in_picture() {
            // console.log("→ Désactivation du Picture in Picture");
            // console.log("videoStore: ")
            // console.log(JSON.parse(JSON.stringify(videoStore)))

            //videoStore.lecteur = this.lecteur;
            // console.log("le lecteur: ")
            videoStore.isPictureInPicture = false;

            // Rediriger vers la page d’accueil
            // console.log(videoStore.uuid)
            this.$router.push("/lecteur_video/");
        },

        startDrag(event) {
            const pip = document.querySelector(".pip-video");
            if (!pip) return;

            this.isDragging = true;
            const rect = pip.getBoundingClientRect();

            // Handle both mouse and touch events
            const clientX = event.clientX || (event.touches && event.touches[0].clientX);
            const clientY = event.clientY || (event.touches && event.touches[0].clientY);

            this.offsetX = clientX - rect.left;
            this.offsetY = clientY - rect.top;

            // Désactiver la sélection pendant le drag
            document.body.style.userSelect = "none";
            document.body.style.pointerEvents = "auto"; // on garde pointer-events pour iframe

            document.addEventListener("mousemove", this.onDrag);
            document.addEventListener("touchmove", this.onDragTouch, { passive: false });
            document.addEventListener("mouseup", this.stopDrag);
            document.addEventListener("touchend", this.stopDrag);
        },

        onDrag(event) {
            if (!this.isDragging) return;
            this.updatePosition(event.clientX, event.clientY);
        },

        onDragTouch(event) {
            if (!this.isDragging) return;
            event.preventDefault(); // Prevent scrolling while dragging
            const touch = event.touches[0];
            this.updatePosition(touch.clientX, touch.clientY);
        },

        updatePosition(clientX, clientY) {
            const pip = document.querySelector(".pip-video");
            if (!pip) return;

            // Empêcher le PiP de sortir de l'écran
            const minX = 0;
            const minY = 0;
            const maxX = window.innerWidth - pip.offsetWidth;
            const maxY = window.innerHeight - pip.offsetHeight;

            let left = clientX - this.offsetX;
            let top = clientY - this.offsetY;

            if (left < minX) left = minX;
            if (top < minY) top = minY;
            if (left > maxX) left = maxX;
            if (top > maxY) top = maxY;

            pip.style.left = left + "px";
            pip.style.top = top + "px";
        },

        stopDrag() {
            if (!this.isDragging) return;

            this.isDragging = false;

            // Snap to nearest corner
            this.snapToCorner();

            // Réactiver la sélection
            document.body.style.userSelect = "";
            document.body.style.pointerEvents = "";

            document.removeEventListener("mousemove", this.onDrag);
            document.removeEventListener("touchmove", this.onDragTouch);
            document.removeEventListener("mouseup", this.stopDrag);
            document.removeEventListener("touchend", this.stopDrag);
        },

        snapToCorner() {
            const pip = document.querySelector(".pip-video");
            if (!pip) return;

            const rect = pip.getBoundingClientRect();
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;

            // Calculate distance to each corner
            const distances = {
                topLeft: Math.sqrt(rect.left ** 2 + rect.top ** 2),
                topRight: Math.sqrt((windowWidth - rect.right) ** 2 + rect.top ** 2),
                bottomLeft: Math.sqrt(rect.left ** 2 + (windowHeight - rect.bottom) ** 2),
                bottomRight: Math.sqrt((windowWidth - rect.right) ** 2 + (windowHeight - rect.bottom) ** 2)
            };

            // Find the closest corner
            const closestCorner = Object.keys(distances).reduce((a, b) =>
                distances[a] < distances[b] ? a : b
            );

            // Snap to the closest corner with some margin
            const margin = 10;
            let newLeft, newTop;

            switch (closestCorner) {
                case 'topLeft':
                    newLeft = margin;
                    newTop = margin;
                    break;
                case 'topRight':
                    newLeft = windowWidth - pip.offsetWidth - margin;
                    newTop = margin;
                    break;
                case 'bottomLeft':
                    newLeft = margin;
                    newTop = windowHeight - pip.offsetHeight - margin;
                    break;
                case 'bottomRight':
                    newLeft = windowWidth - pip.offsetWidth - margin;
                    newTop = windowHeight - pip.offsetHeight - margin;
                    break;
            }

            // Apply smooth transition for snapping
            pip.style.transition = 'all 0.2s ease';
            pip.style.left = newLeft + 'px';
            pip.style.top = newTop + 'px';

            // Remove transition after snapping completes
            setTimeout(() => {
                pip.style.transition = '';
            }, 200);
        },
    },
};
</script>

<template>
    <div class="local-flex">
        <div class="flex-grow">
            <comp_mindmap />
        </div>
        <comp_recent class="recent-component" />
    </div>
    <!-- Si le mode PiP est actif -->
    <div v-if="videoStore.isPictureInPicture" class="pip-video" ref="pip" @mousedown="startDrag"
        @touchstart="startDrag">
        <!-- iframe picture in picture-->
        <component v-if="videoStore.iframeComponent" :is="videoStore.iframeComponent.$options"
            v-bind="videoStore.iframeComponent.$props" />
        <img src="/imgs/agrandir.svg" alt="picture in picture" @click="picture_in_picture">
    </div>
</template>

<style scoped>
.local-flex {
    display: flex;
    height: 100%;
    flex-direction: row;
    /* Default for larger screens */
}

.flex-grow {
    flex-grow: 1;
    margin: 1%;
}

.recent-component {
    margin: 1%;
    min-width: 10%;
    min-width: 300px;
    flex-direction: column;
    align-items: center;
}

/* Mobile styles - controls at top right when screen < 800px */
/* if the viewport width is 800px or less */
@media screen and (max-width: 800px) {
    .local-flex {
        flex-direction: column;
    }

    .flex-grow {
        margin-bottom: 1rem;
        min-height: 100vmin;
    }

    .recent-component {
        width: 100%;
        order: 2;
    }

    .pip-video {
        width: 40%;
        height: 20%;
        bottom: 0.5rem;
        right: 0.5rem;
    }

    .pip-video img {
        width: 12%;
        rotate: 45deg;
    }
}

.pip-video {
    position: fixed;
    bottom: 1rem;
    right: 1rem;
    width: 20%;
    height: 25%;
    overflow: hidden;
    z-index: 9999;
    border-radius: 20px;
    cursor: pointer;
}

/* L'image est positionnée par rapport au conteneur pip-video */
.pip-video img {
    position: absolute;
    /* position par rapport au parent */
    top: 0.5rem;
    left: 0.5rem;
    /* mieux qu'un pourcentage pour un bouton */
    width: 8%;
    /* toujours au-dessus du contenu */
    z-index: 10000;
    cursor: pointer;

    rotate: 90deg;
}
</style>