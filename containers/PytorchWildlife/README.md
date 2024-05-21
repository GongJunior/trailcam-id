# PytorchWildlife Env
## Summary
    This is a basic app that that solves a basic problem for me. I keep a trail camera setup in my backyard, and needed a method to reivew what snoops around out there. I can pass to the videos to this app, and it can let me know when something other than a squirrel is present, so I can review the footage instead of having to watch them all.

## Usage
    For updating the app, I use:
    - docker run -d -p 8080:8000 --name pywl-dev -v .\src\:/src -v .\vids\:/vids -v .\data\:/db pt-wildlife-dev

    To run the app, I use:
    - docker compose up -d

## Additional Notes
- used python:3.8.18-bullseye as the base image due to having trouble running "RUN apt-get update && apt install -y python3-opencv" with base python:3.8 image
- idea blog: https://towardsdatascience.com/detecting-animals-in-the-backyard-practical-application-of-deep-learning-c030d3263ba8
- pytorchwildlife: https://github.com/microsoft/CameraTraps
- docker run -d -p 8080:8000 --name pywl-dev -v .\src\:/app -v .\vids\:/vids -v .\data\:/db pt-wildlife
- docker run -d -p 8000:8000 --name pywl-run -v .\src\:/app -v .\storage:/filestorage -v .\data\:/db -w /src --entrypoint "uvicorn" pt-wildlife "appapi:app" "--host=0.0.0.0"