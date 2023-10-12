ln -s -f $(pwd)/bash_env_vars ~/.bash_env_vars
ln -s -f $(pwd)/bash_aliases ~/.bash_aliases
ln -s -f $(pwd)/bash_functions ~/.bash_functions
ln -s -f $(pwd)/bash_env ~/.bash_env
ln -s -f $(pwd)/bash_source_helpers ~/.bash_source_helpers

rm -rf ~/.platform
rm -rf ~/.secrets
ln -s -f $(pwd)/platform ~/.platform
ln -s -f $(pwd)/MILD_SECRETS ~/.secrets

~/.secrets/build_souper_secrets.sh

cp ~/.bashrc ~/.bashrc_backup

# Check if "source ~/.bash_source_helpers" already exists in .bashrc
if ! grep -q "source ~/.bash_source_helpers" ~/.bashrc; then
    # If not, append it
    echo "source ~/.bash_source_helpers" >> ~/.bashrc
fi
