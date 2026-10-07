import { shallowMount } from '@vue/test-utils'
import miniature_video from '@components/lecteur_video/miniature_video.vue'

describe("miniature_video - update_miniature et DOM", () => {

  test("update_miniature - URL YouTube", async () => {
    const mockVideo = {
      uuid: '1234-5678',
      titre: "Test Video",
      extraits: Promise.resolve([
        { url_miniature_yt: "https://youtube.com/test", duree: 125 }
      ]),
      duree: 0,
    }

    const wrapper = shallowMount(miniature_video, {
      props: { video: mockVideo }
    })

    // Appelle la méthode
    await wrapper.vm.update_miniature()
    await wrapper.vm.$nextTick()
    console.log(wrapper.vm.url)


    // Vérifie que l'image est rendue avec la bonne URL et le bon alt
    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe("https://youtube.com/test")
    expect(img.attributes('alt')).toBe("Test Video")

    // Vérifie la durée
    const p = wrapper.find('.duree')
    expect(p.text()).toBe("02:05") // 125 sec = 2min 5sec
  })


  test("update_miniature - URL Vimeo", async () => {
    const mockExtrait = {
      uuid: '2345-6789',
      url_miniature_yt: null,
      get_url_miniature_vimeo: vi.fn().mockResolvedValue("https://vimeo.com/test"),
      duree: 90
    }

    const mockVideo = {
      uuid: '2345-6789',
      titre: "Video Vimeo",
      extraits: Promise.resolve([mockExtrait]),
    }

    const wrapper = shallowMount(miniature_video, {
      props: { video: mockVideo }
    })

    await wrapper.vm.update_miniature()
    await wrapper.vm.$nextTick()

    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe("https://vimeo.com/test")
    expect(img.attributes('alt')).toBe("Video Vimeo")

    const p = wrapper.find('.duree')
    expect(p.text()).toBe("01:30") // 90 sec
  })


  test("update_miniature - interview sans extrait", async () => {
    const mockVideo = {
      uuid: '3456-7890',
      titre: "Interview vide",
      extraits: Promise.resolve([]),
      url_miniature_yt: null,
      duree: 0
    }

    const wrapper = shallowMount(miniature_video, {
      props: { video: mockVideo }
    })

    // Spy sur console.warn
    const warnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {})

    await wrapper.vm.update_miniature()
    await wrapper.vm.$nextTick()

    // Aucune image affichée
    const img = wrapper.find('img')
    expect(img.exists()).toBe(false)

    // La durée reste 00:00:00
    const p = wrapper.find('.duree')
    expect(p.text()).toBe("00:00")

    // Vérifie le warn
    expect(warnSpy).toHaveBeenCalledWith(
      `Aucun extrait trouvé pour l’interview ${mockVideo.uuid}`
    )

    warnSpy.mockRestore()
  })

})
