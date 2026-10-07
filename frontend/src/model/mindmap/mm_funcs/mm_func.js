import { markRaw } from "vue";
import { mm_createChildNode, set_children_pos } from "./mm_func_node.js"
import { mm_find_compare } from "./mm_func_chemin.js";
import mm_Mindmap from "../mm_mindmap.js";
import mmch_CheminT from "../mm_chemin_submod/mmch_chemin.js";
import mmch_Root from "../mm_chemin_submod/mmch_root.js";

/**
 *  recreate the root node and reset everything
 * @param {mm_Mindmap} mminfo mm_Mindmap  
*/
async function mm_reset_hard(mminfo) {
    // reset everything
    mminfo.reset();
    // reset the mmch_cheminT master class key counter
    mmch_CheminT.reset_key_counter();
    // create root
    let root = markRaw(new mmch_Root(mminfo, 0, 0, 0, null));
    mminfo.node_add(root);
    mminfo.root_key = root.mmch_key;    
    await mm_draw_onecat(mminfo, root, false,false);
}

/**
 * Soft reset of mindmap - clears previews and adjusts nodes based on search
 * @param {mm_Mindmap} mminfo mm_Mindmap
 */
export async function mm_reset_soft(mminfo) {
    // Clear all preview elements and linkages
    mminfo.linkages = []; // Root has no linkages anyway
    mminfo.previewlinkages = [];
    // Safeguard: Check if we have a valid root node
    if (!mminfo.root_key || mminfo.node_data["data"].size === 0 || !mminfo.node_get(mminfo.root_key)) {
        await mm_reset_hard(mminfo);
        return;
    }
    const rootNode = mminfo.node_get(mminfo.root_key);
    const list_cat = [];
    const list_obj = [];
    let search_cat = [];
    let search_obj = [];
    for await (const item of rootNode.constructor.mmch_listcat()) {
        // Determine if category is a simple class or a config object
        if (typeof item.cls === 'function') {
            // It's a config object { cls: mmch_Extrait, content: item }
            list_obj.push(item);
        } else if (typeof item === 'function' && category.prototype) {
            // It's a class constructor (like mmch_Extrait)
            list_cat.push(item);
        } else {
            console.error("Invalid category passed to mm_createChildNode:", category);
            return null;
        }
    }
    for await (const item of rootNode.constructor.mmch_searchcat()) {
        // Determine if category is a simple class or a config object
        if (typeof item.cls === 'function') {
            // It's a config object { cls: mmch_Extrait, content: item }
            search_obj.push(item);
        } else if (typeof item === 'function' && category.prototype) {
            // It's a class constructor (like mmch_Extrait)
            search_cat.push(item);
        } else {
            console.error("Invalid category passed to mm_createChildNode:", category);
            return null;
        }
    }
    // console.log("mm_reset_soft list_cat");
    // console.table({"list_cat" : list_cat,
    //                 "list_obj" : list_obj,
    //                 "search_cat" : search_cat,
    //                 "search_obj" : search_obj});

    if (mminfo.searchval && mminfo.searchval.trim()){
        // on fait une recherche
        if (rootNode.childrens.lenght == (list_cat.length + list_obj.length)){
            // on etait sur une list -> create nodes
            // TODO : rm
            mm_reset_hard(mminfo);
            return;
        } else if (rootNode.childrens.lenght == (search_cat.length + search_obj.length)) {
            // on etait en mode search -> rien
            ;
            // TODO : rm
            mm_reset_hard(mminfo);
            return;
        } else {
            console.error("unknown mm_reset_soft state in search",rootNode.childrens.lenght,"!= list",(list_cat.length + list_obj.length),"!= search",(search_cat.length + search_obj.length));
            // console.table({"list_cat" : list_cat,
            //         "list_obj" : list_obj,
            //         "search_cat" : search_cat,
            //         "search_obj" : search_obj});
            mm_reset_hard(mminfo);
            return;
        }
    } else {
        // on est en mode liste
        if (rootNode.childrens.lenght == (list_cat.length + list_obj.length)){
            // on etait en mode liste -> rien
            ;
            // TODO : rm
            mm_reset_hard(mminfo);
            return;
        } else if (rootNode.childrens.lenght == (search_cat.length + search_obj.length)) {
            // on etait en mode search -> rm nodes
            ;
            // TODO : rm
            mm_reset_hard(mminfo);
            return;
        } else {
            console.error("unknown mm_reset_soft state in search",rootNode.childrens.lenght,"!= list",(list_cat.length + list_obj.length),"!= search",(search_cat.length + search_obj.length));
            // console.table({"list_cat" : list_cat,
            //         "list_obj" : list_obj,
            //         "search_cat" : search_cat,
            //         "search_obj" : search_obj});
            mm_reset_hard(mminfo);
            return;
        }
    }
}


/**
 * draw the categories of one node
 * @param {mm_Mindmap} mminfo mm_Mindmap  
 * @param {mmch_CheminT<T>} node the root node to apply the new nodes to
 * @param {boolean?} createLink? = true do we draw the white line or not
 * @param {boolean?} isPreview? = false whether this is a preview node
*/
export async function mm_draw_onecat(mminfo, node, createLink = true, isPreview = false) {
    // console.log("mm_draw_onecat","mminfo",mminfo, "depth",node.depth,"node",node, "createLink",createLink , "isPreview",isPreview);
    // 0. safe Guards
    // Video / preview-only nodes never expand
    /// console.warn(node.depth, "Link",createLink, "isPreview", isPreview,"isPreview Node" , node.ispreview, "node obj", !!node.mmch_obj, node, mminfo.chemin);
    /// console.log(node.ispreview,node.mmch_obj,node.mmch_hasMiniature());
    if (node.mmch_obj && node.mmch_hasMiniature()) return;
    // uncomment to slow down drawing for COOL VISUALS
    /// await new Promise(r => setTimeout(r, 1000));
    node.loading = true;
    try {
        if (node.ispreview) {
            if (node.depth > mminfo.chemin.length + 4) {
                // safeguard to avoid expanding too deep previews
                console.warn(node.depth, "safeguard to avoid expanding too deep previews", node);
                node.loading = false;
                return;
            }
            if (node.mmch_obj) {
                // ─────────────────────────────
                // 3a. expand PREVIEW NODE with CONTENT
                // ─────────────────────────────
                // do nothing
                /// console.log(node.depth,"3a expand PREVIEW NODE with CONTENT",node);
                ;
            } else {
                // ─────────────────────────────
                // 3b. expand PREVIEW NODE without content
                // ─────────────────────────────
                /// console.log(node.depth,"3b expand PREVIEW NODE without content",node);

                // Handle async* generator
                for await (const catnode of node.mmch_previewinst(mminfo)) {
                    mm_createChildNode(mminfo, node, catnode, true, true);
                }
                set_children_pos(mminfo, node);
                /// TMP
                node.loading = false;
                // for (const child of node.childrens) {
                //     // if that node is parent then only draw content preview
                //     if (child.mmch_obj) {
                //         await mm_draw_onecat(mminfo, child, true, true);
                //     }
                // }
            }
        } else if (node.depth > mminfo.chemin.length + 2) {
            // safeguard to avoid expanding too deep previews
            console.warn(node.depth, "safeguard to avoid expanding too deep how did we get here", node);
            node.loading = false;
            return;
        }
        else if (node.mmch_obj) {
            // ─────────────────────────────
            // 1b. CONTENT NODE → CATEGORIES
            // ─────────────────────────────
            /// console.log(node.depth,"1b CONTENT NODE → CATEGORIES",node);
            // Handle async* generator for instance methods
            for await (const instnode of node.mmch_listinst()) {
                mm_createChildNode(mminfo, node, instnode, isPreview);
            }
            set_children_pos(mminfo, node);
            /// TMP
            // node.loading = false;
            // for (const child of node.childrens) {
            //     await mm_draw_onecat(mminfo, child, true, true);
            // }
        } else {
            // ─────────────────────────────
            // 1a. CATEGORY NODE → CONTENT
            // ─────────────────────────────
            /// console.log(node.depth,"1a CATEGORY NODE → CONTENT",node);
            const getnodefunc = mminfo.searchval ?
                () => node.constructor.mmch_searchcat() :
                () => node.constructor.mmch_listcat();

            // Handle async* generator for static methods
            for await (const catnode of getnodefunc()) {
                mm_createChildNode(mminfo, node, catnode, createLink, isPreview);
            }
            set_children_pos(mminfo, node);
            /// TMP
            // node.loading = false;
            // for (const child of node.childrens) {
            //     await mm_draw_onecat(mminfo, child, true, true);
            // }
        }
        if (node.depth > mminfo.chemin.length) {
            // ─────────────────────────────
            // 2. DRAW previews of subcategories
            // ─────────────────────────────
            /// console.log(node.depth,"2 DRAW previews of subcategories",node);
            /// await Promise.all(
            ///     node.childrens.map(async (child) => {
            ///         await mm_draw_onecat(mminfo, child, false, true);
            ///     })
            /// );
        }
    } catch (err) {
        console.error("mm_draw_onecat error:", err);
    }
    node.loading = false;
}