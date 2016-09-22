#!/bin/sh

http POST http://localhost:8001/deploy \
    "User-Agent:GitHub-HookShot/044aadd" \
    "Content-Type:application/json" \
    "X-GitHub-Event:push" \
    "X-Hub-Signature:2ecac24237e2f8f74f0e432e5751b89ba9c00bf6" \
    --verbose
