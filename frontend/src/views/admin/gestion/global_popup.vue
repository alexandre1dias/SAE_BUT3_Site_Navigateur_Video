<template>
  <div v-if="visible" :class="['toast', type, { show: visible }]">
    <p>{{ message }}</p>
  </div>
</template>

<script scoped>
export default {
  name: "global_popup",
  data() {
    return {
      visible: false,
      message: "test",
      type: "success", // success ou error
      intervalId: null,
    };
  },
  mounted() {
    console.log("global_popup monté, visible =", this.visible);

    // Poll localStorage
    this.intervalId = setInterval(() => {
      const toast = localStorage.getItem("globalToast");
      if (toast) {
        try {
          const data = JSON.parse(toast);
          this.message = data.message || "";
          this.type = data.type;
          console.log(this.type, "toast type reçu");

          this.visible = true;
          localStorage.removeItem("globalToast");

          setTimeout(() => {
            this.visible = false;
          }, 5000);
        } catch (e) {
          console.error("Erreur parsing globalToast:", e);
          localStorage.removeItem("globalToast");
        }
      }
    }, 500);
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
};
</script>

<style scoped>
.toast {
  position: fixed;
  top: 10vh;
  right: 0;
  padding: 20px 30px;
  font-weight: 600;
  font-size: 1.2rem;
  max-width: 400px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  color: #fff;
  z-index: 9999;
  pointer-events: none;
  opacity: 1;
  /* bien visible */
  /* animation d'entrée et sortie */
  animation: slideInRight 0.4s ease-out, fadeOut 1s ease-in 4s forwards;
}

/* Couleurs selon le type */
.toast.success {
  background-color: var(--vert-midel);
}

.toast.error {
  background-color: var(--rouge);
}

.toast p {
  margin: 0;
  line-height: 1.5;
}

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