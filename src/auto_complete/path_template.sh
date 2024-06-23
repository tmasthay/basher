_@@@FUNC_NAME@@@() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local dir_path="$@@@PATH_CONTEXT@@@"

    # Use compgen to generate directory completions
    COMPREPLY=($(compgen -d "$dir_path/$cur" -- $cur))

    local i=0
    for item in "${COMPREPLY[@]}"; do
        COMPREPLY[$i]="${item#$dir_path/}"
        ((i++))
    done

    return 0
}
