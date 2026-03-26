FROM condaforge/miniforge3:latest

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml && conda clean -afy

COPY . .

CMD ["conda", "run", "--no-capture-output", "-n", "PythonVirtualEnv", "python", "main.py"]