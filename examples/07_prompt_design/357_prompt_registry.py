# Prompt-Registry
# Quelle: chapters/07_prompt_design.tex (Zeile 357)
class PromptRegistry:
    def __init__(self, template_dir: str = "prompts/"):
        self.templates: dict[str, Template] = {}
        self.template_dir = template_dir

    def load(self, name: str, version: int = 1) -> Template:
        path = f"{self.template_dir}/v{version}/{name}.jinja2"
        if name not in self.templates:
            with open(path) as f:
                self.templates[name] = Template(f.read())
        return self.templates[name]

    def render(self, name: str, version: int = 1, **kwargs) -> str:
        template = self.load(name, version)
        return template.render(**kwargs)

# Nutzung
registry = PromptRegistry()
prompt = registry.render(
    "classification", version=3,
    examples=db.get_examples(),
    ticket_text=request.text,
)

