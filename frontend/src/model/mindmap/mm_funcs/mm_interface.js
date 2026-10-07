import { videoStore } from "../../videoStore.js";
import mm_Mindmap from "../mm_mindmap.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import { mm_reset_soft, mm_draw_onecat } from "./mm_func.js";
import { mm_chemin_filter } from "./mm_func_chemin.js"

/**
 *  redraw everynode from root
 * @param {mm_Mindmap} mminfo mm_Mindmap 
 * @returns {Promise<Boolean>} if it's a video or not 
*/
async function mm_draw_root(mminfo) {
    await mm_reset_soft(mminfo); // weither we needed to recreate everything or not
    let changevideo, changepath = mm_chemin_filter(mminfo); // we can ignore change path here because it's drawing from the root
    if (changevideo) return true;
    for (const cheminpath of mminfo.chemin) {
        console.log("mm_draw_root loop", "chemin", mminfo.chemin, cheminpath);
        await mm_draw_onecat(mminfo, mminfo.node_get(cheminpath));
    }
    return false;
}

/**
 *  redraw an update
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @returns {Promise<Boolean>} if it's a video or not 
*/
async function mm_draw_update(mminfo) {
    if (mminfo.chemin.length <= 0) return mm_draw_root(mminfo);
    let changevideo, changepath = mm_chemin_filter(mminfo);
    if (changevideo) return true;
    if (changepath) return mm_draw_root(mminfo);
    await mm_draw_onecat(mminfo, mminfo.node_get(mminfo.chemin[mminfo.chemin.length - 1]));
    return false;
}

class SimpleClickLock {
    static #isRunning = false;
    static #latestClickId = 0;

    static async runIfLatest(callback) {
        const myClickId = Date.now();
        // Update latest click ID
        this.#latestClickId = myClickId;
        // Wait if already running
        while (this.#isRunning) {
            await new Promise(resolve => setTimeout(resolve, 100)); // Check every 500ms
            // Check if I'm no longer the latest click
            if (myClickId < this.#latestClickId) {
                return;
            }
        }
        // Double-check I'm still the latest before running
        if (myClickId < this.#latestClickId) {
            return;
        }

        this.#isRunning = true;
        
        try {
            await callback();
        } finally {
            this.#isRunning = false;
        }
    }
}

/**
 * the main entry interface for Mind Map shenanigans 
 * @param {mm_Mindmap} mminfo mm_Mindmap
 * @param {mmch_CheminT<T>} node mm_Node clicked
*/
export function mm_interface_handleclick(mminfo, node) {
    SimpleClickLock.runIfLatest(async () => {
        // console.log("running mm hanldeclick algo");
        try {
            if (node) {
                mminfo.chemin.push(node.mmch_key);
                // console.log("mm hanldeclick", "chemin", mminfo.chemin, "node key", node.mmch_key, "node", node);
            }
            let isvideo = await mm_draw_update(mminfo);
            if (isvideo) {
                // console.log("video store path before", videoStore.chemin);
                // console.log("video store set", mminfo.chemin, mminfo);
                videoStore.chemin = mminfo.chemin;
            }
            // console.log("mm hanldeclick end", mminfo);
            mminfo.update();
        } catch (error) {
            console.error(error);
            mminfo.update();
        }
    });
}