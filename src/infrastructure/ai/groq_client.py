# [EX-001: Asistente apoyo / IA] - Autor: José Luis
import json
import urllib.error
import urllib.request


class GroqClient:
    def __init__(self, api_key=None):
        self.model = "llama-3.3-70b-versatile"
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.timeout = 15
        self.api_key = "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"

    def is_configured(self):
        return bool(self.api_key)

    def _enviar(self, messages):
        if not self.is_configured():
            raise RuntimeError("GROQ_API_KEY no está configurada.")
        payload = {
            "model": self.model,
            "messages": messages,
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detalle = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Groq Error {exc.code}: {detalle}") from exc
        parsed = json.loads(body)
        return parsed["choices"][0]["message"]["content"]

    def generate_json(self, prompt: str) -> str:
        return self._enviar([{"role": "user", "content": prompt}])

    def conversar(self, mensajes, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.extend(mensajes)
        return self._enviar(messages)
