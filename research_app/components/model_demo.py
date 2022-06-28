import logging

import gradio as gr
from lightning.app.components.serve import ServeGradio
from rich.logging import RichHandler

from research_app.dalle_mini import DalleMini

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


class ModelDemo(ServeGradio):
    """Serve model with Gradio UI.

    You need to define i. `build_model` and ii. `predict` method and Lightning `ServeGradio` component will
    automatically launch the Gradio interface.
    """

    inputs = gr.inputs.Textbox(
        default="sunset over a lake in the mountains", label="Generate images from a text prompt"
    )
    outputs = [gr.outputs.Image(label="Images generated by Dalle Mini")] * 8
    enable_queue = True
    examples = [
        ["sunset over a lake in the mountains"],
        ["the Eiffel tower landing on the moon"],
    ]

    def __init__(self):
        super().__init__(parallel=True)

    def build_model(self) -> DalleMini:
        logger.info("loading model...")
        model = DalleMini()
        logger.info("built model!")
        return model

    def predict(self, query: str) -> str:
        return self.model.predict(query)
