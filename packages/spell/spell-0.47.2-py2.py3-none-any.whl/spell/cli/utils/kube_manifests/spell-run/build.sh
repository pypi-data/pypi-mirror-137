#!/usr/bin/env bash
set -e

dockerfile_path=$1
docker_registry_url=$2
docker_image_hash=$3
should_build_image=$4

cd "$dockerfile_path"/src

if [[ $(podman images "$docker_image_hash" | wc -l) -lt 2 ]]; then
  echo "building new image..."
  # we capture build failures by groking through build debug output because podman won't propagate exit codes
  # (see https://github.com/containers/podman/issues/12616)
  # TODO: remove this if the above issue is resolved
  podman build -f Dockerfile $dockerfile_path --log-level=debug -t $docker_image_hash 2>&1 | tee build_output.txt

  set +e # If grep fails to match, don't fail the build!
  build_err=$(
    grep "error building .* exit status" build_output.txt
  )
  set -e
  if [[ $build_err ]]; then
    searchstring="exit status "
    rest=${build_err#*$searchstring}
    error_code=${rest#*$searchstring}
    exit ${error_code}
  fi
else
  echo "image present in local build cache, skipping build..."
fi
echo "pushing image to remote registry at $docker_registry_url..."
podman push $docker_image_hash $docker_registry_url/$docker_image_hash
