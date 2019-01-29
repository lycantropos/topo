ARG PYTHON_IMAGE
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE}:${PYTHON_IMAGE_VERSION}

WORKDIR /opt/topo

COPY topo/ topo/
COPY tests/ tests/
COPY README.md .
COPY setup.py .
COPY setup.cfg .

RUN pip install -e .
