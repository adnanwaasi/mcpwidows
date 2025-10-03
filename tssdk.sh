#!/bin/bash
sudo pacman -S nodejs npm

mkdir $1
cd $1
npm init -y
npm install @modelcontextprotocol/sdk
