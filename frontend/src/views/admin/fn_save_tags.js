export function handleTagsCreated(ctx, tags) {
    console.log(tags)
    if (Array.isArray(tags)) {
        ctx.tagsToCreate = tags;
    } else if (tags) {
        const exists = ctx.tagsToCreate.some(t => t.uuid === tags.uuid);
        if (!exists) {
            ctx.tagsToCreate.push(tags);
        }
    }
}

export function handleTagsDisconnected(ctx, tags) {
    if (Array.isArray(tags)) {
        ctx.tagsToDisconnect = tags;
    } else if (tags) {
        const exists = ctx.tagsToDisconnect.some(t => t.uuid === tags.uuid);
        if (!exists) {
            ctx.tagsToDisconnect.push(tags);
        }
        ctx.tagsConnected = ctx.tagsConnected.filter(t => t.uuid !== tags.uuid);
    }
}

export function handleTagsConnected(ctx, tag) {
    console.log("connecterd")
    if (tag) {
        const exists = ctx.tagsConnected.some(t => t.uuid === tag.uuid);
        if (!exists) {
            ctx.tagsConnected.push(tag);
        }
        ctx.tagsToDisconnect = ctx.tagsToDisconnect.filter(t => t.uuid !== tag.uuid);
    }
}

export async function save_tags(ctx) {
    for (const tag of ctx.tagsConnected) {
        await ctx.current_interview.connect_tag(tag);
    }

    for (const tagData of ctx.tagsToCreate) {
        const newTag = await new Tag({ name: tagData.name }).create();
        await ctx.current_interview.connect_tag(newTag);
    }

    for (const tag of ctx.tagsToDisconnect) {
        await ctx.current_interview.disconnect_tag(tag);
    }

    ctx.tagsConnected = [];
    ctx.tagsToCreate = [];
    ctx.tagsToDisconnect = [];
}
