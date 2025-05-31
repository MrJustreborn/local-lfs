# Local-LFS
Intended for tests and smaller projects that don't need to consume your LFS credits.

## start the local lfs server
Create the ```lfs-storage``` folder and start the server with:
```docker compose up --build```

You can change the path of the folder in the ```docker-compose.yml``` file to point, for example, to a cloud storage folder (Nextcloud, Dropbox, etc.).

## setup your repo

* Run ```git lfs install```
* Run ```git lfs track '*.bin'```
* Set the LFS URL in your repo:
```git config -f .lfsconfig lfs.url http://user:password@localhost:5000```