import { shallowMount } from '@vue/test-utils'
import miniature_video from '@components/lecteur_video/miniature_video.vue'

test("update_miniature met à jour url et duree", async () => {
  // Mock de la vidéo avec des extraits
  const mockExtraits = [
    { duree: 120, url_miniature_yt: "https://youtube.com/extrait1" },
    { duree: 75, url_miniature_yt: null, get_url_miniature_vimeo: async () => "https://vimeo.com/extrait2" },
  ]

  const mockVideo = {
    uuid: '1234-5678',
    extraits: Promise.resolve(mockExtraits),
    url_miniature_yt: null,
    duree: 0,
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockVideo }
  })

  // À ce stade, update_miniature peut être déclenché par le watch
  // On attend que tous les nextTick soient terminés
  await wrapper.vm.$nextTick()
  await wrapper.vm.$nextTick() // parfois besoin de 2 ticks pour les promesses

  // Vérifie que update_miniature a bien mis à jour les données
  expect(wrapper.vm.url).toBe("https://youtube.com/extrait1")
  expect(wrapper.vm.duree).toBe("03:15") // 120 + 75 = 195s = 3m15s
  expect(wrapper.vm.is_loading).toBe(false)
})



