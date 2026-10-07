import { mount } from "@vue/test-utils";
import lecteur from "@components/lecteur_video/lecteur_video.vue";
import { vi } from "vitest";

// Fonction utilitaire pour monter le composant avec provide/mock
function mountComponent({ extrait, interview } = {}) {
  return mount(lecteur, {
    global: {
      stubs: ["iframe_lecture_video", "bar_liste_video", "timecode"],
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

describe("page_lecteur_video - update()", () => {

  beforeAll(() => {
    // Mock du Model global utilisé par Artiste, etc.
    vi.mock("@model/model.js", () => {
      return {
        default: class Model { }
      };
    });
  });

  it("charge extrait, interview, URLs et liste_extraits correctement", async () => {
    const mockExtraits = [
      { uuid: "a", youtube_url: "ytA", vimeo_url: "viA" },
      { uuid: "b", youtube_url: "ytB", vimeo_url: "viB" }
    ];

    const wrapper = mountComponent({
      extrait: { uuid: "a", youtube_url: "ytA", vimeo_url: "viA" },
      interview: { extraits: Promise.resolve(mockExtraits) }
    });

    await wrapper.vm.update();

    // Vérifie que l'extrait courant est correctement défini
    expect(wrapper.vm.extrait.uuid).toBe("a");

    // Vérifie que l'interview est définie
    expect(wrapper.vm.interview).toBeTruthy();

    // Vérifie que la liste des extraits est bien chargée
    expect(wrapper.vm.liste_extraits.length).toBe(2);

    // Vérifie que les URLs YouTube/Vimeo sont bien construites
    expect(wrapper.vm.url_yt).toContain("ytA");
    expect(wrapper.vm.url_vimeo).toContain("viA");
  });
});
