FROM condaforge/miniforge3:latest

WORKDIR /workspace

COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -afy

SHELL ["conda", "run", "-n", "PythonVirtualEnv", "/bin/bash", "-c"]

COPY . .

CMD ["conda", "run", "--no-capture-output", "-n", "PythonVirtualEnv", "python", "main.py"]