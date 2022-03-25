#!/usr/bin/env bash

ROOT_PATH=$(readlink -f "$(dirname -- "$0")/../..")

declare -A env_variables      # Fixed environment variables load from .env file
declare -A env_variables_eval # Environment variables with dependencies load from .env file

function replace_root() {
  # Replace /home/../project/../value by ./value
  echo "${1//$ROOT_PATH/.}"
}

function load_env_file() {
  # Read environment variables from file
  # $1: Input .env file to load

  if [[ -f "${1}" ]]; then
    while IFS='=' read -r key temp || [ -n "$key" ]; do
      local isComment='^[[:space:]]*#'
      local isBlank='^[[:space:]]*$'
      [[ $key =~ $isComment ]] && continue
      [[ $key =~ $isBlank ]] && continue
      [[ "${temp}" == *"\${"* ]] && env_variables_eval["${key}"]="${temp}" || env_variables["${key}"]="${temp}"
    done <"$1"
  fi

}

function save_env_file() {
  # Save the new values of the environment variables to a file
  # $1: Output .env file where to export the final environment variables

  env_file="$1"

  # remove file if it exists
  if [[ -f "${env_file}" ]]; then
    rm "${env_file}"
  fi

  # save environment variables to file
  {
    for key in "${!env_variables[@]}"; do
      value=$(replace_root "${env_variables[${key}]}")
      export "${key}"="${value}"
      echo "${key}=${value}"
    done

    for key in "${!env_variables_eval[@]}"; do
      value=$(replace_root "$(eval echo "${env_variables_eval[${key}]}")")
      export "${key}"="${value}"
      echo "${key}=${value}"
    done
  } >>"${env_file}"

}
