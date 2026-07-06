FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install TeX Live, fonts, tools via apt (much simpler and reliable)
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-full \
    texlive-lang-german \
    latexmk \
    biber \
    fonts-dejavu-core \
    fonts-liberation \
    curl wget ca-certificates \
    git python3 python3-pip python3-venv \
    make gcc g++ pkg-config \
    vim nano less tree jq zip unzip \
    && rm -rf /var/lib/apt/lists/*

# Verify
RUN pdflatex --version | head -2 && latexmk --version | head -1
