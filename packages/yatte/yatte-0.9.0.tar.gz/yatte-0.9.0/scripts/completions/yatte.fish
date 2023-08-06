if command -q yatte
    set -l condition "not __fish_seen_subcommand_from (yatte | cut -f1 -d' ')"
    set -l tasks '(yatte | awk \'/<No tasks/ {exit}; {t=$1; $1=""; print t "\\t" $0}\')'
    complete -c yatte -n $condition -f -a $tasks
end
