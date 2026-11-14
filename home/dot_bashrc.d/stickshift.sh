if command -v stickshift >/dev/null 2>&1; then
    export STICKSHIFT_MODEL_NAME=z-ai/glm-5.3-flash
    export STICKSHIFT_REVIEW_MODEL_NAME=z-ai/glm-5.3
    export STICKSHIFT_REVIEW_EFFORT=high

    eval "$(stickshift completion bash)"
    alias st='stickshift'
    complete -o default -F __start_stickshift st
    alias sti='stickshift implement'
    alias sta='stickshift analyze'
fi
