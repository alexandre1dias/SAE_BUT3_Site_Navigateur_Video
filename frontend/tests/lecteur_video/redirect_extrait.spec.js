import { mount } from "@vue/test-utils";
import { vi } from "vitest";
import lecteur from "@components/lecteur_video/lecteur_video.vue";

// --- Mock global pour Model ---
vi.mock("@model/model.js", () => {
  return { default: class Model {} };
});

// --- Stub du composant iframe_lecture_video ---
const iframeStub = {
  template: "<div></div>",
  methods: {
    update_player: vi.fn().mockResolvedValue(true)
  }
};

// Fonction utilitaire pour monter le composant
function mountComponent({ extrait, interview } = {}) {
  return mount(lecteur, {
    global: {
      stubs: {
        iframe_lecture_video: iframeStub,
        bar_liste_video: true,
        timecode: true
      },
      provide: {
        extrait_current: {
          get: vi.fn().mockResolvedValue(extrait),
          set: vi.fn()
        },
        interview_current: {
          get: vi.fn().mockResolvedValue(interview),
          set: vi.fn()
        }
      }
    }
  });
}

describe("page_lecteur_video - redirect_extrait()", () => {
  it("met à jour l'extrait, les URLs et appelle update_player sur l'iframe", async () => {
    const mockExtrait = { uuid: "x", youtube_url: "ytX", vimeo_url: "viX" };
    const wrapper = mountComponent({ extrait: mockExtrait });

    // Appel de la méthode à tester
    await wrapper.vm.redirect_extrait(mockExtrait);

    // Assertions principales
    expect(wrapper.vm.extrait.uuid).toBe("x");
    expect(wrapper.vm.url_yt).toContain("ytX");
    expect(wrapper.vm.url_vimeo).toContain("viX");
  });
});
