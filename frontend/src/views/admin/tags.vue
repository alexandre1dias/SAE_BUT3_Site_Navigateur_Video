<script>
import { markRaw } from 'vue';
import Tag from '@model/tag';

export default {
    name: "tags",
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    emits: ['update:tagsCreated', 'update:tagsDisconnected', 'update:tagsConnected'],
    computed: {
        tagExistsInDatabase() {
            return this.liste_tags_bd.some(tag =>
                tag.name.toLowerCase() === this.newTagName.trim().toLowerCase()
            );
        },
        tagAlreadyInVideo() {
            const inputName = this.newTagName.trim().toLowerCase();
            return (
                this.liste_tags_video.some(tag => tag.name.toLowerCase() === inputName) ||
                this.liste_tags_video_created.some(tag => tag.name.toLowerCase() === inputName)
            );
        },
        isValidTagName() {
            return this.newTagName.trim().length > 0;
        },
        // Liste complète des tags à afficher (existants + à créer)
        allDisplayedTags() {
            return [...this.liste_tags_video, ...this.liste_tags_video_created];
        }
    },
    data() {
        return {
            liste_tags_video: [],
            liste_tags_video_created: [],
            liste_tags_video_disconnected: [],
            liste_tags_bd: [],
            allTags: [],
            newTagName: '', // For the input field
        }
    },
    methods: {
        loadTags() {
            // Filter out tags that are already associated with the video
            this.liste_tags_bd = this.allTags.filter(tag =>
                !this.liste_tags_video.some(videoTag => videoTag.uuid === tag.uuid) &&
                !this.liste_tags_video_created.some(createdTag => createdTag.name.toLowerCase() === tag.name.toLowerCase())
            );
        },

        addTag() {
            // Find the tag in the available list
            const tag = this.liste_tags_bd.find(t => t.name === this.newTagName);
            if (tag) {
                // Add to video tags
                this.liste_tags_video.push(markRaw(tag));

                // Remove from disconnected list if it was there
                const disconnectedIndex = this.liste_tags_video_disconnected.findIndex(
                    t => t.uuid === tag.uuid
                );
                if (disconnectedIndex !== -1) {
                    this.liste_tags_video_disconnected.splice(disconnectedIndex, 1);
                }

                // Emit the connected tag
                this.$emit('update:tagsConnected', tag);

                this.loadTags(); // Reload tags
                this.newTagName = '';
            }
        },

        createTag() {
            if (this.newTagName.trim()) {
                const tagName = this.newTagName.trim();

                const newTag = {
                    uuid: `temp-${Date.now()}-${tagName}`,
                    name: tagName,
                    isNew: true
                };

                // Track that this tag needs to be created
                this.liste_tags_video_created.push(newTag);

                // Emit the created tag
                this.$emit('update:tagsCreated', newTag);

                this.loadTags(); // Reload tags
                this.newTagName = '';
            }
        },

        removeTag(tag) {
            // Check if this tag is in the created list
            const createdIndex = this.liste_tags_video_created.findIndex(t => t.uuid === tag.uuid);

            if (createdIndex !== -1) {
                // If it was in created list, just remove it from there
                this.liste_tags_video_created.splice(createdIndex, 1);

                // Emit that a created tag was removed (you might want to handle this differently)
                this.$emit('update:tagsCreated', null);
            } else {
                // Find the tag in the video list
                const index = this.liste_tags_video.findIndex(t => t.uuid === tag.uuid);

                if (index !== -1) {
                    // Remove from video tags
                    const removedTag = this.liste_tags_video.splice(index, 1)[0];
                    this.liste_tags_video_disconnected.push(removedTag);

                    // Emit the disconnected tag
                    this.$emit('update:tagsDisconnected', removedTag);
                }
            }

            this.loadTags(); // Reload tags
        }
    },

    watch: {
        // Emit all created tags whenever the list changes
        liste_tags_video_created: {
            handler(newVal) {
                this.$emit('update:tagsCreated', newVal);
            },
            deep: true
        },
        // Emit all disconnected tags whenever the list changes
        liste_tags_video_disconnected: {
            handler(newVal) {
                this.$emit('update:tagsDisconnected', newVal);
            },
            deep: true
        }
    },

    async mounted() {
        const videoTags = await this.video.tags();
        const allTagsList = await Tag.list();

        // Store tags with markRaw on individual objects, not arrays
        this.liste_tags_video = videoTags.map(tag => markRaw(tag));
        this.allTags = allTagsList.map(tag => markRaw(tag));

        this.loadTags();
    }
};
</script>

<template>
    <div>
        <h1>Tags</h1>

        <div>
            <input type="text" v-model="newTagName" list="tagData" placeholder="Tags..." />
            <datalist id="tagData">
                <option v-for="tag in liste_tags_bd" :key="tag.uuid" :value="tag.name" />
            </datalist>
            <button :disabled="tagExistsInDatabase || !isValidTagName || tagAlreadyInVideo" @click="createTag">
                Créer
            </button>
            <button :disabled="!tagExistsInDatabase || !isValidTagName || tagAlreadyInVideo" @click="addTag">
                Ajouter
            </button>

        </div>
        <div class="champ_tags">
            <ul>
                <li v-for="tag in allDisplayedTags" :key="tag.uuid">
                    {{ tag.name }}
                    <span v-if="tag.isNew" class="badge-new">nouveau</span>
                    <button @click="removeTag(tag)" class="btn-remove">✕</button>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
h1 {
    text-align: center;
}

/* ====== INPUT ====== */
input[type="text"] {
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #ccc;
    outline: none;
    margin-right: 8px;
    min-width: 200px;
}

input[type="text"]:focus {
    border-color: var(--vert-pale);
    box-shadow: 0 0 0 2px rgba(0, 150, 0, 0.15);
}


/* ====== BOUTONS ====== */
div>button {
    padding: 8px 14px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    margin-right: 6px;
}

/* Bouton créer */
div>button:first-of-type {
    background-color: #4caf50;
    color: white;
}

div>button:first-of-type:hover:not(:disabled) {
    background-color: #43a047;
}

/* Bouton ajouter */
div>button:last-of-type {
    background-color: #2196f3;
    color: white;
}

div>button:last-of-type:hover:not(:disabled) {
    background-color: #1e88e5;
}

div>button:disabled {
    opacity: 0.45;
    cursor: not-allowed;
}

/* ====== ZONE TAGS ====== */
.champ_tags {
    min-height: 30vh;
    background-color: var(--gris-moyen);
    padding: 15px;
    border-radius: 16px;
    margin-top: 20px;
    margin-bottom: 20px;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}

.champ_tags ul {
    list-style: none;
    padding: 0;
}

.champ_tags li {
    display: inline-block;
    padding: 5px 10px;
    margin: 5px;
    background-color: var(--vert-pale);
    border-radius: 5px;
}

.btn-remove {
    margin-left: 8px;
    background: none;
    border: none;
    cursor: pointer;
    color: #d4c6c6;
}

.btn-remove:hover {
    color: #ff0000;
}

.badge-new {
    margin-left: 6px;
    font-size: 0.75em;
    background-color: #ff9800;
    color: white;
    padding: 2px 6px;
    border-radius: 3px;
    font-weight: bold;
}
</style>