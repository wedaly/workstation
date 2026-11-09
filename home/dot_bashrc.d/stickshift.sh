if command -v stickshift >/dev/null 2>&1; then
    export STICKSHIFT_MODEL_NAME=qwen/qwen3-coder-next
    eval "$(stickshift completion bash)"
    alias st='stickshift'
    complete -o default -F __start_stickshift st
    alias sti='stickshift implement'
    alias sta='stickshift analyze'
fi
