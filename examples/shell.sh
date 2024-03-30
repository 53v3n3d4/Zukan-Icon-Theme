#!/bin/bash
echo "Hello World"

alias h='fc -l -25'
alias j='jobs -l'
alias la='ls -aF'
alias lf='ls -FA'
alias ll='ls -lAF'
alias s='df -h .; du -sh -- * | sort -hr'

func listening() {
    if [ $# -eq 0 ]; then
        lsof -iTCP -sTCP:LISTEN -n -P
    elif [ $# -eq 1 ]; then
        lsof -iTCP -sTCP:LISTEN -n -P | grep -i --color $1
    else
        echo "Usage: listening [pattern]"
    fi
}

# defaut color prompt
PS1="🚥 %B%F{249}in %~$%f%b "
# light theme terminal
alias day='PS1="🚥 %B%F{249}in %~$%f%b "'
# dark theme terminal
alias night='PS1="❄️  %B%F{244}in %~$%f%b "'

# Sublime Text and Merge
alias st='open -a "Sublime Text"'
alias sm='open -a "Sublime Merge"'

# Homebrew
# nvm node
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm
[ -s "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/opt/homebrew/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion