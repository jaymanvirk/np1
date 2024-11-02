import subprocess

class OllamaManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, model_name):
        if model_name not in self.processes:
            ollama_command = f"ollama run {model_name}"
            process = subprocess.Popen(
                ollama_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
            self.processes[model_name] = process
        return self.processes[model_name]

    def stop_process(self, model_name):
        if model_name in self.processes:
            process = self.processes[model_name]
            process.stdin.close()
            process.terminate()
            del self.processes[model_name]

    def get_process(self, model_name):
        return self.processes.get(model_name)

ollama_manager = OllamaManager()

