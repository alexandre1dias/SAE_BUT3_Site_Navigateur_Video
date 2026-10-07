import { shallowMount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import miniature_video from '@components/lecteur_video/miniature_video.vue'

describe("get_duree", () => {

  it("retourne la durée formatée pour un extrait seul", async () => {
    const mockExtrait = { duree: 125 } // 2min 5sec
    const wrapper = shallowMount(miniature_video, {
      props: { video: mockExtrait }
    })

    const result = await wrapper.vm.get_duree(mockExtrait)
    expect(result).toBe("02:05") // minutes:seconds
  })

  it("retourne la somme des durées pour une interview avec plusieurs extraits", async () => {
    const mockExtraits = [
      { duree: 120 }, // 2min
      { duree: 75 },  // 1min 15sec
      { duree: 3665 } // 1h 1min 5sec
    ]
    const mockVideo = { uuid: "interview-1" }
    const wrapper = shallowMount(miniature_video, {
      props: { video: mockVideo }
    })

    const result = await wrapper.vm.get_duree(mockVideo, mockExtraits)
    // 120 + 75 + 3665 = 3855 sec = 1h 4min 20sec
    expect(result).toBe("01:04:20")
  })

  it("retourne 00:00 pour vidéo sans durée", async () => {
    const mockExtrait = { duree: 0 }
    const wrapper = shallowMount(miniature_video, {
      props: { video: mockExtrait }
    })

    const result = await wrapper.vm.get_duree(mockExtrait)
    expect(result).toBe("00:00")
  })

})
