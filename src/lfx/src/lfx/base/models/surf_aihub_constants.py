from .model_metadata import create_model_metadata

ICON = "SURF"

SURF_MODELS_DETAILED = [
    create_model_metadata(provider="SURF AI Hub", name="Zephyr 7B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Mixtral Instruct AWQ", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Llama 3.1 8B Instruct", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Phi-3.5 mini", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Qwen2.5 7B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Qwen2.5-Coder-1.5B-Instruct", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Qwen2.5-Coder-7B-Instruct", icon=ICON, tool_calling=True),
    create_model_metadata(
        provider="SURF AI Hub", name="stabilityai/stable-code-instruct-3b", icon=ICON, tool_calling=True
    ),
    create_model_metadata(provider="SURF AI Hub", name="gemma-2 9b", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="DeepSeek Distilled Llama 70B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Llama 3.3 70b Instruct AWQ", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="LLaVa 1.5 7B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Qwen 2.5 Coder 32B Instruct AWQ", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="default-text-large", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Qwen 2.5 VL 32B Instruct AWQ", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="SmolVLM 2 Instruct 2.2B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="DeepSeek 2 VL 4.5B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="default-text-medium", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Gemma-3 27B GPTQ", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="zai-org/GLM-4.5-Air-FP8", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="meta-llama/Llama-Guard-3-8B", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="default-code-instruct-small", icon=ICON, tool_calling=True),
    create_model_metadata(
        provider="SURF AI Hub", name="mistralai/Mistral-Small-3.2-24B-Instruct-2506", icon=ICON, tool_calling=True
    ),
    create_model_metadata(provider="SURF AI Hub", name="openai/gpt-oss-safeguard-120b", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="openai/gpt-oss-120b", icon=ICON, tool_calling=True),
    create_model_metadata(provider="SURF AI Hub", name="Gemma-3-1B RAG", icon=ICON, tool_calling=True),
    create_model_metadata(
        provider="SURF AI Hub", name="Llama 3.3 70b Instruct AWQ [RAG Mode]", icon=ICON, tool_calling=True
    ),
    create_model_metadata(
        provider="SURF AI Hub", name="DeepSeek Distilled Llama 70B AWQ [RAG Mode]", icon=ICON, tool_calling=True
    ),
]

SURF_MODELS = [
    metadata["name"]
    for metadata in SURF_MODELS_DETAILED
    if not metadata.get("deprecated", False) and metadata.get("tool_calling", False)
]

TOOL_CALLING_SUPPORTED_SURF_MODELS = [
    metadata["name"] for metadata in SURF_MODELS_DETAILED if metadata.get("tool_calling", False)
]

TOOL_CALLING_UNSUPPORTED_SURF_MODELS = [
    metadata["name"] for metadata in SURF_MODELS_DETAILED if not metadata.get("tool_calling", False)
]

DEPRECATED_MODELS = [metadata["name"] for metadata in SURF_MODELS_DETAILED if metadata.get("deprecated", False)]


DEFAULT_SURF_API_URL = "https://willma.surf.nl/api/v0"
