// ne fonctionne pas


import { mount } from "@vue/test-utils";
import bar_list_video from "@components/lecteur_video/bar_liste_video.vue";
import Extrait from "@model/extrait";
import { vi, describe, it, expect } from "vitest";

vi.mock("@model/extrait", () => ({
  default: {
    list: vi.fn().mockResolvedValue([
      { uuid: "1", titre: "A" },
      { uuid: "2", titre: "B" }
    ])
  }
}));

function mountComponent() {
  return mount(bar_list_video, {
    global: {
      provide: {
        extrait_current: { get: vi.fn(), set: vi.fn() },
        interview_current: { get: vi.fn(), set: vi.fn() },
      }
    }
  });
}

describe("current_reco()", () => {
  it("charge les extraits et définit selected='reco'", async () => {
    const wrapper = mountComponent();

    await wrapper.vm.current_reco();

    expect(wrapper.vm.selected).toBe("reco");
    expect(Extrait.list).toHaveBeenCalled();
    expect(wrapper.vm.videos.length).toBe(2);
  });
});
