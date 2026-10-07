import router from "../../../router.js";
import mm_Mindmap from "../mm_mindmap.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "../mm_chemin_submod/mmch_root.js";
import mmch_Extrait from "../mm_chemin_submod/mmch_extrait.js";
import mmch_Interview from "../mm_chemin_submod/mmch_interview.js";

/**
 *  check video
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean} if there is a goto video or not
*/
export function mm_checkvideo(mminfo) {
    if (mminfo.chemin.length == 0) return false;    
    let last = mminfo.node_get(mminfo.chemin[mminfo.chemin.length - 1]);
    if (last instanceof mmch_Extrait && last.mmch_obj) {
        mminfo.extrait_current.set(last.mmch_obj);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    } else if (last instanceof mmch_Interview && last.mmch_obj) {
        mminfo.interview_current.set(last.mmch_obj);
        router.push({
            path: "/lecteur_video/"
        });
        return true;
    }
    return false;
}

/**
 *  filter chemin to maintain proper depth hierarchy
 * @param {mm_Mindmap} mminfo mm_mindmap  
 * @return {boolean,boolean} change goto video , change in path
*/
export function mm_chemin_filter(mminfo) {
    // Step 1: Filter out mm_Root from chemin if present
    mminfo.chemin = mminfo.chemin.filter(item => !(item instanceof mmch_Root));
    
    let original_lenght = mminfo.chemin.length;
    let change_goto_video = false;
    let change_in_path = false;
    // console.log("HERE mm_chemin_filter 1",mminfo.chemin);
    
    
    // Step 1: Validate depth and handle depth mismatches
    // if (mminfo.chemin.length > 0) {
    //     let lastElement = mminfo.chemin[mminfo.chemin.length - 1];
    //     let minDepth = lastElement.depth;
    //     mminfo.chemin = mminfo.chemin.filter((element, index) => {
    //         // Always keep the last element
    //         if (index === mminfo.chemin.length - 1) return true;
    //         // Keep if depth is smaller
    //         if (element.depth < minDepth) {
    //             return true;
    //         } else {
    //             return false;
    //         }
    //     });
    // }
    
    // Step 2: Clean preview nodes (after depth filtering, so we have the correct parent)
    // if (mminfo.chemin.length >= 2) {
    //     mm_convert_preview_to_regular(mminfo, mminfo.chemin[mminfo.chemin.length - 1]);
    //     mm_clean_preview(mminfo);
    // }
    
    // Step 3: Check if we need to go to video
    change_goto_video = mm_checkvideo(mminfo);
    if (change_goto_video) {
        // Video check handles navigation, just return
        return true, false;
    }
    
    
    
    // Step 5: Determine if path changed
    change_in_path = original_lenght != mminfo.chemin.length;
    
    // console.log("HERE mm_chemin_filter 1",mminfo.chemin);
    return false, change_in_path ;// change_in_path;
}

/**
 * clear the preview nodes and linkages
 * @param {mm_Mindmap} mminfo mm_mindmap  
*/
export function mm_clean_preview(mminfo){    
    // If chemin has less than 2 elements, there's no parent node to clean from
    if (mminfo.chemin.length < 2) return;
    // Get the parent node (second-to-last in chemin)
    const parentNode = mminfo.chemin.at(-2);
    // Use DFS stack to traverse all nodes in the subtree
    const stack = [parentNode];
    
    while (stack.length > 0) {
        const currentNode = stack.pop();
        
        // Check all children of current node
        for (let i = currentNode.childrens.length - 1; i >= 0; i--) {
            const child = currentNode.childrens[i];
            
            if (child.ispreview) {
                // Remove this preview child from its parent's children array
                currentNode.childrens.splice(i, 1);
                
                // Also remove from previewnodes array if it exists there
                const previewIndex = mminfo.previewnodes.indexOf(child);
                if (previewIndex !== -1) {
                    mminfo.previewnodes.splice(previewIndex, 1);
                }
                
                // Don't push children of preview nodes to stack since we're deleting the preview node
                // The preview node's children will be garbage collected
            } else {
                // If not a preview, check if it has children to explore
                if (child.childrens && child.childrens.length > 0) {
                    stack.push(child);
                }
            }
        }
    }
}

/**
 * Convert preview nodes to regular nodes when they become part of the main path
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT<T>} targetNode - The node that was just clicked
 */
export function mm_convert_preview_to_regular(mminfo, targetNode) {
    // Convert the target node if it is a preview node
    // console.log("mm_convert_preview_to_regular",targetNode);
    // TODO : FIX UNDERFINED 
    if (!targetNode) return;
    
    if (targetNode.ispreview) {
        targetNode.ispreview = false;
        
        // Remove from preview nodes array and add to regular nodes array
        const previewIndex = mminfo.previewnodes.indexOf(targetNode);
        if (previewIndex !== -1) {
            mminfo.previewnodes.splice(previewIndex, 1);
            mminfo.node_add(targetNode);
        }
        
        // Process preview links that connect to the target node
        for (let i = mminfo.previewlinkages.length - 1; i >= 0; i--) {
            const linkage = mminfo.previewlinkages[i];
            if (linkage.toNode === targetNode) {
                linkage.ispreview = false;
                mminfo.linkages.push(linkage);
                mminfo.previewlinkages.splice(i, 1);
            }
        }
        
        // Recursively process parent node if it is also a preview node
        // const parent = mminfo.nodes.find(node => 
        //     node.childrens && node.childrens.includes(targetNode)
        // );
        
        if (parent && parent.ispreview) {
            mm_convert_preview_to_regular(mminfo, parent);
        }
    }
}

/**
 * Compare two nodes for equality
 * Compares by: 1) reference, 2) class type, 3) object content (UUID), 4) position for non-content nodes
 * @param {mmch_CheminT} one - First node to compare (can be instance or class constructor)
 * @param {mmch_CheminT} other - Second node to compare (can be instance or class constructor)
 * @returns {boolean} - True if nodes are considered equal
 */
export function mm_find_compare(one, other) {
    if (!one || !other) return false;
    if (one === other) return true;
    
    // Get constructors from instances if they exist, otherwise use the value itself
    const oneConstructor = one.prototype ? one : (one.constructor ? one.constructor : one);
    const otherConstructor = other.prototype ? other : (other.constructor ? other.constructor : other);
    
    // Compare constructors
    if (oneConstructor !== otherConstructor) return false;
    
    // If both are instances with mmch_obj, compare by UUID
    if (one.mmch_obj && other.mmch_obj) {
        if (one.mmch_obj.uuid && other.mmch_obj.uuid) {
            return one.mmch_obj.uuid === other.mmch_obj.uuid;
        }
        return one.mmch_obj === other.mmch_obj;
    }
    
    // If both don't have mmch_obj (either both are class references or both are instances without mmch_obj)
    if (!one.mmch_obj && !other.mmch_obj) {
        return true;
    }
    
    // Special case: one is class reference, other is instance (or vice versa)
    // If we reached here, constructors are equal, so they're the same type
    return true;
}

/**
 * Find a node in the mindmap using multiple search strategies
 * First searches in the current path (chemin), then searches from root
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path to found node or null if not found
 */
export function mm_find_node(mminfo, searched) {
    return mm_find_top(mminfo, searched) || mm_find_fromroot(mminfo, searched);
}

/**
 * Search for a node starting from the current navigation path (chemin)
 * Checks nodes in the chemin, then searches recursively through children
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path to found node or null if not found
 */
function mm_find_top(mminfo, searched) {
    if (!searched || mminfo.chemin.length === 0) return null;
    
    // Check chemin nodes
    for (let i = 0; i < mminfo.chemin.length; i++) {
        if (mm_find_compare(mminfo.chemin[i], searched)) {
            return mminfo.chemin.slice(0, i + 1);
        }
    }
    
    // Use DFS to search through children of last chemin node
    const lastNode = mminfo.chemin[mminfo.chemin.length - 1];
    return dfs_search_stack(lastNode, searched, mminfo.chemin);
}

/**
 * Search for a node starting from the root node (full depth-first search)
 * @param {mm_Mindmap} mminfo - The mindmap instance
 * @param {mmch_CheminT} searched - The node to search for
 * @returns {Array<mmch_CheminT>|null} - Path from root to found node or null if not found
 */
function mm_find_fromroot(mminfo, searched) {
    if (!searched || mminfo.node_data["data"].size === 0) return null;
    return dfs_search_stack(mminfo.node_get(mminfo.root_key), searched, [mminfo.node_get(mminfo.root_key)]);
}

/**
 * Generic Depth-First Search function using a stack
 * @param {mmch_CheminT} startNode - Node to start search from
 * @param {mmch_CheminT} searched - Node to search for
 * @param {Array<mmch_CheminT>} initialPath - Initial path to startNode
 * @returns {Array<mmch_CheminT>|null} - Complete path if found, null otherwise
 */
function dfs_search_stack(startNode, searched, initialPath) {
    const stack = [{ node: startNode, path: initialPath }];
    
    while (stack.length > 0) {
        const { node, path } = stack.pop();        
        if (mm_find_compare(node, searched)) {
            return [...path, node];
        }
        // Push children to stack (in reverse order for DFS)
        for (let i = node.childrens.length - 1; i >= 0; i--) {
            const child = node.childrens[i];
            stack.push({ node: child, path: [...path, child] });
        }
    }
    return null;
}