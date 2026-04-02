#!/bin/bash

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== Code Generator Docker Script ===${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}docker-compose is not installed. Please install docker-compose first.${NC}"
    exit 1
fi

build() {
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t codegenlinux -f utils/Dockerfile .
    echo -e "${GREEN}Build complete!${NC}"
}

run() {
    if [ -z "$GROQ_API_KEY" ]; then
        echo -e "${YELLOW}GROQ_API_KEY not set. Using value from .env file.${NC}"
        source .env 2>/dev/null || true
    fi
    
    if [ -z "$GROQ_API_KEY" ]; then
        echo -e "${RED}GROQ_API_KEY is required. Set it in .env or export GROQ_API_KEY${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Running container...${NC}"
    docker run -it --rm \
        -e GROQ_API_KEY="$GROQ_API_KEY" \
        --network host \
        codegenlinux
}

up() {
    echo -e "${YELLOW}Starting services with docker-compose...${NC}"
    docker-compose -f utils/docker-compose.yml up -d
    echo -e "${GREEN}Services started!${NC}"
}

down() {
    echo -e "${YELLOW}Stopping services...${NC}"
    docker-compose -f utils/docker-compose.yml down
    echo -e "${GREEN}Services stopped!${NC}"
}

logs() {
    docker-compose -f utils/docker-compose.yml logs -f
}

rebuild() {
    echo -e "${YELLOW}Rebuilding Docker image...${NC}"
    docker build -t codegenlinux -f utils/Dockerfile utils/
    echo -e "${GREEN}Rebuild complete!${NC}"
}

help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build    - Build Docker image"
    echo "  run      - Run container interactively"
    echo "  up       - Start services with docker-compose"
    echo "  down     - Stop services"
    echo "  logs     - Show docker-compose logs"
    echo "  rebuild  - Rebuild Docker image"
    echo "  help     - Show this help message"
}

case "${1:-help}" in
    build) build ;;
    run) run ;;
    up) up ;;
    down) down ;;
    logs) logs ;;
    rebuild) rebuild ;;
    help|--help|-h) help ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        help
        exit 1
        ;;
esac
