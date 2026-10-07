import { shallowMount } from '@vue/test-utils'
import miniature_video from '@components/lecteur_video/miniature_video.vue'


test('get_miniature extrait : retourne url miniature youtube', async () => {
  // Création de la vidéo "interview" ou extrait avec miniature YouTube
  const mockExtrait = {
    uuid: '1234-5678',
    url_miniature_yt: "https://youtube.com",
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockExtrait }
  })

  await wrapper.vm.$nextTick()

  // On appelle directement la méthode
  const result = await wrapper.vm.get_miniature(mockExtrait)

  // Vérifie que la fonction retourne bien l'URL YouTube
  expect(result).toBe("https://youtube.com")
})

test('get_miniature extrait : retourne url miniature vimeo', async () => {
  // Création de la vidéo ou extrait avec url_miniature_yt null
  const mockExtrait = {
    uuid: '1234-5678',
    url_miniature_yt: null,
    get_url_miniature_vimeo: vi.fn().mockResolvedValue("https://vimeo.com") // mock de la méthode
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockExtrait }
  })

  await wrapper.vm.$nextTick()

  // On appelle directement la méthode
  const result = await wrapper.vm.get_miniature(mockExtrait)

  // Vérifie que la fonction retourne bien l'URL Vimeo
  expect(result).toBe("https://vimeo.com")

  // Vérifie que la méthode mockée a bien été appelée
  expect(mockExtrait.get_url_miniature_vimeo).toHaveBeenCalled()
})


test('get_miniature interview : retourne null et log warning si interview sans extrait', async () => {
  // Mock de console.warn pour vérifier qu'il est appelé
  const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})

  // Création de la vidéo "interview" sans extrait
  const mockVideo = {
    uuid: '1234-5678',
    extraits: Promise.resolve([]),
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockVideo }
  })

  await wrapper.vm.$nextTick()

  // On appelle directement la méthode
  const result = await wrapper.vm.get_miniature(mockVideo, await mockVideo.extraits)

  // Vérifie que le warning a été appelé avec le bon message
  expect(warnSpy).toHaveBeenCalledWith('Aucun extrait trouvé pour l’interview 1234-5678')

  // Vérifie que la fonction retourne bien null
  expect(result).toBeNull()

  // Restaure console.warn pour ne pas impacter d'autres tests
  warnSpy.mockRestore()
})

test("get_miniature interview : retourne url youtube de l'extrait de l'interview", async () => {
  // Mock de l’extrait avec miniature YouTube
  const mockExtrait = {
    uuid: 'extrait-1',
    url_miniature_yt: "https://youtube.com/extrait",
    get_url_miniature_vimeo: vi.fn()
  }

  // Mock de l’interview
  const mockVideo = {
    uuid: 'interview-1',
    extraits: Promise.resolve([mockExtrait])
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockVideo }
  })

  await wrapper.vm.$nextTick()

  const extraits = await mockVideo.extraits
  const result = await wrapper.vm.get_miniature(mockVideo, extraits)

  expect(result).toBe("https://youtube.com/extrait")
  // Vimeo ne doit pas être appelé
  expect(mockExtrait.get_url_miniature_vimeo).not.toHaveBeenCalled()
})


test("get_miniature interview : retourne url vimeo de l'extrait de l'interview", async () => {
  // Mock de l’extrait sans miniature YouTube
  const mockExtrait = {
    uuid: 'extrait-1',
    url_miniature_yt: null,
    get_url_miniature_vimeo: vi.fn().mockResolvedValue("https://vimeo.com/extrait")
  }

  // Mock de l’interview
  const mockVideo = {
    uuid: 'interview-1',
    extraits: Promise.resolve([mockExtrait])
  }

  const wrapper = shallowMount(miniature_video, {
    props: { video: mockVideo }
  })

  await wrapper.vm.$nextTick()

  const extraits = await mockVideo.extraits
  const result = await wrapper.vm.get_miniature(mockVideo, extraits)

  expect(result).toBe("https://vimeo.com/extrait")
  // Vimeo doit être appelé
  expect(mockExtrait.get_url_miniature_vimeo).toHaveBeenCalled()
})


