import { markRaw } from "vue";
import mm_Mindmap from "../mm_mindmap.js";
import mm_Linkage from "../mm_linkage.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "../mm_chemin_submod/mmch_root.js";

/**
 *  utils to create a child node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT<T>} parent the parent node  
 * @param {mmch_CheminT<T>} category the class of node  
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
 * @return {mmch_CheminT<T>} the created child
*/
export function mm_createChildNode(mminfo, parent, category, createLink = true, isPreview = false) {
    const thickness_base = (mminfo.chemin.length + 1) * 3;
    let Cls, content;
    // Determine if category is a simple class or a config object
    if (category && typeof category.cls === 'function') {
        // It's a config object { cls: mmch_Extrait, content: item }
        Cls = category.cls;
        content = category.content;
    } else if (typeof category === 'function' && category.prototype) {
        // It's a class constructor (like mmch_Extrait)
        Cls = category;
        content = null;
    } else {
        console.error("Invalid category passed to mm_createChildNode:", category);
        return null;
    }
    // Create the instance
    const tmp_child = new Cls(mminfo, parent.x, parent.y, parent.depth, content);
    // Add to parent's children
    parent.childrens.push(tmp_child.mmch_key);
    // add to mminfo nodes or previewnodes    
    if (isPreview) {
        tmp_child.ispreview = true;
    }
    mminfo.node_add(markRaw(tmp_child));
    // create linkage
    if (createLink) {
        const linkage = new mm_Linkage(parent, tmp_child, thickness_base * (1 / tmp_child.depth));
        if (isPreview) {
            mminfo.previewlinkages.push(markRaw(linkage));
        } else {
            mminfo.linkages.push(markRaw(linkage));
        }
    }
    return tmp_child;
}

function mod(n, m) {
    return ((n % m) + m) % m;
}

/**
 * pos the children of a node in a circle
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT<T>} parent the root node to witch the children has been added
 */
export function set_children_pos(mminfo, parent) {
    // failsafe , si pas enfant
    if (!parent.childrens.length) return;
    // est ce que c'est mm_Root ou pas 
    const isRoot = parent instanceof mmch_Root;
    const totalArc = isRoot ? 360 : 90; // Full circle for root, semicircle for others
    // Count children with and without content (mmch_obj)
    let childrenWithPreview = 0;
    let childrenWithContent = 0;
    let childrenEmpty = 0;

    for (let child_key of parent.childrens) {
        let child = mminfo.node_get(child_key);
        // console.log("set_children_pos child","child_key",child_key,"child",child,"parent",parent,"mminfo",mminfo);

        if (child.mmch_hasMiniature()) {
            childrenWithPreview++;
        } else if (child.mmch_obj) {
            childrenWithContent++;
        } else {
            childrenEmpty++;
        }
    }
    
    // ANGLE WEIGHTS - control spacing around circle
    const anglePreviewWeight = 20.0;    // Big preview images get more space
    const angleContentWeight = 8.0;     // Content nodes get medium space  
    const angleEmptyWeight = 5.0;       // Empty nodes get less space
    
    // DISTANCE WEIGHTS - control how far from parent
    const distancePreviewWeight = 8.0;  // Preview nodes go further
    const distanceContentWeight = 3.5;  // Content nodes medium distance
    const distanceEmptyWeight = 2;    // Empty nodes stay closer
    
    // Calculate angle per child based on content
    const effectiveAngleChildren = childrenWithPreview * anglePreviewWeight
        + childrenWithContent * angleContentWeight
        + childrenEmpty * angleEmptyWeight;
    const angle_per_child = totalArc / effectiveAngleChildren;

    // Calculate effective children for distance
    const effectiveDistanceChildren = childrenWithPreview * distancePreviewWeight
        + childrenWithContent * distanceContentWeight
        + childrenEmpty * distanceEmptyWeight;

    // console.log("set_children_pos", parent.depth, parent);
    // console.table({
    //     "prev": childrenWithPreview, 
    //     "angleCalc": childrenWithPreview * anglePreviewWeight,
    //     "distanceCalc": childrenWithPreview * distancePreviewWeight,
    //     "content": childrenWithContent, 
    //     "angleCalc": childrenWithContent * angleContentWeight,
    //     "distanceCalc": childrenWithContent * distanceContentWeight,
    //     "empty": childrenEmpty, 
    //     "angleCalc": childrenEmpty * angleEmptyWeight,
    //     "distanceCalc": childrenEmpty * distanceEmptyWeight,
    //     "totalEffectiveAngle": effectiveAngleChildren, 
    //     "totalEffectiveDistance": effectiveDistanceChildren,
    //     "angle_per_child": angle_per_child
    // });


    // distance entre root et enfant ;
    // so the distance is inversly proportional to the number of angle_per_child
    const depthFactor = Math.min(1, Math.max(1.2, parent.depth / 2)); // augment distance as depth increases

    // spreadFactor based on number of children AND children with content
    const spreadFactor = Math.max(5, effectiveDistanceChildren); // Increase distance if many children or many with content, but with a minimum to avoid too much clustering
    const distance = 400 + 15 * depthFactor * spreadFactor;

    // Calculate starting position - centered on origin_angle
    let start_angle = isRoot ? 0 : parent.origin_angle;
    const degree_to_rad = Math.PI / 180;
    let currentEffectiveIndex = 0;

    for (let index = 0; index < parent.childrens.length; index++) {
        const child = mminfo.node_get(parent.childrens[index]);
        
        // Get angle weight based on child type
        let angleWeight;
        if (child.mmch_hasMiniature()) {
            angleWeight = anglePreviewWeight;
        } else if (child.mmch_obj) {
            angleWeight = angleContentWeight;
        } else {
            angleWeight = angleEmptyWeight;
        }
        
        currentEffectiveIndex += angleWeight / 2;
        const current_angle = mod(start_angle + ((index % 2 == 0 ? 1 : -1) * (angle_per_child * currentEffectiveIndex)), 360);

        const angleRad = current_angle * degree_to_rad;

        child.targetX = parent.x + Math.cos(angleRad) * distance;
        child.targetY = parent.y + Math.sin(angleRad) * distance;
        child.origin_angle = current_angle;
        // console.log("origin_angle", parent.origin_angle, "start_angle", start_angle, "effectiveChildren", effectiveChildren, "currentEffectiveIndex", currentEffectiveIndex, "angle_per_child", angle_per_child, "i", index, "current_angle", current_angle, child);
        currentEffectiveIndex += angleWeight / 2;
        // Trigger animation for this child if at appropriate depth
        // console.log(root,child,mminfo.chemin.length, ">=", child.depth);
        if (mminfo.chemin.length >= child.depth) {
            child.animateToTarget();
        } else {
            child.x = child.targetX;
            child.y = child.targetY;
        }
        mminfo.update();
    }
}