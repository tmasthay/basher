SCRIPT_DIR="$(dirname $(realpath $0))"
SUPER_SECRETS_SCRIPTS=( $(find $SCRIPT_DIR/SUPER_SECRETS -type f -name "build_super_secrets.sh") )

# Count number of scripts found
NUM_SCRIPTS=${#SUPER_SECRETS_SCRIPTS[@]}

if [ "$NUM_SCRIPTS" -eq 0 ]; then
    echo "No super secrets found...exiting"
    exit 0
elif [ "$NUM_SCRIPTS" -eq 1 ]; then
    echo -n "Generating super secrets and expecting results to be dumped to $SCRIPT_DIR..."
    chmod +x "${SUPER_SECRETS_SCRIPTS[0]}"
    "${SUPER_SECRETS_SCRIPTS[0]}"
    echo "SUCCESS"
    exit 0
else
    echo "More than one super scripts found...exiting with no side effect"
    exit 1
fi
