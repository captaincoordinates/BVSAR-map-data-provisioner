docker run --name=provisioner -e CORE_URL=0.0.0.0:20009 -e TILE_URL=0.0.0.0:20008 -v provisioned-data:/root/data -v provisioning-home:/root/provisioning -p 1100:22 -p 20008:20008 -p 20009:20009 -d -t provisioner