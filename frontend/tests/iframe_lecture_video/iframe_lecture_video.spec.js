import { mount } from "@vue/test-utils";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Iframe from "@components/lecteur_video/iframe_lecture_video.vue";
import { videoStore } from "@model/videoStore";

// Reset videoStore et DOM avant chaque test
beforeEach(() => {
  videoStore.url = "";
  videoStore.url_yt = "https://youtu.be/testYT";
  videoStore.url_vimeo = "https://vimeo.com/testVimeo";
  videoStore.currentTime = 0;
  videoStore.isPlaying = false;
  videoStore.intervalId = null;

  // Création d'un div#player pour initVimeo
  const playerContainer = document.getElementById("player");
  if (!playerContainer) {
    const div = document.createElement("div");
    div.id = "player";
    document.body.appendChild(div);
  }
});

// Mock des API externes
beforeEach(() => {
  // Mock YouTube
  window.YT = {
    Player: vi.fn().mockImplementation(() => ({
      playVideo: vi.fn(),
      pauseVideo: vi.fn(),
      seekTo: vi.fn(),
      destroy: vi.fn(),
    })),
    PlayerState: {
      PLAYING: 1,
      PAUSED: 2,
      ENDED: 0,
    },
  };

  // Mock Vimeo avec constructeur valide
  window.Vimeo = {
    Player: class {
      constructor(iframe) {
        this.iframe = iframe;
        this.ready = vi.fn().mockResolvedValue(true);
        this.play = vi.fn();
        this.pause = vi.fn();
        this.setCurrentTime = vi.fn();
        this.on = vi.fn();
      }
    },
  };
});

describe("iframe_lecture_video methods", () => {
  it("extrait l'ID depuis différentes URLs YouTube", () => {
    const wrapper = mount(Iframe);
    const fn = wrapper.vm.get_YT_videoId;

    expect(fn("https://youtu.be/abcd1234")).toBe("abcd1234");
    expect(fn("https://www.youtube.com/watch?v=ZZ99YY")).toBe("ZZ99YY");
    expect(fn("https://youtube.com/embed/HELLO_WORLD")).toBe("HELLO_WORLD");
    expect(fn("https://youtube.com/watch?x=1")).toBe(null);
    expect(fn("not a url")).toBe(null);
  });

  it("set_url change videoStore.url et appelle update_player", async () => {
    const wrapper = mount(Iframe);
    const spy = vi.spyOn(wrapper.vm, "update_player").mockResolvedValue();

    wrapper.vm.set_url("YouTube");
    expect(videoStore.url).toBe(videoStore.url_yt);
    expect(spy).toHaveBeenCalled();

    wrapper.vm.set_url("Vimeo");
    expect(videoStore.url).toBe(videoStore.url_vimeo);
    expect(spy).toHaveBeenCalledTimes(2);

    spy.mockRestore();
  });

  it("startTracking et stopTracking modifient videoStore.currentTime et intervalId", () => {
    const wrapper = mount(Iframe);

    // Mock player avec getCurrentTime
    wrapper.vm.player = { getCurrentTime: vi.fn().mockReturnValue(42) };

    wrapper.vm.startTracking();
    expect(videoStore.intervalId).not.toBeNull();

    wrapper.vm.stopTracking();
    expect(videoStore.intervalId).toBeNull();
  });

  it("reset_old_lecteur détruit le player existant", () => {
    const destroyMock = vi.fn();
    const wrapper = mount(Iframe);
    wrapper.vm.player = { destroy: destroyMock };

    wrapper.vm.reset_old_lecteur();
    expect(destroyMock).toHaveBeenCalled();
    expect(wrapper.vm.player).toBeNull();
  });

  it("update_player appelle initYouTube ou initVimeo selon videoStore.url", async () => {
    const wrapper = mount(Iframe, { attachTo: document.body });

    // Spy sur l'instance réelle
    const initYTSpy = vi.spyOn(wrapper.vm, "initYouTube").mockResolvedValue();
    const initVimeoSpy = vi.spyOn(wrapper.vm, "initVimeo").mockResolvedValue();

    // Test YouTube
    videoStore.url = "https://youtu.be/test";
    await wrapper.vm.update_player();
    expect(initYTSpy).toHaveBeenCalled();

    // Test Vimeo
    videoStore.url = "https://vimeo.com/test";
    await wrapper.vm.update_player();
    expect(initVimeoSpy).toHaveBeenCalled();

    wrapper.unmount();
  });



});
