import mm_Mindmap from "./mm_mindmap.js";

export default class mm_Node {
    // Real/current positions (animating positions)
    /** @type {number} */
    x;
    /** @type {number} */
    y;
    // Target positions
    /** @type {number} */
    targetX;
    /** @type {number} */
    targetY;
    /** @type {number} */
    depth;
    /** @type {Array<Number>} key number of mminfo.nodes*/
    childrens;
    /** @type {boolean} */
    ispreview;
    /** @type {number} */
    origin_angle = null;
    /** @type {boolean} */
    loading = false;
    /** @type {mm_Mindmap} */
    mminfo; // Reference to mindmap instance needed by mmch_draw

    /**
    * constructor for mindmap node
    * @param {mm_Mindmap} mminfo mm_mindmap
    * @param {number} x x pos
    * @param {number} y y pos
    * @param {number} depth depth
    * @param {boolean} ispreview is a preview node
    */
    constructor(mminfo, targetX, targetY, depth, ispreview = false) {
        this.mminfo = mminfo;
        // Both start at same position initially
        this.x = targetX;
        this.y = targetY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.depth = depth;
        this.childrens = [];
        this.ispreview = ispreview;
    }

    toJSON() {
        return {
            x: this.x,
            y: this.y,
            targetX: this.targetX,
            targetY: this.targetY,
            depth: this.depth,
            childrens: this.childrens,
            origin_angle: this.origin_angle,
            loading: this.loading,
        };
    }

    // Animate to target position
    animateToTarget(duration = 500) {
        const startX = this.x;
        const startY = this.y;
        const endX = this.targetX;
        const endY = this.targetY;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeProgress = this.easeInOutCubic(progress);

            this.x = startX + (endX - startX) * easeProgress;
            this.y = startY + (endY - startY) * easeProgress;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
            this.mminfo.update();
        };
        requestAnimationFrame(animate);
    }

    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
}