import { app } from "/scripts/app.js";
import { api } from "/scripts/api.js";

app.registerExtension({
    name: "nkchocoai.danbooru_prompt_quiz",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "DanbooruPromptQuiz") {
            const originalOnNodeCreated = nodeType.prototype.onNodeCreated;

            nodeType.prototype.onNodeCreated = function () {
                if (originalOnNodeCreated) {
                    originalOnNodeCreated.call(this);
                }

                this.addWidget(
                    "button",
                    "Submit",
                    null,
                    () => {
                        const body = new FormData();
                        const id = app.runningNodeId;
                        const node = app.graph.getNodeById(id);
                        body.append('id', id);
                        body.append('input', node.widgets[0].element.value);
                        console.log(node);
                        console.log(node.widgets_values[0]);
                        console.log(node.widgets[0].element.value);
                        console.log(body);
                        api.fetchApi("/dpq_submit", { method: "POST", body, });
                    }, {
                    width: 150
                }
                );
            };
        }
    },

});
